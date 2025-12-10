"""
LABBAIK AI v6.0 - Test Configuration
====================================
Pytest configuration, fixtures, and test utilities.
"""

import pytest
import os
import sys
from typing import Generator, Dict, Any
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, date
import tempfile

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# =============================================================================
# PYTEST CONFIGURATION
# =============================================================================

def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# =============================================================================
# ENVIRONMENT FIXTURES
# =============================================================================

@pytest.fixture(scope="session")
def test_env():
    """Set up test environment variables."""
    original_env = os.environ.copy()
    
    os.environ.update({
        "LABBAIK_ENV": "testing",
        "DATABASE_URL": "postgresql://test:test@localhost:5432/labbaik_test",
        "GROQ_API_KEY": "test_groq_api_key",
        "OPENAI_API_KEY": "test_openai_api_key",
        "SESSION_SECRET_KEY": "test_secret_key_at_least_32_chars_long",
        "JWT_SECRET_KEY": "test_jwt_secret_key_at_least_32_chars",
    })
    
    yield os.environ
    
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


# =============================================================================
# CONFIGURATION FIXTURES
# =============================================================================

@pytest.fixture
def mock_settings():
    """Create mock settings object."""
    from core.config import Settings, DatabaseConfig, AIConfig, AuthConfig, UIConfig
    
    return Settings(
        environment="testing",
        debug=True,
        database=DatabaseConfig(url="postgresql://test:test@localhost/test"),
        ai=AIConfig(
            groq_api_key="test_key",
            groq_model="llama-3.3-70b-versatile"
        ),
        auth=AuthConfig(
            session_secret_key="test_secret_key_12345678901234567890"
        ),
        ui=UIConfig(
            app_name="LABBAIK AI Test",
            app_version="6.0.0-test"
        )
    )


@pytest.fixture
def config_manager(mock_settings):
    """Create config manager with mock settings."""
    from core.config import ConfigManager
    
    manager = ConfigManager()
    manager._settings = mock_settings
    return manager


# =============================================================================
# DATABASE FIXTURES
# =============================================================================

@pytest.fixture
def mock_db():
    """Create mock database connection."""
    db = Mock()
    db.fetch_one = Mock(return_value=None)
    db.fetch_all = Mock(return_value=[])
    db.execute = Mock(return_value=1)
    return db


@pytest.fixture
def mock_user_repo(mock_db):
    """Create mock user repository."""
    from services.database.repository import UserRepository
    
    repo = UserRepository(db=mock_db)
    return repo


@pytest.fixture
def mock_chat_repo(mock_db):
    """Create mock chat repository."""
    from services.database.repository import ChatRepository
    
    repo = ChatRepository(db=mock_db)
    return repo


# =============================================================================
# AI SERVICE FIXTURES
# =============================================================================

@pytest.fixture
def mock_chat_response():
    """Create mock chat completion response."""
    from services.ai.base import ChatCompletionResponse
    
    return ChatCompletionResponse(
        content="This is a test response from the AI.",
        model="test-model",
        usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
        finish_reason="stop",
        latency_ms=100.0
    )


@pytest.fixture
def mock_groq_service(mock_chat_response):
    """Create mock Groq chat service."""
    from services.ai.chat_service import GroqChatService
    
    service = Mock(spec=GroqChatService)
    service.provider_name = "groq"
    service.is_initialized = True
    service.complete = Mock(return_value=mock_chat_response)
    service.stream = Mock(return_value=iter(["Hello", " ", "World"]))
    
    return service


@pytest.fixture
def mock_embedding_service():
    """Create mock embedding service."""
    from services.ai.rag_service import LocalEmbeddingService
    
    service = Mock(spec=LocalEmbeddingService)
    service._initialized = True
    service.embed = Mock(return_value=[[0.1] * 384])
    service.embed_single = Mock(return_value=[0.1] * 384)
    
    return service


@pytest.fixture
def mock_vector_store(mock_embedding_service):
    """Create mock vector store."""
    from services.ai.rag_service import ChromaVectorStore, RetrievalResult, Document
    
    store = Mock(spec=ChromaVectorStore)
    store._initialized = True
    store.count = Mock(return_value=100)
    
    mock_doc = Document(
        id="test_doc_1",
        content="This is test content about Umrah.",
        metadata={"source": "test"}
    )
    
    store.search = Mock(return_value=RetrievalResult(
        documents=[mock_doc],
        scores=[0.95],
        query="test query"
    ))
    
    return store


# =============================================================================
# USER FIXTURES
# =============================================================================

