#!/usr/bin/env python3
"""
Test script to verify RAG + LoRA setup.
Run this after installation to check if everything is working.
"""

# Fix SQLite version for ChromaDB (must be before any chromadb imports)
try:
    __import__("pysqlite3")
    import sys

    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass  # pysqlite3 not installed, will use system sqlite3

import sys
from pathlib import Path


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 80)
    print(f" {text}")
    print("=" * 80 + "\n")


def check_imports():
    """Check if all required packages are installed."""
    print_header("Checking Python Dependencies")

    packages = {
        "torch": "PyTorch",
        "transformers": "Transformers",
        "peft": "PEFT",
        "chromadb": "ChromaDB",
        "sentence_transformers": "Sentence Transformers",
        "pandas": "Pandas",
        "numpy": "NumPy",
    }

    missing = []
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✓ {name:25} installed")
        except ImportError:
            print(f"✗ {name:25} NOT FOUND")
            missing.append(package)

    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False

    print("\n✓ All dependencies installed!")
    return True


def check_datasets():
    """Check if dataset files exist."""
    print_header("Checking Dataset Files")

    files = {
        "datasets/Input/hdb_interior_design_prompts_300.csv": "Prompts CSV",
        "datasets/Input/Furniture Dataset - Furniture Data.csv": "Furniture CSV",
        "datasets/Output/training_examples_with_outputs.json": "Training Examples",
    }

    missing = []
    for filepath, name in files.items():
        path = Path(filepath)
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            print(f"✓ {name:30} found ({size_mb:.1f} MB)")
        else:
            print(f"✗ {name:30} NOT FOUND")
            missing.append(filepath)

    if missing:
        print(f"\n❌ Missing files: {len(missing)}")
        for f in missing:
            print(f"  - {f}")
        return False

    print("\n✓ All dataset files present!")
    return True


def check_rag_components():
    """Check if RAG scripts are present."""
    print_header("Checking RAG Components")

    files = {
        "rag/__init__.py": "RAG Init",
        "rag/build_furniture_db.py": "Build Database",
        "rag/furniture_retriever.py": "Furniture Retriever",
        "rag/rag_inference.py": "RAG Inference",
    }

    missing = []
    for filepath, name in files.items():
        path = Path(filepath)
        if path.exists():
            print(f"✓ {name:30} present")
        else:
            print(f"✗ {name:30} NOT FOUND")
            missing.append(filepath)

    if missing:
        print(f"\n❌ Missing RAG files: {len(missing)}")
        return False

    print("\n✓ All RAG components present!")
    return True


def check_lora_components():
    """Check if LoRA scripts are present."""
    print_header("Checking LoRA Components")

    files = {
        "lora/__init__.py": "LoRA Init",
        "lora/prepare_training_data.py": "Data Preparation",
        "lora/train_lora.py": "LoRA Training",
        "lora/inference.py": "Inference Script",
        "lora/evaluate.py": "Evaluation Script",
    }

    missing = []
    for filepath, name in files.items():
        path = Path(filepath)
        if path.exists():
            print(f"✓ {name:30} present")
        else:
            print(f"✗ {name:30} NOT FOUND")
            missing.append(filepath)

    if missing:
        print(f"\n❌ Missing LoRA files: {len(missing)}")
        return False

    print("\n✓ All LoRA components present!")
    return True


def check_cuda():
    """Check CUDA availability."""
    print_header("Checking CUDA Support")

    try:
        import torch

        if torch.cuda.is_available():
            print(f"✓ CUDA available")
            print(f"  - CUDA Version: {torch.version.cuda}")
            print(f"  - GPU: {torch.cuda.get_device_name(0)}")
            print(
                f"  - VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB"
            )
            return True
        else:
            print("⚠ CUDA not available")
            print("  LoRA training will require CUDA")
            print("  RAG retrieval will still work on CPU")
            return False
    except ImportError:
        print("✗ PyTorch not installed")
        return False


def check_optional_setup():
    """Check optional components that may be generated later."""
    print_header("Checking Optional Components")

    components = {
        "furniture_db/": "RAG Vector Database",
        "models/lora_checkpoints/": "LoRA Checkpoints",
        "datasets/Output/lora_splits/": "Train/Val Splits",
    }

    for path_str, name in components.items():
        path = Path(path_str)
        if path.exists():
            print(f"✓ {name:30} exists")
        else:
            print(f"⚠ {name:30} not yet created (will be generated)")

    print("\n✓ Optional components check complete")
    return True


def print_next_steps():
    """Print next steps for user."""
    print_header("Next Steps")

    print("To get started:")
    print("")
    print("1. Build RAG vector database:")
    print("   python rag/build_furniture_db.py \\")
    print(
        '       --furniture_csv "datasets/Input/Furniture Dataset - Furniture Data.csv"'
    )
    print("")
    print("2. Test RAG retrieval:")
    print("   python rag/furniture_retriever.py \\")
    print('       --query "minimalist living room"')
    print("")
    print("3. Prepare training data:")
    print("   python lora/prepare_training_data.py --create_split")
    print("")
    print("4. (Optional) Train LoRA adapter:")
    print("   python lora/train_lora.py")
    print("")
    print("Or run the automated setup:")
    print("   bash setup_rag_lora.sh")
    print("")
    print("See QUICKSTART_RAG_LORA.md for detailed instructions.")


def main():
    """Run all checks."""
    print("\n" + "=" * 80)
    print(" DecoPlan RAG + LoRA Setup Verification")
    print("=" * 80)

    checks = [
        ("Dependencies", check_imports),
        ("Datasets", check_datasets),
        ("RAG Components", check_rag_components),
        ("LoRA Components", check_lora_components),
        ("CUDA", check_cuda),
        ("Optional Setup", check_optional_setup),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error checking {name}: {e}")
            results.append((name, False))

    # Summary
    print_header("Summary")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:10} {name}")

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n🎉 All checks passed! System is ready.")
        print_next_steps()
        return 0
    else:
        print("\n⚠ Some checks failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
