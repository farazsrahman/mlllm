import { z } from "zod";

// Run Configuration Schema
export const runConfigSchema = z.object({
  lr: z.number().positive(),
  epochs: z.number().int().positive(),
  batch_size: z.number().int().positive(),
});

export type RunConfig = z.infer<typeof runConfigSchema>;

// Run Status Type
export type RunStatus = "pending" | "running" | "completed" | "failed";

// Run Schema
export const runSchema = z.object({
  id: z.string(),
  status: z.enum(["pending", "running", "completed", "failed"]),
  config: runConfigSchema,
  val_loss: z.number().optional(),
  lr_used: z.number().optional(),
  created_at: z.string().optional(),
});

export type Run = z.infer<typeof runSchema>;

// Chat Message Schema
export const chatMessageSchema = z.object({
  id: z.string(),
  role: z.enum(["user", "assistant", "system"]),
  content: z.string(),
  timestamp: z.string(),
  runConfigs: z.array(runConfigSchema).optional(),
});

export type ChatMessage = z.infer<typeof chatMessageSchema>;

// Plot Data Schema (for Plotly)
export const plotDataSchema = z.object({
  data: z.array(z.any()),
  layout: z.object({
    title: z.string().optional(),
    xaxis: z.any().optional(),
    yaxis: z.any().optional(),
  }).passthrough(),
});

export type PlotData = z.infer<typeof plotDataSchema>;

// API Request/Response Schemas
export const createRunsRequestSchema = z.object({
  configs: z.array(runConfigSchema),
});

export type CreateRunsRequest = z.infer<typeof createRunsRequestSchema>;

export const chatRequestSchema = z.object({
  message: z.string().min(1),
});

export type ChatRequest = z.infer<typeof chatRequestSchema>;
