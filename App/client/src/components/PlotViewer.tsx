import { useEffect, useState } from "react";
import type { PlotData } from "@shared/schema";
import { Card } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

interface PlotViewerProps {
  plotData: PlotData | null;
  isLoading?: boolean;
}

export function PlotViewer({ plotData, isLoading }: PlotViewerProps) {
  const [Plot, setPlot] = useState<any>(null);
  const [windowWidth, setWindowWidth] = useState(typeof window !== "undefined" ? window.innerWidth : 1200);
  
  useEffect(() => {
    import("react-plotly.js").then((mod) => setPlot(() => mod.default));
  }, []);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const handleResize = () => setWindowWidth(window.innerWidth);
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);
  
  if (isLoading || !Plot) {
    return (
      <Card className="p-6">
        <Skeleton className="w-full h-[500px]" />
      </Card>
    );
  }
  
  if (!plotData) {
    return (
      <Card className="p-6">
        <div className="flex items-center justify-center h-[500px]">
          <p className="text-muted-foreground">No plot data available</p>
        </div>
      </Card>
    );
  }
  
  const layout = {
    ...plotData.layout,
    autosize: true,
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: {
      color: "#f5f5f5",
      family: "Inter, system-ui, sans-serif",
    },
    xaxis: {
      ...plotData.layout.xaxis,
      gridcolor: "rgba(255,255,255,0.1)",
      color: "#f5f5f5",
    },
    yaxis: {
      ...plotData.layout.yaxis,
      gridcolor: "rgba(255,255,255,0.1)",
      color: "#f5f5f5",
    },
    margin: { t: 40, r: 20, b: 40, l: 60 },
  };
  
  return (
    <Card className="p-6" data-testid="plot-viewer">
      <Plot
        data={plotData.data}
        layout={layout}
        config={{
          responsive: true,
          displayModeBar: true,
          displaylogo: false,
        }}
        style={{ width: "100%", height: "500px" }}
      />
    </Card>
  );
}
