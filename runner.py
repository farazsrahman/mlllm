# runner.py
import subprocess
import shlex

def run_safe_command(command: str):
    """Executes python train.py safely and returns raw stdout+stderr."""

    if not command.startswith("python ") or "train.py" not in command:
        return {"stdout": "", "stderr": f"Blocked unsafe command: {command}"}
    print(command)
    process = subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    out, err = process.communicate()
    print(out)
    print(err)
    return {
        "stdout": out.decode(),
        "stderr": err.decode()
    }


tools = [
    {
        "type": "function",
        "function": {
            "name": "run_safe_command",
            "description": "Run python train.py and return raw output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"}
                },
                "required": ["command"],
            },
        },
    }
]
