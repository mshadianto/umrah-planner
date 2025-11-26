"""
Vector Store Manager for RAG System
===================================
Manages ChromaDB vector store for document storage and retrieval
Updated for ChromaDB 0.4.x+
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import chromadb

from config import CHROMA_DIR, DATA_DIR
from .embeddings import EmbeddingHandler


class VectorStoreManager:
    """Manages ChromaDB vector store"""
    
    def __init__(self, collection_name: str = "umrah_knowledge"):
        self.collection_name = collection_name
        self.embedding_handler = EmbeddingHandler()
        
        # NEW: Use PersistentClient (ChromaDB 0.4.x+)
        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Umrah knowledge base"}
        )
    
    def load_knowledge_base(self, json_path: Optional[Path] = None) -> int:
        if json_path is None:
            json_path = DATA_DIR / "knowledge_base.json"
        
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        documents = data.get("documents", [])
        
        if not documents:
            return 0
        
        ids = []
        texts = []
        metadatas = []
        
        for doc in documents:
            doc_id = doc.get("id", f"doc_{len(ids)}")
            content = doc.get("content", "")
            
            if not content:
                continue
            
            full_text = f"{doc.get('title', '')}\n\n{content}"
            
            ids.append(doc_id)
            texts.append(full_text)
            metadatas.append({
                "id": doc_id,
                "category": doc.get("category", "general"),
                "title": doc.get("title", ""),
            })
        
        embeddings = self.embedding_handler.embed_texts(texts)
        
        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )
        
        return len(ids)
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        filter_category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        query_embedding = self.embedding_handler.embed_query(query)
        
        where = None
        if filter_category:
            where = {"category": filter_category}
        
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"]
        )
        
        formatted_results = []
        if results["ids"] and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i],
                    "relevance_score": 1 - results["distances"][0][i]
                })
        
        return formatted_results
    
    def get_all_categories(self) -> List[str]:
        all_docs = self.collection.get(include=["metadatas"])
        categories = set()
        for metadata in all_docs.get("metadatas", []):
            if metadata and "category" in metadata:
                categories.add(metadata["category"])
        return list(categories)
    
    def get_document_count(self) -> int:
        return self.collection.count()
    
    def clear_collection(self):
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"description": "Umrah knowledge base"}
        )