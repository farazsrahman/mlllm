from openai import OpenAI
# from groq import Groq
import json
import argparse

from runner import run_safe_command
from console_logs_to_png import plot_from_logs

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate ML experiments from a user request")
parser.add_argument(
    "--request",
    type=str,
    required=True,
    help="User request describing what experiments to run (e.g., 'train models on 10%, 20%, 30%... to 100% of data')"
)
args = parser.parse_args()

client = OpenAI()
# client = Groq()

SCRIPT_PATH = "mnist67/train.py"  # Path to your ML script

# ============================================
#               STAGE 1 PROMPT
# ============================================
system_prompt_stage1 = f"""
You are an ML experiment planner.

Your tasks:
1. Read the provided Python training script.
2. Infer valid hyperparameters from argparse/click.
3. Generate N commands as specified by the user's prompt.
4. Each command MUST begin with:
python {SCRIPT_PATH}

⚙️ Respond ONLY with a JSON object in this exact structure:
{{
  "commands": [
    "python {SCRIPT_PATH} --arg1 value1 --arg2 value2",
    "python {SCRIPT_PATH} --arg1 value3 --arg2 value4",
    ...
  ]
}}

CRITICAL RULES:
- Output ONLY valid JSON.
- Do NOT include any explanation outside the JSON.
- All commands must start with "python {SCRIPT_PATH}".
"""

# 1️⃣ Read the training script
with open(SCRIPT_PATH, "r") as f:
    train_code = f.read()

# 2️⃣ Build Stage 1 user prompt
stage1_user_prompt = f"""
Training script:
{train_code}

User request:
{args.request}
"""

# ============================================================================
# STEP 1: PROMPTS → LIST OF COMMANDS
# ============================================================================
print("=" * 80)
print("STEP 1: Generating commands from prompt...")
print("=" * 80)

plan = client.chat.completions.create(
    model="gpt-5",
    response_format={"type": "json_object"},   # Force JSON output
    messages=[
        {"role": "system", "content": system_prompt_stage1},
        {"role": "user", "content": stage1_user_prompt},
    ],
)

# Parse commands from JSON response
plan_json = json.loads(plan.choices[0].message.content)
commands = plan_json.get("commands", [])

print(f"✓ Generated {len(commands)} commands to execute")
for i, cmd in enumerate(commands, 1):
    print(f"  {i}. {cmd}")

# ============================================================================
# STEP 2: LIST OF COMMANDS → CONSOLE LOGS
# ============================================================================
print("\n" + "=" * 80)
print("STEP 2: Executing commands and collecting console logs...")
print("=" * 80)
console_logs = []  # List to collect all commands and outputs

for i, cmd in enumerate(commands, 1):
    print(f"\n[{i}/{len(commands)}] Executing: {cmd}")
    
    # Add command to log
    console_logs.append(f"[{i}/{len(commands)}] Command: {cmd}\n")
    
    # Run the actual training command
    out = run_safe_command(cmd)
    
    # Add output to log
    console_logs.append(f"STDOUT:\n{out['stdout']}\n")
    if out['stderr']:
        console_logs.append(f"STDERR:\n{out['stderr']}\n")
    console_logs.append("-" * 80 + "\n")

# Combine all logs into a single string
console_logs_string = "".join(console_logs)
print(f"\n✓ Collected console logs: {len(console_logs_string)} characters")

# ============================================================================
# STEP 3: CONSOLE LOGS → PNG
# ============================================================================
print("\n" + "=" * 80)
print("STEP 3: Generating PNG plot from console logs...")
print("=" * 80)

plotting_request = "please make a plot of scaling laws from the above training console logs please make sure to keep everything on a log log scale and to fit a line of best fit. the line of best fit should match the color of the points"

try:
    plot_path = plot_from_logs(
        console_logs=console_logs_string,
        plotting_request=plotting_request,
        name="scaling_law_plot",
        model="gpt-4o"
    )
    print(f"\n✓ Plot successfully generated: {plot_path}")
except Exception as e:
    print(f"\n✗ Error generating plot: {e}")
    import traceback
    traceback.print_exc()