# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
import json

from runner import run_safe_command, tools

client = OpenAI()
app = FastAPI()

SCRIPT_PATH = "mnist67/train.py"


# ============================================
#               STAGE 1 PROMPT
# ============================================
system_prompt_stage1 = f"""
You are an ML experiment planner.

Your tasks:
1. Read the provided Python training script.
2. Infer valid hyperparameters from argparse/click.
3. Generate N commands (default: 3) as specified by the user's prompt.
4. Each command MUST begin with:
python {SCRIPT_PATH}
5. For each command, call the function run_safe_command with:
{{ "command": "..." }}

CRITICAL RULES:
- Output ONLY tool_calls.
- Do NOT summarize.
- Do NOT produce JSON.
- Do NOT write explanations.
- ONLY produce tool calls to run_safe_command.
"""


# ============================================
#               STAGE 2 PROMPT
# ============================================
system_prompt_stage2 = """
You are an ML experiment analyzer.

You will receive raw experiment results including:
- command
- stdout
- stderr

Your tasks:
1. Parse hyperparameters by reading --flags from each command.
2. Extract accuracy values from stdout (look for patterns like "acc:" or "accuracy").
3. Produce a STRICT JSON OBJECT in the exact format below:

{
  "experiments": [
    {
      "run_id": unique number,
      "command": "...",
      "hyperparameters": {},
      "accuracy": ...,
      "stdout": "...",
      "stderr": "..."
    }
  ],
  "summary": "...",
  "raw_output": "..."
}

Rules:
- NO extra text.
- Only valid JSON.
- Hyperparameters must be numbers when possible.
- accuracy must be numeric.
"""


# ============================================
#                FASTAPI ENDPOINT
# ============================================
@app.post("/run_experiments")
async def run_experiments(request: Request):
    body = await request.json()
    user_prompt = body.get("prompt", "")

    # 1. Load train.py
    with open(SCRIPT_PATH, "r") as f:
        train_code = f.read()

    # 2. Build Stage 1 user prompt
    stage1_user_prompt = f"""
Training script:
{train_code}

User request:
{user_prompt}
"""

    # ===========================
    #       STAGE 1 → PLAN
    # ===========================
    plan = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": system_prompt_stage1},
            {"role": "user", "content": stage1_user_prompt},
        ],
        tools=tools,
    )

    # ===========================
    #       EXECUTE COMMANDS
    # ===========================
    raw_results = []

    for choice in plan.choices:
        msg = choice.message
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments)
                cmd = args["command"]

                # Run the actual training command
                out = run_safe_command(cmd)

                raw_results.append({
                    "command": cmd,
                    "stdout": out["stdout"],
                    "stderr": out["stderr"]
                })

    # Save raw JSON for Stage 2
    raw_output_string = json.dumps(raw_results, indent=2)

    # ===========================
    #       STAGE 2 → STRUCTURE
    # ===========================
    structured = client.chat.completions.create(
        model="gpt-5",
        response_format={"type": "json_object"},   # STRICT JSON
        messages=[
            {"role": "system", "content": system_prompt_stage2},
            {"role": "user", "content": raw_output_string},
        ]
    )

    final_json = json.loads(structured.choices[0].message.content)

    return JSONResponse(content=final_json)
