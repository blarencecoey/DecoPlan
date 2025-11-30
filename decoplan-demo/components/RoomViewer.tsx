'use client';

import { useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Grid, PerspectiveCamera } from '@react-three/drei';
import { Furniture } from '@/types/furniture';
import * as THREE from 'three';

/**
 * Individual furniture piece rendered in 3D
 * Uses basic geometric shapes as placeholders
 */
function FurnitureMesh({ item }: { item: Furniture }) {
  if (!item.visible) return null;

  const { position, dimensions, color } = item;
  const hexColor = `#${[color.r, color.g, color.b]
    .map(x => {
      const hex = x.toString(16);
      return hex.length === 1 ? '0' + hex : hex;
    })
    .join('')}`;

  // Different shapes for different furniture types
  const getGeometry = () => {
    switch (item.category) {
      case 'lamp':
        // Lamp: cylinder for stand, sphere for shade
        return (
          <group>
            <mesh position={[0, 0, 0]}>
              <cylinderGeometry args={[0.05, 0.05, dimensions.height * 0.8, 8]} />
              <meshStandardMaterial color={hexColor} />
            </mesh>
            <mesh position={[0, dimensions.height * 0.4, 0]}>
              <sphereGeometry args={[0.15, 16, 16]} />
              <meshStandardMaterial color={hexColor} emissive={hexColor} emissiveIntensity={0.3} />
            </mesh>
          </group>
        );
      case 'chair':
        // Chair: box seat with taller back
        return (
          <group>
            <mesh position={[0, 0, 0]}>
              <boxGeometry args={[dimensions.width, dimensions.height * 0.4, dimensions.depth]} />
              <meshStandardMaterial color={hexColor} />
            </mesh>
            <mesh position={[0, dimensions.height * 0.3, -dimensions.depth * 0.35]}>
              <boxGeometry args={[dimensions.width, dimensions.height * 0.6, dimensions.depth * 0.1]} />
              <meshStandardMaterial color={hexColor} />
            </mesh>
          </group>
        );
      case 'shelf':
        // Shelf: thinner box
        return (
          <mesh>
            <boxGeometry args={[dimensions.width, dimensions.height, dimensions.depth]} />
            <meshStandardMaterial color={hexColor} wireframe={false} transparent opacity={0.9} />
          </mesh>
        );
      default:
        // Default: simple box
        return (
          <mesh>
            <boxGeometry args={[dimensions.width, dimensions.height, dimensions.depth]} />
            <meshStandardMaterial color={hexColor} />
          </mesh>
        );
    }
  };

  return (
    <group position={[position.x, position.y, position.z]}>
      {getGeometry()}
      {/* Hover outline effect could be added here */}
    </group>
  );
}

/**
 * HDB Room structure with walls, floor, and ceiling
 */
function Room() {
  const roomWidth = 10;
  const roomLength = 8;
  const roomHeight = 3;

  const wallColor = '#f5f5f5';
  const floorColor = '#d4c4b0';

  return (
    <group>
      {/* Floor */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
        <planeGeometry args={[roomWidth, roomLength]} />
        <meshStandardMaterial color={floorColor} />
      </mesh>

      {/* Back wall */}
      <mesh position={[0, roomHeight / 2, -roomLength / 2]} receiveShadow>
        <planeGeometry args={[roomWidth, roomHeight]} />
        <meshStandardMaterial color={wallColor} side={THREE.DoubleSide} />
      </mesh>

      {/* Left wall */}
      <mesh
        position={[-roomWidth / 2, roomHeight / 2, 0]}
        rotation={[0, Math.PI / 2, 0]}
        receiveShadow
      >
        <planeGeometry args={[roomLength, roomHeight]} />
        <meshStandardMaterial color={wallColor} side={THREE.DoubleSide} />
      </mesh>

      {/* Right wall */}
      <mesh
        position={[roomWidth / 2, roomHeight / 2, 0]}
        rotation={[0, -Math.PI / 2, 0]}
        receiveShadow
      >
        <planeGeometry args={[roomLength, roomHeight]} />
        <meshStandardMaterial color={wallColor} side={THREE.DoubleSide} />
      </mesh>

      {/* Grid helper for spatial reference */}
      <Grid
        args={[roomWidth, roomLength]}
        cellSize={0.5}
        cellThickness={0.5}
        cellColor="#b0b0b0"
        sectionSize={1}
        sectionThickness={1}
        sectionColor="#909090"
        fadeDistance={25}
        fadeStrength={1}
        followCamera={false}
        position={[0, 0.01, 0]}
      />
    </group>
  );
}

/**
 * Scene lighting setup
 */
function Lights() {
  return (
    <>
      {/* Ambient light for overall illumination */}
      <ambientLight intensity={0.6} />

      {/* Directional light for shadows and depth */}
      <directionalLight
        position={[5, 10, 5]}
        intensity={0.8}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
      />

      {/* Fill light from opposite side */}
      <directionalLight position={[-5, 5, -5]} intensity={0.3} />

      {/* Point light for additional warmth */}
      <pointLight position={[0, 3, 0]} intensity={0.4} color="#fff5e6" />
    </>
  );
}

/**
 * Main 3D Room Viewer Component
 * Renders the room and furniture using React Three Fiber
 */
interface RoomViewerProps {
  furniture: Furniture[];
  onResetCamera?: () => void;
}

export default function RoomViewer({ furniture }: RoomViewerProps) {
  const controlsRef = useRef<any>(null);

  return (
    <div className="w-full h-full bg-gradient-to-b from-gray-800 to-gray-900">
      <Canvas shadows>
        {/* Camera setup */}
        <PerspectiveCamera makeDefault position={[8, 6, 8]} fov={60} />

        {/* Lighting */}
        <Lights />

        {/* Room structure */}
        <Room />

        {/* Furniture items */}
        {furniture.map(item => (
          <FurnitureMesh key={item.id} item={item} />
        ))}

        {/* Camera controls */}
        <OrbitControls
          ref={controlsRef}
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          minDistance={3}
          maxDistance={20}
          maxPolarAngle={Math.PI / 2 - 0.1} // Prevent going below floor
          target={[0, 1, 0]}
        />
      </Canvas>
    </div>
  );
}
