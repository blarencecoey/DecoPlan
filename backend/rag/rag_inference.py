#!/usr/bin/env python3
"""
RAG-enhanced inference for DecoPlan LLM.
Combines furniture retrieval with LLM generation.
"""

# Fix SQLite version for ChromaDB (must be before any chromadb imports)
try:
    __import__("pysqlite3")
    import sys

    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass  # pysqlite3 not installed, will use system sqlite3

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional
from .furniture_retriever import FurnitureRetriever


class RAGInference:
    """RAG-enhanced inference for interior design recommendations."""

    def __init__(
        self, db_path: str = "./furniture_db", model_name: str = "all-MiniLM-L6-v2"
    ):
        """
        Initialize RAG inference.

        Args:
            db_path: Path to furniture vector database
            model_name: Sentence transformer model name
        """
        self.retriever = FurnitureRetriever(db_path=db_path, model_name=model_name)

    def create_prompt_with_context(
        self,
        user_prompt: str,
        room_type: str,
        style: str,
        floor_plan_metadata: Optional[Dict] = None,
        n_furniture: int = 15,
    ) -> str:
        """
        Create enhanced prompt with retrieved furniture context.

        Args:
            user_prompt: User's design request
            room_type: Type of room (living_room, bedroom, etc.)
            style: Design style
            floor_plan_metadata: Optional floor plan information
            n_furniture: Number of furniture items to retrieve

        Returns:
            Complete prompt with context for LLM
        """
        # Retrieve relevant furniture
        furniture_context = self.retriever.retrieve_for_prompt(
            user_prompt=user_prompt,
            room_type=room_type,
            style=style,
            n_results=n_furniture,
        )

        # Build the complete prompt
        prompt_parts = [
            "You are an expert interior designer specializing in Singapore HDB flats.",
            "\n\nUser Request:",
            f"Room Type: {room_type.replace('_', ' ').title()}",
            f"Style: {style.title()}",
            f"Description: {user_prompt}",
        ]

        # Add floor plan info if available
        if floor_plan_metadata:
            prompt_parts.append("\nRoom Dimensions:")
            if "room_dimensions" in floor_plan_metadata:
                dims = floor_plan_metadata["room_dimensions"]
                prompt_parts.append(
                    f"  Length: {dims.get('length', 'N/A')}m, "
                    f"Width: {dims.get('width', 'N/A')}m"
                )
            if "available_space" in floor_plan_metadata:
                prompt_parts.append(
                    f"  Available Space: {floor_plan_metadata['available_space']}m²"
                )

        # Add furniture context
        prompt_parts.append(f"\n{furniture_context}")

        # Add task instruction
        prompt_parts.append(
            "\nTask: Based on the user's request and the available furniture options above, "
            "suggest a complete furniture arrangement. For each piece:\n"
            "1. Select from the available furniture list above\n"
            "2. Explain why it fits the design style and user requirements\n"
            "3. Suggest positioning (if floor plan dimensions are provided)\n"
            "4. Provide design notes about the overall aesthetic\n"
            "\nPlease provide your recommendations:"
        )

        return "\n".join(prompt_parts)

    def format_for_json_output(
        self,
        user_prompt: str,
        room_type: str,
        style: str,
        floor_plan_metadata: Optional[Dict] = None,
        n_furniture: int = 15,
    ) -> Dict:
        """
        Format input and retrieved context as JSON for model consumption.

        Args:
            user_prompt: User's design request
            room_type: Type of room
            style: Design style
            floor_plan_metadata: Optional floor plan information
            n_furniture: Number of furniture items to retrieve

        Returns:
            Dictionary with prompt and context
        """
        # Retrieve furniture
        enhanced_query = f"{style} {room_type.replace('_', ' ')}: {user_prompt}"
        furniture_items = self.retriever.retrieve(
            query=enhanced_query, n_results=n_furniture
        )

        # Format output
        output = {
            "user_input": {
                "prompt": user_prompt,
                "room_type": room_type,
                "style": style,
                "floor_plan_metadata": floor_plan_metadata or {},
            },
            "retrieved_furniture": [
                {
                    "name": item["name"],
                    "furniture_type": item["furniture_type"],
                    "material": item["material"],
                    "color": item["color"],
                    "feel": item["feel"],
                    "is_accessory": item["is_accessory"],
                    "dimensions": item["dimensions"],
                    "relevance_score": round(item["relevance_score"], 4),
                }
                for item in furniture_items
            ],
            "llm_prompt": self.create_prompt_with_context(
                user_prompt, room_type, style, floor_plan_metadata, n_furniture
            ),
        }

        return output

    def process_batch(self, prompts_csv: str, output_file: str, n_furniture: int = 15):
        """
        Process multiple prompts from CSV and save with retrieved context.

        Args:
            prompts_csv: Path to CSV with prompts
            output_file: Output JSON file path
            n_furniture: Number of furniture items per prompt
        """
        import pandas as pd

        print(f"Loading prompts from: {prompts_csv}")
        df = pd.read_csv(prompts_csv)
        print(f"Processing {len(df)} prompts...")

        results = []
        for idx, row in df.iterrows():
            print(f"Processing {idx + 1}/{len(df)}: {row['user_prompt'][:50]}...")

            result = self.format_for_json_output(
                user_prompt=row["user_prompt"],
                room_type=row["room_type"],
                style=row["style_category"],
                n_furniture=n_furniture,
            )
            result["prompt_id"] = int(row["prompt_id"])
            results.append(result)

        # Save results
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n✓ Saved {len(results)} prompts with RAG context to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate RAG-enhanced prompts for interior design"
    )
    parser.add_argument(
        "--db_path",
        type=str,
        default="./furniture_db",
        help="Path to furniture vector database",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["single", "batch"],
        default="single",
        help="Processing mode",
    )

    # Single prompt mode
    parser.add_argument(
        "--prompt",
        type=str,
        default="I want a clean, minimalist living room with neutral colors",
        help="User prompt (single mode)",
    )
    parser.add_argument(
        "--room_type", type=str, default="living_room", help="Room type (single mode)"
    )
    parser.add_argument(
        "--style", type=str, default="minimalist", help="Design style (single mode)"
    )

    # Batch mode
    parser.add_argument(
        "--prompts_csv",
        type=str,
        default="datasets/Input/hdb_interior_design_prompts_300.csv",
        help="CSV file with prompts (batch mode)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="datasets/Output/rag_enhanced_prompts.json",
        help="Output file (batch mode)",
    )

    parser.add_argument(
        "--n_furniture",
        type=int,
        default=15,
        help="Number of furniture items to retrieve",
    )

    args = parser.parse_args()

    # Initialize RAG inference
    rag = RAGInference(db_path=args.db_path)

    if args.mode == "single":
        # Single prompt
        print("\n" + "=" * 80)
        print("RAG-Enhanced Prompt Generation")
        print("=" * 80)

        enhanced_prompt = rag.create_prompt_with_context(
            user_prompt=args.prompt,
            room_type=args.room_type,
            style=args.style,
            n_furniture=args.n_furniture,
        )

        print(enhanced_prompt)
        print("\n" + "=" * 80)

    elif args.mode == "batch":
        # Batch processing
        rag.process_batch(
            prompts_csv=args.prompts_csv,
            output_file=args.output,
            n_furniture=args.n_furniture,
        )


if __name__ == "__main__":
    main()
