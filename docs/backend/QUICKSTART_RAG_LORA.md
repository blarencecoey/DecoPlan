# Quick Start: RAG + LoRA for DecoPlan LLM

Get up and running with RAG and LoRA in 5 minutes!

## Prerequisites

- Python 3.8+
- CUDA-capable GPU (for LoRA training, 12GB+ VRAM)
- 20GB free disk space

## Option 1: Automated Setup (Recommended)

Run the setup script:

```bash
bash setup_rag_lora.sh
```

This will guide you through:
1. Installing dependencies
2. Building RAG vector database
3. Testing retrieval
4. Preparing training data
5. (Optional) Training LoRA adapter

## Option 2: Manual Setup

### Step 1: Install Dependencies (2 min)

```bash
pip install -r requirements.txt
```

### Step 2: Build RAG Database (3 min)

```bash
python rag/build_furniture_db.py \
    --furniture_csv "datasets/Input/Furniture Dataset - Furniture Data.csv" \
    --db_path ./furniture_db
```

Expected output:
```
Loading furniture data from: datasets/Input/...
Loaded 10000 furniture items
Creating furniture descriptions...
Generating embeddings...
✓ Successfully built vector database with 10000 items
```

### Step 3: Test RAG Retrieval (30 sec)

```bash
python rag/furniture_retriever.py \
    --query "minimalist living room with neutral colors" \
    --n_results 10
```

You should see a list of relevant furniture items with relevance scores.

### Step 4: Prepare Training Data (1 min)

```bash
python lora/prepare_training_data.py \
    --input datasets/Output/training_examples_with_outputs.json \
    --output datasets/Output/lora_training_data.json \
    --format conversation \
    --create_split \
    --val_ratio 0.1
```

This creates:
- `datasets/Output/lora_training_data.json` (full dataset)
- `datasets/Output/lora_splits/train.json` (90% training)
- `datasets/Output/lora_splits/val.json` (10% validation)

## Usage Examples

### RAG Only (No GPU Required)

Generate enhanced prompts with furniture context:

```bash
python rag/rag_inference.py \
    --mode single \
    --prompt "I want a cozy Scandinavian bedroom" \
    --room_type bedroom \
    --style scandinavian \
    --n_furniture 15
```

### LoRA Training (GPU Required, ~2-4 hours)

```bash
python lora/train_lora.py \
    --model_name "llava-hf/llava-1.5-7b-hf" \
    --train_data datasets/Output/lora_splits/train.json \
    --val_data datasets/Output/lora_splits/val.json \
    --output_dir models/lora_checkpoints \
    --num_epochs 3 \
    --batch_size 4
```

**Training Tips:**
- Start with `--num_epochs 1` for a quick test
- Monitor VRAM with `nvidia-smi`
- Reduce `--batch_size` if you get OOM errors
- Use `--max_seq_length 1024` to save memory

### RAG + LoRA Inference (GPU Required)

After training, run inference:

```bash
python lora/inference.py \
    --base_model "llava-hf/llava-1.5-7b-hf" \
    --lora_adapter models/lora_checkpoints/final_model \
    --furniture_db ./furniture_db \
    --prompt "I want a modern minimalist living room for entertaining" \
    --room_type living_room \
    --style modern \
    --n_furniture 15
```

## Common Use Cases

### 1. Test Different Retrieval Strategies

```bash
# More furniture options
python rag/furniture_retriever.py \
    --query "industrial loft bedroom" \
    --n_results 20

# Specific furniture type
python rag/furniture_retriever.py \
    --query "scandinavian style" \
    --n_results 10
```

### 2. Generate RAG Contexts for All Prompts

```bash
python rag/rag_inference.py \
    --mode batch \
    --prompts_csv datasets/Input/hdb_interior_design_prompts_300.csv \
    --output datasets/Output/rag_enhanced_prompts.json
```

This creates enhanced prompts for all 300 examples that can be used with any LLM.

### 3. Quick LoRA Test (Without Full Training)

If you want to test the LoRA pipeline without full training:

```bash
# Use only first 10 examples for quick test
python lora/prepare_training_data.py \
    --input datasets/Output/training_examples_with_outputs.json \
    --output datasets/Output/lora_test_data.json \
    --format conversation \
    --max_examples 10 \
    --create_split

# Train for 1 epoch
python lora/train_lora.py \
    --train_data datasets/Output/lora_splits/train.json \
    --num_epochs 1 \
    --batch_size 2
```

### 4. Evaluate Model Performance

```bash
python lora/evaluate.py \
    --base_model "llava-hf/llava-1.5-7b-hf" \
    --lora_adapter models/lora_checkpoints/final_model \
    --test_data datasets/Output/lora_splits/val.json \
    --output evaluation/results.json \
    --max_samples 10
```

## What Each Component Does

### RAG System
- **Input**: User prompt like "minimalist living room"
- **Process**: Searches 10,000 furniture items using semantic similarity
- **Output**: Top 15 most relevant furniture items with details
- **Benefit**: Grounds LLM responses in actual available furniture

### LoRA Training
- **Input**: Training examples with user prompts and expected furniture selections
- **Process**: Fine-tunes vision-language model using efficient LoRA adapters
- **Output**: Specialized model for interior design tasks
- **Benefit**: Model learns Singapore HDB-specific design patterns

### Combined RAG + LoRA
- **Input**: User's interior design request
- **Process**:
  1. RAG retrieves relevant furniture
  2. LoRA model generates recommendations using retrieved context
- **Output**: Personalized furniture arrangement suggestions
- **Benefit**: Best of both worlds - grounded in real furniture + trained on design patterns

## Expected File Sizes

After setup:
```
furniture_db/           ~500 MB   (Vector database)
models/lora_checkpoints/ ~8 GB    (LoRA adapters)
datasets/Output/        ~50 MB    (Training data)
```

## Troubleshooting

### "CUDA out of memory"
```bash
# Reduce batch size
python lora/train_lora.py --batch_size 2

# Or reduce sequence length
python lora/train_lora.py --max_seq_length 1024
```

### "ChromaDB not found"
```bash
# Rebuild database
python rag/build_furniture_db.py \
    --furniture_csv "datasets/Input/Furniture Dataset - Furniture Data.csv"
```

### "Model not found"
The first time you train, Hugging Face will download the base model (~14GB).
Make sure you have a stable internet connection.

## Next Steps

1. **Experiment with RAG**: Try different queries and retrieval counts
2. **Train LoRA**: Fine-tune on your dataset
3. **Evaluate**: Test model performance on validation set
4. **Iterate**: Adjust hyperparameters based on results
5. **Deploy**: Integrate with your DecoPlan C++ inference pipeline

## Getting Help

- See full documentation: `RAG_LORA_README.md`
- Check code comments in each script
- Review example outputs in `datasets/Output/`

## Performance Benchmarks

On a typical setup (RTX 3090, 24GB VRAM):

| Task | Time | VRAM |
|------|------|------|
| Build RAG DB | ~3 min | N/A |
| RAG Retrieval | <1 sec | N/A |
| LoRA Training (3 epochs) | ~2 hours | 18GB |
| Inference (single) | ~5 sec | 12GB |

## Citation

```bibtex
@software{decoplan_rag_lora_2024,
  title = {RAG + LoRA for Interior Design},
  year = {2024},
  url = {https://github.com/yourusername/decoplan-llm}
}
```
