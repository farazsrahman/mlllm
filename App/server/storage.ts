import type { Run, RunConfig, ChatMessage } from "@shared/schema";
import { randomUUID } from "crypto";

export interface IStorage {
  getRuns(): Promise<Run[]>;
  getRun(id: string): Promise<Run | undefined>;
  createRuns(configs: RunConfig[]): Promise<Run[]>;
  getMessages(): Promise<ChatMessage[]>;
  addMessage(message: ChatMessage): Promise<ChatMessage>;
}

export class MemStorage implements IStorage {
  private runs: Map<string, Run>;
  private messages: ChatMessage[];

  constructor() {
    this.runs = new Map();
    this.messages = [];
  }

  async getRuns(): Promise<Run[]> {
    return Array.from(this.runs.values());
  }

  async getRun(id: string): Promise<Run | undefined> {
    return this.runs.get(id);
  }

  async createRuns(configs: RunConfig[]): Promise<Run[]> {
    const runs = configs.map((config) => ({
      id: `run-${randomUUID()}`,
      status: "pending" as const,
      config,
      created_at: new Date().toISOString(),
    }));

    runs.forEach((run) => this.runs.set(run.id, run));
    return runs;
  }

  async getMessages(): Promise<ChatMessage[]> {
    return this.messages;
  }

  async addMessage(message: ChatMessage): Promise<ChatMessage> {
    this.messages.push(message);
    return message;
  }
}

export const storage = new MemStorage();
