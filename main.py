# main.py
from openai import OpenAI
from runner import run_safe_command, tools
import json

client = OpenAI()

user_prompt = """
You are an ML experiment planner.
Use python mnist67/train.py to train the MNIST 6-vs-7 model.

You can vary the following hyperparameters:
--learning_rate, --batch_size, --model_width, --model_depth, --dataset_size, and --epochs.

Run a few experiments (2–3 commands) to see which configuration gives the best accuracy.
"""

# Step 1: Ask GPT to propose and run experiments
plan = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {
            "role": "system",
            "content": (
                "You can run experiments by calling run_safe_command with different CLI arguments. "
                "Only use 'python mnist67/train.py' followed by valid hyperparameters."
            ),
        },
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

# Step 2: Summarize
summary = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": "Summarize the results of all training runs and highlight the best configuration."},
        {"role": "user", "content": json.dumps(results)},
    ],
)

print("\n📊 Training Results:\n")
for r in results:
    print(r["stdout"])

print("\n🧠 Summary:\n", summary.choices[0].message.content)
