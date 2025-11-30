# DecoPlan Demo - HDB Interior Design Visualization

A proof-of-concept demonstration of DecoPlan, an HDB interior design visualization system that showcases furniture retrieved by a RAG (Retrieval-Augmented Generation) system rendered in an interactive 3D room viewer.

![DecoPlan Demo](https://img.shields.io/badge/Next.js-14+-black?style=flat-square&logo=next.js)
![React](https://img.shields.io/badge/React-19+-61DAFB?style=flat-square&logo=react)
![Three.js](https://img.shields.io/badge/Three.js-Latest-black?style=flat-square&logo=three.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6?style=flat-square&logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-4+-38B2AC?style=flat-square&logo=tailwind-css)

## Features

- **3D Room Viewer**: Interactive HDB room visualization using Three.js
- **Mock RAG System**: Simulated furniture retrieval with confidence scores
- **Interactive Furniture Placement**: Toggle visibility and explore furniture items
- **Real-time Statistics**: Room coverage, footprint calculations, and item counts
- **Responsive UI**: Split-screen layout with 3D viewer and furniture panel
- **Modern Tech Stack**: Built with Next.js 14, TypeScript, and React Three Fiber

## Tech Stack

- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **3D Graphics**: Three.js via @react-three/fiber and @react-three/drei
- **Styling**: Tailwind CSS 4
- **State Management**: React Hooks (useState)

## Project Structure

```
decoplan-demo/
├── app/
│   ├── globals.css          # Global styles with Tailwind imports
│   ├── layout.tsx            # Root layout component
│   └── page.tsx              # Main application page
├── components/
│   ├── RoomViewer.tsx        # Three.js 3D scene component
│   ├── FurniturePanel.tsx    # Sidebar furniture list panel
│   └── FurnitureItem.tsx     # Individual furniture card component
├── lib/
│   ├── mockRAG.ts            # Simulated RAG retrieval system
│   └── furnitureData.ts      # Mock furniture database
├── types/
│   └── furniture.ts          # TypeScript type definitions
├── public/                   # Static assets
├── next.config.js            # Next.js configuration
├── tailwind.config.ts        # Tailwind CSS configuration
├── tsconfig.json             # TypeScript configuration
└── package.json              # Dependencies and scripts
```

## Getting Started

### Prerequisites

- Node.js 18.x or higher
- npm or yarn package manager

### Installation

1. **Navigate to the demo directory**:
   ```bash
   cd decoplan-demo
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

4. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

### Build for Production

```bash
npm run build
npm start
```

## Usage Guide

### Retrieving Furniture

1. Click the **"Retrieve Furniture"** button in the right panel
2. Wait for the simulated RAG retrieval (1.5 second delay)
3. Furniture items will appear in both the 3D viewer and the panel

### Interacting with the 3D Scene

- **Rotate View**: Left-click and drag
- **Pan Camera**: Right-click and drag
- **Zoom**: Scroll wheel

### Managing Furniture Visibility

- Click on any furniture item card to toggle its visibility
- Use the **"Show All"/"Hide All"** button to toggle all items at once
- Visible items are highlighted with a blue border

### Understanding the Data

Each furniture item displays:
- **Name and Category**: Type of furniture (sofa, table, chair, etc.)
- **Dimensions**: Width × Depth × Height in meters
- **Confidence Score**: RAG retrieval relevance (0-100%)
- **Color Indicator**: Visual category identification

### Statistics Panel

The statistics panel shows:
- **Visible**: Number of currently visible furniture items
- **Coverage**: Percentage of room floor space occupied
- **Footprint**: Total floor area covered by furniture (m²)

## Mock RAG System

The demo includes a simulated RAG system that:

1. **Simulates Network Delay**: 1.5 second retrieval time
2. **Returns Furniture Data**: Pre-configured furniture items with metadata
3. **Includes Confidence Scores**: Simulated relevance ranking (0.79-0.95)
4. **Provides Room Statistics**: Coverage calculations and space utilization

In a production system, this would:
- Query a vector database of furniture items
- Use embedding models for semantic search
- Leverage LLMs for ranking and filtering
- Integrate with real furniture catalogs

## Customization

### Adding New Furniture

Edit `lib/furnitureData.ts` to add new furniture items:

```typescript
{
  id: 'custom-001',
  name: 'Custom Furniture',
  category: 'sofa',
  position: { x: 0, y: 0.5, z: 0 },
  dimensions: { width: 2, height: 1, depth: 1 },
  color: { r: 150, g: 150, b: 150 },
  confidenceScore: 0.90,
  description: 'Your custom furniture description',
}
```

### Modifying Room Dimensions

Edit the `Room` component in `components/RoomViewer.tsx`:

```typescript
const roomWidth = 10;  // Change room width
const roomLength = 8;  // Change room length
const roomHeight = 3;  // Change room height
```

### Adjusting Colors and Styling

Modify `tailwind.config.ts` to change the color scheme:

```typescript
colors: {
  primary: {
    500: '#YOUR_COLOR',
    600: '#YOUR_COLOR',
    700: '#YOUR_COLOR',
  },
}
```

## Known Limitations

- Furniture models use basic geometric shapes (boxes, cylinders, spheres)
- RAG system is simulated with hardcoded data
- No real-time collaboration or persistence
- Limited to single room visualization
- No texture mapping or advanced materials

## Future Enhancements

Potential improvements for a production system:

- [ ] Integration with real RAG/LLM system
- [ ] 3D model loading (GLTF/GLB format)
- [ ] Multiple room types (bedroom, kitchen, etc.)
- [ ] Drag-and-drop furniture placement
- [ ] Save/load room configurations
- [ ] AR view for mobile devices
- [ ] Furniture dimension editing
- [ ] Material and texture customization
- [ ] Lighting controls
- [ ] Screenshot/export functionality

## Troubleshooting

### 3D Scene Not Loading

- Ensure you're using a modern browser (Chrome, Firefox, Edge, Safari)
- Check browser console for WebGL errors
- Try disabling browser extensions
- Clear browser cache and reload

### Dependencies Installation Issues

If you encounter issues during `npm install`:

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### WSL/Windows Path Issues

If running on WSL with path errors:

```bash
# Run from WSL terminal, not Windows Command Prompt
cd /mnt/c/path/to/decoplan-demo
npm run dev
```

## Contributing

This is a proof-of-concept demo. For production implementation:

1. Replace mock RAG with actual retrieval system
2. Integrate proper 3D furniture models
3. Add authentication and user management
4. Implement backend API for persistence
5. Add comprehensive error handling
6. Optimize for performance and scalability

## License

This demo is part of the DecoPlan project. See LICENSE file for details.

## Support

For questions or issues:
- Check the [documentation](../docs/)
- Review existing issues in the project repository
- Create a new issue with detailed description

---

**Built with** Next.js, React, Three.js, and Tailwind CSS

**Demo Purpose**: Proof-of-concept for RAG-powered furniture visualization in HDB interior design
