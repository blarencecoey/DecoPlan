/**
 * Represents a 3D position in space
 */
export interface Position {
  x: number;
  y: number;
  z: number;
}

/**
 * Represents the dimensions of a furniture piece
 */
export interface Dimensions {
  width: number;
  height: number;
  depth: number;
}

/**
 * Represents the color of a furniture piece in RGB format
 */
export interface Color {
  r: number;
  g: number;
  b: number;
}

/**
 * Furniture category types
 */
export type FurnitureCategory =
  | 'sofa'
  | 'table'
  | 'chair'
  | 'bed'
  | 'cabinet'
  | 'shelf'
  | 'lamp'
  | 'other';

/**
 * Main furniture interface representing a furniture item retrieved by RAG
 */
export interface Furniture {
  id: string;
  name: string;
  category: FurnitureCategory;
  position: Position;
  dimensions: Dimensions;
  color: Color;
  confidenceScore: number; // RAG retrieval confidence score (0-1)
  visible: boolean; // Toggle visibility in the 3D scene
  description?: string;
}

/**
 * Room configuration interface
 */
export interface RoomConfig {
  width: number;
  length: number;
  height: number;
  wallColor: Color;
  floorColor: Color;
}

/**
 * RAG retrieval result interface
 */
export interface RAGRetrievalResult {
  furniture: Furniture[];
  timestamp: Date;
  query?: string;
}
