import { RAGResponse, FurnitureItem } from '../types/furniture';

// Flask backend URL - can be configured via environment variable
const FLASK_API_URL = import.meta.env.VITE_FLASK_API_URL || 'http://localhost:5000';

/**
 * Sends a prompt to the Flask backend RAG model
 * @param prompt - User's furniture request prompt
 * @param furnitureTypes - Optional array of furniture types to filter by
 * @returns Promise with furniture recommendations
 */
export async function getFurnitureRecommendations(
  prompt: string,
  furnitureTypes?: string[]
): Promise<RAGResponse> {
  try {
    const requestBody: { prompt: string; furniture_types?: string[] } = { prompt };

    if (furnitureTypes && furnitureTypes.length > 0) {
      requestBody.furniture_types = furnitureTypes;
    }

    console.log('Sending request to backend:', requestBody);

    const response = await fetch(`${FLASK_API_URL}/api/recommendations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch recommendations');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching recommendations:', error);
    throw error;
  }
}
