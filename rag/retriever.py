"""
RAG Retriever Module
====================
Handles retrieval and context building for the RAG system
"""

from typing import List, Dict, Any, Optional
from .vectorstore import VectorStoreManager


class RAGRetriever:
    """RAG Retriever for context-aware responses"""
    
    def __init__(self, collection_name: str = "umrah_knowledge"):
        """
        Initialize RAG retriever
        
        Args:
            collection_name: Name of the vector store collection
        """
        self.vector_store = VectorStoreManager(collection_name)
        self._initialized = False
    
    def initialize(self, force_reload: bool = False) -> int:
        """
        Initialize the retriever by loading knowledge base
        
        Args:
            force_reload: Force reload even if already loaded
            
        Returns:
            Number of documents in the knowledge base
        """
        if self._initialized and not force_reload:
            return self.vector_store.get_document_count()
        
        # Check if collection already has documents
        doc_count = self.vector_store.get_document_count()
        
        if doc_count == 0 or force_reload:
            if force_reload:
                self.vector_store.clear_collection()
            doc_count = self.vector_store.load_knowledge_base()
        
        self._initialized = True
        return doc_count
    
    def retrieve(
        self,
        query: str,
        n_results: int = 5,
        category: Optional[str] = None,
        min_relevance: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: User query
            n_results: Maximum number of results
            category: Optional category filter
            min_relevance: Minimum relevance score threshold
            
        Returns:
            List of relevant documents
        """
        if not self._initialized:
            self.initialize()
        
        results = self.vector_store.search(
            query=query,
            n_results=n_results,
            filter_category=category
        )
        
        # Filter by relevance score
        filtered_results = [
            r for r in results
            if r.get("relevance_score", 0) >= min_relevance
        ]
        
        return filtered_results
    
    def build_context(
        self,
        query: str,
        n_results: int = 3,
        category: Optional[str] = None
    ) -> str:
        """
        Build context string from retrieved documents
        
        Args:
            query: User query
            n_results: Number of documents to include
            category: Optional category filter
            
        Returns:
            Formatted context string
        """
        results = self.retrieve(query, n_results, category)
        
        if not results:
            return "Tidak ditemukan informasi relevan dalam knowledge base."
        
        context_parts = []
        for i, doc in enumerate(results, 1):
            title = doc["metadata"].get("title", "Untitled")
            content = doc["content"]
            category = doc["metadata"].get("category", "general")
            
            context_parts.append(
                f"[Sumber {i}: {title}]\n"
                f"Kategori: {category}\n"
                f"{content}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    def get_relevant_categories(self, query: str) -> List[str]:
        """
        Determine relevant categories for a query
        
        Args:
            query: User query
            
        Returns:
            List of relevant category names
        """
        # Map keywords to categories
        category_keywords = {
            "overview": ["umrah", "haji", "rukun", "wajib", "pengertian"],
            "visa": ["visa", "paspor", "dokumen", "persyaratan"],
            "transportasi": ["pesawat", "tiket", "bus", "kereta", "transport"],
            "akomodasi": ["hotel", "penginapan", "kamar", "menginap"],
            "konsumsi": ["makan", "makanan", "restoran", "kuliner"],
            "waktu": ["musim", "waktu", "kapan", "bulan", "ramadhan"],
            "perlengkapan": ["bawa", "perlengkapan", "oleh-oleh", "kurma"],
            "paket": ["paket", "travel", "harga", "biaya"],
            "tips": ["tips", "hemat", "murah", "cara"],
            "kesehatan": ["vaksin", "kesehatan", "sakit", "obat"],
            "ibadah": ["thawaf", "sai", "ihram", "manasik", "ziarah"],
            "keuangan": ["bayar", "cicilan", "tabung", "biaya", "asuransi"],
        }
        
        query_lower = query.lower()
        relevant = []
        
        for category, keywords in category_keywords.items():
            if any(kw in query_lower for kw in keywords):
                relevant.append(category)
        
        return relevant if relevant else ["overview"]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        return {
            "total_documents": self.vector_store.get_document_count(),
            "categories": self.vector_store.get_all_categories(),
            "initialized": self._initialized,
        }
