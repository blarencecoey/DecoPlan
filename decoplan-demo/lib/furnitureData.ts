import { Furniture, FurnitureCategory } from '@/types/furniture';

/**
 * Mock furniture database simulating items that would be retrieved by RAG system
 * Each item represents furniture that matches a typical HDB living room layout
 */
export const MOCK_FURNITURE_DATABASE: Omit<Furniture, 'visible'>[] = [
  {
    id: 'sofa-001',
    name: 'Modern L-Shaped Sofa',
    category: 'sofa',
    position: { x: -2, y: 0.4, z: 0 },
    dimensions: { width: 2.5, height: 0.8, depth: 1.5 },
    color: { r: 100, g: 100, b: 120 },
    confidenceScore: 0.95,
    description: 'Comfortable modern L-shaped sofa perfect for HDB living rooms',
  },
  {
    id: 'table-001',
    name: 'Coffee Table',
    category: 'table',
    position: { x: -1, y: 0.2, z: 2 },
    dimensions: { width: 1.2, height: 0.4, depth: 0.6 },
    color: { r: 139, g: 90, b: 60 },
    confidenceScore: 0.92,
    description: 'Wooden coffee table with storage compartment',
  },
  {
    id: 'table-002',
    name: 'Dining Table',
    category: 'table',
    position: { x: 3, y: 0.4, z: -2 },
    dimensions: { width: 1.6, height: 0.8, depth: 0.9 },
    color: { r: 160, g: 120, b: 80 },
    confidenceScore: 0.88,
    description: '4-seater dining table, space-saving design',
  },
  {
    id: 'chair-001',
    name: 'Dining Chair',
    category: 'chair',
    position: { x: 2.5, y: 0.45, z: -1.5 },
    dimensions: { width: 0.5, height: 0.9, depth: 0.5 },
    color: { r: 80, g: 80, b: 80 },
    confidenceScore: 0.90,
    description: 'Modern dining chair with ergonomic design',
  },
  {
    id: 'chair-002',
    name: 'Dining Chair',
    category: 'chair',
    position: { x: 3.5, y: 0.45, z: -1.5 },
    dimensions: { width: 0.5, height: 0.9, depth: 0.5 },
    color: { r: 80, g: 80, b: 80 },
    confidenceScore: 0.90,
    description: 'Modern dining chair with ergonomic design',
  },
  {
    id: 'cabinet-001',
    name: 'TV Console',
    category: 'cabinet',
    position: { x: -4, y: 0.3, z: 3 },
    dimensions: { width: 2.0, height: 0.6, depth: 0.4 },
    color: { r: 70, g: 50, b: 40 },
    confidenceScore: 0.87,
    description: 'Modern TV console with shelving',
  },
  {
    id: 'shelf-001',
    name: 'Wall Shelf Unit',
    category: 'shelf',
    position: { x: 4, y: 1.0, z: 2 },
    dimensions: { width: 1.0, height: 2.0, depth: 0.3 },
    color: { r: 200, g: 200, b: 200 },
    confidenceScore: 0.85,
    description: 'Vertical storage shelf unit',
  },
  {
    id: 'lamp-001',
    name: 'Floor Lamp',
    category: 'lamp',
    position: { x: -3, y: 0.8, z: -2 },
    dimensions: { width: 0.3, height: 1.6, depth: 0.3 },
    color: { r: 220, g: 180, b: 100 },
    confidenceScore: 0.83,
    description: 'Modern floor lamp with adjustable head',
  },
  {
    id: 'sofa-002',
    name: 'Accent Chair',
    category: 'sofa',
    position: { x: 0, y: 0.4, z: -3 },
    dimensions: { width: 0.8, height: 0.9, depth: 0.8 },
    color: { r: 180, g: 140, b: 100 },
    confidenceScore: 0.81,
    description: 'Stylish accent chair for additional seating',
  },
  {
    id: 'table-003',
    name: 'Side Table',
    category: 'table',
    position: { x: 0.5, y: 0.3, z: -3.5 },
    dimensions: { width: 0.5, height: 0.6, depth: 0.5 },
    color: { r: 100, g: 70, b: 50 },
    confidenceScore: 0.79,
    description: 'Compact side table for small spaces',
  },
];

/**
 * Japanese-style furniture database
 * Focused on minimalist, low-profile furniture with natural materials
 */
