#!/usr/bin/env python3
"""
Furniture retrieval module for RAG system.
"""

# Fix SQLite version for ChromaDB (must be before any chromadb imports)
try:
    __import__("pysqlite3")
    import sys

    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass  # pysqlite3 not installed, will use system sqlite3

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from pathlib import Path
from typing import List, Dict, Optional
import json


class FurnitureRetriever:
    """Retrieve relevant furniture from vector database based on user queries."""

    def __init__(
        self, db_path: str = "./furniture_db", model_name: str = "all-MiniLM-L6-v2"
    ):
        """
        Initialize the furniture retriever.

        Args:
            db_path: Path to the ChromaDB database
            model_name: Name of the sentence transformer model (must match building model)
        """
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Vector database not found at {db_path}. "
                "Please run build_furniture_db.py first."
            )

        print(f"Loading embedding model: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.db_path), settings=Settings(anonymized_telemetry=False)
        )

        # Load statistics if available
        stats_path = self.db_path / "stats.json"
        if stats_path.exists():
            with open(stats_path, "r") as f:
                self.stats = json.load(f)
        else:
            self.stats = {}

    def retrieve(
        self,
        query: str,
        n_results: int = 10,
        collection_name: str = "furniture_catalog",
        filters: Optional[Dict] = None,
    ) -> List[Dict]:
        """
        Retrieve relevant furniture based on query.

        Args:
            query: User's furniture query or room description
            n_results: Number of results to return
            collection_name: Name of the ChromaDB collection
            filters: Optional metadata filters (e.g., {"furniture_type": "Sofa"})

        Returns:
            List of furniture items with metadata and relevance scores
        """
        # Get collection
        collection = self.client.get_collection(collection_name)

        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()

        # Build where clause for filtering
        where_clause = None
        if filters:
            where_clause = filters

        # Query the database
        results = collection.query(
            query_embeddings=[query_embedding], n_results=n_results, where=where_clause
        )

        # Format results
        formatted_results = []
        for i in range(len(results["ids"][0])):
            formatted_results.append(
                {
                    "id": results["ids"][0][i],
                    "name": results["metadatas"][0][i]["name"],
                    "furniture_type": results["metadatas"][0][i]["furniture_type"],
                    "material": results["metadatas"][0][i]["material"],
                    "color": results["metadatas"][0][i]["color"],
                    "feel": results["metadatas"][0][i]["feel"],
                    "is_accessory": results["metadatas"][0][i].get(
                        "is_accessory", "N/A"
                    ),
                    "dimensions": results["metadatas"][0][i].get("dimensions", "N/A"),
                    "description": results["documents"][0][i],
                    "relevance_score": 1
                    - results["distances"][0][i],  # Convert distance to similarity
                }
            )

        return formatted_results

    def retrieve_by_style(
        self,
        style: str,
        room_type: str,
        n_results: int = 10,
        collection_name: str = "furniture_catalog",
    ) -> Dict[str, List[Dict]]:
        """
        Retrieve furniture grouped by type for a specific style and room.

        Args:
            style: Design style (e.g., "minimalist", "scandinavian")
            room_type: Room type (e.g., "living_room", "bedroom")
            n_results: Total number of results to retrieve
            collection_name: Name of the ChromaDB collection

        Returns:
            Dictionary with furniture grouped by type
        """
        # Create query based on style and room type
        query = f"{style} style furniture for {room_type.replace('_', ' ')}"

        # Retrieve items
        results = self.retrieve(
            query=query,
            n_results=n_results * 2,  # Get more to ensure variety
            collection_name=collection_name,
        )

        # Group by furniture type
        grouped = {}
        for item in results:
            ftype = item["furniture_type"]
            if ftype not in grouped:
                grouped[ftype] = []
            if len(grouped[ftype]) < 3:  # Limit per type
                grouped[ftype].append(item)

        return grouped

    def retrieve_for_prompt(
        self,
        user_prompt: str,
        room_type: str,
        style: str,
        n_results: int = 15,
        collection_name: str = "furniture_catalog",
    ) -> str:
        """
        Retrieve furniture and format as context for LLM.

        Args:
            user_prompt: User's interior design request
            room_type: Type of room
            style: Design style
            n_results: Number of furniture items to retrieve
            collection_name: Name of the ChromaDB collection

        Returns:
            Formatted context string for LLM
        """
        # Combine prompt with style and room info for better retrieval
        enhanced_query = f"{style} {room_type.replace('_', ' ')}: {user_prompt}"

        # Retrieve furniture
        results = self.retrieve(
            query=enhanced_query, n_results=n_results, collection_name=collection_name
        )

        # Format as context
        context = "Available Furniture Options:\n\n"

        for i, item in enumerate(results, 1):
            context += f"{i}. {item['name']}\n"
            context += f"   Type: {item['furniture_type']}\n"
            context += f"   Material: {item['material']}\n"
            context += f"   Color: {item['color']}\n"
            context += f"   Style: {item['feel']}\n"
            context += f"   Dimensions: {item['dimensions']}\n"
            context += f"   Is Accessory: {item['is_accessory']}\n"
            context += f"   Relevance: {item['relevance_score']:.3f}\n\n"

        return context

    def get_stats(self) -> Dict:
        """Get database statistics."""
        return self.stats


def main():
    """Test the retriever with example queries."""
    import argparse

    parser = argparse.ArgumentParser(description="Test furniture retriever")
    parser.add_argument(
        "--query",
        type=str,
        default="minimalist living room with neutral colors",
        help="Query to test",
    )
    parser.add_argument(
        "--db_path", type=str, default="./furniture_db", help="Path to vector database"
    )
    parser.add_argument(
        "--n_results", type=int, default=10, help="Number of results to retrieve"
    )

    args = parser.parse_args()

    # Initialize retriever
    retriever = FurnitureRetriever(db_path=args.db_path)

    # Test retrieval
    print(f"\nQuery: {args.query}\n")
    print("=" * 80)

    results = retriever.retrieve(query=args.query, n_results=args.n_results)

    for i, item in enumerate(results, 1):
        print(f"\n{i}. {item['name']}")
        print(f"   Type: {item['furniture_type']}")
        print(
            f"   Material: {item['material']}, Color: {item['color']}, Style: {item['feel']}"
        )
        print(
            f"   Dimensions: {item['dimensions']}, Is Accessory: {item['is_accessory']}"
        )
        print(f"   Relevance: {item['relevance_score']:.4f}")

    print("\n" + "=" * 80)
    print(f"Retrieved {len(results)} items")


if __name__ == "__main__":
    main()
