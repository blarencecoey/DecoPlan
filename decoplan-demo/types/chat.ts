/**
 * Chat message types for the DecoPlan chatbox
 */

export type MessageRole = 'user' | 'assistant' | 'system';

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: Date;
}

export type RoomStyle =
  | 'modern'
  | 'japanese'
  | 'minimalist'
  | 'scandinavian'
  | 'industrial'
  | 'traditional';

export interface StyleQuery {
  style: RoomStyle;
  query: string;
}