@pytest.fixture
def sample_user_data():
    """Create sample user data."""
    return {
        "id": "user_123",
        "email": "test@example.com",
        "name": "Test User",
        "phone": "+6281234567890",
        "role": "user",
        "subscription_tier": "free",
        "is_verified": True,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


@pytest.fixture
def sample_user(sample_user_data):
    """Create sample user model."""
    from data.models import User
    return User(**sample_user_data)


@pytest.fixture
def sample_admin_user():
    """Create sample admin user."""
    from data.models import User, UserRole, SubscriptionTier
    
    return User(
        id="admin_123",
        email="admin@labbaik.cloud",
        name="Admin User",
        role=UserRole.ADMIN,
        subscription_tier=SubscriptionTier.ENTERPRISE,
        is_verified=True,
        is_active=True
    )


# =============================================================================
# BOOKING FIXTURES
# =============================================================================

@pytest.fixture
def sample_traveler_data():
    """Create sample traveler data."""
    return {
        "name": "Test Traveler",
        "passport_number": "A12345678",
        "passport_expiry": date(2030, 12, 31),
        "birth_date": date(1990, 1, 1),
        "gender": "male",
        "nationality": "ID"
    }


@pytest.fixture
def sample_booking_data(sample_traveler_data):
    """Create sample booking data."""
    from data.models import TravelerInfo
    
    return {
        "user_id": "user_123",
        "package_type": "reguler",
        "departure_city": "Jakarta",
        "departure_date": date(2025, 3, 1),
        "return_date": date(2025, 3, 15),
        "travelers": [TravelerInfo(**sample_traveler_data)]
    }


@pytest.fixture
def sample_booking(sample_booking_data):
    """Create sample booking model."""
    from data.models import Booking
    return Booking(**sample_booking_data)


# =============================================================================
# COST SIMULATION FIXTURES
# =============================================================================

@pytest.fixture
def sample_cost_input():
    """Create sample cost simulation input."""
    from data.models import CostSimulationInput, HotelStarRating, PackageType
    
    return CostSimulationInput(
        departure_city="Jakarta",
        departure_date=date(2025, 3, 1),
        return_date=date(2025, 3, 15),
        traveler_count=2,
        hotel_makkah_star=HotelStarRating.STANDARD,
        hotel_madinah_star=HotelStarRating.STANDARD,
        days_makkah=6,
        days_madinah=5,
        package_type=PackageType.REGULER,
        include_visa=True,
        include_insurance=True,
        include_mutawif=True
    )


# =============================================================================
# PLUGIN FIXTURES
# =============================================================================

@pytest.fixture
def mock_plugin_context():
    """Create mock plugin context."""
    from plugins.base import PluginContext
    
    return PluginContext(
        app=Mock(),
        config={"test": True},
        services={},
        user={"id": "user_123", "role": "user"}
    )


@pytest.fixture
def mock_plugin_registry():
    """Create mock plugin registry."""
    from plugins.base import PluginRegistry
    
    registry = PluginRegistry()
    registry._plugins = {}
    registry._hooks = {}
    return registry


# =============================================================================
# STREAMLIT FIXTURES
# =============================================================================

@pytest.fixture
def mock_streamlit():
    """Mock Streamlit for testing UI components."""
    with patch.dict('sys.modules', {'streamlit': MagicMock()}):
        import streamlit as st
        
        st.session_state = {}
        st.write = Mock()
        st.markdown = Mock()
        st.error = Mock()
        st.success = Mock()
        st.warning = Mock()
        st.info = Mock()
        st.button = Mock(return_value=False)
        st.text_input = Mock(return_value="")
        st.selectbox = Mock(return_value="")
        st.form = Mock()
        st.columns = Mock(return_value=[Mock(), Mock()])
        
        yield st


# =============================================================================
# TEST UTILITIES
# =============================================================================

class TestHelpers:
    """Helper utilities for tests."""
    
    @staticmethod
    def assert_model_valid(model, required_fields: list):
        """Assert model has required fields."""
        for field in required_fields:
            assert hasattr(model, field), f"Missing field: {field}"
            assert getattr(model, field) is not None, f"Field is None: {field}"
    
    @staticmethod
    def create_mock_response(data: dict, status_code: int = 200):
        """Create mock HTTP response."""
        response = Mock()
        response.status_code = status_code
        response.json = Mock(return_value=data)
        response.text = str(data)
        return response
    
    @staticmethod
    def generate_test_id(prefix: str = "test"):
        """Generate unique test ID."""
        import uuid
        return f"{prefix}_{uuid.uuid4().hex[:8]}"


@pytest.fixture
def test_helpers():
    """Provide test helper utilities."""
    return TestHelpers()


# =============================================================================
# ASYNC FIXTURES
# =============================================================================

@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    import asyncio
    
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# =============================================================================
# CLEANUP FIXTURES
# =============================================================================

@pytest.fixture(autouse=True)
def cleanup_session_state(mock_streamlit):
    """Clean up session state between tests."""
    yield
    if hasattr(mock_streamlit, 'session_state'):
        mock_streamlit.session_state.clear()
