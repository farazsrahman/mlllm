# main.py
from openai import OpenAI
import json

client = OpenAI()

# Path to any training script
script_path = "mnist67/train.py"

# 1️⃣ Read the training script
with open(script_path, "r") as f:
    train_code = f.read()

# 2️⃣ System prompt — clear schema and JSON example
system_prompt = f"""
You are an ML experiment orchestrator.

You will be given the code for a Python training script.

Tasks:
1. Inspect the code and read its argument parser (argparse or click) to discover valid hyperparameters and their defaults.
2. Generate a number of valid training commands specified by the user, otherwise default to 3, that start with:
   python {script_path}
3. For each command, output:
   - "command": full CLI command used
   - "hyperparameters": a dictionary of all parameters and values used
   - "accuracy": the numeric accuracy (simulate a realistic value based on hyperparameters)
4. Finally, include a "summary" describing which configuration performed best and why.

⚙️ Respond ONLY with a JSON object in this exact structure:


"experiments": [
    
"command": "python path/to/train.py --learning_rate 0.001 --batch_size 64 --epochs 5",
      "hyperparameters": 
"learning_rate": 0.001,
        "batch_size": 64,
        "epochs": 5,
        "model_width": 128,
        "model_depth": 3
      ,
      "accuracy": 0.942
    
  ],
  "summary": "The best configuration achieved 94.2% accuracy with learning_rate=0.001, batch_size=64, and model_width=128."


Notes:
- The specific keys inside "hyperparameters" vary by script, but the overall structure must stay consistent.
- All numeric values must be numbers, not strings.
- Accuracy must be a realistic float or percentage.
- Do not include any explanation outside the JSON.
"""

user_prompt = f"""
Here is the training script code:
{train_code}

Analyze it and generate 5 different valid combinations of hyperparameters mentioned in the script.
Return the JSON in the specified format.
"""

# 3️⃣ Ask GPT-5 for structured JSON
response = client.chat.completions.create(
    model="gpt-5",
    response_format={"type": "json_object"},  # Force JSON output
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
)

# 4️⃣ Parse the response
final_output = json.loads(response.choices[0].message.content)

# 5️⃣ Print or send to frontend
print(json.dumps(final_output, indent=2))
