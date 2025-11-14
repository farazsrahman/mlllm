# smart_runner.py
import subprocess, shlex, json
from openai import OpenAI
from pathlib import Path

client = OpenAI()

def run_safe_command(command: str):
    """Run only python scripts inside the current directory."""
    if not command.startswith("python "):
        return {"error": "Unsafe command blocked!"}
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
            "description": "Execute an ML training script safely with specific command-line arguments.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Full command to execute, e.g. 'python train.py --lr 0.001 --bsz 32'"
                    }
                },
                "required": ["command"]
            }
        }
    }
]
