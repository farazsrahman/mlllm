import { z } from "zod";

// Run Configuration Schema
export const runConfigSchema = z.object({
  lr: z.number().positive().optional(),
  epochs: z.number().int().positive().optional(),
  batch_size: z.number().int().positive().optional(),
}).passthrough(); // Allow additional hyperparameters

export type RunConfig = z.infer<typeof runConfigSchema>;

// Experiment Schema (new format from backend)
// Use preprocess to handle missing/null fields from GPT responses
export const experimentSchema = z.preprocess((data: any) => {
  // Normalize the data before validation - handle missing or null fields
  if (typeof data !== 'object' || data === null) {
    return { command: "", hyperparameters: {} };
  }
  return {
    ...data,
    command: data.command ?? "",
    hyperparameters: (data.hyperparameters && typeof data.hyperparameters === 'object' && !Array.isArray(data.hyperparameters)) 
      ? data.hyperparameters 
      : {},
  };
}, z.object({
  command: z.string(),
  hyperparameters: z.record(z.any()),
  accuracy: z.preprocess((val: any) => {
    if (val === undefined || val === null) return undefined;
    if (typeof val === 'string') {
      // Try to parse string numbers, handle percentage strings
      const cleaned = String(val).replace('%', '').trim();
      const parsed = parseFloat(cleaned);
      return isNaN(parsed) ? undefined : parsed;
    }
    return typeof val === 'number' ? val : undefined;
  }, z.number().optional()),
  stdout: z.string().optional(),
  stderr: z.string().optional(),
})); // Preprocess handles normalization, no need for passthrough

export type Experiment = z.infer<typeof experimentSchema>;

// Run Status Type
export type RunStatus = "pending" | "running" | "completed" | "failed";

// Run Schema
export const runSchema = z.object({
  id: z.string(),
  status: z.enum(["pending", "running", "completed", "failed"]),
  config: runConfigSchema, // Legacy format, will be populated from experiment
  // New fields from experiment format
  command: z.string().optional(),
  hyperparameters: z.record(z.any()).optional(), // Full hyperparameters dict
  accuracy: z.number().optional(),
  stdout: z.string().optional(),
  stderr: z.string().optional(),
  // Legacy fields
  val_loss: z.number().optional(),
  lr_used: z.number().optional(),
  created_at: z.string().optional(),
  image_url: z.string().optional(), // URL to associated image
});

export type Run = z.infer<typeof runSchema>;

// Chat Message Schema
export const chatMessageSchema = z.object({
  id: z.string(),
  role: z.enum(["user", "assistant", "system"]),
  content: z.string(),
  timestamp: z.string(), // Accept any string format for timestamp
  runConfigs: z.array(runConfigSchema).optional(), // Legacy format
  experiments: z.array(experimentSchema).optional(), // New format
  summary: z.string().optional(),
  raw_output: z.string().optional(),
}).passthrough(); // Allow additional fields

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
