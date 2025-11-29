"""
Prepare training data for LoRA fine-tuning from DecoPlan datasets.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
from tqdm import tqdm


class TrainingDataPreparator:
    """Prepare training data in format suitable for LoRA fine-tuning."""

    def __init__(self):
        """Initialize the data preparator."""
        pass

    def format_furniture_list(self, furniture_list: List[Dict]) -> str:  # noqa: E501
        """
        Format furniture list as structured text.

        Args:
            furniture_list: List of furniture items with details

        Returns:
            Formatted string representation
        """
        output = []
        for i, item in enumerate(furniture_list, 1):
            output.append(f"{i}. {item['name']}")
            output.append(f"   - Type: {item['furniture_type']}")
            output.append(
                f"   - Material: {item['material']}, Color: {item['color']}, "
                f"Style: {item['feel']}"
            )

            # Add is_accessory if available
            if "is_accessory" in item:
                output.append(f"   - Is Accessory: {item['is_accessory']}")

            # Add dimensions if available
            if "dimensions" in item:
                dims = item["dimensions"]
                output.append(
                    f"   - Dimensions: {dims['length']}×{dims['width']}"
                    f"×{dims['height']} {dims['unit']}"
                )

            # Add position if available
            if "position" in item:
                pos = item["position"]
                output.append(
                    f"   - Position: x={pos['x']}, y={pos['y']}, "
                    f"rotation={pos['rotation']}°"
                )

        return "\n".join(output)

    def create_conversation_format(
        self,
        user_prompt: str,
        room_type: str,
        style: str,
        expected_output: Dict,
        floor_plan_metadata: Optional[Dict] = None,
        system_prompt: str = (
            "You are an expert interior designer specializing in "
            "Singapore HDB flats."
        ),
    ) -> Dict:
        """
        Create training example in conversation format.

        Args:
            user_prompt: User's design request
            room_type: Type of room
            style: Design style
            expected_output: Expected model output with furniture list and design notes
            floor_plan_metadata: Optional floor plan information
            system_prompt: System instruction for the model

        Returns:
            Dictionary with conversation structure
        """
        # Build user message
        user_message = f"Room Type: {room_type.replace('_', ' ').title()}\n"
        user_message += f"Style: {style.title()}\n"

        if floor_plan_metadata and "room_dimensions" in floor_plan_metadata:
            dims = floor_plan_metadata["room_dimensions"]
            user_message += f"Room Dimensions: {dims['length']}m × {dims['width']}m\n"
            if "available_space" in floor_plan_metadata:
                user_message += (
                    f"Available Space: {floor_plan_metadata['available_space']}m²\n"
                )

        user_message += f"\nRequest: {user_prompt}\n\n"
        user_message += "Please suggest furniture arrangements for this space."

        # Build assistant response
        assistant_message = "I recommend the following furniture arrangement:\n\n"
        assistant_message += self.format_furniture_list(
            expected_output["furniture_list"]
        )
        assistant_message += (
            f"\n\nTotal Furniture Items: "
            f"{expected_output['total_furniture_count']}\n\n"
        )
        assistant_message += f"Design Notes: {expected_output['design_notes']}"

        return {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": assistant_message},
            ]
        }

    def create_alpaca_format(
        self,
        user_prompt: str,
        room_type: str,
        style: str,
        expected_output: Dict,
        floor_plan_metadata: Optional[Dict] = None,
        instruction: str = (
            "Suggest furniture arrangements for a Singapore HDB "
            "interior design request."
        ),
    ) -> Dict:
        """
        Create training example in Alpaca format.

        Args:
            user_prompt: User's design request
            room_type: Type of room
            style: Design style
            expected_output: Expected model output
            floor_plan_metadata: Optional floor plan information
            instruction: Base instruction text

        Returns:
            Dictionary with Alpaca structure (instruction, input, output)
        """
        # Build input context
        input_text = f"Room Type: {room_type.replace('_', ' ').title()}\n"
        input_text += f"Style: {style.title()}\n"

        if floor_plan_metadata and "room_dimensions" in floor_plan_metadata:
            dims = floor_plan_metadata["room_dimensions"]
            input_text += f"Room Dimensions: {dims['length']}m × {dims['width']}m\n"

        input_text += f"\nUser Request: {user_prompt}"

        # Build output
        output_text = "Furniture Recommendations:\n\n"
        output_text += self.format_furniture_list(expected_output["furniture_list"])
        output_text += (
            f"\n\nTotal Items: {expected_output['total_furniture_count']}\n\n"
        )
        output_text += f"Design Notes: {expected_output['design_notes']}"

        return {
            "instruction": instruction,
            "input": input_text,
            "output": output_text,
        }

    def prepare_from_json(
        self,
        json_path: str,
        output_path: str,
        format_type: str = "conversation",
        max_examples: Optional[int] = None,
    ):
        """
        Prepare training data from JSON file.

        Args:
            json_path: Path to training examples JSON
            output_path: Output path for prepared data
            format_type: Format type ("conversation" or "alpaca")
            max_examples: Maximum number of examples to process
        """
        print(f"Loading training examples from: {json_path}")
        with open(json_path, "r") as f:
            examples = json.load(f)

        if max_examples:
            examples = examples[:max_examples]

        print(f"Processing {len(examples)} training examples...")

        prepared_data = []
        for example in tqdm(examples):
            if format_type == "conversation":
                formatted = self.create_conversation_format(
                    user_prompt=example["user_prompt"],
                    room_type=example["room_type"],
                    style=example["style"],
                    expected_output=example["expected_output"],
                    floor_plan_metadata=example.get("floor_plan_metadata"),
                )
            elif format_type == "alpaca":
                formatted = self.create_alpaca_format(
                    user_prompt=example["user_prompt"],
                    room_type=example["room_type"],
                    style=example["style"],
                    expected_output=example["expected_output"],
                    floor_plan_metadata=example.get("floor_plan_metadata"),
                )
            else:
                raise ValueError(f"Unknown format type: {format_type}")

            prepared_data.append(formatted)

        # Save prepared data
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as f:
            json.dump(prepared_data, f, indent=2)

        print(f"\n✓ Saved {len(prepared_data)} prepared examples to: {output_file}")
        print(f"  Format: {format_type}")

        # Save sample for inspection
        sample_file = output_file.parent / f"sample_{output_file.name}"
        with open(sample_file, "w") as f:
            json.dump(prepared_data[:3], f, indent=2)
        print(f"  Sample (3 examples): {sample_file}")

        return prepared_data

    def create_train_val_split(
        self, data: List[Dict], output_dir: str, val_ratio: float = 0.1, seed: int = 42
    ):
        """
        Split data into training and validation sets.

        Args:
            data: List of prepared training examples
            output_dir: Directory to save train/val splits
            val_ratio: Ratio of validation data
            seed: Random seed for reproducibility
        """
        import random

        random.seed(seed)

        # Shuffle data
        shuffled = data.copy()
        random.shuffle(shuffled)

        # Split
        val_size = int(len(shuffled) * val_ratio)
        val_data = shuffled[:val_size]
        train_data = shuffled[val_size:]

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save splits
        train_file = output_path / "train.json"
        val_file = output_path / "val.json"

        with open(train_file, "w") as f:
            json.dump(train_data, f, indent=2)

        with open(val_file, "w") as f:
            json.dump(val_data, f, indent=2)

        print(f"\n✓ Created train/val split:")
        print(f"  Training: {len(train_data)} examples → {train_file}")
        print(f"  Validation: {len(val_data)} examples → {val_file}")

        return train_data, val_data


def main():
    parser = argparse.ArgumentParser(
        description="Prepare training data for LoRA fine-tuning"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="datasets/Output/training_examples_with_outputs.json",
        help="Input JSON file with training examples",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="datasets/Output/lora_training_data.json",
        help="Output file for prepared training data",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["conversation", "alpaca"],
        default="conversation",
        help="Output format for training data",
    )
    parser.add_argument(
        "--max_examples",
        type=int,
        default=None,
        help="Maximum number of examples to process",
    )
    parser.add_argument(
        "--create_split", action="store_true", help="Create train/val split"
    )
    parser.add_argument(
        "--val_ratio",
        type=float,
        default=0.1,
        help="Validation data ratio (if creating split)",
    )
    parser.add_argument(
        "--split_dir",
        type=str,
        default="datasets/Output/lora_splits",
        help="Directory for train/val splits",
    )

    args = parser.parse_args()

    # Prepare data
    preparator = TrainingDataPreparator()
    prepared_data = preparator.prepare_from_json(
        json_path=args.input,
        output_path=args.output,
        format_type=args.format,
        max_examples=args.max_examples,
    )

    # Create split if requested
    if args.create_split:
        preparator.create_train_val_split(
            data=prepared_data, output_dir=args.split_dir, val_ratio=args.val_ratio
        )


if __name__ == "__main__":
    main()
