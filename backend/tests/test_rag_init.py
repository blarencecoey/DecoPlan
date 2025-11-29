#!/usr/bin/env python3
"""
Pytest tests for RAG system initialization
"""

import os
import sys
from pathlib import Path
import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Determine correct database path
DB_PATH = Path(__file__).parent.parent.parent / "data" / "furniture_db"
DB_PATH_STR = str(DB_PATH)

# Check if database exists (skip tests if not)
DB_EXISTS = DB_PATH.exists()
skip_if_no_db = pytest.mark.skipif(
    not DB_EXISTS,
    reason=f"Database not found at {DB_PATH}. Run build_furniture_db.py to create it.",
)


def test_database_exists():
    """Test 1: Check database exists (or skip if not available)"""
    if not DB_PATH.exists():
        pytest.skip(
            f"Database not found at {DB_PATH}. This is expected in CI environments."
        )

    db_files = list(DB_PATH.glob("*"))
    assert len(db_files) > 0, "Database directory is empty"
    print(f"✓ Database found at {DB_PATH}")
    print(f"  Files: {[f.name for f in db_files[:5]]}")


def test_import_furniture_retriever():
    """Test 2: Import FurnitureRetriever"""
    from rag.furniture_retriever import FurnitureRetriever

    print("✓ FurnitureRetriever imported successfully")


def test_import_rag_inference():
    """Test 3: Import RAGInference"""
    from rag.rag_inference import RAGInference

    print("✓ RAGInference imported successfully")


@skip_if_no_db
def test_initialize_furniture_retriever():
    """Test 4: Initialize FurnitureRetriever"""
    from rag.furniture_retriever import FurnitureRetriever

    retriever = FurnitureRetriever(db_path=DB_PATH_STR)
    assert retriever is not None, "Failed to initialize FurnitureRetriever"
    print("✓ FurnitureRetriever initialized successfully")


@skip_if_no_db
def test_retrieval():
    """Test 5: Test retrieval functionality"""
    from rag.furniture_retriever import FurnitureRetriever

    retriever = FurnitureRetriever(db_path=DB_PATH_STR)
    results = retriever.retrieve(query="modern sofa", n_results=3)

    assert results is not None, "Retrieval returned None"
    assert len(results) > 0, "No results returned from retrieval"
    assert "name" in results[0], "Result missing 'name' field"

    print(f"✓ Retrieval successful! Found {len(results)} results")
    print(f"  Sample result: {results[0]['name']}")
