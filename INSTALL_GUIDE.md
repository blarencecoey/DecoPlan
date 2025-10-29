# Installation Guide for RAG + LoRA System

## Quick Install (CPU Only - For RAG)

If you only want to use RAG (retrieval system) without LoRA training:

```bash
# Install minimal dependencies for RAG
python3 -m pip install --user \
    chromadb \
    sentence-transformers \
    pandas \
    numpy

# This will allow you to:
# - Build the furniture vector database
# - Run semantic retrieval
# - Generate RAG-enhanced prompts
```

##Full Install (GPU Required - For RAG + LoRA)

If you want both RAG and LoRA training capabilities:

```bash
# Install all dependencies (this will download ~2GB of packages)
python3 -m pip install --user -r requirements.txt

# Or install core packages one by one:
python3 -m pip install --user \
    torch \
    transformers \
    peft \
    bitsandbytes \
    accelerate \
    chromadb \
    sentence-transformers \
    pandas \
    scikit-learn
```

## Installation Issues

### PyYAML Conflict

If you see: `Cannot uninstall PyYAML 5.3.1`

**Solution**: Use `--ignore-installed` flag:
```bash
python3 -m pip install --ignore-installed --user pyyaml peft chromadb sentence-transformers pandas
```

### CUDA Libraries Taking Long Time

The full install downloads large CUDA libraries (~2GB+). This is normal and can take 10-15 minutes.

**If you only need RAG** (no LoRA training), install minimal dependencies only (see CPU Only section above).

### Permission Denied Errors

**Solution**: Always use `--user` flag:
```bash
python3 -m pip install --user package_name
```

### Python vs Python3

If `python` command doesn't work, use `python3`:
```bash
python3 --version
python3 -m pip install --user packagename
```

## Verify Installation

### For RAG Only:
```bash
python3 -c "import chromadb; import sentence_transformers; import pandas; print('RAG dependencies OK!')"
```

### For Full System:
```bash
python3 test_setup.py
```

## What Each Package Does

| Package | Size | Purpose | Required For |
|---------|------|---------|--------------|
| chromadb | ~50MB | Vector database | RAG |
| sentence-transformers | ~100MB | Text embeddings | RAG |
| pandas | ~50MB | Data processing | Both |
| torch | ~800MB | Deep learning | LoRA |
| transformers | ~100MB | LLM models | LoRA |
| peft | ~5MB | LoRA training | LoRA |
| bitsandbytes | ~50MB | 4-bit quantization | LoRA |
| accelerate | ~5MB | Training utilities | LoRA |

## Minimal Working Setup

To get started quickly with just RAG:

```bash
# 1. Install minimal deps (~200MB)
python3 -m pip install --user chromadb sentence-transformers pandas

# 2. Build RAG database
python3 rag/build_furniture_db.py

# 3. Test retrieval
python3 rag/furniture_retriever.py --query "minimalist living room"
```

## Add LoRA Later

If you start with RAG only and want to add LoRA later:

```bash
# Install LoRA dependencies
python3 -m pip install --user torch transformers peft bitsandbytes accelerate

# Then proceed with training
python3 lora/prepare_training_data.py --create_split
python3 lora/train_lora.py
```

## Troubleshooting

### Check What's Installed
```bash
python3 -m pip list | grep -E "chromadb|peft|sentence|pandas|torch"
```

### Uninstall and Reinstall
```bash
python3 -m pip uninstall chromadb peft sentence-transformers
python3 -m pip install --user chromadb peft sentence-transformers
```

### Check Python Path
```bash
python3 -c "import sys; print(sys.path)"
```

### Use Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install packages
pip install -r requirements.txt

# Deactivate when done
deactivate
```

## Platform-Specific Notes

### WSL2 (Windows Subsystem for Linux)
- Use `python3` instead of `python`
- Install with `--user` flag
- CUDA should work if you have NVIDIA drivers installed on Windows

### Linux
- May need to install `python3-pip` first: `sudo apt install python3-pip`
- Use `--user` flag to avoid permission issues

### macOS
- PyTorch will use CPU only (no CUDA)
- LoRA training will be much slower
- RAG will work normally

## Next Steps After Installation

1. **Verify**: Run `python3 test_setup.py`
2. **Build RAG DB**: `python3 rag/build_furniture_db.py`
3. **Test RAG**: `python3 rag/furniture_retriever.py`
4. **(Optional) Train LoRA**: `python3 lora/train_lora.py`

## Getting Help

If installation fails:
1. Check error messages carefully
2. Try minimal install first (RAG only)
3. Use virtual environment
4. Check Python version (`python3 --version` should be 3.8+)
