import { useEffect, useRef } from "react";
import { ChatBubble } from "./ChatBubble";
import { ScrollArea } from "@/components/ui/scroll-area";
import type { ChatMessage } from "@shared/schema";
import { Sparkles } from "lucide-react";

interface ChatWindowProps {
  messages: ChatMessage[];
  onRunConfigsAccept?: (configs: any[]) => void;
}

export function ChatWindow({ messages, onRunConfigsAccept }: ChatWindowProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);
  
  return (
    <ScrollArea className="flex-1 p-4" data-testid="chat-window">
      <div ref={scrollRef}>
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-[400px] text-center px-8">
            <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-4">
              <Sparkles className="w-8 h-8 text-primary" />
            </div>
            <h2 className="text-xl font-semibold mb-2">Welcome to Trex</h2>
            <p className="text-muted-foreground text-sm max-w-md">
              Your ML experiment assistant. Describe what you want to test, and I'll help you
              configure and run multiple training jobs.
            </p>
            <div className="mt-6 space-y-2 text-left w-full max-w-md">
              <div className="text-xs font-mono bg-secondary/50 rounded p-3">
                "Test learning rates from 0.001 to 0.0001"
              </div>
              <div className="text-xs font-mono bg-secondary/50 rounded p-3">
                "Compare batch sizes 16, 32, and 64"
              </div>
              <div className="text-xs font-mono bg-secondary/50 rounded p-3">
                "Run 5, 10, and 20 epochs with lr=0.001"
              </div>
            </div>
          </div>
        ) : (
          <div>
            {messages.map((message) => (
              <ChatBubble
                key={message.id}
                message={message}
                onRunConfigsAccept={onRunConfigsAccept}
              />
            ))}
          </div>
        )}
      </div>
    </ScrollArea>
  );
}
