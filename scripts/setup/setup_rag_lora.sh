#!/bin/bash

# Setup script for RAG + LoRA system
# This script will guide you through setting up the entire system

set -e

echo "========================================"
echo "DecoPlan RAG + LoRA Setup"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Install dependencies
echo "========================================"
echo "Step 1: Installing Python dependencies"
echo "========================================"
read -p "Install dependencies? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "Skipped dependency installation"
fi
echo ""

# Build RAG database
echo "========================================"
echo "Step 2: Building RAG Vector Database"
echo "========================================"
read -p "Build furniture vector database? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python rag/build_furniture_db.py \
        --furniture_csv "datasets/Input/Furniture Dataset - Furniture Data.csv" \
        --db_path ./furniture_db \
        --model "all-MiniLM-L6-v2"
    echo "✓ Vector database built"
else
    echo "Skipped database building"
fi
echo ""

# Test RAG retrieval
echo "========================================"
echo "Step 3: Testing RAG Retrieval"
echo "========================================"
read -p "Test RAG retrieval? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python rag/furniture_retriever.py \
        --query "minimalist living room with neutral colors" \
        --n_results 10
    echo "✓ RAG retrieval tested"
else
    echo "Skipped RAG testing"
fi
echo ""

# Prepare training data
echo "========================================"
echo "Step 4: Preparing LoRA Training Data"
echo "========================================"
read -p "Prepare training data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python lora/prepare_training_data.py \
        --input datasets/Output/training_examples_with_outputs.json \
        --output datasets/Output/lora_training_data.json \
        --format conversation \
        --create_split \
        --val_ratio 0.1
    echo "✓ Training data prepared"
else
    echo "Skipped data preparation"
fi
echo ""

# Train LoRA (optional - requires GPU)
echo "========================================"
echo "Step 5: Training LoRA Adapter"
echo "========================================"
echo "NOTE: LoRA training requires a GPU with 12GB+ VRAM"
echo "This step can take several hours depending on your hardware"
read -p "Train LoRA adapter now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting LoRA training..."
    echo "You can modify hyperparameters in lora/train_lora.py"
    python lora/train_lora.py \
        --model_name "llava-hf/llava-1.5-7b-hf" \
        --train_data datasets/Output/lora_splits/train.json \
        --val_data datasets/Output/lora_splits/val.json \
        --output_dir models/lora_checkpoints \
        --num_epochs 3 \
        --batch_size 4 \
        --learning_rate 2e-4
    echo "✓ LoRA training completed"
else
    echo "Skipped LoRA training"
    echo "You can train later with: python lora/train_lora.py"
fi
echo ""

# Generate RAG-enhanced prompts
echo "========================================"
echo "Step 6: Generating RAG-Enhanced Prompts"
echo "========================================"
read -p "Generate RAG-enhanced prompts for all examples? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python rag/rag_inference.py \
        --mode batch \
        --prompts_csv datasets/Input/hdb_interior_design_prompts_300.csv \
        --output datasets/Output/rag_enhanced_prompts.json \
        --n_furniture 15
    echo "✓ RAG-enhanced prompts generated"
else
    echo "Skipped prompt generation"
fi
echo ""

# Summary
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "You can now:"
echo ""
echo "1. Test RAG retrieval:"
echo "   python rag/furniture_retriever.py --query 'your query here'"
echo ""
echo "2. Train LoRA (if not done already):"
echo "   python lora/train_lora.py"
echo ""
echo "3. Run inference with RAG + LoRA:"
echo "   python lora/inference.py --prompt 'your design request'"
echo ""
echo "4. Evaluate the model:"
echo "   python lora/evaluate.py"
echo ""
echo "For more details, see RAG_LORA_README.md"
echo ""
