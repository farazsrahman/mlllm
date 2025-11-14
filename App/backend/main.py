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

# TODO: Implement FastAPI application
# TODO: Add CORS middleware for frontend communication
# TODO: Set up WebSocket manager for log streaming
# TODO: Import service modules (runner, analyzer, llm_agent, plotting, storage)
# TODO: Implement all API endpoints listed above
