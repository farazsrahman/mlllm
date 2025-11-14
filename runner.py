# runner.py
import subprocess
import shlex

def run_safe_command(command: str):
    """Execute python train.py commands, print command + raw output, and return them."""

    # SAFETY CHECK
    if not command.startswith("python ") or "train.py" not in command:
        error_msg = f"Blocked unsafe command: {command}"
        print(error_msg)
        return {"stdout": "", "stderr": error_msg}

    # PRINT COMMAND BEING RUN
    print("\n============================")
    print("RUNNING COMMAND:")
    print(command)
    print("============================")

    # EXECUTE THE COMMAND
    process = subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    out, err = process.communicate()

    stdout = out.decode()
    stderr = err.decode()

    # PRINT RAW OUTPUT
    print("----- STDOUT -----")
    print(stdout)
    print("----- STDERR -----")
    print(stderr)
    print("============================\n")

    return {
        "stdout": stdout,
        "stderr": stderr
    }


# Tool schema for GPT
tools = [
    {
        "type": "function",
        "function": {
            "name": "run_safe_command",
            "description": "Run a python train.py command and return raw stdout/stderr.",
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
