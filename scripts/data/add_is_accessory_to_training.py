#!/usr/bin/env python3
"""
Add is_accessory field to existing training examples.
"""

import json
from pathlib import Path


def is_accessory_type(furniture_type: str) -> bool:
    """
    Determine if a furniture type is typically an accessory.

    Args:
        furniture_type: Type of furniture

    Returns:
        True if it's an accessory, False otherwise
    """
    # Define accessory furniture types (smaller, decorative items)
    accessory_types = {
        'Lamp', 'Mirror', 'Rug', 'Cushion', 'Pillow',
        'Vase', 'Plant', 'Picture Frame', 'Clock', 'Candle',
        'Nightstand', 'Side Table', 'Ottoman', 'Stool'
    }

    return furniture_type in accessory_types


def add_is_accessory_field(input_file: str, output_file: str):
    """
    Add is_accessory field to training examples.

    Args:
        input_file: Path to input JSON file
        output_file: Path to output JSON file
    """
    print(f"Loading training examples from: {input_file}")

    with open(input_file, 'r') as f:
        examples = json.load(f)

    print(f"Processing {len(examples)} examples...")

    # Add is_accessory field to each furniture item
    updated_count = 0
    for example in examples:
        if 'expected_output' in example and 'furniture_list' in example['expected_output']:
            for item in example['expected_output']['furniture_list']:
                # Add is_accessory based on furniture type
                item['is_accessory'] = is_accessory_type(item['furniture_type'])
                updated_count += 1

    # Save updated data
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(examples, f, indent=2)

    print(f"\n✓ Updated {updated_count} furniture items")
    print(f"✓ Saved to: {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Add is_accessory field to training examples")
    parser.add_argument(
        "--input",
        type=str,
        default="datasets/Output/training_examples_with_outputs.json",
        help="Input JSON file"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="datasets/Output/training_examples_with_outputs.json",
        help="Output JSON file (can be same as input to update in place)"
    )

    args = parser.parse_args()

    add_is_accessory_field(args.input, args.output)
