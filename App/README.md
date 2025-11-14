# Trex 

**Automate ML Experiments: Automate and Track Your Experiments**

Trex helps you run and manage multiple machine learning training jobs through a conversational interface. Describe what you want to test in plain language, and Trex will propose hyperparameter configurations and execute them for you.

## Why Trex?

ML researchers face a common pain point: **running multiple experiments with different hyperparameters is tedious**. You end up:

- Manually editing config files
- Copy-pasting training commands
- Losing track of which runs used which settings
- Struggling to compare results across experiments

Trex solves this by:

1. **Conversational interface**: "Test learning rates from 0.001 to 0.0001" → Trex generates configs
2. **Parallel execution**: Run multiple training jobs simultaneously
3. **Automatic tracking**: All runs, configs, and results in one place
4. **Visual comparison**: Plotly charts to compare training curves

## Project Status

✅ **Frontend**: Fully implemented and ready to use  
⏳ **Backend**: Placeholder structure for backend teammates to implement

This is a **GitHub-ready collaborative project** where:
- Frontend developers can immediately start using the UI
- Backend developers have a clear roadmap for implementation
- The two teams can work in parallel

## Architecture Overview

```
trex/
├── client/              # Fully implemented Next.js frontend
│   └── src/
│       ├── components/  # Chat UI, RunsGrid, PlotViewer
│       ├── lib/         # API client, LLM stubs
│       └── pages/       # Home, Run detail pages
│
├── backend/             # Placeholder Python backend (TODO)
│   ├── main.py         # FastAPI app (stub)
│   ├── runner.py       # Job execution (stub)
│   ├── analyzer.py     # Metrics analysis (stub)
│   ├── llm_agent.py    # OpenAI integration (stub)
│   ├── plotting.py     # Plotly charts (stub)
│   ├── storage.py      # Database layer (stub)
│   └── sample_scripts/
│       └── train_example.py  # ✅ Working sample script
│
└── shared/             # Shared schemas
    ├── schema.ts       # ✅ TypeScript interfaces
    └── schemas.py      # TODO: Pydantic models
```

## Color Palette

Trex uses a distinctive dark theme optimized for long research sessions:

- **Primary Background**: `#00143c` (dark navy)
- **Accent Blue**: `#00b4f0` (interactive elements, highlights)
- **Accent Purple**: `#b428ff` (secondary highlights, badges)
- **Text**: White/light gray on dark backgrounds

## Getting Started

### Frontend (Ready to Use)

The frontend is fully functional with mock data:

```bash
cd client
npm install
npm run dev
```

Visit `127.0.0.1:5000` to see:np
- Two-column layout (chat left, runs grid right)
- Conversational experiment interface
- Run cards with hyperparameters and status
- Plot viewer page with Plotly charts

### Backend (For Implementation)

Backend teammates should implement the Python backend:

#### Running the Backend

Once the backend is implemented, you can run it with:

```bash
# Navigate to the backend directory
cd App/backend

# Create and activate a virtual environment (if not already done)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi "uvicorn[standard]" python-multipart

# Run the FastAPI server
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The backend will be available at `http://127.0.0.1:8000`. The frontend is configured to connect to this address.

**Note**: The `--reload` flag enables auto-reload during development. Remove it for production.

#### Prerequisites

```bash
# Install Python 3.9+
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (once requirements.txt is uncommented)
# pip install -r requirements.txt
```

#### Testing the Sample Script

The training script is **fully functional** for testing:

```bash
python backend/sample_scripts/train_example.py --lr 0.001 --epochs 5 --batch_size 32
```

Output:
```
Starting training with lr=0.001, epochs=5, batch_size=32
Epoch 1/5
  train_loss: 0.8234
  val_loss: 0.9045
...
```

## API Contracts

Backend teammates should implement these endpoints:

### POST /run-job

Start new training runs with given configurations.

**Request:**
```json
{
  "configs": [
    { "lr": 0.001, "epochs": 5, "batch_size": 32 },
    { "lr": 0.0005, "epochs": 10, "batch_size": 64 }
  ]
}
```

**Response:**
```json
[
  {
    "id": "run-abc123",
    "status": "pending",
    "config": { "lr": 0.001, "epochs": 5, "batch_size": 32 }
  },
  {
    "id": "run-def456",
    "status": "pending",
    "config": { "lr": 0.0005, "epochs": 10, "batch_size": 64 }
  }
]
```

### GET /runs

List all training runs.

