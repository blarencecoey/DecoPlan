# DecoPlan Demo - Quick Start Guide

## Installation & Running

```bash
# 1. Navigate to the demo directory
cd decoplan-demo

# 2. Install dependencies (if not already done)
npm install

# 3. Run the development server
npm run dev

# 4. Open your browser
# Navigate to http://localhost:3000
```

## What to Expect

When you first load the application:

1. **Left Side (70%)**: Empty 3D room viewer with:
   - Gray walls and wooden floor
   - Grid overlay for spatial reference
   - Info badge in top-left corner
   - Camera controls guide in bottom-left

2. **Right Side (30%)**: Furniture panel with:
   - "Retrieve Furniture" button
   - Empty state message

## How to Use

### Step 1: Retrieve Furniture
Click the **"Retrieve Furniture"** button in the right panel. You'll see:
- Loading spinner animation (1.5 seconds)
- 10 furniture items will appear
- 3D models will render in the room
- Statistics panel will show coverage data

### Step 2: Explore the 3D View
**Camera Controls:**
- **Rotate**: Left-click and drag
- **Pan**: Right-click and drag
- **Zoom**: Mouse scroll wheel

### Step 3: Toggle Furniture
- Click any furniture item card to hide/show it
- Use "Show All" / "Hide All" to toggle everything
- Watch the 3D scene update in real-time

### Step 4: Review Statistics
The stats panel shows:
- **Visible**: Number of items currently shown
- **Coverage**: % of floor space used
- **Footprint**: Total area in m²

## Furniture Categories

The demo includes:
- **Sofas** (gray): L-shaped sofa, accent chair
- **Tables** (brown): Coffee table, dining table, side table
- **Chairs** (dark gray): Dining chairs
- **Cabinets** (dark brown): TV console
- **Shelves** (light gray): Wall shelf unit
- **Lamps** (gold): Floor lamp

## Technical Details

- **Framework**: Next.js 14 with App Router
- **3D Engine**: Three.js via React Three Fiber
- **Mock RAG**: Simulated 1.5s retrieval delay
- **Room Size**: 10m × 8m × 3m HDB living room
- **Confidence Scores**: Range from 79% to 95%

## Troubleshooting

### Page Won't Load
- Check console for errors
- Ensure port 3000 is available
- Try clearing browser cache

### 3D Scene Black/Empty
- Verify WebGL is enabled in browser
- Try a different browser (Chrome recommended)
- Check for GPU/graphics driver issues

### Installation Errors
If you see TAR_ENTRY_ERROR warnings on WSL, these are normal and don't affect functionality. The installation is successful if you see "added X packages" and "0 vulnerabilities".

## Next Steps

After exploring the demo:
1. Review the code structure in the README
2. Customize furniture data in `lib/furnitureData.ts`
3. Modify room dimensions in `components/RoomViewer.tsx`
4. Adjust colors in `tailwind.config.ts`

---

**Enjoy exploring DecoPlan!**
