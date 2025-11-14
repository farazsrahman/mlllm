"""
main.py — FastAPI entrypoint (placeholder)

This file should be implemented by backend teammates to provide:

API Endpoints:
- POST /run-job
  Request: { "configs": [{ "lr": float, "epochs": int, "batch_size": int }] }
  Response: [{ "id": str, "status": str, "config": {...} }]
  
- GET /runs
  Response: [{ "id": str, "status": str, "config": {...}, "val_loss": float, "lr_used": float }]
  
- GET /run/{id}
  Response: { "id": str, "status": str, "config": {...}, "val_loss": float, "lr_used": float }
  
- GET /plot/{id}
  Response: { "data": [...], "layout": {...} }
  Plotly JSON format for rendering training curves
  
- WebSocket /ws/logs
  Stream real-time training logs to frontend

Backend Implementation Steps:
1. Initialize FastAPI app with CORS middleware
2. Import and integrate runner, analyzer, llm_agent, plotting, storage modules
3. Set up WebSocket connection manager for log streaming
4. Implement endpoint handlers calling appropriate service modules
5. Add error handling and validation using Pydantic models from schemas.py

This file is intentionally left incomplete for backend teammates to implement.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import time

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
    # TODO: Implement LLM agent to parse prompt and generate configs
    # TODO: Execute runs using runner module
    # TODO: Return ChatMessage format response
    
    return {
        "id": f"msg-{int(time.time() * 1000)}",
        "role": "assistant",
        "content": f"Received prompt: {request.prompt}. (Backend implementation pending)",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "runConfigs": []
    }

# TODO: Set up WebSocket manager for log streaming
# TODO: Import service modules (runner, analyzer, llm_agent, plotting, storage)
# TODO: Implement all API endpoints listed above