**Response:**
```json
[
  {
    "id": "run-abc123",
    "status": "completed",
    "config": { "lr": 0.001, "epochs": 5, "batch_size": 32 },
    "val_loss": 0.234,
    "lr_used": 0.001
  }
]
```

**Status values**: `"pending"`, `"running"`, `"completed"`, `"failed"`

### GET /run/{id}

Get details for a specific run.

**Response:**
```json
{
  "id": "run-abc123",
  "status": "completed",
  "config": { "lr": 0.001, "epochs": 5, "batch_size": 32 },
  "val_loss": 0.234,
  "lr_used": 0.001,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### GET /plot/{id}

Get Plotly chart data for a run.

**Response:**
```json
{
  "data": [
    {
      "x": [1, 2, 3, 4, 5],
      "y": [0.8, 0.6, 0.4, 0.3, 0.2],
      "type": "scatter",
      "mode": "lines+markers",
      "name": "Training Loss",
      "line": { "color": "#00b4f0" }
    },
    {
      "x": [1, 2, 3, 4, 5],
      "y": [0.9, 0.7, 0.5, 0.4, 0.3],
      "type": "scatter",
      "mode": "lines+markers",
      "name": "Validation Loss",
      "line": { "color": "#b428ff" }
    }
  ],
  "layout": {
    "title": "Training Progress",
    "xaxis": { "title": "Epoch" },
    "yaxis": { "title": "Loss" }
  }
}
```

### WebSocket /ws/logs (Optional)

Stream real-time training logs to the frontend.

**Message format:**
```json
{
  "run_id": "run-abc123",
  "timestamp": "2024-01-15T10:30:45Z",
  "message": "Epoch 3/5 - train_loss: 0.234"
}
```

## Backend Implementation Guide

### Module Responsibilities

#### `main.py` - FastAPI Application
- Set up FastAPI app with CORS
- Define all API endpoints
- Integrate service modules
- WebSocket connection management

#### `runner.py` - Job Execution
- Spawn training processes via subprocess
- Manage job queue (pending → running → completed)
- Monitor process status
- Capture stdout/stderr
- Update storage with results

#### `analyzer.py` - Metrics Analysis
- Parse training logs
- Extract metrics (loss, accuracy)
- Compare configurations
- Generate insights

#### `llm_agent.py` - AI Suggestions
- Call OpenAI API
- Parse natural language requests
- Generate hyperparameter configs
- Validate proposed settings

#### `plotting.py` - Visualization
- Convert metrics to Plotly JSON
- Create training curves
- Apply Trex color scheme
- Support multi-run comparisons

#### `storage.py` - Data Persistence
- Store run configurations
- Save metrics and logs
- Query by status, config, date
- Support SQLite (dev) / PostgreSQL (prod)

### Implementation Checklist

- [ ] Define Pydantic models in `shared/schemas.py`
- [ ] Implement storage layer (`storage.py`)
- [ ] Build job runner (`runner.py`)
- [ ] Create FastAPI app (`main.py`)
- [ ] Add log analyzer (`analyzer.py`)
- [ ] Implement plotting (`plotting.py`)
- [ ] Optional: Add LLM agent (`llm_agent.py`)
- [ ] Optional: WebSocket log streaming
- [ ] Write tests
- [ ] Add production deployment config

## Development Workflow

1. **Frontend team**: Already complete! Just run `npm run dev`
2. **Backend team**: 
   - Start with `storage.py` (define your database)
   - Then `runner.py` (make jobs actually run)
   - Then `main.py` (connect everything via FastAPI)
   - Finally `plotting.py`, `analyzer.py`, `llm_agent.py` (enhancements)

3. **Integration**: Once backend is running, frontend will automatically connect to `http://localhost:8000`

## Design Philosophy

Trex is built for **productivity over aesthetics**:

- **Information density**: Researchers need data, not whitespace
- **Dark theme**: Reduce eye strain during long sessions
- **Scannable metrics**: Quick visual parsing of results
- **Minimal animations**: Keep UI snappy

## Contributing

This project is designed for team collaboration:

- **Frontend**: Fully implemented, can be extended with new features
- **Backend**: Intentionally incomplete, ready for implementation
- **Design**: Follow the Trex color palette for consistency

## License

MIT License - Use freely for research and commercial projects

---

**Built with**: React, TypeScript, Tailwind CSS, Plotly.js, FastAPI (placeholder), Python

**Questions?** Check the code comments in each file for detailed implementation guidance.
