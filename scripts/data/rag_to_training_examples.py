#!/usr/bin/env python3
"""
Convert RAG-enhanced prompts to training examples format.
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Optional
import argparse


class RAGToTrainingConverter:
    """Convert RAG-enhanced prompts to training examples."""

    def __init__(self, seed: int = 42):
        """
        Initialize converter.

        Args:
            seed: Random seed for reproducibility
        """
        random.seed(seed)
        self.seed = seed

    def parse_dimensions(self, dim_string: str) -> Optional[Dict]:
        """
        Parse dimension string like "98x28x116" into dict.

        Args:
            dim_string: Dimension string

        Returns:
            Dictionary with length, width, height, unit or None
        """
        if not dim_string or dim_string == "N/A":
            return None

        try:
            parts = dim_string.split('x')
            if len(parts) == 3:
                return {
                    "length": int(parts[0]),
                    "width": int(parts[1]),
                    "height": int(parts[2]),
                    "unit": "cm"
                }
        except (ValueError, AttributeError):
            pass

        return None

    def generate_position(
        self,
        furniture_index: int,
        furniture_type: str,
        room_dimensions: Optional[Dict] = None
    ) -> Dict:
        """
        Generate synthetic position for furniture.

        Args:
            furniture_index: Index of furniture item
            furniture_type: Type of furniture
            room_dimensions: Room dimensions if available

        Returns:
            Position dictionary with x, y, rotation
        """
        # Default room size (in cm) if not provided
        room_width = 400
        room_length = 500

        if room_dimensions:
            room_width = int(room_dimensions.get('width', 4) * 100)
            room_length = int(room_dimensions.get('length', 5) * 100)

        # Position based on furniture type and index
        furniture_type_lower = furniture_type.lower()

        # Walls and major furniture
        if 'sofa' in furniture_type_lower or 'couch' in furniture_type_lower:
            x = random.randint(100, 200)
            y = random.randint(100, 200)
            rotation = random.choice([0, 180])

        elif 'bed' in furniture_type_lower:
            x = random.randint(150, 250)
            y = random.randint(100, 150)
            rotation = random.choice([0, 90])

        elif 'table' in furniture_type_lower and 'dining' in furniture_type_lower:
            x = random.randint(200, 300)
            y = random.randint(200, 300)
            rotation = 0

        elif 'desk' in furniture_type_lower:
            x = random.randint(50, 150)
            y = random.randint(50, 150)
            rotation = random.choice([0, 90, 180, 270])

        elif 'wardrobe' in furniture_type_lower or 'closet' in furniture_type_lower:
            x = random.randint(50, 100)
            y = random.randint(50, 100)
            rotation = 0

        elif 'nightstand' in furniture_type_lower or 'side table' in furniture_type_lower:
            x = random.randint(50, 100)
            y = random.randint(100, 200)
            rotation = 0

        elif 'chair' in furniture_type_lower or 'armchair' in furniture_type_lower:
            x = random.randint(250, 350)
            y = random.randint(150, 250)
            rotation = random.choice([0, 90, 180, 270])

        elif 'bookshelf' in furniture_type_lower or 'cabinet' in furniture_type_lower:
            x = random.randint(50, 100)
            y = random.randint(50, 100)
            rotation = 0

        # Default position for other types
        else:
            x = random.randint(100, min(300, room_width - 100))
            y = random.randint(100, min(300, room_length - 100))
            rotation = random.choice([0, 90, 180, 270])

        # Add some randomness
        x += random.randint(-20, 20)
        y += random.randint(-20, 20)

        return {
            "x": max(50, min(x, room_width - 50)),
            "y": max(50, min(y, room_length - 50)),
            "rotation": rotation
        }

    def generate_design_notes(
        self,
        user_prompt: str,
        style: str,
        room_type: str,
        furniture_count: int
    ) -> str:
        """
        Generate design notes based on prompt and furniture.

        Args:
            user_prompt: User's design request
            style: Design style
            room_type: Type of room
            furniture_count: Number of furniture items

        Returns:
            Design notes string
        """
        # Extract key themes from prompt
        prompt_lower = user_prompt.lower()

        notes_parts = []

        # Style-based notes
        style_notes = {
            'minimalist': 'Clean lines, minimal clutter, and functional design',
            'modern': 'Contemporary aesthetic with sleek, modern pieces',
            'scandinavian': 'Light wood tones, natural materials, and cozy atmosphere',
            'industrial': 'Raw materials, exposed elements, and urban aesthetic',
            'japanese': 'Zen-like simplicity, natural materials, and mindful design',
            'japandi': 'Harmonious blend of Japanese minimalism and Scandinavian warmth',
            'bohemian': 'Eclectic mix, rich textures, and artistic flair',
            'contemporary': 'Current design trends with clean, sophisticated look',
            'vintage': 'Classic pieces with timeless appeal and character',
            'rustic': 'Natural materials, warm tones, and cozy farmhouse feel'
        }

        if style.lower() in style_notes:
            notes_parts.append(style_notes[style.lower()])

        # Space-specific notes
        if 'small' in prompt_lower or 'compact' in prompt_lower or 'tiny' in prompt_lower:
            notes_parts.append('space-efficient layout for compact areas')
        elif 'large' in prompt_lower or 'spacious' in prompt_lower:
            notes_parts.append('generous spacing for comfortable living')

        # Function-specific notes
        if 'storage' in prompt_lower:
            notes_parts.append('ample storage solutions')
        if 'family' in prompt_lower or 'kids' in prompt_lower:
            notes_parts.append('family-friendly and durable furniture')
        if 'work' in prompt_lower or 'office' in prompt_lower:
            notes_parts.append('productive workspace setup')
        if 'entertaining' in prompt_lower or 'guests' in prompt_lower:
            notes_parts.append('designed for hosting and entertaining')
        if 'cozy' in prompt_lower or 'warm' in prompt_lower:
            notes_parts.append('warm and inviting atmosphere')
        if 'budget' in prompt_lower or 'affordable' in prompt_lower:
            notes_parts.append('cost-effective furniture selection')

        # Add furniture count note
        notes_parts.append(f'{furniture_count} carefully selected pieces for optimal room function')

        return ', '.join(notes_parts).capitalize()

    def convert_rag_prompt(self, rag_entry: Dict, prompt_id: int) -> Dict:
        """
        Convert single RAG-enhanced prompt to training example.

        Args:
            rag_entry: RAG-enhanced prompt entry
            prompt_id: Prompt ID

        Returns:
            Training example dictionary
        """
        user_input = rag_entry['user_input']
        retrieved_furniture = rag_entry['retrieved_furniture']

        # Limit to reasonable number of furniture items (5-10)
        num_items = random.randint(5, min(10, len(retrieved_furniture)))
        selected_furniture = retrieved_furniture[:num_items]

        # Get room dimensions from floor plan if available
        room_dimensions = user_input.get('floor_plan_metadata', {}).get('room_dimensions')

        # Convert furniture to expected format
        furniture_list = []
        for idx, item in enumerate(selected_furniture):
            # Parse dimensions
            dims = self.parse_dimensions(item['dimensions'])
            if dims is None:
                # Generate random dimensions if not available
                dims = {
                    "length": random.randint(50, 200),
                    "width": random.randint(40, 100),
                    "height": random.randint(30, 180),
                    "unit": "cm"
                }

            # Generate position
            position = self.generate_position(
                furniture_index=idx,
                furniture_type=item['furniture_type'],
                room_dimensions=room_dimensions
            )

            # Parse is_accessory
            is_accessory = item['is_accessory']
            if isinstance(is_accessory, str):
                is_accessory = is_accessory.lower() == 'true'

            furniture_item = {
                "name": item['name'],
                "furniture_type": item['furniture_type'],
                "material": item['material'],
                "color": item['color'],
                "feel": item['feel'],
                "is_accessory": is_accessory,
                "dimensions": dims,
                "position": position
            }

            furniture_list.append(furniture_item)

        # Generate design notes
        design_notes = self.generate_design_notes(
            user_prompt=user_input['prompt'],
            style=user_input['style'],
            room_type=user_input['room_type'],
            furniture_count=len(furniture_list)
        )

        # Create training example
        training_example = {
            "prompt_id": prompt_id,
            "user_prompt": user_input['prompt'],
            "room_type": user_input['room_type'],
            "style": user_input['style'],
            "floor_plan_metadata": user_input.get('floor_plan_metadata', {}),
            "expected_output": {
                "furniture_list": furniture_list,
                "total_furniture_count": len(furniture_list),
                "design_notes": design_notes
            }
        }

        return training_example

    def convert_all(
        self,
        rag_prompts_file: str,
        output_file: str,
        max_examples: Optional[int] = None
    ):
        """
        Convert all RAG prompts to training examples.

        Args:
            rag_prompts_file: Path to RAG-enhanced prompts JSON
            output_file: Output path for training examples
            max_examples: Maximum number of examples to convert
        """
        print(f"Loading RAG-enhanced prompts from: {rag_prompts_file}")

        with open(rag_prompts_file, 'r') as f:
            rag_prompts = json.load(f)

        if max_examples:
            rag_prompts = rag_prompts[:max_examples]

        print(f"Converting {len(rag_prompts)} RAG prompts to training examples...")

        training_examples = []
        for idx, rag_entry in enumerate(rag_prompts, 1):
            if idx % 50 == 0:
                print(f"  Processed {idx}/{len(rag_prompts)}...")

            training_example = self.convert_rag_prompt(rag_entry, prompt_id=idx)
            training_examples.append(training_example)

        # Save to file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(training_examples, f, indent=2)

        print(f"\n✓ Saved {len(training_examples)} training examples to: {output_path}")

        # Print statistics
        total_furniture = sum(ex['expected_output']['total_furniture_count'] for ex in training_examples)
        avg_furniture = total_furniture / len(training_examples)

        print(f"\nStatistics:")
        print(f"  Total examples: {len(training_examples)}")
        print(f"  Total furniture items: {total_furniture}")
        print(f"  Average furniture per example: {avg_furniture:.1f}")

        return training_examples


def main():
    parser = argparse.ArgumentParser(
        description="Convert RAG-enhanced prompts to training examples"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="datasets/Output/rag_enhanced_prompts.json",
        help="Input RAG-enhanced prompts file"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="datasets/Output/training_examples_500.json",
        help="Output training examples file"
    )
    parser.add_argument(
        "--max_examples",
        type=int,
        default=500,
        help="Maximum number of examples to generate"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility"
    )

    args = parser.parse_args()

    converter = RAGToTrainingConverter(seed=args.seed)
    converter.convert_all(
        rag_prompts_file=args.input,
        output_file=args.output,
        max_examples=args.max_examples
    )


if __name__ == "__main__":
    main()
