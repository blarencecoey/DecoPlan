'use client';

import { useState } from 'react';
import dynamic from 'next/dynamic';
import { Furniture } from '@/types/furniture';
import { ChatMessage } from '@/types/chat';
import { retrieveFurniture, detectRoomStyle } from '@/lib/mockRAG';
import FurniturePanel from '@/components/FurniturePanel';
import ChatBox from '@/components/ChatBox';

// Dynamically import RoomViewer to avoid SSR issues with Three.js
const RoomViewer = dynamic(() => import('@/components/RoomViewer'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full flex items-center justify-center bg-gradient-to-b from-gray-800 to-gray-900">
      <div className="text-white text-center">
        <div className="w-16 h-16 border-4 border-white border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p>Loading 3D Viewer...</p>
      </div>
    </div>
  ),
});

/**
 * Main DecoPlan application page
 * Manages state for furniture retrieval and visualization
 */
export default function HomePage() {
  const [furniture, setFurniture] = useState<Furniture[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);

  /**
   * Handles furniture retrieval from mock RAG system
   */
  const handleRetrieveFurniture = async () => {
    setIsLoading(true);
    try {
      const result = await retrieveFurniture('Modern HDB living room setup', 10);
      setFurniture(result.furniture);
    } catch (error) {
      console.error('Error retrieving furniture:', error);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Handles chat messages from the chatbox
   */
  const handleSendMessage = async (message: string) => {
    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: message,
      timestamp: new Date(),
    };
    setChatMessages(prev => [...prev, userMessage]);

    // Start loading
    setIsLoading(true);

    try {
      // Detect style from message
      const style = detectRoomStyle(message);

      // Retrieve furniture based on query
      const result = await retrieveFurniture(message, 10);
      setFurniture(result.furniture);

      // Add assistant response
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `I've generated a ${style} style living room with ${result.furniture.length} furniture items. The furniture has been placed in the 3D viewer for you to explore!`,
        timestamp: new Date(),
      };
      setChatMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error retrieving furniture:', error);

      // Add error message
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error while generating the room. Please try again.',
        timestamp: new Date(),
      };
      setChatMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Toggles visibility of a specific furniture item
   */
  const handleToggleFurniture = (id: string) => {
    setFurniture(prevFurniture =>
      prevFurniture.map(item =>
        item.id === id ? { ...item, visible: !item.visible } : item
      )
    );
  };

  return (
    <main className="h-screen w-screen flex overflow-hidden">
      {/* 3D Viewer Section (70%) */}
      <div className="flex-1 relative">
        <RoomViewer furniture={furniture} />

        {/* Floating info badge */}
        <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg shadow-lg p-3 max-w-xs">
          <h1 className="text-lg font-bold text-gray-900 mb-1">
            DecoPlan Demo
          </h1>
          <p className="text-xs text-gray-600">
            HDB Interior Design Visualization with RAG-powered furniture retrieval
          </p>
          <div className="mt-2 flex gap-2 text-xs">
            <span className="bg-primary-100 text-primary-700 px-2 py-1 rounded">
              Next.js 14
            </span>
            <span className="bg-purple-100 text-purple-700 px-2 py-1 rounded">
              Three.js
            </span>
            <span className="bg-green-100 text-green-700 px-2 py-1 rounded">
              RAG Mock
            </span>
          </div>
        </div>

        {/* Camera controls info */}
        <div className="absolute bottom-4 left-4 bg-black/70 text-white rounded-lg p-3 text-xs backdrop-blur-sm">
          <div className="font-semibold mb-2">Camera Controls:</div>
          <div className="space-y-1">
            <div><span className="text-primary-400">Left Click + Drag:</span> Rotate</div>
            <div><span className="text-primary-400">Right Click + Drag:</span> Pan</div>
            <div><span className="text-primary-400">Scroll:</span> Zoom</div>
          </div>
        </div>

        {/* Item count indicator */}
        {furniture.length > 0 && (
          <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm rounded-lg shadow-lg px-4 py-2">
            <div className="text-sm text-gray-600">Showing</div>
            <div className="text-2xl font-bold text-primary-600">
              {furniture.filter(f => f.visible).length}/{furniture.length}
            </div>
            <div className="text-xs text-gray-500">items</div>
          </div>
        )}
      </div>

      {/* Right Panel Section (30%) */}
      <div className="w-[400px] border-l border-gray-300 flex-shrink-0 shadow-2xl flex flex-col">
        {/* Chat Box - Upper half */}
        <div className="h-1/2 border-b border-gray-300">
          <ChatBox
            messages={chatMessages}
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
          />
        </div>

        {/* Furniture Panel - Lower half */}
        <div className="h-1/2 overflow-hidden">
          <FurniturePanel
            furniture={furniture}
            onToggleFurniture={handleToggleFurniture}
            onRetrieveFurniture={handleRetrieveFurniture}
            isLoading={isLoading}
          />
        </div>
      </div>
    </main>
  );
}
