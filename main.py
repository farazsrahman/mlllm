# main.py
from openai import OpenAI
from runner import run_safe_command, tools
import json

client = OpenAI()

# Path to any training script
script_path = "mnist67/train.py"

# 1️⃣ Read the training script
with open(script_path, "r") as f:
    train_code = f.read()

# 2️⃣ System prompt: tell GPT what to do
system_prompt = f"""
You are an ML experiment orchestrator.

You will be given the full code of a Python training script. 
Your job is to:
1. Inspect its argument parser (e.g., argparse or click) to identify valid hyperparameters and their defaults.
2. Generate 2–3 training commands that vary these hyperparameters to explore model performance.
3. Each command must start with: python {script_path}
4. Call the `run_safe_command` function to run each command.

After all runs, you will summarize the results.
"""

user_prompt = f"""
Here is the code of the training script:
{train_code}

Analyze it and call run_safe_command with 2–3 valid CLI commands using the hyperparameters it defines.
"""

# 3️⃣ Ask GPT to plan and run experiments
plan = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    tools=tools,
)

results = []
for choice in plan.choices:
    msg = choice.message
    if hasattr(msg, "tool_calls") and msg.tool_calls:
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            result = run_safe_command(**args)
            results.append(result)

# 4️⃣ Summarize results
summary = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": "Summarize all experiment results and highlight best hyperparameters."},
        {"role": "user", "content": json.dumps(results)},
    ],
)

print("\n📊 Training Results:")
for r in results:
    print(r["stdout"])

print("\n🧠 Summary:")
print(summary.choices[0].message.content)
