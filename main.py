from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
import json

from runner import run_safe_command, tools

client = OpenAI()


SCRIPT_PATH = "mnist67/train.py"
user_prompt = "Can you generate a scaling law for my MNIST MLP by training on fractions of my dataset? Specifically train models on 10%, 20%, 30%, … to 100% of my data. I want 10 models trained at each data level. Then collect the information and generate for me a plot of the scaling law "

# load script code
with open(SCRIPT_PATH, "r") as f:
    train_code = f.read()

system_prompt = f"""
You are an ML experiment orchestrator.

Your responsibilities:
1. Read the Python training script code.
2. Infer valid hyperparameters from argparse/click.
3. Generate valid commands that start with:
  python {SCRIPT_PATH}
4. For each command, call run_safe_command.
5. You will be given RAW OUTPUT (stdout, stderr) from the script.
6. Using ONLY the raw output + the command, produce a clean JSON object:

{{
"experiments": [
{{
  "command": "...",
  "hyperparameters": {{}},
  "accuracy": ...,
  "stdout": "...",
  "stderr": "..."
}}
],
"summary": "..."
}}

Rules:
- Extract hyperparameters by parsing the --flags inside each command.
- Extract accuracy by reading the raw logs (look for 'acc:' or similar).
- Return numeric values as numbers, not strings.
- Do not output anything except JSON.
"""

# Prompt to GPT (ask for commands)
plan_prompt = f"""
Training script:
{train_code}
{user_prompt}
"""

# STEP 1 — GPT generates tool calls (commands)
plan = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": plan_prompt},
    ],
    tools=tools  # enables run_safe_command
)

# STEP 2 — Execute commands and collect raw output
raw_results = []

for choice in plan.choices:
    msg = choice.message
    if hasattr(msg, "tool_calls") and msg.tool_calls:
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            cmd = args["command"]

            # run real training script
            res = run_safe_command(cmd)

            raw_results.append({
                "command": cmd,
                "stdout": res["stdout"],
                "stderr": res["stderr"]
            })

# STEP 3 — Let GPT structure + summarize (using RAW data only)
summarize_prompt = json.dumps(raw_results, indent=2)

summary = client.chat.completions.create(
    model="gpt-5",
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "system",
            "content": "You analyze experiment results and output strict JSON only."
        },
        {
            "role": "user",
            "content": summarize_prompt
        }
    ]
)

final = json.loads(summary.choices[0].message.content)
print(final)