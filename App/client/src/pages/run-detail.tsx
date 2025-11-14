import { useParams, Link } from "wouter";
import { useQuery } from "@tanstack/react-query";
import { getRun, getPlot } from "@/lib/api";
import { PlotViewer } from "@/components/PlotViewer";
import { ThemeToggle } from "@/components/ThemeToggle";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { ArrowLeft, Activity, CheckCircle2, Clock, XCircle } from "lucide-react";
import { cn } from "@/lib/utils";

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

export default function RunDetail() {
  const params = useParams<{ id: string }>();
  const runId = params.id || "";
  
  const { data: run, isLoading: runLoading } = useQuery({
    queryKey: ["/api/run", runId],
    queryFn: () => getRun(runId),
    enabled: !!runId,
  });
  
  const { data: plotData, isLoading: plotLoading } = useQuery({
    queryKey: ["/api/plot", runId],
    queryFn: () => getPlot(runId),
    enabled: !!runId,
  });
  
  if (!runId) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <p className="text-muted-foreground">Invalid run ID</p>
      </div>
    );
  }
  
  const status = run ? statusConfig[run.status] : null;
  const StatusIcon = status?.icon;
  
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border bg-card px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/">
              <Button variant="ghost" size="sm" className="gap-2" data-testid="button-back">
                <ArrowLeft className="w-4 h-4" />
                Back
              </Button>
            </Link>
            <div className="flex-1">
              <h1 className="text-xl font-bold" data-testid="text-run-title">Run Details</h1>
            </div>
          </div>
          <ThemeToggle />
        </div>
      </header>
      
      <div className="max-w-7xl mx-auto p-6 space-y-6">
        {runLoading ? (
          <Card className="p-6">
            <Skeleton className="h-8 w-48 mb-4" />
            <Skeleton className="h-4 w-full mb-2" />
            <Skeleton className="h-4 w-3/4" />
          </Card>
        ) : run ? (
          <Card className="p-6">
            <div className="flex items-start justify-between mb-6">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <Badge 
                    variant="outline" 
                    className="font-mono bg-[#b428ff]/10 border-[#b428ff]/20 text-[#b428ff]"
                    data-testid="badge-run-id"
                  >
                    {run.id}
                  </Badge>
                  {status && StatusIcon && (
                    <div className={cn("flex items-center gap-1.5 text-sm", status.color)}>
                      <StatusIcon className="w-4 h-4" />
                      <span className="font-medium">{status.label}</span>
                    </div>
                  )}
                </div>
                <h2 className="text-2xl font-bold">Training Run</h2>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <div>
                <h3 className="text-sm font-semibold mb-3 text-muted-foreground">Hyperparameters</h3>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Learning Rate</span>
                    <span className="font-mono font-semibold" data-testid="text-lr">{run.config.lr}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Epochs</span>
                    <span className="font-mono font-semibold" data-testid="text-epochs">{run.config.epochs}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Batch Size</span>
                    <span className="font-mono font-semibold" data-testid="text-batch">{run.config.batch_size}</span>
                  </div>
                </div>
              </div>
              
              {(run.val_loss !== undefined || run.lr_used !== undefined) && (
                <div>
                  <h3 className="text-sm font-semibold mb-3 text-muted-foreground">Metrics</h3>
                  <div className="space-y-2">
                    {run.val_loss !== undefined && (
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-muted-foreground">Validation Loss</span>
                        <span className="font-mono font-semibold text-primary" data-testid="text-val-loss">
                          {run.val_loss.toFixed(4)}
                        </span>
                      </div>
                    )}
                    {run.lr_used !== undefined && (
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-muted-foreground">LR Used</span>
                        <span className="font-mono font-semibold">{run.lr_used}</span>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </Card>
        ) : (
          <Card className="p-6">
            <p className="text-muted-foreground">Run not found</p>
          </Card>
        )}
        
        <div>
          <h3 className="text-lg font-semibold mb-4">Training Progress</h3>
          <PlotViewer plotData={plotData || null} isLoading={plotLoading} />
        </div>
      </div>
    </div>
  );
}
