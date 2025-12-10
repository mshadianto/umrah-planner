"""
LABBAIK AI v6.0 - AI Services Unit Tests
========================================
Tests for chat service, RAG service, and embedding service.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from services.ai.base import (
    ChatMessage,
    MessageRole,
    ChatCompletionRequest,
    ChatCompletionResponse,
    RateLimiter,
    AIServiceFactory,
)
from services.ai.chat_service import (
    GroqChatService,
    OpenAIChatService,
    UnifiedChatService,
)
from services.ai.rag_service import (
    Document,
    RetrievalResult,
    LocalEmbeddingService,
    ChromaVectorStore,
    RAGService,
)


# =============================================================================
# CHAT MESSAGE TESTS
# =============================================================================

class TestChatMessage:
    """Tests for ChatMessage model."""
    
    def test_create_user_message(self):
        """Test creating user message."""
        msg = ChatMessage.user("Hello, world!")
        
        assert msg.role == MessageRole.USER
        assert msg.content == "Hello, world!"
        assert msg.timestamp is not None
    
    def test_create_assistant_message(self):
        """Test creating assistant message."""
        msg = ChatMessage.assistant("Hi there!")
        
        assert msg.role == MessageRole.ASSISTANT
        assert msg.content == "Hi there!"
    
    def test_create_system_message(self):
        """Test creating system message."""
        msg = ChatMessage.system("You are a helpful assistant.")
        
        assert msg.role == MessageRole.SYSTEM
        assert msg.content == "You are a helpful assistant."
    
    def test_to_dict(self):
        """Test converting message to dictionary."""
        msg = ChatMessage.user("Test message")
        d = msg.to_dict()
        
        assert d == {"role": "user", "content": "Test message"}


class TestChatCompletionRequest:
    """Tests for ChatCompletionRequest."""
    
    def test_create_request(self):
        """Test creating completion request."""
        messages = [
            ChatMessage.system("System prompt"),
            ChatMessage.user("User message"),
        ]
        
        request = ChatCompletionRequest(
            messages=messages,
            temperature=0.8,
            max_tokens=2048
        )
        
        assert len(request.messages) == 2
        assert request.temperature == 0.8
        assert request.max_tokens == 2048
        assert request.stream is False


class TestChatCompletionResponse:
    """Tests for ChatCompletionResponse."""
    
    def test_response_properties(self, mock_chat_response):
        """Test response properties."""
        assert mock_chat_response.total_tokens == 30
        assert mock_chat_response.prompt_tokens == 10
        assert mock_chat_response.completion_tokens == 20


# =============================================================================
# RATE LIMITER TESTS
# =============================================================================

class TestRateLimiter:
    """Tests for rate limiter."""
    
    def test_can_proceed_initially(self):
        """Test that requests can proceed initially."""
        limiter = RateLimiter(requests_per_minute=30, tokens_per_minute=100000)
        
        can_proceed, wait_time = limiter.can_proceed(1000)
        
        assert can_proceed is True
        assert wait_time == 0
    
    def test_rate_limit_requests(self):
        """Test request rate limiting."""
        limiter = RateLimiter(requests_per_minute=2, tokens_per_minute=100000)
        
        # Record 2 requests
        limiter.record_request(100)
        limiter.record_request(100)
        
        # Third request should be limited
        can_proceed, wait_time = limiter.can_proceed(100)
        
        assert can_proceed is False
        assert wait_time > 0
    
    def test_record_request(self):
        """Test recording requests."""
        limiter = RateLimiter(requests_per_minute=30, tokens_per_minute=100000)
        
        limiter.record_request(500)
        
        assert len(limiter._request_timestamps) == 1
        assert len(limiter._token_usage) == 1


# =============================================================================
# GROQ CHAT SERVICE TESTS
# =============================================================================

class TestGroqChatService:
    """Tests for Groq chat service."""
    
    @pytest.fixture
    def groq_service(self):
        """Create Groq service instance."""
        return GroqChatService(
            api_key="test_api_key",
            model="llama-3.3-70b-versatile"
        )
    
    def test_provider_name(self, groq_service):
        """Test provider name."""
        assert groq_service.provider_name == "groq"
    
    def test_available_models(self, groq_service):
        """Test available models list."""
        assert "llama-3.3-70b-versatile" in groq_service.AVAILABLE_MODELS
    
    def test_default_model(self, groq_service):
        """Test default model."""
        assert groq_service.model == "llama-3.3-70b-versatile"
    
    @patch("services.ai.chat_service.GroqChatService.initialize")
    def test_initialize(self, mock_init, groq_service):
        """Test service initialization."""
        mock_init.return_value = True
        
        result = groq_service.initialize()
        
        assert result is True
    
    def test_simple_complete(self, mock_groq_service, mock_chat_response):
        """Test simple complete interface."""
        mock_groq_service.simple_complete = Mock(return_value="Test response")
        
        result = mock_groq_service.simple_complete("Hello")
        
        assert result == "Test response"


# =============================================================================
# OPENAI CHAT SERVICE TESTS
# =============================================================================

class TestOpenAIChatService:
    """Tests for OpenAI chat service."""
    
    @pytest.fixture
    def openai_service(self):
        """Create OpenAI service instance."""
        return OpenAIChatService(
            api_key="test_api_key",
            model="gpt-4o-mini"
        )
    
    def test_provider_name(self, openai_service):
        """Test provider name."""
        assert openai_service.provider_name == "openai"
    
    def test_available_models(self, openai_service):
        """Test available models list."""
        assert "gpt-4o-mini" in openai_service.AVAILABLE_MODELS


# =============================================================================
# UNIFIED CHAT SERVICE TESTS
# =============================================================================

class TestUnifiedChatService:
    """Tests for unified chat service with fallback."""
    
    @pytest.fixture
    def unified_service(self, mock_groq_service):
        """Create unified service with mock primary."""
        fallback = Mock()
        fallback.complete = Mock()
        
        return UnifiedChatService(
            primary_service=mock_groq_service,
            fallback_service=fallback
        )
    
    def test_uses_primary_first(self, unified_service, mock_chat_response):
        """Test that primary service is used first."""
        request = ChatCompletionRequest(
            messages=[ChatMessage.user("Test")]
        )
        
        result = unified_service.complete(request)
        
        assert result == mock_chat_response
        unified_service.primary.complete.assert_called_once()


# =============================================================================
# DOCUMENT & RETRIEVAL TESTS
# =============================================================================

class TestDocument:
    """Tests for Document model."""
    
    def test_create_document(self):
        """Test creating document."""
        doc = Document(
            id="doc_1",
            content="Test content",
            metadata={"source": "test"}
        )
        
        assert doc.id == "doc_1"
        assert doc.content == "Test content"
        assert doc.metadata["source"] == "test"
    
    def test_to_dict(self):
        """Test converting to dictionary."""
        doc = Document(
            id="doc_1",
            content="Test content",
            metadata={"source": "test"}
        )
        
        d = doc.to_dict()
        
        assert d["id"] == "doc_1"
        assert d["content"] == "Test content"


class TestRetrievalResult:
    """Tests for RetrievalResult model."""
    
    @pytest.fixture
    def retrieval_result(self):
        """Create sample retrieval result."""
        docs = [
            Document(id="1", content="First doc", metadata={"source": "a"}),
            Document(id="2", content="Second doc", metadata={"source": "b"}),
        ]
        return RetrievalResult(
            documents=docs,
            scores=[0.9, 0.8],
            query="test query"
        )
    
    def test_best_match(self, retrieval_result):
        """Test getting best match."""
        best = retrieval_result.best_match
        
        assert best.id == "1"
        assert best.content == "First doc"
    
    def test_get_context(self, retrieval_result):
        """Test getting combined context."""
        context = retrieval_result.get_context(max_docs=2)
        
        assert "First doc" in context
        assert "Second doc" in context


# =============================================================================
# LOCAL EMBEDDING SERVICE TESTS
# =============================================================================

class TestLocalEmbeddingService:
    """Tests for local embedding service."""
    
    @pytest.fixture
    def embedding_service(self):
        """Create embedding service instance."""
        return LocalEmbeddingService(model_name="all-MiniLM-L6-v2")
    
    def test_default_model(self, embedding_service):
        """Test default model name."""
        assert embedding_service.model_name == "all-MiniLM-L6-v2"
    
    def test_embed_single_mock(self, mock_embedding_service):
        """Test embedding single text with mock."""
        result = mock_embedding_service.embed_single("Test text")
        
        assert len(result) == 384  # Expected embedding dimension


# =============================================================================
# VECTOR STORE TESTS
# =============================================================================

class TestChromaVectorStore:
    """Tests for ChromaDB vector store."""
    
    def test_count(self, mock_vector_store):
        """Test document count."""
        count = mock_vector_store.count()
        
        assert count == 100
    
    def test_search(self, mock_vector_store):
        """Test document search."""
        result = mock_vector_store.search("test query")
        
        assert len(result.documents) == 1
        assert result.scores[0] == 0.95


# =============================================================================
# RAG SERVICE TESTS
# =============================================================================

class TestRAGService:
    """Tests for RAG service."""
    
    @pytest.fixture
    def rag_service(self, mock_groq_service, mock_vector_store):
        """Create RAG service with mocks."""
        return RAGService(
            chat_service=mock_groq_service,
            vector_store=mock_vector_store,
            top_k=5
        )
    
    def test_get_stats(self, rag_service):
        """Test getting RAG stats."""
        stats = rag_service.get_stats()
        
        assert "document_count" in stats
        assert "top_k" in stats
        assert stats["top_k"] == 5
    
    def test_chunk_text(self, rag_service):
        """Test text chunking."""
        text = "This is a test. " * 100
        chunks = rag_service._chunk_text(text, chunk_size=100, overlap=20)
        
        assert len(chunks) > 1
        assert all(len(c) <= 120 for c in chunks)  # Allow some overflow


# =============================================================================
# AI SERVICE FACTORY TESTS
# =============================================================================

class TestAIServiceFactory:
    """Tests for AI service factory."""
    
    def test_available_chat_providers(self):
        """Test listing available providers."""
        providers = AIServiceFactory.available_chat_providers()
        
        assert "groq" in providers
        assert "openai" in providers
    
    def test_create_groq_service(self):
        """Test creating Groq service via factory."""
        service = AIServiceFactory.create_chat_service(
            provider="groq",
            api_key="test_key"
        )
        
        assert service.provider_name == "groq"
    
    def test_create_openai_service(self):
        """Test creating OpenAI service via factory."""
        service = AIServiceFactory.create_chat_service(
            provider="openai",
            api_key="test_key"
        )
        
        assert service.provider_name == "openai"
    
    def test_unknown_provider(self):
        """Test error for unknown provider."""
        with pytest.raises(ValueError, match="Unknown chat service provider"):
            AIServiceFactory.create_chat_service(
                provider="unknown",
                api_key="test_key"
            )
