import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Link } from "wouter";
import type { Run } from "@shared/schema";
import { Activity, CheckCircle2, Clock, XCircle, BarChart3 } from "lucide-react";
import { cn } from "@/lib/utils";

interface RunCardProps {
  run: Run;
}

const statusConfig = {
  pending: {
    icon: Clock,
    color: "text-muted-foreground",
    bg: "bg-muted",
    label: "Pending",
  },
  running: {
    icon: Activity,
    color: "text-primary",
    bg: "bg-primary/10",
    label: "Running",
  },
  completed: {
    icon: CheckCircle2,
    color: "text-green-500",
    bg: "bg-green-500/10",
    label: "Completed",
  },
  failed: {
    icon: XCircle,
    color: "text-destructive",
    bg: "bg-destructive/10",
    label: "Failed",
  },
};

export function RunCard({ run }: RunCardProps) {
  const status = statusConfig[run.status];
  const StatusIcon = status.icon;
  
  return (
    <Card className="p-4 hover-elevate" data-testid={`run-card-${run.id}`}>
      <div className="flex items-start justify-between mb-3">
        <Badge variant="outline" className="font-mono text-xs bg-[#b428ff]/10 border-[#b428ff]/20 text-[#b428ff]">
          {run.id}
        </Badge>
        <div className={cn("flex items-center gap-1.5 text-xs", status.color)}>
          <StatusIcon className="w-3.5 h-3.5" />
          <span className="font-medium">{status.label}</span>
        </div>
      </div>
      
      <div className="space-y-2 mb-4">
        <div className="text-xs text-muted-foreground">Hyperparameters</div>
        <div className="grid grid-cols-3 gap-2">
          <div className="bg-secondary/50 rounded p-2">
            <div className="text-xs text-muted-foreground">lr</div>
            <div className="font-mono text-sm font-semibold">{run.config.lr}</div>
          </div>
          <div className="bg-secondary/50 rounded p-2">
            <div className="text-xs text-muted-foreground">epochs</div>
            <div className="font-mono text-sm font-semibold">{run.config.epochs}</div>
          </div>
          <div className="bg-secondary/50 rounded p-2">
            <div className="text-xs text-muted-foreground">batch</div>
            <div className="font-mono text-sm font-semibold">{run.config.batch_size}</div>
          </div>
        </div>
      </div>
      
      {(run.val_loss !== undefined || run.lr_used !== undefined) && (
        <div className="space-y-2 mb-4 pb-4 border-b border-border">
          <div className="text-xs text-muted-foreground">Metrics</div>
          <div className="grid grid-cols-2 gap-2">
            {run.val_loss !== undefined && (
              <div>
                <div className="text-xs text-muted-foreground">Val Loss</div>
                <div className="font-mono text-base font-semibold text-primary">
                  {run.val_loss.toFixed(4)}
                </div>
              </div>
            )}
            {run.lr_used !== undefined && (
              <div>
                <div className="text-xs text-muted-foreground">LR Used</div>
                <div className="font-mono text-sm">
                  {run.lr_used}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
      
      <Link href={`/run/${run.id}`}>
        <Button variant="default" size="sm" className="w-full gap-2" data-testid={`button-view-plot-${run.id}`}>
          <BarChart3 className="w-4 h-4" />
          View Plot
        </Button>
      </Link>
    </Card>
  );
}
