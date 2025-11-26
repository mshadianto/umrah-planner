"""
Embedding Handler - Fixed for CPU
"""

import os
from typing import List
import numpy as np

os.environ["TOKENIZERS_PARALLELISM"] = "false"

from config import embedding_config


class EmbeddingHandler:
    _instance = None
    _model = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not EmbeddingHandler._initialized:
            self._load_model()
    
    def _load_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            
            model_name = embedding_config.model_name
            print(f"Loading embedding model: {model_name}")
            
            EmbeddingHandler._model = SentenceTransformer(
                model_name,
                device='cpu'
            )
            EmbeddingHandler._initialized = True
            print("✓ Embedding model loaded!")
            
        except Exception as e:
            print(f"Warning: {e}")
            print("Using fallback embeddings...")
            EmbeddingHandler._model = None
            EmbeddingHandler._initialized = True
    
    @property
    def model(self):
        return EmbeddingHandler._model
    
    def embed_text(self, text: str) -> np.ndarray:
        if self.model is None:
            return self._fallback_embed(text)
        try:
            return self.model.encode(text, convert_to_numpy=True, show_progress_bar=False)
        except:
            return self._fallback_embed(text)
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        if self.model is None:
            return np.array([self._fallback_embed(t) for t in texts])
        try:
            return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        except:
            return np.array([self._fallback_embed(t) for t in texts])
    
    def embed_query(self, query: str) -> np.ndarray:
        return self.embed_text(query)
    
    def _fallback_embed(self, text: str, dim: int = 384) -> np.ndarray:
        import hashlib
        hash_obj = hashlib.sha256(text.encode('utf-8'))
        hash_bytes = hash_obj.digest()
        embedding = [(hash_bytes[i % len(hash_bytes)] - 128) / 128.0 for i in range(dim)]
        return np.array(embedding, dtype=np.float32)
    
    def get_embedding_dimension(self) -> int:
        if self.model:
            return self.model.get_sentence_embedding_dimension()
        return 384