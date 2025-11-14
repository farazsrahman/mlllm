from openai import OpenAI
# from groq import Groq
import json

client = OpenAI()
# client = Groq()

SCRIPT_PATH = "mnist67/train.py"  # Path to your ML scrip

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


Can you generate a scaling law for my MNIST MLP by training on fractions of my dataset? Specifically train models on 10%, 20%, 30%, … to 100% of my data. I want 10 models trained at each data level. Then collect the information and generate for me a plot of the scaling law
"""


# 4️⃣ Ask LLM for structured JSON output
response = client.chat.completions.create(
    # model="llama-3.1-70b-versatile",  # Groq model (change to "gpt-4" or "gpt-3.5-turbo" for OpenAI)
    # model="gpt-3.5-turbo",  # Fast OpenAI model
    model="gpt-5",  # Fast OpenAI model
    response_format={"type": "json_object"},  # Force JSON output
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": final_user_prompt},
    ],
)

# 5️⃣ Parse and display JSON response in a readable format
final_output = json.loads(response.choices[0].message.content)
import pprint
pprint.pprint(final_output)