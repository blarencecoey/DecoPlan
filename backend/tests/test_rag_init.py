#!/usr/bin/env python3
"""
Diagnostic script to test RAG system initialization
Run this to debug initialization issues
"""

import sys
import traceback

print("=" * 60)
print("DecoPlan RAG System Diagnostic")
print("=" * 60)

# Test 1: Check database
print("\n[1/4] Checking database...")
import os
from pathlib import Path

DB_PATH = "./furniture_db"
if not os.path.exists(DB_PATH):
    print(f"❌ FAILED: Database not found at {DB_PATH}")
    sys.exit(1)
else:
    print(f"✓ Database found at {DB_PATH}")
    db_files = list(Path(DB_PATH).glob("*"))
    print(f"  Files: {[f.name for f in db_files[:5]]}")

# Test 2: Import RAG modules
print("\n[2/4] Testing imports...")
try:
    from rag.furniture_retriever import FurnitureRetriever
    print("✓ FurnitureRetriever imported successfully")
except Exception as e:
    print(f"❌ FAILED to import FurnitureRetriever:")
    print(f"  Error: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    from rag.rag_inference import RAGInference
    print("✓ RAGInference imported successfully")
except Exception as e:
    print(f"❌ FAILED to import RAGInference:")
    print(f"  Error: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 3: Initialize FurnitureRetriever
print("\n[3/4] Initializing FurnitureRetriever...")
try:
    retriever = FurnitureRetriever(db_path=DB_PATH)
    print("✓ FurnitureRetriever initialized successfully")
except Exception as e:
    print(f"❌ FAILED to initialize FurnitureRetriever:")
    print(f"  Error: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 4: Test retrieval
print("\n[4/4] Testing retrieval...")
try:
    results = retriever.retrieve(query="modern sofa", n_results=3)
    print(f"✓ Retrieval successful! Found {len(results)} results")
    if results:
        print(f"  Sample result: {results[0]['name']}")
except Exception as e:
    print(f"❌ FAILED to retrieve:")
    print(f"  Error: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED!")
print("RAG system is working correctly.")
print("=" * 60)
print("\nIf Flask still fails, check:")
print("1. Virtual environment is activated")
print("2. All dependencies are installed")
print("3. Flask app.py imports are correct")
