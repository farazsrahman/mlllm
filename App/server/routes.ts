import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { existsSync, readdirSync } from "fs";
import { join, extname, resolve } from "path";

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

  // Serve images from outputs directory
  // For now: Show IMG_9817.jpeg for all runs
  // Later: Images should be named with run ID prefix: {runId}-*.png
  app.get("/api/run/:id/image", async (req, res) => {
    try {
      const runId = req.params.id;
      // Path to outputs directory: App/backend/outputs
      // process.cwd() should be App directory when server runs
      const outputsDir = resolve(process.cwd(), "backend", "outputs");
      
      // Check if outputs directory exists
      if (!existsSync(outputsDir)) {
        console.error(`Outputs directory not found at: ${outputsDir} (cwd: ${process.cwd()})`);
        return res.status(404).json({ error: "Outputs directory not found", path: outputsDir });
      }

      // For now: Always serve IMG_9817.jpeg for all runs
      const imageFile = "IMG_9817.jpeg";
      const imagePath = resolve(join(outputsDir, imageFile));
      
      console.log(`Looking for image at: ${imagePath}`);
      console.log(`File exists: ${existsSync(imagePath)}`);

      if (!existsSync(imagePath)) {
        // Fallback: Try to find any image with run ID prefix
        const files = readdirSync(outputsDir);
        const foundImage = files.find(
          (file) => file.startsWith(runId) && [".png", ".jpg", ".jpeg", ".gif", ".webp"].includes(extname(file).toLowerCase())
        );
        
        if (!foundImage) {
          console.error(`Image not found. Looking for: ${imagePath}`);
          console.error(`Files in outputs dir:`, files);
          return res.status(404).json({ error: "Image not found for this run", path: imagePath, files });
        }
        
        const fallbackPath = resolve(join(outputsDir, foundImage));
        return res.sendFile(fallbackPath);
      }

      // Send file with absolute path (Express sendFile handles absolute paths)
      res.sendFile(imagePath);
    } catch (error) {
      console.error("Error serving image:", error);
      res.status(500).json({ error: "Failed to serve image", details: error instanceof Error ? error.message : String(error) });
    }
  });

  // Get list of available images for a run
  app.get("/api/run/:id/images", async (req, res) => {
    try {
      const runId = req.params.id;
      // Path to outputs directory: App/backend/outputs
      const outputsDir = resolve(join(process.cwd(), "backend", "outputs"));
      
      if (!existsSync(outputsDir)) {
        return res.json([]);
      }

      const files = readdirSync(outputsDir);
      const imageFiles = files
        .filter((file) => 
          file.startsWith(runId) && 
          [".png", ".jpg", ".jpeg", ".gif", ".webp"].includes(extname(file).toLowerCase())
        )
        .map((file) => ({
          filename: file,
          url: `/api/run/${runId}/image`,
        }));

      res.json(imageFiles);
    } catch (error) {
      console.error("Error listing images:", error);
      res.status(500).json({ error: "Failed to list images" });
    }
  });

  const httpServer = createServer(app);

  return httpServer;
}
