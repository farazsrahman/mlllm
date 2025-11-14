"""
main.py — FastAPI entrypoint

This file provides the backend API endpoints for the Trex ML experiment assistant.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
from datetime import datetime
import json
import time
import os

# Initialize FastAPI app
app = FastAPI(title="Trex Backend API")

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client (lazy initialization - only created when needed)
_client = None

def get_openai_client():
    """Get OpenAI client, creating it if it doesn't exist"""
    global _client
    if _client is None:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it with: export OPENAI_API_KEY='your-key-here'")
        _client = OpenAI(api_key=api_key)
    return _client

# Path to training script (relative to App/backend directory, going up to root)
SCRIPT_PATH = "../../mnist67/train.py"

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Trex backend is running"}

class RunExperimentsRequest(BaseModel):
    prompt: str

@app.post("/run_experiments")
async def run_experiments(request: RunExperimentsRequest):
    """
    Run experiments based on a natural language prompt.
    
    Request body: { "prompt": "Try 5 different learning rates between 1e-4 and 1e-2." }
    """
    user_prompt = request.prompt.strip()
    
    # Get absolute path to training script
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    script_abs_path = os.path.join(backend_dir, SCRIPT_PATH)
    script_abs_path = os.path.normpath(script_abs_path)
    
    # 1️⃣ Read the training script
    try:
        with open(script_abs_path, "r") as f:
            train_code = f.read()
    except FileNotFoundError:
        return JSONResponse(
            status_code=404,
            content={
                "id": f"msg-{int(time.time() * 1000)}",
                "role": "assistant",
                "content": f"Error: Training script not found at {script_abs_path}",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "runConfigs": []
            }
        )

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

{user_prompt}
"""

    try:
        # 4️⃣ Ask GPT for structured JSON output
        client = get_openai_client()  # Get client when needed
        response = client.chat.completions.create(
            model="gpt-4o",  # Using gpt-4o (gpt-5 doesn't exist)
            response_format={"type": "json_object"},  # Force JSON output
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": final_user_prompt},
            ],
        )

        # 5️⃣ Parse JSON response
        llm_output = json.loads(response.choices[0].message.content)
        
        # 6️⃣ Transform to ChatMessage format expected by frontend
        experiments = llm_output.get("experiments", [])
        summary = llm_output.get("summary", "")
        
        # Convert experiments to runConfigs format
        run_configs = []
        for exp in experiments:
            hyperparams = exp.get("hyperparameters", {})
            # Map hyperparameters to the format expected by frontend
            # Adjust field names as needed (lr vs learning_rate, etc.)
            config = {}
            if "learning_rate" in hyperparams:
                config["lr"] = hyperparams["learning_rate"]
            if "batch_size" in hyperparams:
                config["batch_size"] = hyperparams["batch_size"]
            if "epochs" in hyperparams:
                config["epochs"] = hyperparams["epochs"]
            # Add any other hyperparameters
            for key, value in hyperparams.items():
                if key not in ["learning_rate", "batch_size", "epochs"]:
                    config[key] = value
            
            run_configs.append(config)
        
        # Build response message
        content = summary if summary else f"Generated {len(experiments)} experiment configurations."
        if experiments:
            best_exp = max(experiments, key=lambda x: x.get("accuracy", 0))
            content += f"\n\nBest configuration: {best_exp.get('command', 'N/A')}"
        
        return {
            "id": f"msg-{int(time.time() * 1000)}",
            "role": "assistant",
            "content": content,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "runConfigs": run_configs
        }
        
    except ValueError as e:
        # API key not set
        return JSONResponse(
            status_code=500,
            content={
                "id": f"msg-{int(time.time() * 1000)}",
                "role": "assistant",
                "content": f"Configuration error: {str(e)}",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "runConfigs": []
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "id": f"msg-{int(time.time() * 1000)}",
                "role": "assistant",
                "content": f"Error processing request: {str(e)}",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "runConfigs": []
            }
        )

# TODO: Set up WebSocket manager for log streaming
# TODO: Import service modules (runner, analyzer, llm_agent, plotting, storage)
# TODO: Implement all API endpoints listed above
