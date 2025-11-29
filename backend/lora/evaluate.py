"""
Evaluation utilities for LoRA fine-tuned models.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
import torch
from tqdm import tqdm

sys.path.append(str(Path(__file__).parent.parent))

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


class ModelEvaluator:
    """Evaluate LoRA fine-tuned model on test data."""

    def __init__(
        self,
        base_model_name: str,
        lora_adapter_path: str,
        device: str = "auto",
    ):
        """
        Initialize evaluator.

        Args:
            base_model_name: Name or path of base model
            lora_adapter_path: Path to LoRA adapter weights
            device: Device to use
        """
        print(f"Loading model for evaluation...")
        print(f"  Base: {base_model_name}")
        print(f"  Adapter: {lora_adapter_path}")

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            base_model_name, trust_remote_code=True
        )

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Load model
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            device_map=device,
            torch_dtype=torch.float16,
            trust_remote_code=True,
        )

        self.model = PeftModel.from_pretrained(
            base_model, lora_adapter_path, torch_dtype=torch.float16
        )

        self.model.eval()
        print("  Model loaded!")

    def generate_response(
        self,
        prompt: str,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate response for a prompt.

        Args:
            prompt: Input prompt
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated response
        """
        inputs = self.tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=2048
        ).to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        prompt_length = len(
            self.tokenizer.decode(inputs.input_ids[0], skip_special_tokens=True)
        )
        response = generated_text[prompt_length:].strip()

        return response

    def evaluate_on_dataset(
        self,
        test_data_path: str,
        output_path: str,
        max_samples: int = None,
        max_new_tokens: int = 512,
    ) -> Dict:
        """
        Evaluate model on test dataset.

        Args:
            test_data_path: Path to test data JSON
            output_path: Path to save predictions
            max_samples: Maximum number of samples to evaluate
            max_new_tokens: Maximum tokens to generate

        Returns:
            Evaluation metrics
        """
        print(f"\nLoading test data from: {test_data_path}")
        with open(test_data_path, "r") as f:
            test_data = json.load(f)

        if max_samples:
            test_data = test_data[:max_samples]

        print(f"Evaluating on {len(test_data)} examples...")

        predictions = []
        perplexities = []

        for i, example in enumerate(tqdm(test_data)):
            # Extract input
            if "messages" in example:
                # Conversation format
                messages = example["messages"]
                prompt = messages[1]["content"]  # User message
                reference = messages[2]["content"]  # Assistant message
            elif "instruction" in example:
                # Alpaca format
                prompt = f"### Instruction:\n{example['instruction']}\n\n"
                prompt += f"### Input:\n{example['input']}\n\n### Response:\n"
                reference = example["output"]
            else:
                print(f"Warning: Unknown format for example {i}")
                continue

            # Generate prediction
            prediction = self.generate_response(
                prompt=prompt, max_new_tokens=max_new_tokens
            )

            # Calculate perplexity
            perplexity = self.calculate_perplexity(prompt + reference)
            perplexities.append(perplexity)

            predictions.append(
                {
                    "example_id": i,
                    "prompt": prompt,
                    "reference": reference,
                    "prediction": prediction,
                    "perplexity": perplexity,
                }
            )

        # Calculate metrics
        avg_perplexity = np.mean(perplexities)

        metrics = {
            "num_examples": len(predictions),
            "average_perplexity": float(avg_perplexity),
            "perplexity_std": float(np.std(perplexities)),
            "min_perplexity": float(np.min(perplexities)),
            "max_perplexity": float(np.max(perplexities)),
        }

        # Save predictions
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        results = {"metrics": metrics, "predictions": predictions}

        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n{'='*80}")
        print("Evaluation Results:")
        print(f"{'='*80}")
        print(f"  Examples evaluated: {metrics['num_examples']}")
        print(f"  Average Perplexity: {metrics['average_perplexity']:.4f}")
        print(f"  Perplexity Std Dev: {metrics['perplexity_std']:.4f}")
        print(f"\n  Results saved to: {output_file}")

        return metrics

    def calculate_perplexity(self, text: str) -> float:
        """
        Calculate perplexity for a text.

        Args:
            text: Input text

        Returns:
            Perplexity score
        """
        encodings = self.tokenizer(
            text, return_tensors="pt", truncation=True, max_length=2048
        ).to(self.model.device)

        with torch.no_grad():
            outputs = self.model(**encodings, labels=encodings.input_ids)
            loss = outputs.loss

        perplexity = torch.exp(loss).item()
        return perplexity


def compare_models(
    base_model_name: str,
    lora_adapters: List[str],
    test_data_path: str,
    output_dir: str,
):
    """
    Compare multiple LoRA adapters.

    Args:
        base_model_name: Base model name
        lora_adapters: List of LoRA adapter paths
        test_data_path: Path to test data
        output_dir: Output directory for results
    """
    results = {}

    for adapter_path in lora_adapters:
        adapter_name = Path(adapter_path).name
        print(f"\n{'='*80}")
        print(f"Evaluating: {adapter_name}")
        print(f"{'='*80}")

        evaluator = ModelEvaluator(
            base_model_name=base_model_name, lora_adapter_path=adapter_path
        )

        output_path = Path(output_dir) / f"{adapter_name}_results.json"
        metrics = evaluator.evaluate_on_dataset(
            test_data_path=test_data_path, output_path=str(output_path)
        )

        results[adapter_name] = metrics

    # Save comparison
    comparison_file = Path(output_dir) / "model_comparison.json"
    with open(comparison_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*80}")
    print("Model Comparison Summary:")
    print(f"{'='*80}")
    for name, metrics in results.items():
        print(f"\n{name}:")
        print(f"  Perplexity: {metrics['average_perplexity']:.4f}")


def main():
    parser = argparse.ArgumentParser(description="Evaluate LoRA fine-tuned model")

    parser.add_argument(
        "--mode",
        type=str,
        choices=["single", "compare"],
        default="single",
        help="Evaluation mode",
    )
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
        help="Path to LoRA adapter (single mode)",
    )
    parser.add_argument(
        "--lora_adapters", nargs="+", help="List of LoRA adapter paths (compare mode)"
    )
    parser.add_argument(
        "--test_data",
        type=str,
        default="datasets/Output/lora_splits/val.json",
        help="Path to test data",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="evaluation/results.json",
        help="Output path for results",
    )
    parser.add_argument(
        "--max_samples",
        type=int,
        default=None,
        help="Maximum number of samples to evaluate",
    )
    parser.add_argument(
        "--max_tokens", type=int, default=512, help="Maximum tokens to generate"
    )

    args = parser.parse_args()

    if args.mode == "single":
        evaluator = ModelEvaluator(
            base_model_name=args.base_model, lora_adapter_path=args.lora_adapter
        )

        evaluator.evaluate_on_dataset(
            test_data_path=args.test_data,
            output_path=args.output,
            max_samples=args.max_samples,
            max_new_tokens=args.max_tokens,
        )

    elif args.mode == "compare":
        if not args.lora_adapters:
            raise ValueError("--lora_adapters required for compare mode")

        compare_models(
            base_model_name=args.base_model,
            lora_adapters=args.lora_adapters,
            test_data_path=args.test_data,
            output_dir=Path(args.output).parent,
        )


if __name__ == "__main__":
    main()
