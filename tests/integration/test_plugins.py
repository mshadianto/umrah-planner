"""
LABBAIK AI v6.0 - Plugin System Integration Tests
================================================
Integration tests for the plugin system.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

from plugins.base import (
    BasePlugin,
    PluginMetadata,
    PluginStatus,
    PluginPriority,
    PluginContext,
    PluginRegistry,
    PluginLoader,
    HookEvents,
    PluginHook,
    get_registry,
)


# =============================================================================
# TEST PLUGIN IMPLEMENTATIONS
# =============================================================================

class TestPlugin(BasePlugin):
    """Simple test plugin for testing."""
    
    def __init__(self, name: str = "test-plugin"):
        metadata = PluginMetadata(
            name=name,
            version="1.0.0",
            description="Test plugin"
        )
        super().__init__(metadata)
        self.init_called = False
        self.activate_called = False
        self.deactivate_called = False
        self.hook_calls = []
    
    def initialize(self, context: PluginContext) -> bool:
        self.context = context
        self.init_called = True
        return True
    
    def activate(self) -> bool:
        self.activate_called = True
        self.status = PluginStatus.ACTIVE
        return True
    
    def deactivate(self) -> bool:
        self.deactivate_called = True
        self.status = PluginStatus.LOADED
        return True
    
    @PluginHook(HookEvents.USER_LOGIN, priority=PluginPriority.NORMAL)
    def on_user_login(self, user_id: str, **kwargs):
        self.hook_calls.append(("user_login", user_id, kwargs))
    
    @PluginHook(HookEvents.CHAT_MESSAGE_SENT, priority=PluginPriority.HIGH)
    def on_chat_message(self, user_id: str, message: str, **kwargs):
        self.hook_calls.append(("chat_message", user_id, message))


class HighPriorityPlugin(BasePlugin):
    """High priority test plugin."""
    
    def __init__(self):
        metadata = PluginMetadata(
            name="high-priority-plugin",
            version="1.0.0",
            description="High priority test plugin"
        )
        super().__init__(metadata)
        self.hook_order = []
    
    def initialize(self, context: PluginContext) -> bool:
        return True
    
    def activate(self) -> bool:
        self.status = PluginStatus.ACTIVE
        return True
    
    @PluginHook(HookEvents.USER_LOGIN, priority=PluginPriority.HIGHEST)
    def on_user_login(self, user_id: str, **kwargs):
        self.hook_order.append("high")


class LowPriorityPlugin(BasePlugin):
    """Low priority test plugin."""
    
    def __init__(self):
        metadata = PluginMetadata(
            name="low-priority-plugin",
            version="1.0.0",
            description="Low priority test plugin"
        )
        super().__init__(metadata)
        self.hook_order = []
    
    def initialize(self, context: PluginContext) -> bool:
        return True
    
    def activate(self) -> bool:
        self.status = PluginStatus.ACTIVE
        return True
    
    @PluginHook(HookEvents.USER_LOGIN, priority=PluginPriority.LOWEST)
    def on_user_login(self, user_id: str, **kwargs):
        self.hook_order.append("low")


# =============================================================================
# PLUGIN LIFECYCLE TESTS
# =============================================================================

class TestPluginLifecycle:
    """Tests for plugin lifecycle management."""
    
    @pytest.fixture
    def plugin(self):
        """Create a test plugin."""
        return TestPlugin()
    
    @pytest.fixture
    def context(self):
        """Create a test context."""
        return PluginContext(
            app=Mock(),
            config={"test": True},
            services={},
            user={"id": "user_123", "role": "user"}
        )
    
    def test_plugin_initialization(self, plugin, context):
        """Test plugin initialization."""
        result = plugin.initialize(context)
        
        assert result is True
        assert plugin.init_called is True
        assert plugin.context == context
    
    def test_plugin_activation(self, plugin, context):
        """Test plugin activation."""
        plugin.initialize(context)
        result = plugin.activate()
        
        assert result is True
        assert plugin.activate_called is True
        assert plugin.status == PluginStatus.ACTIVE
    
    def test_plugin_deactivation(self, plugin, context):
        """Test plugin deactivation."""
        plugin.initialize(context)
        plugin.activate()
        result = plugin.deactivate()
        
        assert result is True
        assert plugin.deactivate_called is True
        assert plugin.status == PluginStatus.LOADED
    
    def test_plugin_full_lifecycle(self, plugin, context):
        """Test complete plugin lifecycle."""
        # Initialize
        assert plugin.initialize(context) is True
        assert plugin.status == PluginStatus.LOADED
        
        # Activate
        assert plugin.activate() is True
        assert plugin.status == PluginStatus.ACTIVE
        
        # Deactivate
        assert plugin.deactivate() is True
        assert plugin.status == PluginStatus.LOADED


# =============================================================================
# PLUGIN REGISTRY TESTS
# =============================================================================

class TestPluginRegistry:
    """Tests for plugin registry."""
    
    @pytest.fixture(autouse=True)
    def reset_registry(self):
        """Reset registry before each test."""
        registry = get_registry()
        registry._plugins.clear()
        registry._hooks.clear()
        yield
    
    @pytest.fixture
    def registry(self):
        """Get fresh registry."""
        return get_registry()
    
    @pytest.fixture
    def context(self):
        """Create test context."""
        return PluginContext(
            app=Mock(),
            config={},
            services={},
            user={"id": "user_123"}
        )
    
    def test_register_plugin(self, registry, context):
        """Test registering a plugin."""
        plugin = TestPlugin()
        plugin.initialize(context)
        
        registry.register(plugin)
        
        assert registry.get("test-plugin") == plugin
    
    def test_unregister_plugin(self, registry, context):
        """Test unregistering a plugin."""
        plugin = TestPlugin()
        plugin.initialize(context)
        
        registry.register(plugin)
        result = registry.unregister("test-plugin")
        
        assert result is True
        assert registry.get("test-plugin") is None
    
    def test_get_all_plugins(self, registry, context):
        """Test getting all plugins."""
        plugin1 = TestPlugin("plugin-1")
        plugin2 = TestPlugin("plugin-2")
        
        plugin1.initialize(context)
        plugin2.initialize(context)
        
        registry.register(plugin1)
        registry.register(plugin2)
        
        all_plugins = registry.get_all()
        
        assert len(all_plugins) == 2
    
    def test_get_active_plugins(self, registry, context):
        """Test getting active plugins only."""
        plugin1 = TestPlugin("plugin-1")
        plugin2 = TestPlugin("plugin-2")
        
        plugin1.initialize(context)
        plugin2.initialize(context)
        
        plugin1.activate()
        # plugin2 not activated
        
        registry.register(plugin1)
        registry.register(plugin2)
        
        active = registry.get_active()
        
        assert len(active) == 1
        assert active[0].metadata.name == "plugin-1"


# =============================================================================
# HOOK SYSTEM TESTS
# =============================================================================

class TestHookSystem:
    """Tests for the hook system."""
    
    @pytest.fixture(autouse=True)
    def reset_registry(self):
        """Reset registry before each test."""
        registry = get_registry()
        registry._plugins.clear()
        registry._hooks.clear()
        yield
    
    @pytest.fixture
    def registry(self):
        """Get fresh registry."""
        return get_registry()
    
    @pytest.fixture
    def context(self):
        """Create test context."""
        return PluginContext(
            app=Mock(),
            config={},
            services={},
            user={"id": "user_123"}
        )
    
    def test_hook_firing(self, registry, context):
        """Test that hooks are fired correctly."""
        plugin = TestPlugin()
        plugin.initialize(context)
        plugin.activate()
        
        registry.register(plugin)
        registry.fire_hook(HookEvents.USER_LOGIN, user_id="user_123")
        
        assert len(plugin.hook_calls) == 1
        assert plugin.hook_calls[0][0] == "user_login"
        assert plugin.hook_calls[0][1] == "user_123"
    
    def test_hook_with_kwargs(self, registry, context):
        """Test hooks receive kwargs."""
        plugin = TestPlugin()
        plugin.initialize(context)
        plugin.activate()
        
        registry.register(plugin)
        registry.fire_hook(
            HookEvents.USER_LOGIN,
            user_id="user_123",
            extra_param="test"
        )
        
        assert plugin.hook_calls[0][2].get("extra_param") == "test"
    
    def test_hook_priority_ordering(self, registry, context):
        """Test hooks are called in priority order."""
        high_plugin = HighPriorityPlugin()
        low_plugin = LowPriorityPlugin()
        
        high_plugin.initialize(context)
        low_plugin.initialize(context)
        
        high_plugin.activate()
        low_plugin.activate()
        
        # Register in reverse order to test sorting
        registry.register(low_plugin)
        registry.register(high_plugin)
        
        # Share hook order list
        shared_order = []
        high_plugin.hook_order = shared_order
        low_plugin.hook_order = shared_order
        
        registry.fire_hook(HookEvents.USER_LOGIN, user_id="user_123")
        
        # High priority should be called first
        assert shared_order == ["high", "low"]
    
    def test_inactive_plugin_hooks_not_fired(self, registry, context):
        """Test that inactive plugin hooks are not fired."""
        plugin = TestPlugin()
        plugin.initialize(context)
        # Not activated!
        
        registry.register(plugin)
        registry.fire_hook(HookEvents.USER_LOGIN, user_id="user_123")
        
        assert len(plugin.hook_calls) == 0


# =============================================================================
# PLUGIN LOADER TESTS
# =============================================================================

class TestPluginLoader:
    """Tests for plugin loader."""
    
    @pytest.fixture
    def context(self):
        """Create test context."""
        return PluginContext(
            app=Mock(),
            config={},
            services={},
            user={"id": "user_123"}
        )
    
    def test_loader_initialization(self):
        """Test loader initialization."""
        loader = PluginLoader("/path/to/plugins")
        
        assert loader.plugin_dir == "/path/to/plugins"
        assert len(loader._loaded_plugins) == 0
    
    @patch("os.path.exists")
    @patch("os.listdir")
    def test_discover_plugins(self, mock_listdir, mock_exists):
        """Test plugin discovery."""
        mock_exists.return_value = True
        mock_listdir.return_value = ["plugin1", "plugin2", "__pycache__"]
        
        loader = PluginLoader("/path/to/plugins")
        discovered = loader.discover()
        
        # Should exclude __pycache__
        assert "plugin1" in discovered
        assert "plugin2" in discovered
        assert "__pycache__" not in discovered


# =============================================================================
# GAMIFICATION PLUGIN INTEGRATION TESTS
# =============================================================================

class TestGamificationPluginIntegration:
    """Integration tests for gamification plugin."""
    
    @pytest.fixture
    def context(self):
        """Create test context."""
        return PluginContext(
            app=Mock(),
            config={},
            services={},
            user={"id": "user_123", "role": "user"}
        )
    
    def test_gamification_plugin_loads(self, context):
        """Test that gamification plugin can be loaded."""
        try:
            from plugins.available.gamification.plugin import GamificationPlugin
            
            plugin = GamificationPlugin()
            assert plugin.initialize(context) is True
            assert plugin.activate() is True
            
        except ImportError:
            pytest.skip("Gamification plugin not available")
    
    def test_gamification_badge_system(self, context):
        """Test badge awarding system."""
        try:
            from plugins.available.gamification.plugin import GamificationPlugin
            
            plugin = GamificationPlugin()
            plugin.initialize(context)
            plugin.activate()
            
            # Check badges are loaded
            badges = plugin.get_all_badges()
            assert len(badges) > 0
            
        except ImportError:
            pytest.skip("Gamification plugin not available")


# =============================================================================
# ANALYTICS PLUGIN INTEGRATION TESTS
# =============================================================================

class TestAnalyticsPluginIntegration:
    """Integration tests for analytics plugin."""
    
    @pytest.fixture
    def context(self):
        """Create test context."""
        return PluginContext(
            app=Mock(),
            config={},
            services={},
            user={"id": "user_123", "role": "user"}
        )
    
    def test_analytics_plugin_loads(self, context):
        """Test that analytics plugin can be loaded."""
        try:
            from plugins.available.analytics.plugin import AnalyticsPlugin
            
            plugin = AnalyticsPlugin()
            assert plugin.initialize(context) is True
            assert plugin.activate() is True
            
        except ImportError:
            pytest.skip("Analytics plugin not available")
    
    def test_analytics_tracking(self, context):
        """Test event tracking."""
        try:
            from plugins.available.analytics.plugin import (
                AnalyticsPlugin,
                EventType
            )
            
            plugin = AnalyticsPlugin()
            plugin.initialize(context)
            plugin.activate()
            
            # Track an event
            plugin.analytics.track(
                EventType.PAGE_VIEW,
                user_id="user_123",
                properties={"page": "home"}
            )
            
            # Check event was tracked
            summary = plugin.analytics.get_summary()
            assert summary["total_events"] >= 1
            
        except ImportError:
            pytest.skip("Analytics plugin not available")
    
    def test_analytics_dashboard_data(self, context):
        """Test dashboard data generation."""
        try:
            from plugins.available.analytics.plugin import AnalyticsPlugin
            
            plugin = AnalyticsPlugin()
            plugin.initialize(context)
            plugin.activate()
            
            data = plugin.get_dashboard_data()
            
            assert "total_events" in data
            assert "total_users" in data
            assert "today" in data
            
        except ImportError:
            pytest.skip("Analytics plugin not available")
