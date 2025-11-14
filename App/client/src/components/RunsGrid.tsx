import { RunCard } from "./RunCard";
import type { Run } from "@shared/schema";
import { Loader2, Inbox } from "lucide-react";

interface RunsGridProps {
  runs: Run[];
  isLoading?: boolean;
}

export function RunsGrid({ runs, isLoading }: RunsGridProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-[400px]">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin text-primary mx-auto mb-2" />
          <p className="text-sm text-muted-foreground">Loading runs...</p>
        </div>
      </div>
    );
  }
  
  if (runs.length === 0) {
    return (
      <div className="flex items-center justify-center h-[400px]">
        <div className="text-center">
          <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center mx-auto mb-4">
            <Inbox className="w-8 h-8 text-muted-foreground" />
          </div>
          <h3 className="text-lg font-semibold mb-2">No runs yet</h3>
          <p className="text-sm text-muted-foreground max-w-sm">
            Start a conversation in the chat to create your first training runs.
          </p>
        </div>
      </div>
    );
  }
  
  return (
    <div 
      className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4"
      data-testid="runs-grid"
    >
      {runs.map((run) => (
        <RunCard key={run.id} run={run} />
      ))}
    </div>
  );
}
