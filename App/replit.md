# Trex ML Experiment Assistant

## Overview

Trex is a lightweight experiment assistant designed for ML researchers to run and manage multiple machine learning training jobs through a conversational interface. The application allows users to describe experiments in plain language, automatically generates hyperparameter configurations, executes multiple training runs in parallel, and provides visual comparison of results through interactive plots.

The project features a fully implemented React/TypeScript frontend with a Node.js/Express backend using in-memory storage. The architecture is designed to be extended with real job execution, LLM-based configuration generation, and persistent database storage.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Stack:**
- **Framework:** React 18 with TypeScript
- **Routing:** Wouter (lightweight client-side routing)
- **State Management:** TanStack Query (React Query) for server state
- **UI Components:** Radix UI primitives with shadcn/ui component library
- **Styling:** Tailwind CSS with custom design tokens
- **Plotting:** Plotly.js via react-plotly.js for interactive charts

**Design System:**
- Dark mode first approach with light mode support via ThemeProvider
- Custom color palette: navy background (#00143c), blue accent (#00b4f0), purple accent (#b428ff)
- Utility-focused design prioritizing readability and efficiency for researchers
- Component-based architecture with reusable UI primitives

**Key Pages:**
1. **Home Page (`/`)**: Two-column layout with chat interface (left) and runs grid (right)
2. **Run Detail Page (`/run/:id`)**: Individual run visualization with metadata and training curves

**Core Components:**
- `ChatWindow`: Displays conversation history with user and assistant messages
- `ChatInput`: Text input for experiment descriptions with keyboard shortcuts
- `ChatBubble`: Individual message component with support for embedded run configurations
- `RunsGrid`: Responsive grid displaying all training runs
- `RunCard`: Compact card showing run metadata, hyperparameters, metrics, and status
- `PlotViewer`: Dynamic Plotly chart renderer for training curves

### Backend Architecture

**Current Implementation:**
- **Runtime:** Node.js with TypeScript
- **Framework:** Express.js for HTTP server
- **Build System:** Vite for frontend bundling, esbuild for backend compilation
- **Session Management:** In-memory storage via `MemStorage` class

**API Endpoints:**
- `GET /api/runs` - Retrieve all training runs
- `GET /api/run/:id` - Get specific run details
- `POST /api/run-job` - Create new training runs from configurations
- `GET /api/messages` - Fetch chat message history

**Placeholder Backend Services (Python - Not Implemented):**
The `/backend` directory contains stub files for future Python-based implementation:
- `main.py`: FastAPI application with WebSocket support for log streaming
- `runner.py`: Job execution engine for managing subprocess training scripts
- `analyzer.py`: Log parsing and metrics extraction
- `llm_agent.py`: OpenAI integration for natural language experiment generation
- `plotting.py`: Plotly chart generation with Trex color scheme
- `storage.py`: Database persistence layer (SQLite/PostgreSQL)

**Current Data Flow:**
1. User sends experiment description via chat interface
2. Frontend calls `proposeRunsFromUserMessage()` stub that pattern-matches keywords
3. Configurations sent to `POST /api/run-job` endpoint
4. Backend creates run records with "pending" status in memory
5. Frontend polls `GET /api/runs` to display updated run grid

**Future Architecture (Backend Python Implementation):**
1. LLM agent processes natural language → generates hyperparameter configs
2. Job runner spawns training processes using subprocess
3. Real-time log streaming via WebSocket (`/ws/logs`)
4. Analyzer parses training output and extracts metrics
5. Plotter generates interactive charts from training history
6. Storage layer persists all data to database

### Data Models

**Shared Schema (TypeScript/Zod):**
```typescript
RunConfig: { lr: number, epochs: number, batch_size: number }
Run: { id: string, status: "pending" | "running" | "completed" | "failed", 
       config: RunConfig, val_loss?: number, lr_used?: number, created_at?: string }
ChatMessage: { id: string, role: "user" | "assistant" | "system", 
               content: string, timestamp: string, runConfigs?: RunConfig[] }
PlotData: { data: Array<any>, layout: object } // Plotly format
```

**Storage Pattern:**
- Current: In-memory Map/Array structures
- Planned: Drizzle ORM with PostgreSQL (configuration present in `drizzle.config.ts`)

### Design Decisions

**Why two-column layout?**
- Enables simultaneous interaction with chat and monitoring of runs
- Reduces context switching for researchers managing multiple experiments
- Chat remains accessible while browsing run results

**Why in-memory storage initially?**
- Allows frontend development to proceed independently
- Simple mental model for testing and development
- Easy migration path to database via storage interface abstraction

**Why Plotly over alternatives?**
- Interactive charts essential for comparing training curves
- JSON-serializable format enables backend generation
- Dark theme support matches application design

**Why stub LLM integration?**
- Pattern-matching provides immediate functionality for testing UI
- Separates concerns: frontend can be fully tested without API keys
- Clear interface contract for future OpenAI integration

**Why separate Python backend (planned)?**
- ML ecosystem primarily Python-based (training scripts, libraries)
- Subprocess management and log parsing better suited to Python
- FastAPI provides async support for WebSocket log streaming

**Why Express for current backend?**
- Rapid development for API prototyping
- Seamless TypeScript integration with frontend
- Vite middleware integration for HMR during development

## External Dependencies

### Frontend Dependencies
- **@tanstack/react-query**: Server state management and caching
- **@radix-ui/**: Headless UI component primitives (accordion, dialog, dropdown, etc.)
- **react-plotly.js**: Interactive plotting library
- **wouter**: Lightweight client-side routing
- **tailwindcss**: Utility-first CSS framework
- **zod**: Runtime type validation and schema definition

### Backend Dependencies (Node.js)
- **express**: HTTP server framework
- **drizzle-orm**: SQL query builder and ORM
- **@neondatabase/serverless**: PostgreSQL client for serverless environments
- **connect-pg-simple**: PostgreSQL session store (configured but not actively used)

### Build Tools
- **vite**: Frontend build tool and dev server
- **esbuild**: Backend TypeScript compilation
- **tsx**: TypeScript execution for development
- **drizzle-kit**: Database schema management and migrations

### Future Dependencies (Python Backend - Not Yet Implemented)
- **fastapi**: Modern async web framework
- **openai**: GPT-based experiment configuration generation
- **plotly**: Chart generation library
- **pydantic**: Data validation and schema definition
- **sqlalchemy** or **peewee**: Database ORM (if not using Drizzle via Node)

### Environment Variables Required
- `DATABASE_URL`: PostgreSQL connection string (validated in drizzle.config.ts)
- `OPENAI_API_KEY`: For LLM agent functionality (future implementation)

### Font Dependencies
- **Google Fonts**: Inter (sans-serif), JetBrains Mono (monospace)
- Loaded via CDN in client/index.html