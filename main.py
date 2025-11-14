from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
import json

client = OpenAI()
app = FastAPI()

SCRIPT_PATH = "mnist67/train.py"  # Path to your ML script

@app.post("/run_experiments")
async def run_experiments(request: Request):
    data = await request.json()
    user_prompt = data.get("prompt", "").strip()

    # 1️⃣ Read the training script
    with open(SCRIPT_PATH, "r") as f:
        train_code = f.read()

    # 2️⃣ System prompt with clear structure
    system_prompt = f"""
You are an ML experiment orchestrator.

You will be given the code for a Python training script.

Tasks:
1. Inspect the code and read its argument parser (argparse or click) to discover valid hyperparameters and their defaults.
2. Generate a number of valid training commands specified by the user (default: 3) that start with:
   python {SCRIPT_PATH}
3. For each command, output:
   - "command": full CLI command used
   - "hyperparameters": dictionary of parameter names and values
   - "accuracy": numeric accuracy (simulate a realistic float)
4. Finally include a "summary" describing which configuration performed best and why.

⚙️ Respond ONLY with a JSON object in this exact structure:
{{
  "experiments": [
    {{
      "command": "python path/to/train.py --learning_rate 0.001 --batch_size 64 --epochs 5",
      "hyperparameters": {{
        "learning_rate": 0.001,
        "batch_size": 64,
        "epochs": 5,
        "model_width": 128,
        "model_depth": 3
      }},
      "accuracy": 0.942
    }}
  ],
  "summary": "The best configuration achieved 94.2% accuracy with learning_rate=0.001, batch_size=64, and model_width=128."
}}

Notes:
- The specific keys inside "hyperparameters" vary by script, but the outer JSON structure must stay consistent.
- All numeric values must be numbers, not strings.
- Accuracy must be a realistic float or percentage.
- Do not include any explanation outside the JSON.
"""

    # 3️⃣ Merge script and user instruction
    final_user_prompt = f"""
Here is the training script code:
{train_code}

{user_prompt}
"""

    # 4️⃣ Ask GPT for structured JSON output
    response = client.chat.completions.create(
        model="gpt-5",
        response_format={"type": "json_object"},  # Force JSON output
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": final_user_prompt},
        ],
    )

    # 5️⃣ Parse and return JSON response
    final_output = json.loads(response.choices[0].message.content)
    return JSONResponse(content=final_output)