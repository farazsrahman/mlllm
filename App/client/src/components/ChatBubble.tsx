import { cn } from "@/lib/utils";
import type { ChatMessage } from "@shared/schema";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Sparkles, User } from "lucide-react";

interface ChatBubbleProps {
  message: ChatMessage;
  onRunConfigsAccept?: (configs: any[]) => void;
}

export function ChatBubble({ message, onRunConfigsAccept }: ChatBubbleProps) {
  const isUser = message.role === "user";
  const isAssistant = message.role === "assistant";
  
  return (
    <div
      className={cn(
        "flex gap-3 mb-4",
        isUser ? "justify-end" : "justify-start"
      )}
      data-testid={`chat-bubble-${message.id}`}
    >
      {isAssistant && (
        <div className="flex-shrink-0 w-8 h-8 rounded-md bg-primary flex items-center justify-center">
          <Sparkles className="w-4 h-4 text-primary-foreground" />
        </div>
      )}
      
      <div
        className={cn(
          "max-w-[75%] rounded-md p-4",
          isUser
            ? "bg-primary text-primary-foreground"
            : "bg-card border border-card-border"
        )}
      >
        <p className="text-sm whitespace-pre-wrap" data-testid={`message-content-${message.id}`}>
          {message.content}
        </p>
        
        {message.runConfigs && message.runConfigs.length > 0 && (
          <div className="mt-3 space-y-2">
            <p className="text-xs text-muted-foreground">Proposed configurations:</p>
            <div className="space-y-2">
              {message.runConfigs.map((config, idx) => (
                <div
                  key={idx}
                  className="bg-secondary/50 rounded p-2 text-xs font-mono"
                  data-testid={`config-${idx}`}
                >
                  lr: {config.lr} | epochs: {config.epochs} | batch: {config.batch_size}
                </div>
              ))}
            </div>
            <Button
              size="sm"
              className="w-full mt-2"
              onClick={() => onRunConfigsAccept?.(message.runConfigs!)}
              data-testid="button-accept-configs"
            >
              Start These Runs
            </Button>
          </div>
        )}
        
        <p className="text-xs text-muted-foreground mt-2">
          {new Date(message.timestamp).toLocaleTimeString()}
        </p>
      </div>
      
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-md bg-secondary flex items-center justify-center">
          <User className="w-4 h-4 text-secondary-foreground" />
        </div>
      )}
    </div>
  );
}
