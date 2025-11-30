import { Furniture, RAGRetrievalResult } from '@/types/furniture';
import { MOCK_FURNITURE_DATABASE, JAPANESE_FURNITURE_DATABASE } from './furnitureData';
import { RoomStyle } from '@/types/chat';

/**
 * Simulates a RAG (Retrieval-Augmented Generation) system for furniture retrieval
 * In a real implementation, this would:
 * 1. Take user query/room requirements
 * 2. Query a vector database of furniture items
 * 3. Use LLM to rank and filter relevant furniture
 * 4. Return confidence-scored results
 */

/**
 * Simulates network delay for realistic retrieval experience
 */
const simulateDelay = (ms: number = 1500): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

/**
 * Detects room style from user query
 * Uses simple keyword matching (in real implementation, would use NLP/LLM)
 */
export function detectRoomStyle(query: string): RoomStyle {
  const lowerQuery = query.toLowerCase();

  if (lowerQuery.includes('japanese') || lowerQuery.includes('japan') ||
      lowerQuery.includes('zen') || lowerQuery.includes('tatami')) {
    return 'japanese';
  }
  if (lowerQuery.includes('minimalist') || lowerQuery.includes('minimal')) {
    return 'minimalist';
  }
  if (lowerQuery.includes('scandinavian') || lowerQuery.includes('nordic')) {
    return 'scandinavian';
  }
  if (lowerQuery.includes('industrial')) {
    return 'industrial';
  }
  if (lowerQuery.includes('traditional')) {
    return 'traditional';
  }

  // Default to modern
  return 'modern';
}

/**
 * Gets furniture database based on detected style
 */
function getFurnitureByStyle(style: RoomStyle): Omit<Furniture, 'visible'>[] {
  switch (style) {
    case 'japanese':
      return JAPANESE_FURNITURE_DATABASE;
    case 'modern':
    case 'minimalist':
    case 'scandinavian':
    case 'industrial':
    case 'traditional':
    default:
      return MOCK_FURNITURE_DATABASE;
  }
}

/**
 * Mock RAG retrieval function
 * Simulates retrieving furniture based on a query
 *
 * @param query - User query (e.g., "modern living room", "japanese style room")
 * @param maxResults - Maximum number of results to return
 * @returns RAGRetrievalResult with furniture items and metadata
 */
export async function retrieveFurniture(
  query: string = 'HDB living room furniture',
  maxResults: number = 10
): Promise<RAGRetrievalResult> {
  // Simulate network delay
  await simulateDelay(1500);

  // Detect room style from query
  const style = detectRoomStyle(query);

  // Get appropriate furniture database
  const furnitureDatabase = getFurnitureByStyle(style);

  // In a real implementation, this would:
  // 1. Embed the query using an embedding model
  // 2. Perform vector similarity search
  // 3. Re-rank results using LLM
  // For now, we'll return all furniture sorted by confidence score

  const retrievedFurniture: Furniture[] = furnitureDatabase
    .slice(0, maxResults)
    .map(item => ({
      ...item,
      visible: true, // All items visible by default
    }))
    .sort((a, b) => b.confidenceScore - a.confidenceScore);

  return {
    furniture: retrievedFurniture,
    timestamp: new Date(),
    query,
  };
}

/**
 * Simulates a targeted retrieval for specific furniture categories
 *
 * @param categories - Array of furniture categories to retrieve
 * @returns RAGRetrievalResult with filtered furniture items
 */
export async function retrieveFurnitureByCategory(
  categories: string[]
): Promise<RAGRetrievalResult> {
  await simulateDelay(1000);

  const retrievedFurniture: Furniture[] = MOCK_FURNITURE_DATABASE
    .filter(item => categories.includes(item.category))
    .map(item => ({
      ...item,
      visible: true,
    }))
    .sort((a, b) => b.confidenceScore - a.confidenceScore);

  return {
    furniture: retrievedFurniture,
    timestamp: new Date(),
    query: `Categories: ${categories.join(', ')}`,
  };
}

/**
 * Calculates room coverage statistics
 * Useful for understanding space utilization
 */
export function calculateRoomCoverage(
  furniture: Furniture[],
  roomWidth: number,
  roomDepth: number
): {
  totalFootprint: number;
  coveragePercentage: number;
  itemCount: number;
} {
  const visibleFurniture = furniture.filter(f => f.visible);

  const totalFootprint = visibleFurniture.reduce(
    (sum, item) => sum + (item.dimensions.width * item.dimensions.depth),
    0
  );

  const roomArea = roomWidth * roomDepth;
  const coveragePercentage = (totalFootprint / roomArea) * 100;

  return {
    totalFootprint: Math.round(totalFootprint * 100) / 100,
    coveragePercentage: Math.round(coveragePercentage * 10) / 10,
    itemCount: visibleFurniture.length,
  };
}
