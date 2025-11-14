# main.py
from runner import client, run_safe_command, tools
import json

script_path = "train.py"

# Step 1: Load the contents of the training script
with open(script_path, "r") as f:
    script_code = f.read()

# Step 2: Ask GPT-5 to inspect the script and generate commands
system_prompt = """
You are an intelligent CLI agent. The user provides a Python training script.
You must:
1. Inspect the code to find which command-line arguments are defined (e.g. using argparse).
2. Generate one or more valid CLI commands to run it.
3. Call run_safe_command with those commands.
"""

user_prompt = f"""
Here is the training script code:
Now generate appropriate 'python {script_path} --args ...' commands to run a few experiments.
"""

response = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    tools=tools,
)

# Step 3: Execute whatever commands GPT proposes
results = []
for choice in response.choices:
    msg = choice.message
    if hasattr(msg, "tool_calls") and msg.tool_calls:
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            result = run_safe_command(**args)
            results.append(result)

# Step 4: Summarize the runs
summary = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": "Summarize the results of all training runs."},
        {"role": "user", "content": json.dumps(results)}
    ]
)

print("\n📊 Experiment results:")
for r in results:
    print(r["stdout"])
print("\n🧠 Summary:")
print(summary.choices[0].message.content)