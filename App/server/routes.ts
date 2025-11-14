import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";

export async function registerRoutes(app: Express): Promise<Server> {
  app.get("/api/runs", async (_req, res) => {
    const runs = await storage.getRuns();
    res.json(runs);
  });

  app.get("/api/run/:id", async (req, res) => {
    const run = await storage.getRun(req.params.id);
    if (!run) {
      return res.status(404).json({ error: "Run not found" });
    }
    res.json(run);
  });

  app.post("/api/run-job", async (req, res) => {
    const { configs } = req.body;
    const runs = await storage.createRuns(configs);
    res.json(runs);
  });

  // Proxy run_experiments requests to Python FastAPI backend (port 8000)
  // Returns error if backend is unavailable (mock mode is disabled)
  app.post("/api/run_experiments", async (req, res) => {
    try {
      const { prompt } = req.body;
      if (!prompt) {
        return res.status(400).json({ error: "Prompt is required" });
      }

      // Forward request to Python FastAPI backend
      try {
        // Create AbortController for timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout (OpenAI API can take time)

        const pythonResponse = await fetch("http://localhost:8000/run_experiments", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt }),
          signal: controller.signal,
        });

        clearTimeout(timeoutId);

        if (pythonResponse.ok) {
          const data = await pythonResponse.json();
          return res.json(data);
        } else {
          const errorText = await pythonResponse.text();
          console.error("Python backend error:", errorText);
          return res.status(pythonResponse.status).json({ 
            error: "Python backend error",
            details: errorText 
          });
        }
      } catch (fetchError) {
        // Backend is not available or connection failed
        console.error("Failed to connect to Python backend:", fetchError instanceof Error ? fetchError.message : "Unknown error");
        return res.status(503).json({ 
          error: "Python backend unavailable",
          details: fetchError instanceof Error ? fetchError.message : "Failed to connect to backend"
        });
      }
    } catch (error) {
      console.error("Error in /api/run_experiments:", error);
      return res.status(500).json({ 
        error: "Failed to process experiment request",
        details: error instanceof Error ? error.message : "Unknown error"
      });
    }
  });

  app.get("/api/messages", async (_req, res) => {
    const messages = await storage.getMessages();
    res.json(messages);
  });

  const httpServer = createServer(app);

  return httpServer;
}
