import subprocess, shlex


def run_safe_command(command: str):
    """Executes only 'python <something>/train.py' commands."""
    if not command.startswith("python ") or "train.py" not in command:
        return {"error": f"Unsafe command blocked: {command}"}

    print(f"💻 Executing: {command}")
    process = subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = process.communicate()
    return {"stdout": out.decode(), "stderr": err.decode()}


tools = [
    {
        "type": "function",
        "function": {
            "name": "run_safe_command",
            "description": "Execute a safe training command for any ML model script.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": (
                            "The CLI command, e.g. 'python mnist67/train.py --lr 0.001 --batch_size 64'"
                        )
                    }
                },
                "required": ["command"],
            },
        },
    }
]
