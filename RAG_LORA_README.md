# RAG + LoRA System for DecoPlan LLM

This document describes the Retrieval-Augmented Generation (RAG) and Low-Rank Adaptation (LoRA) systems implemented for DecoPlan LLM.

## Overview

The system combines two powerful techniques:

1. **RAG (Retrieval-Augmented Generation)**: Retrieves relevant furniture items from a vector database to provide context for the LLM
2. **LoRA (Low-Rank Adaptation)**: Fine-tunes vision-language models efficiently on interior design tasks

## Architecture

```
User Prompt → RAG Retrieval → Furniture Context
                                     ↓
                              LoRA Fine-tuned LLM
                                     ↓
                           Furniture Recommendations
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Build RAG Vector Database

```bash
# Build furniture vector database from catalog
python rag/build_furniture_db.py \
    --furniture_csv "datasets/Input/Furniture Dataset - Furniture Data.csv" \
    --db_path ./furniture_db
```

### 3. Test RAG Retrieval

```bash
# Test retrieval with example query
python rag/furniture_retriever.py \
    --query "minimalist living room with neutral colors" \
    --n_results 10
```

### 4. Prepare Training Data for LoRA

```bash
# Prepare data in conversation format
python lora/prepare_training_data.py \
    --input datasets/Output/training_examples_with_outputs.json \
    --output datasets/Output/lora_training_data.json \
    --format conversation \
    --create_split \
    --val_ratio 0.1
```

### 5. Train LoRA Adapter

```bash
# Fine-tune with LoRA (requires GPU)
python lora/train_lora.py \
    --model_name "llava-hf/llava-1.5-7b-hf" \
    --train_data datasets/Output/lora_splits/train.json \
    --val_data datasets/Output/lora_splits/val.json \
    --output_dir models/lora_checkpoints \
    --num_epochs 3 \
    --batch_size 4 \
    --learning_rate 2e-4
```

### 6. Run Inference with RAG + LoRA

```bash
# Generate design recommendations
python lora/inference.py \
    --base_model "llava-hf/llava-1.5-7b-hf" \
    --lora_adapter models/lora_checkpoints/final_model \
    --furniture_db ./furniture_db \
    --prompt "I want a clean, minimalist living room with neutral colors" \
    --room_type living_room \
    --style minimalist
```

## RAG System Details

### Components

1. **build_furniture_db.py**: Builds vector database from furniture catalog
   - Uses sentence-transformers for embeddings
   - Stores in ChromaDB for efficient retrieval
   - Creates searchable descriptions combining all furniture attributes

2. **furniture_retriever.py**: Retrieves relevant furniture based on queries
   - Semantic search using cosine similarity
   - Filtering by furniture type, material, style
   - Returns top-k most relevant items

3. **rag_inference.py**: Creates enhanced prompts with furniture context
   - Combines user request with retrieved furniture
   - Formats context for LLM consumption
   - Supports batch processing

### RAG Configuration

The default embedding model is `all-MiniLM-L6-v2`, which provides:
- Fast inference
- Good semantic understanding
- Low memory footprint (~90MB)

You can use other models:
```bash
python rag/build_furniture_db.py --model "sentence-transformers/all-mpnet-base-v2"
```

### RAG Workflow

```
1. User Query → Embed with sentence-transformers
2. Search Vector DB → Find top-k similar furniture
3. Format Context → Create structured furniture list
4. Combine with Prompt → Send to LLM
```

## LoRA System Details

### Components

1. **prepare_training_data.py**: Formats training examples
   - Supports conversation and Alpaca formats
   - Creates train/validation splits
   - Structures inputs for fine-tuning

2. **train_lora.py**: LoRA fine-tuning pipeline
   - 4-bit quantization with bitsandbytes
   - PEFT library for LoRA adapters
   - Configurable hyperparameters

3. **inference.py**: Combined RAG + LoRA inference
   - Loads base model + LoRA adapter
   - Integrates RAG retrieval
   - Generates design recommendations

4. **evaluate.py**: Model evaluation utilities
   - Calculates perplexity
   - Compares multiple adapters
   - Generates predictions on test set

### LoRA Configuration

Default hyperparameters:
```python
lora_r = 16              # Rank of LoRA matrices
lora_alpha = 32          # Scaling factor
lora_dropout = 0.05      # Dropout rate
target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"]
```

Training settings:
```python
num_epochs = 3
batch_size = 4
gradient_accumulation = 4
learning_rate = 2e-4
optimizer = "paged_adamw_32bit"
```

### LoRA Benefits

- **Efficiency**: Only ~1-2% of parameters are trainable
- **Speed**: Much faster than full fine-tuning
- **Memory**: Works with 4-bit quantization on consumer GPUs
- **Modularity**: Adapters can be swapped without changing base model

## System Requirements

### For RAG
- CPU: Any modern processor
- RAM: 4GB minimum
- Storage: ~500MB for vector database

### For LoRA Training
- GPU: NVIDIA GPU with 12GB+ VRAM (RTX 3060 or better)
- CUDA: 11.0 or higher
- RAM: 16GB system RAM
- Storage: ~20GB for model weights

### For Inference (RAG + LoRA)
- GPU: 8GB+ VRAM recommended
- RAM: 8GB minimum
- Storage: Model weights + database (~15GB)

## Data Formats

### Input Format (Training Examples)
```json
{
  "prompt_id": 1,
  "user_prompt": "I want a minimalist living room",
  "room_type": "living_room",
  "style": "minimalist",
  "floor_plan_metadata": {
    "room_dimensions": {"length": 5.0, "width": 4.0},
    "available_space": 20.0
  },
  "expected_output": {
    "furniture_list": [...],
    "total_furniture_count": 4,
    "design_notes": "..."
  }
}
```

### Conversation Format (LoRA Training)
```json
{
  "messages": [
    {"role": "system", "content": "You are an expert interior designer..."},
    {"role": "user", "content": "Room Type: Living Room\nStyle: Minimalist\n..."},
    {"role": "assistant", "content": "I recommend the following furniture..."}
  ]
}
```

## Advanced Usage

### Custom RAG Queries

```python
from rag.furniture_retriever import FurnitureRetriever

