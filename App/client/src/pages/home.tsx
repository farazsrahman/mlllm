import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { ChatWindow } from "@/components/ChatWindow";
import { ChatInput } from "@/components/ChatInput";
import { RunsGrid } from "@/components/RunsGrid";
import { ThemeToggle } from "@/components/ThemeToggle";
import { getRuns, createRuns, sendChatMessage } from "@/lib/api";
// import { proposeRunsFromUserMessage } from "@/lib/llm"; // Kept for future implementation
import type { ChatMessage, RunConfig } from "@shared/schema";
import { useToast } from "@/hooks/use-toast";
import { queryClient } from "@/lib/queryClient";
import { Beaker } from "lucide-react";

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const { toast } = useToast();
  
  const { data: runs = [], isLoading: runsLoading } = useQuery({
    queryKey: ["/api/runs"],
    queryFn: getRuns,
  });
  
  const createRunsMutation = useMutation({
    mutationFn: createRuns,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/runs"] });
      toast({
        title: "Runs created",
        description: "Your training jobs have been queued successfully.",
      });
    },
    onError: () => {
      toast({
        title: "Error",
        description: "Failed to create runs. Please try again.",
        variant: "destructive",
      });
    },
  });
  
  const handleSendMessage = async (content: string) => {
    const userMessage: ChatMessage = {
      id: `msg-${Date.now()}`,
      role: "user",
      content,
      timestamp: new Date().toISOString(),
    };
    
    setMessages((prev) => [...prev, userMessage]);
    setIsProcessing(true);
    
    try {
      // Call backend API - backend will process message, generate configs, and execute runs immediately
      const assistantMessage = await sendChatMessage(content);
      
      setMessages((prev) => [...prev, assistantMessage]);
      
      // Refresh runs list since backend executed runs immediately
      queryClient.invalidateQueries({ queryKey: ["/api/runs"] });
      
      toast({
        title: "Runs executed",
        description: `Successfully processed your request and executed ${assistantMessage.runConfigs?.length || 0} training runs.`,
      });
    } catch (error) {
      const errorContent = error instanceof Error ? error.message : "Sorry, I encountered an error processing your request. Please try again.";
      const errorMessage: ChatMessage = {
        id: `msg-${Date.now() + 1}`,
        role: "assistant",
        content: errorContent,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
      
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to process your message. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
    
    // FUTURE IMPLEMENTATION: For back-and-forth approval flow, use this code instead:
    // const configs = await proposeRunsFromUserMessage(content);
    // const assistantMessage: ChatMessage = {
    //   id: `msg-${Date.now() + 1}`,
    //   role: "assistant",
    //   content: `I've analyzed your request and proposed ${configs.length} configurations. Would you like to start these runs?`,
    //   timestamp: new Date().toISOString(),
    //   runConfigs: configs,
    // };
    // setMessages((prev) => [...prev, assistantMessage]);
  };
  
  const handleAcceptConfigs = (configs: RunConfig[]) => {
    createRunsMutation.mutate(configs);
    
    const confirmMessage: ChatMessage = {
      id: `msg-${Date.now()}`,
      role: "system",
      content: `Starting ${configs.length} training runs...`,
      timestamp: new Date().toISOString(),
    };
    
    setMessages((prev) => [...prev, confirmMessage]);
  };
  
  return (
    <div className="h-screen flex flex-col bg-background">
      <header className="border-b border-border bg-card px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-md bg-primary flex items-center justify-center">
              <Beaker className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-xl font-bold" data-testid="text-title">Trex</h1>
              <p className="text-xs text-muted-foreground">ML Experiment Assistant</p>
            </div>
          </div>
          <ThemeToggle />
        </div>
      </header>
      
      <div className="flex-1 overflow-hidden">
        <div className="h-full flex flex-col lg:flex-row">
          <div className="lg:w-[40%] flex flex-col border-r border-border bg-card">
            <div className="flex-1 overflow-hidden flex flex-col">
              <ChatWindow
                messages={messages}
                onRunConfigsAccept={handleAcceptConfigs}
                isProcessing={isProcessing}
              />
              <ChatInput
                onSend={handleSendMessage}
                disabled={isProcessing}
              />
            </div>
          </div>
          
          <div className="lg:w-[60%] p-6 overflow-auto">
            <div className="mb-6">
              <h2 className="text-lg font-semibold mb-1">Training Runs</h2>
              <p className="text-sm text-muted-foreground">
                View and manage your experiment runs
              </p>
            </div>
            <RunsGrid runs={runs} isLoading={runsLoading} />
          </div>
        </div>
      </div>
    </div>
  );
}
