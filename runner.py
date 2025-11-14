import subprocess, shlex

def run_safe_command(command: str):
    """Executes only approved python mnist67/train.py commands."""
    if not command.startswith("python mnist67/train.py"):
        return {"error": f"Unsafe command blocked: {command}"}

    print(f"💻 Executing: {command}")
    process = subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = process.communicate()
    return {"stdout": out.decode(), "stderr": err.decode()}


# Function-calling schema for GPT
tools = [
    {
        "type": "function",
        "function": {
            "name": "run_safe_command",
            "description": "Execute a safe ML training command for the MNIST 6-vs-7 model.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": (
                            "Full CLI command, e.g. "
                            "'python mnist67/train.py --learning_rate 0.001 "
                            "--batch_size 64 --model_width 128 --epochs 5'"
                        )
                    }
                },
                "required": ["command"]
            }
        }
    }
]
