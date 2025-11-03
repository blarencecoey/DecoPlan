export interface FurnitureItem {
  id: string;
  name: string;
  category: string;
  style: string;
  price: number;
  description: string;
  imageUrl: string;
  dimensions?: string;
  material?: string;
  color?: string;
  relevanceScore?: number;
}

export interface RAGResponse {
  query: string;
  recommendations: FurnitureItem[];
  totalResults: number;
  processingTime?: number;
}

export interface FurnitureFilters {
  furnitureTypes?: string[];
  styles?: string[];
  minPrice?: number;
  maxPrice?: number;
  roomType?: string;
}
