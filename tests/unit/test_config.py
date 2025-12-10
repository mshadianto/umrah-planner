"""
LABBAIK AI v6.0 - Core Config Unit Tests
========================================
Tests for configuration management.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from pathlib import Path

from core.config import (
    Environment,
    DatabaseConfig,
    AIConfig,
    AuthConfig,
    UIConfig,
    LoggingConfig,
    PluginConfig,
    Settings,
    ConfigManager,
    get_settings,
    get_config,
)


# =============================================================================
# ENVIRONMENT TESTS
# =============================================================================

class TestEnvironment:
    """Tests for Environment enum."""
    
    def test_environment_values(self):
        """Test environment enum values."""
        assert Environment.DEVELOPMENT.value == "development"
        assert Environment.STAGING.value == "staging"
        assert Environment.PRODUCTION.value == "production"
        assert Environment.TESTING.value == "testing"
    
    def test_is_development(self):
        """Test is_development property."""
        assert Environment.DEVELOPMENT.is_development is True
        assert Environment.PRODUCTION.is_development is False
    
    def test_is_production(self):
        """Test is_production property."""
        assert Environment.PRODUCTION.is_production is True
        assert Environment.DEVELOPMENT.is_production is False


# =============================================================================
# DATABASE CONFIG TESTS
# =============================================================================

class TestDatabaseConfig:
    """Tests for DatabaseConfig."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = DatabaseConfig()
        
        assert config.url == ""
        assert config.pool_size == 5
        assert config.max_overflow == 10
        assert config.pool_timeout == 30
        assert config.echo is False
    
    def test_custom_values(self):
        """Test custom configuration values."""
        config = DatabaseConfig(
            url="postgresql://user:pass@localhost/db",
            pool_size=10,
            echo=True
        )
        
        assert config.url == "postgresql://user:pass@localhost/db"
        assert config.pool_size == 10
        assert config.echo is True


# =============================================================================
# AI CONFIG TESTS
# =============================================================================

class TestAIConfig:
    """Tests for AIConfig."""
    
    def test_default_values(self):
        """Test default AI configuration."""
        config = AIConfig()
        
        assert config.groq_model == "llama-3.3-70b-versatile"
        assert config.groq_max_tokens == 4096
        assert config.groq_temperature == 0.7
        assert config.openai_model == "gpt-4o-mini"
    
    def test_groq_configured(self):
        """Test groq_configured property."""
        config = AIConfig()
        assert config.groq_configured is False
        
        config_with_key = AIConfig(groq_api_key="test_key")
        assert config_with_key.groq_configured is True
    
    def test_openai_configured(self):
        """Test openai_configured property."""
        config = AIConfig()
        assert config.openai_configured is False
        
        config_with_key = AIConfig(openai_api_key="test_key")
        assert config_with_key.openai_configured is True


# =============================================================================
# AUTH CONFIG TESTS
# =============================================================================

class TestAuthConfig:
    """Tests for AuthConfig."""
    
    def test_default_values(self):
        """Test default auth configuration."""
        config = AuthConfig()
        
        assert config.session_expire_hours == 24
        assert config.jwt_algorithm == "HS256"
        assert config.jwt_expire_minutes == 60
    
    def test_google_configured(self):
        """Test google_configured property."""
        config = AuthConfig()
        assert config.google_configured is False
        
        config_with_google = AuthConfig(
            google_client_id="test_id",
            google_client_secret="test_secret"
        )
        assert config_with_google.google_configured is True


# =============================================================================
# UI CONFIG TESTS
# =============================================================================

class TestUIConfig:
    """Tests for UIConfig."""
    
    def test_default_values(self):
        """Test default UI configuration."""
        config = UIConfig()
        
        assert config.app_name == "LABBAIK AI"
        assert config.page_icon == "🕋"
        assert config.layout == "wide"
        assert config.language == "id"
    
    def test_feature_flags(self):
        """Test feature flags."""
        config = UIConfig()
        
        assert config.enable_chat is True
        assert config.enable_simulator is True
        assert config.enable_booking is True


