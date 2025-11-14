import { cn } from "@/lib/utils";
import type { ChatMessage } from "@shared/schema";
import { Sparkles, User } from "lucide-react";

interface ChatBubbleProps {
  message: ChatMessage;
}

export function ChatBubble({ message }: ChatBubbleProps) {
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
            <p className="text-xs text-muted-foreground">Created {message.runConfigs.length} training run{message.runConfigs.length !== 1 ? 's' : ''}</p>
            <div className="space-y-2">
              {message.runConfigs.map((config, idx) => (
                <div
                  key={idx}
                  className="bg-secondary/50 rounded p-2 text-xs font-mono"
                  data-testid={`config-${idx}`}
                >
                  {Object.entries(config)
                    .map(([key, value]) => {
                      // Format key names nicely
                      const displayKey = key === 'lr' ? 'lr' : key === 'learning_rate' ? 'lr' : key;
                      return `${displayKey}: ${typeof value === 'number' ? value.toFixed(4) : value}`;
                    })
                    .join(' | ')}
                </div>
              ))}
            </div>
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
