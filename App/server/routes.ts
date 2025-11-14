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

  app.get("/api/messages", async (_req, res) => {
    const messages = await storage.getMessages();
    res.json(messages);
  });

  const httpServer = createServer(app);

  return httpServer;
}