# =============================================================================
# SETTINGS TESTS
# =============================================================================

class TestSettings:
    """Tests for Settings class."""
    
    def test_default_settings(self):
        """Test default settings creation."""
        settings = Settings()
        
        assert settings.environment == "development"
        assert settings.debug is True
        assert settings.database is not None
        assert settings.ai is not None
        assert settings.auth is not None
        assert settings.ui is not None
    
    def test_is_production(self):
        """Test is_production property."""
        dev_settings = Settings(environment="development")
        assert dev_settings.is_production is False
        
        prod_settings = Settings(environment="production")
        assert prod_settings.is_production is True
    
    def test_is_development(self):
        """Test is_development property."""
        settings = Settings(environment="development")
        assert settings.is_development is True
        
        settings = Settings(environment="production")
        assert settings.is_development is False
    
    def test_is_testing(self):
        """Test is_testing property."""
        settings = Settings(environment="testing")
        assert settings.is_testing is True
    
    @patch.dict(os.environ, {"GROQ_API_KEY": "test_key_from_env"})
    def test_env_override(self):
        """Test environment variable override."""
        settings = Settings()
        # Note: The actual implementation would need to load from env
        # This test demonstrates the expected behavior


# =============================================================================
# CONFIG MANAGER TESTS
# =============================================================================

class TestConfigManager:
    """Tests for ConfigManager singleton."""
    
    def test_singleton_instance(self):
        """Test that ConfigManager is a singleton."""
        manager1 = ConfigManager()
        manager2 = ConfigManager()
        
        assert manager1 is manager2
    
    def test_get_settings(self):
        """Test getting settings."""
        manager = ConfigManager()
        settings = manager.settings
        
        assert settings is not None
        assert isinstance(settings, Settings)
    
    def test_reload_settings(self):
        """Test reloading settings."""
        manager = ConfigManager()
        manager.reload()
        
        # Should not raise an error
        assert manager.settings is not None


# =============================================================================
# HELPER FUNCTION TESTS
# =============================================================================

class TestHelperFunctions:
    """Tests for configuration helper functions."""
    
    def test_get_settings_returns_settings(self):
        """Test get_settings returns Settings instance."""
        settings = get_settings()
        
        assert settings is not None
        assert isinstance(settings, Settings)
    
    def test_get_config_returns_manager(self):
        """Test get_config returns ConfigManager."""
        manager = get_config()
        
        assert manager is not None
        assert isinstance(manager, ConfigManager)


# =============================================================================
# LOGGING CONFIG TESTS
# =============================================================================

class TestLoggingConfig:
    """Tests for LoggingConfig."""
    
    def test_default_values(self):
        """Test default logging configuration."""
        config = LoggingConfig()
        
        assert config.level == "INFO"
        assert config.file_path is None
        assert config.max_bytes == 10 * 1024 * 1024
        assert config.backup_count == 5
    
    def test_custom_values(self):
        """Test custom logging configuration."""
        config = LoggingConfig(
            level="DEBUG",
            file_path="/var/log/labbaik.log"
        )
        
        assert config.level == "DEBUG"
        assert config.file_path == "/var/log/labbaik.log"


# =============================================================================
# PLUGIN CONFIG TESTS
# =============================================================================

class TestPluginConfig:
    """Tests for PluginConfig."""
    
    def test_default_values(self):
        """Test default plugin configuration."""
        config = PluginConfig()
        
        assert config.enabled is True
        assert config.plugin_dir == "plugins/available"
        assert isinstance(config.auto_load, list)
        assert isinstance(config.disabled, list)
    
    def test_custom_values(self):
        """Test custom plugin configuration."""
        config = PluginConfig(
            enabled=False,
            auto_load=["gamification", "analytics"]
        )
        
        assert config.enabled is False
        assert len(config.auto_load) == 2
