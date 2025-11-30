'use client';

import { useState, useRef, useEffect } from 'react';
import { ChatMessage } from '@/types/chat';

interface ChatBoxProps {
  messages: ChatMessage[];
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

/**
 * ChatBox component for user interaction
 * Allows users to request specific room styles and furniture
 */
export default function ChatBox({ messages, onSendMessage, isLoading }: ChatBoxProps) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleQuickPrompt = (prompt: string) => {
    if (!isLoading) {
      onSendMessage(prompt);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white border-t border-gray-200">
      {/* Chat header */}
      <div className="px-4 py-3 bg-gradient-to-r from-purple-600 to-purple-700 text-white">
        <h3 className="font-semibold text-sm">AI Design Assistant</h3>
        <p className="text-xs text-purple-100 mt-0.5">
          Ask me to generate different room styles
        </p>
      </div>

      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3 min-h-0">
        {messages.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-gray-400 mb-3">
              <svg
                className="w-12 h-12 mx-auto"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                />
              </svg>
            </div>
            <p className="text-sm text-gray-500 mb-4">
              Start by asking for a room style
            </p>

            {/* Quick prompts */}
            <div className="space-y-2">
              <p className="text-xs text-gray-400 font-medium">Try these:</p>
              <div className="flex flex-col gap-2">
                <button
                  onClick={() => handleQuickPrompt('Generate a Japanese style living room')}
                  disabled={isLoading}
                  className="px-3 py-2 bg-purple-50 hover:bg-purple-100 text-purple-700 rounded-lg text-xs transition-colors disabled:opacity-50"
                >
                  Japanese style living room
                </button>
                <button
                  onClick={() => handleQuickPrompt('Generate a modern minimalist room')}
                  disabled={isLoading}
                  className="px-3 py-2 bg-purple-50 hover:bg-purple-100 text-purple-700 rounded-lg text-xs transition-colors disabled:opacity-50"
                >
                  Modern minimalist room
                </button>
                <button
                  onClick={() => handleQuickPrompt('Show me traditional HDB furniture')}
                  disabled={isLoading}
                  className="px-3 py-2 bg-purple-50 hover:bg-purple-100 text-purple-700 rounded-lg text-xs transition-colors disabled:opacity-50"
                >
                  Traditional HDB furniture
                </button>
              </div>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-lg px-4 py-2 ${
                    message.role === 'user'
                      ? 'bg-purple-600 text-white'
                      : message.role === 'system'
                      ? 'bg-blue-50 text-blue-900 border border-blue-200'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  {message.role === 'assistant' && (
                    <div className="flex items-center gap-2 mb-1">
                      <svg
                        className="w-4 h-4 text-purple-600"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z"
                          clipRule="evenodd"
                        />
                      </svg>
                      <span className="text-xs font-semibold text-purple-600">
                        AI Assistant
                      </span>
                    </div>
                  )}
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  <p
                    className={`text-xs mt-1 ${
                      message.role === 'user'
                        ? 'text-purple-200'
                        : 'text-gray-500'
                    }`}
                  >
                    {new Date(message.timestamp).toLocaleTimeString([], {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </p>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input area */}
      <form onSubmit={handleSubmit} className="p-3 border-t border-gray-200 bg-gray-50">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask for a room style (e.g., Japanese living room)..."
            disabled={isLoading}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
          >
            {isLoading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Generating...</span>
              </>
            ) : (
              <>
                <svg
                  className="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                  />
                </svg>
                <span>Send</span>
              </>
            )}
          </button>
        </div>

        {/* Quick action buttons when chat has started */}
        {messages.length > 0 && (
          <div className="mt-2 flex gap-2 flex-wrap">
            <button
              type="button"
              onClick={() => handleQuickPrompt('Generate a Japanese style living room')}
              disabled={isLoading}
              className="px-2 py-1 bg-white hover:bg-gray-50 border border-gray-300 text-gray-700 rounded text-xs transition-colors disabled:opacity-50"
            >
              Japanese
            </button>
            <button
              type="button"
              onClick={() => handleQuickPrompt('Generate a modern room')}
              disabled={isLoading}
              className="px-2 py-1 bg-white hover:bg-gray-50 border border-gray-300 text-gray-700 rounded text-xs transition-colors disabled:opacity-50"
            >
              Modern
            </button>
            <button
              type="button"
              onClick={() => handleQuickPrompt('Generate a minimalist room')}
              disabled={isLoading}
              className="px-2 py-1 bg-white hover:bg-gray-50 border border-gray-300 text-gray-700 rounded text-xs transition-colors disabled:opacity-50"
            >
              Minimalist
            </button>
          </div>
        )}
      </form>
    </div>
  );
}