retriever = FurnitureRetriever(db_path="./furniture_db")

# Retrieve with filters
results = retriever.retrieve(
    query="modern sofa",
    n_results=5,
    filters={"furniture_type": "Sofa", "feel": "Modern"}
)

# Retrieve by style
grouped = retriever.retrieve_by_style(
    style="scandinavian",
    room_type="living_room",
    n_results=20
)
```

### Custom LoRA Training

```python
from lora.train_lora import LoRATrainingConfig, LoRATrainer

config = LoRATrainingConfig(
    model_name="llava-hf/llava-1.5-7b-hf",
    lora_r=32,
    lora_alpha=64,
    num_train_epochs=5,
    learning_rate=1e-4
)

trainer = LoRATrainer(config)
trainer.train()
```

### Batch Inference

```python
from lora.inference import DecoPlanInference

inference = DecoPlanInference(
    base_model_name="llava-hf/llava-1.5-7b-hf",
    lora_adapter_path="models/lora_checkpoints/final_model",
    furniture_db_path="./furniture_db"
)

# Process multiple prompts
prompts = [...]
for prompt_data in prompts:
    result = inference.predict(
        user_prompt=prompt_data['prompt'],
        room_type=prompt_data['room_type'],
        style=prompt_data['style']
    )
    print(result['model_response'])
```

## Evaluation

### Evaluate LoRA Model

```bash
python lora/evaluate.py \
    --base_model "llava-hf/llava-1.5-7b-hf" \
    --lora_adapter models/lora_checkpoints/final_model \
    --test_data datasets/Output/lora_splits/val.json \
    --output evaluation/results.json
```

### Compare Multiple Adapters

```bash
python lora/evaluate.py \
    --mode compare \
    --base_model "llava-hf/llava-1.5-7b-hf" \
    --lora_adapters \
        models/lora_checkpoints/checkpoint-100 \
        models/lora_checkpoints/checkpoint-200 \
        models/lora_checkpoints/final_model \
    --test_data datasets/Output/lora_splits/val.json \
    --output evaluation/comparison
```

## Troubleshooting

### CUDA Out of Memory
- Reduce batch size: `--batch_size 2`
- Reduce max sequence length: `--max_seq_length 1024`
- Enable gradient checkpointing in code

### RAG Retrieval Poor Quality
- Use better embedding model: `--model "all-mpnet-base-v2"`
- Increase number of results: `--n_results 20`
- Check database was built correctly

### LoRA Training Not Converging
- Increase learning rate: `--learning_rate 5e-4`
- Increase LoRA rank: `--lora_r 32`
- Train for more epochs: `--num_epochs 5`

## File Structure

```
DecoPlan LLM/
├── rag/
│   ├── __init__.py
│   ├── build_furniture_db.py      # Build vector database
│   ├── furniture_retriever.py     # Retrieve furniture
│   └── rag_inference.py            # RAG-enhanced prompts
├── lora/
│   ├── __init__.py
│   ├── prepare_training_data.py   # Format training data
│   ├── train_lora.py               # LoRA training
│   ├── inference.py                # RAG + LoRA inference
│   └── evaluate.py                 # Model evaluation
├── datasets/
│   ├── Input/
│   │   ├── hdb_interior_design_prompts_300.csv
│   │   └── Furniture Dataset - Furniture Data.csv
│   └── Output/
│       ├── training_examples_with_outputs.json
│       ├── lora_training_data.json
│       └── lora_splits/
│           ├── train.json
│           └── val.json
├── furniture_db/                   # Vector database (generated)
├── models/
│   └── lora_checkpoints/           # LoRA adapters (generated)
└── requirements.txt
```

## Citation

If you use this system in your research, please cite:

```bibtex
@software{decoplan_rag_lora,
  title = {RAG + LoRA System for Interior Design},
  author = {DecoPlan Team},
  year = {2024},
  url = {https://github.com/yourusername/decoplan-llm}
}
```

## License

See [LICENSE](LICENSE) for details.

## Acknowledgments

- **RAG**: ChromaDB, sentence-transformers
- **LoRA**: PEFT, bitsandbytes, Hugging Face Transformers
- **Models**: LLaVA, Qwen2-VL, Llama 3.2 Vision