export const JAPANESE_FURNITURE_DATABASE: Omit<Furniture, 'visible'>[] = [
  {
    id: 'jp-table-001',
    name: 'Chabudai Low Table',
    category: 'table',
    position: { x: 0, y: 0.15, z: 0 },
    dimensions: { width: 1.2, height: 0.3, depth: 0.8 },
    color: { r: 139, g: 90, b: 60 },
    confidenceScore: 0.96,
    description: 'Traditional Japanese low dining table',
  },
  {
    id: 'jp-sofa-001',
    name: 'Futon Seating',
    category: 'sofa',
    position: { x: -2.5, y: 0.2, z: -2 },
    dimensions: { width: 1.8, height: 0.4, depth: 0.9 },
    color: { r: 120, g: 110, b: 100 },
    confidenceScore: 0.94,
    description: 'Low-profile Japanese futon seating',
  },
  {
    id: 'jp-cabinet-001',
    name: 'Tansu Storage Cabinet',
    category: 'cabinet',
    position: { x: -4, y: 0.4, z: 2 },
    dimensions: { width: 1.5, height: 0.8, depth: 0.4 },
    color: { r: 90, g: 60, b: 40 },
    confidenceScore: 0.92,
    description: 'Traditional Japanese chest of drawers',
  },
  {
    id: 'jp-lamp-001',
    name: 'Andon Floor Lamp',
    category: 'lamp',
    position: { x: -3.5, y: 0.6, z: -3 },
    dimensions: { width: 0.35, height: 1.2, depth: 0.35 },
    color: { r: 240, g: 230, b: 210 },
    confidenceScore: 0.90,
    description: 'Traditional Japanese paper lantern lamp',
  },
  {
    id: 'jp-shelf-001',
    name: 'Shoji Screen Shelf',
    category: 'shelf',
    position: { x: 4, y: 0.9, z: 0 },
    dimensions: { width: 1.2, height: 1.8, depth: 0.25 },
    color: { r: 230, g: 220, b: 200 },
    confidenceScore: 0.88,
    description: 'Japanese-style display shelf with sliding doors',
  },
  {
    id: 'jp-table-002',
    name: 'Tea Ceremony Table',
    category: 'table',
    position: { x: 2, y: 0.12, z: -2.5 },
    dimensions: { width: 0.8, height: 0.25, depth: 0.6 },
    color: { r: 110, g: 75, b: 50 },
    confidenceScore: 0.86,
    description: 'Small low table for tea ceremonies',
  },
  {
    id: 'jp-chair-001',
    name: 'Zaisu Floor Chair',
    category: 'chair',
    position: { x: 0.8, y: 0.15, z: 0.5 },
    dimensions: { width: 0.55, height: 0.3, depth: 0.55 },
    color: { r: 100, g: 90, b: 80 },
    confidenceScore: 0.85,
    description: 'Japanese legless floor chair',
  },
  {
    id: 'jp-chair-002',
    name: 'Zaisu Floor Chair',
    category: 'chair',
    position: { x: -0.8, y: 0.15, z: 0.5 },
    dimensions: { width: 0.55, height: 0.3, depth: 0.55 },
    color: { r: 100, g: 90, b: 80 },
    confidenceScore: 0.85,
    description: 'Japanese legless floor chair',
  },
  {
    id: 'jp-cabinet-002',
    name: 'Kotatsu Table',
    category: 'table',
    position: { x: 2.5, y: 0.2, z: 1.5 },
    dimensions: { width: 1.0, height: 0.4, depth: 1.0 },
    color: { r: 130, g: 85, b: 55 },
    confidenceScore: 0.83,
    description: 'Heated table with blanket (winter essential)',
  },
  {
    id: 'jp-other-001',
    name: 'Bonsai Display Stand',
    category: 'other',
    position: { x: 3.5, y: 0.35, z: -1 },
    dimensions: { width: 0.5, height: 0.7, depth: 0.4 },
    color: { r: 140, g: 100, b: 70 },
    confidenceScore: 0.80,
    description: 'Decorative stand for bonsai or ikebana',
  },
];

/**
 * Category color mapping for 3D visualization
 * Returns consistent colors for each furniture category
 */
export const CATEGORY_COLORS: Record<FurnitureCategory, string> = {
  sofa: '#6B7280', // Gray
  table: '#8B5A3C', // Brown
  chair: '#505050', // Dark Gray
  bed: '#9CA3AF', // Light Gray
  cabinet: '#46362C', // Dark Brown
  shelf: '#C8C8C8', // Light Gray
  lamp: '#DCC864', // Yellow/Gold
  other: '#94A3B8', // Slate Gray
};

/**
 * Helper function to get hex color from RGB
 */
export function rgbToHex(r: number, g: number, b: number): string {
  return '#' + [r, g, b].map(x => {
    const hex = x.toString(16);
    return hex.length === 1 ? '0' + hex : hex;
  }).join('');
}
