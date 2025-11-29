#!/usr/bin/env python3
"""
Inference script combining LoRA fine-tuned model with RAG retrieval.
"""

# Fix SQLite version for ChromaDB (must be before any chromadb imports)
try:
    __import__("pysqlite3")
    import sys

    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass  # pysqlite3 not installed, will use system sqlite3

import argparse
import sys
from pathlib import Path
from typing import Dict, Optional

import torch

# Add parent directory to path for RAG imports
sys.path.append(str(Path(__file__).parent.parent))

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from rag.furniture_retriever import FurnitureRetriever


class DecoPlanInference:
    """Combined RAG + LoRA inference for interior design recommendations."""

    def __init__(
        self,
        base_model_name: str,
        lora_adapter_path: str,
        furniture_db_path: str = "./furniture_db",
        device: str = "auto",
    ):
        """
        Initialize DecoPlan inference system.

        Args:
            base_model_name: Name or path of base model
            lora_adapter_path: Path to LoRA adapter weights
            furniture_db_path: Path to furniture vector database
            device: Device to use for inference
        """
        print("Initializing DecoPlan Inference System...")
        print(f"  Base Model: {base_model_name}")
        print(f"  LoRA Adapter: {lora_adapter_path}")
        print(f"  Furniture DB: {furniture_db_path}")

        self.device = device

        # Load RAG retriever
        print("\nLoading RAG retriever...")
        self.retriever = FurnitureRetriever(db_path=furniture_db_path)

        # Load model and tokenizer
        print("\nLoading model and tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            base_model_name, trust_remote_code=True
        )

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Load base model
        print("  Loading base model...")
        self.base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            device_map=device,
            torch_dtype=torch.float16,
            trust_remote_code=True,
        )

        # Load LoRA adapter
        print("  Loading LoRA adapter...")
        self.model = PeftModel.from_pretrained(
            self.base_model, lora_adapter_path, torch_dtype=torch.float16
        )

        self.model.eval()
        print("  Model loaded successfully!")

    def create_rag_prompt(
        self,
        user_prompt: str,
        room_type: str,
        style: str,
        floor_plan_metadata: Optional[Dict] = None,
        n_furniture: int = 15,
    ) -> str:
        """
        Create prompt with RAG-retrieved furniture context.

        Args:
            user_prompt: User's design request
            room_type: Type of room
            style: Design style
            floor_plan_metadata: Optional floor plan information
            n_furniture: Number of furniture items to retrieve

        Returns:
            Complete prompt with furniture context
        """
        # Use RAG retriever to get context
        context = self.retriever.retrieve_for_prompt(
            user_prompt=user_prompt,
            room_type=room_type,
            style=style,
            n_results=n_furniture,
        )

        # Build prompt
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

        # Add furniture context
        prompt_parts.append(f"\n{context}")

        # Add task instruction
        prompt_parts.append(
            "\nTask: Based on the available furniture options above, "
            "suggest a complete furniture arrangement that matches the user's requirements."
        )

        return "\n".join(prompt_parts)

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        do_sample: bool = True,
    ) -> str:
        """
        Generate response using LoRA-finetuned model.

        Args:
            prompt: Input prompt
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            do_sample: Whether to use sampling

        Returns:
            Generated text
        """
        # Tokenize input
        inputs = self.tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=2048
        ).to(self.model.device)

        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=do_sample,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )

        # Decode
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract only the generated part (remove prompt)
        prompt_length = len(
            self.tokenizer.decode(inputs.input_ids[0], skip_special_tokens=True)
        )
        response = generated_text[prompt_length:].strip()

        return response

    def predict(
        self,
        user_prompt: str,
        room_type: str,
        style: str,
        floor_plan_metadata: Optional[Dict] = None,
        n_furniture: int = 15,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
    ) -> Dict:
        """
        End-to-end prediction with RAG + LoRA.

        Args:
            user_prompt: User's design request
            room_type: Type of room
            style: Design style
            floor_plan_metadata: Optional floor plan information
            n_furniture: Number of furniture items to retrieve
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Dictionary with prompt, retrieved furniture, and generated response
        """
        # Create RAG-enhanced prompt
        rag_prompt = self.create_rag_prompt(
            user_prompt=user_prompt,
            room_type=room_type,
            style=style,
            floor_plan_metadata=floor_plan_metadata,
            n_furniture=n_furniture,
        )

        # Generate response
        response = self.generate(
            prompt=rag_prompt, max_new_tokens=max_new_tokens, temperature=temperature
        )

        # Get retrieved furniture for reference
        retrieved_furniture = self.retriever.retrieve(
            query=f"{style} {room_type.replace('_', ' ')}: {user_prompt}",
            n_results=n_furniture,
        )

        return {
            "user_input": {
                "prompt": user_prompt,
                "room_type": room_type,
                "style": style,
                "floor_plan_metadata": floor_plan_metadata,
            },
            "retrieved_furniture": [
                {
                    "name": item["name"],
                    "type": item["furniture_type"],
                    "material": item["material"],
                    "color": item["color"],
                    "feel": item["feel"],
                }
                for item in retrieved_furniture
            ],
            "model_response": response,
        }


def main():
    parser = argparse.ArgumentParser(
        description="Run inference with LoRA + RAG for interior design",
    )

    # Model
    parser.add_argument(
        "--base_model",
        type=str,
        default="llava-hf/llava-1.5-7b-hf",
        help="Base model name or path",
    )
    parser.add_argument(
        "--lora_adapter",
        type=str,
        default="models/lora_checkpoints/final_model",
        help="Path to LoRA adapter",
    )
    parser.add_argument(
        "--furniture_db",
        type=str,
        default="./furniture_db",
        help="Path to furniture vector database",
    )

    # Input
    parser.add_argument(
        "--prompt",
        type=str,
        default="I want a clean, minimalist living room with neutral colors",
        help="User's design request",
    )
    parser.add_argument(
        "--room_type",
        type=str,
        default="living_room",
        help="Room type",
    )
    parser.add_argument(
        "--style",
        type=str,
        default="minimalist",
        help="Design style",
    )

    # Generation
    parser.add_argument(
        "--n_furniture",
        type=int,
        default=15,
        help="Number of furniture items to retrieve",
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=512,
        help="Maximum tokens to generate",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature",
    )

    args = parser.parse_args()

    # Initialize inference system
    inference = DecoPlanInference(
        base_model_name=args.base_model,
        lora_adapter_path=args.lora_adapter,
        furniture_db_path=args.furniture_db,
    )

    # Run prediction
    print("\n" + "=" * 80)
    print("Running Inference")
    print("=" * 80)
    print(f"\nUser Prompt: {args.prompt}")
    print(f"Room Type: {args.room_type}")
    print(f"Style: {args.style}\n")

    result = inference.predict(
        user_prompt=args.prompt,
        room_type=args.room_type,
        style=args.style,
        n_furniture=args.n_furniture,
        max_new_tokens=args.max_tokens,
        temperature=args.temperature,
    )

    print("=" * 80)
    print("Model Response:")
    print("=" * 80)
    print(result["model_response"])
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
