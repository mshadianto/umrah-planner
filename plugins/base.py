"""
LABBAIK AI v6.0 - Plugin System
==============================
Extensible plugin architecture for adding features without modifying core.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Type, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import importlib
import importlib.util
import logging
import inspect
import yaml

logger = logging.getLogger(__name__)


# =============================================================================
# PLUGIN ENUMS & DATA CLASSES
# =============================================================================

class PluginStatus(str, Enum):
    """Plugin lifecycle status."""
    UNLOADED = "unloaded"
    LOADING = "loading"
    LOADED = "loaded"
    ACTIVE = "active"
    ERROR = "error"
    DISABLED = "disabled"


class PluginPriority(int, Enum):
    """Plugin execution priority."""
    LOWEST = 0
    LOW = 25
    NORMAL = 50
    HIGH = 75
    HIGHEST = 100


@dataclass
class PluginMetadata:
    """Plugin metadata and configuration."""
    name: str
    version: str
    description: str
    author: str = "LABBAIK Team"
    dependencies: List[str] = field(default_factory=list)
    priority: PluginPriority = PluginPriority.NORMAL
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PluginMetadata":
        """Create metadata from dictionary."""
        return cls(
            name=data.get("name", "unknown"),
            version=data.get("version", "0.0.0"),
            description=data.get("description", ""),
            author=data.get("author", "LABBAIK Team"),
            dependencies=data.get("dependencies", []),
            priority=PluginPriority(data.get("priority", 50)),
            enabled=data.get("enabled", True),
            config=data.get("config", {})
        )
    
    @classmethod
    def from_yaml(cls, path: Path) -> "PluginMetadata":
        """Load metadata from YAML file."""
        if not path.exists():
            raise FileNotFoundError(f"Plugin config not found: {path}")
        
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        return cls.from_dict(data)


@dataclass
class PluginContext:
    """Context passed to plugins during lifecycle events."""
    app: Any  # Streamlit app reference
    config: Dict[str, Any]
    services: Dict[str, Any]
    user: Optional[Dict[str, Any]] = None
    
    def get_service(self, name: str) -> Any:
        """Get a service by name."""
        return self.services.get(name)


# =============================================================================
# BASE PLUGIN CLASS
# =============================================================================

class BasePlugin(ABC):
    """
    Abstract base class for all plugins.
    Plugins must implement this interface.
    """
    
    def __init__(self, metadata: PluginMetadata):
        self.metadata = metadata
        self.status = PluginStatus.UNLOADED
        self._hooks: Dict[str, List[Callable]] = {}
        self._context: Optional[PluginContext] = None
    
    @property
    def name(self) -> str:
        """Plugin name."""
        return self.metadata.name
    
    @property
    def version(self) -> str:
        """Plugin version."""
        return self.metadata.version
    
    @property
    def is_active(self) -> bool:
        """Check if plugin is active."""
        return self.status == PluginStatus.ACTIVE
    
    @abstractmethod
    def initialize(self, context: PluginContext) -> bool:
        """
        Initialize the plugin.
        Called when plugin is loaded.
        
        Args:
            context: Plugin context with app and services
        
        Returns:
            True if initialization successful
        """
        pass
    
    @abstractmethod
    def activate(self) -> bool:
        """
        Activate the plugin.
        Called when plugin should start running.
        
        Returns:
            True if activation successful
        """
        pass
    
    @abstractmethod
    def deactivate(self) -> bool:
        """
        Deactivate the plugin.
        Called when plugin should stop running.
        
        Returns:
            True if deactivation successful
        """
        pass
    
    def shutdown(self) -> bool:
        """
        Shutdown the plugin.
        Called when plugin is unloaded.
        
        Returns:
            True if shutdown successful
        """
        self.status = PluginStatus.UNLOADED
        return True
    
    def register_hook(self, event: str, callback: Callable):
        """
        Register a callback for an event hook.
        
        Args:
            event: Event name (e.g., 'on_chat_message', 'on_user_login')
            callback: Function to call when event fires
        """
        if event not in self._hooks:
            self._hooks[event] = []
        self._hooks[event].append(callback)
    
    def get_hooks(self, event: str) -> List[Callable]:
        """Get all registered hooks for an event."""
        return self._hooks.get(event, [])
    
    def render_ui(self) -> None:
        """
        Render plugin UI components.
        Override in plugins that add UI elements.
        """
        pass
    
    def get_api_routes(self) -> List[Dict[str, Any]]:
        """
        Get API routes provided by this plugin.
        Override in plugins that add API endpoints.
        
        Returns:
            List of route definitions
        """
        return []
    
    def get_config_schema(self) -> Dict[str, Any]:
        """
        Get JSON schema for plugin configuration.
        Override to define configurable options.
        
        Returns:
            JSON schema dictionary
        """
        return {}


# =============================================================================
# PLUGIN HOOKS
# =============================================================================

class PluginHook:
    """Decorator for marking plugin hook methods."""
    
    def __init__(self, event: str, priority: int = PluginPriority.NORMAL):
        self.event = event
        self.priority = priority
    
    def __call__(self, func: Callable) -> Callable:
        func._plugin_hook = {
            "event": self.event,
            "priority": self.priority
        }
        return func


# Standard hook events
class HookEvents:
    """Standard plugin hook event names."""
    # Application lifecycle
    APP_STARTUP = "app_startup"
    APP_SHUTDOWN = "app_shutdown"
    
    # User events
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_REGISTER = "user_register"
    
    # Chat events
    CHAT_MESSAGE_SENT = "chat_message_sent"
    CHAT_MESSAGE_RECEIVED = "chat_message_received"
    CHAT_STREAM_START = "chat_stream_start"
    CHAT_STREAM_END = "chat_stream_end"
    
    # Booking events
    BOOKING_CREATED = "booking_created"
    BOOKING_UPDATED = "booking_updated"
    BOOKING_CANCELLED = "booking_cancelled"
    
    # Cost simulation
    COST_CALCULATED = "cost_calculated"
    
    # UI events
    PAGE_RENDERED = "page_rendered"
    SIDEBAR_RENDERED = "sidebar_rendered"


# =============================================================================
# PLUGIN REGISTRY
# =============================================================================

class PluginRegistry:
    """
    Central registry for managing plugins.
    Handles plugin discovery, loading, and lifecycle.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._plugins: Dict[str, BasePlugin] = {}
            cls._instance._hooks: Dict[str, List[tuple]] = {}  # (priority, plugin, callback)
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> "PluginRegistry":
        """Get singleton instance."""
        return cls()
    
    def register(self, plugin: BasePlugin) -> bool:
        """
        Register a plugin with the registry.
        
        Args:
            plugin: Plugin instance to register
        
        Returns:
            True if registration successful
        """
        if plugin.name in self._plugins:
            logger.warning(f"Plugin already registered: {plugin.name}")
            return False
        
        self._plugins[plugin.name] = plugin
        logger.info(f"Registered plugin: {plugin.name} v{plugin.version}")
        
        # Register hooks
        self._register_plugin_hooks(plugin)
        
        return True
    
    def unregister(self, plugin_name: str) -> bool:
        """
        Unregister a plugin from the registry.
        
        Args:
            plugin_name: Name of plugin to unregister
        
        Returns:
            True if unregistration successful
        """
        if plugin_name not in self._plugins:
            return False
        
        plugin = self._plugins[plugin_name]
        
        # Deactivate and shutdown
        if plugin.is_active:
            plugin.deactivate()
        plugin.shutdown()
        
        # Remove hooks
        self._unregister_plugin_hooks(plugin)
        
        del self._plugins[plugin_name]
        logger.info(f"Unregistered plugin: {plugin_name}")
        
        return True
    
    def get(self, plugin_name: str) -> Optional[BasePlugin]:
        """Get a registered plugin by name."""
        return self._plugins.get(plugin_name)
    
    def get_all(self) -> List[BasePlugin]:
        """Get all registered plugins."""
        return list(self._plugins.values())
    
    def get_active(self) -> List[BasePlugin]:
        """Get all active plugins."""
        return [p for p in self._plugins.values() if p.is_active]
    
    def _register_plugin_hooks(self, plugin: BasePlugin):
        """Register all hooks from a plugin."""
        # Check for hook decorators
        for name, method in inspect.getmembers(plugin, predicate=inspect.ismethod):
            if hasattr(method, "_plugin_hook"):
                hook_info = method._plugin_hook
                event = hook_info["event"]
                priority = hook_info["priority"]
                
                if event not in self._hooks:
                    self._hooks[event] = []
                
                self._hooks[event].append((priority, plugin, method))
                self._hooks[event].sort(key=lambda x: x[0], reverse=True)
        
        # Also check plugin's registered hooks
        for event, callbacks in plugin._hooks.items():
            if event not in self._hooks:
                self._hooks[event] = []
            for callback in callbacks:
                self._hooks[event].append((plugin.metadata.priority, plugin, callback))
            self._hooks[event].sort(key=lambda x: x[0], reverse=True)
    
    def _unregister_plugin_hooks(self, plugin: BasePlugin):
        """Unregister all hooks from a plugin."""
        for event in list(self._hooks.keys()):
            self._hooks[event] = [
                (p, pl, cb) for p, pl, cb in self._hooks[event]
                if pl != plugin
            ]
    
    def fire_hook(self, event: str, **kwargs) -> List[Any]:
        """
        Fire a hook event and collect results.
        
        Args:
            event: Event name to fire
            **kwargs: Arguments to pass to hook callbacks
        
        Returns:
            List of results from hook callbacks
        """
        results = []
        
        if event not in self._hooks:
            return results
        
        for priority, plugin, callback in self._hooks[event]:
            if not plugin.is_active:
                continue
            
            try:
                result = callback(**kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Hook error in {plugin.name}.{callback.__name__}: {e}")
        
        return results
    
    async def fire_hook_async(self, event: str, **kwargs) -> List[Any]:
        """Async version of fire_hook."""
        import asyncio
        
        results = []
        
        if event not in self._hooks:
            return results
        
        for priority, plugin, callback in self._hooks[event]:
            if not plugin.is_active:
                continue
            
            try:
                if asyncio.iscoroutinefunction(callback):
                    result = await callback(**kwargs)
                else:
                    result = callback(**kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Async hook error in {plugin.name}.{callback.__name__}: {e}")
        
        return results


# =============================================================================
# PLUGIN LOADER
# =============================================================================

class PluginLoader:
    """
    Utility for loading plugins from various sources.
    """
    
    def __init__(self, plugin_dir: str = "plugins/available"):
        self.plugin_dir = Path(plugin_dir)
        self.registry = PluginRegistry.get_instance()
    
    def discover(self) -> List[PluginMetadata]:
        """
        Discover available plugins in the plugin directory.
        
        Returns:
            List of plugin metadata for discovered plugins
        """
        discovered = []
        
        if not self.plugin_dir.exists():
            logger.warning(f"Plugin directory not found: {self.plugin_dir}")
            return discovered
        
        for path in self.plugin_dir.iterdir():
            if not path.is_dir():
                continue
            
            # Look for plugin.py and config.yaml
            plugin_file = path / "plugin.py"
            config_file = path / "config.yaml"
            
            if not plugin_file.exists():
                continue
            
            try:
                if config_file.exists():
                    metadata = PluginMetadata.from_yaml(config_file)
                else:
                    # Create default metadata from directory name
                    metadata = PluginMetadata(
                        name=path.name,
                        version="0.0.0",
                        description=f"Plugin: {path.name}"
                    )
                
                discovered.append(metadata)
                logger.debug(f"Discovered plugin: {metadata.name}")
                
            except Exception as e:
                logger.error(f"Error discovering plugin in {path}: {e}")
        
        return discovered
    
    def load(self, plugin_name: str, context: PluginContext) -> Optional[BasePlugin]:
        """
        Load a plugin by name.
        
        Args:
            plugin_name: Name of plugin to load
            context: Plugin context to pass during initialization
        
        Returns:
            Loaded plugin instance or None if failed
        """
        plugin_path = self.plugin_dir / plugin_name / "plugin.py"
        config_path = self.plugin_dir / plugin_name / "config.yaml"
        
        if not plugin_path.exists():
            logger.error(f"Plugin not found: {plugin_name}")
            return None
        
        try:
            # Load metadata
            if config_path.exists():
                metadata = PluginMetadata.from_yaml(config_path)
            else:
                metadata = PluginMetadata(
                    name=plugin_name,
                    version="0.0.0",
                    description=f"Plugin: {plugin_name}"
                )
            
            # Check if enabled
            if not metadata.enabled:
                logger.info(f"Plugin disabled: {plugin_name}")
                return None
            
            # Import plugin module
            spec = importlib.util.spec_from_file_location(
                f"plugins.{plugin_name}",
                plugin_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find plugin class
            plugin_class = None
            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj) and
                    issubclass(obj, BasePlugin) and
                    obj != BasePlugin
                ):
                    plugin_class = obj
                    break
            
            if not plugin_class:
                logger.error(f"No plugin class found in {plugin_name}")
                return None
            
            # Create instance
            plugin = plugin_class(metadata)
            plugin.status = PluginStatus.LOADING
            
            # Initialize
            if plugin.initialize(context):
                plugin.status = PluginStatus.LOADED
                self.registry.register(plugin)
                logger.info(f"Loaded plugin: {plugin_name}")
                return plugin
            else:
                plugin.status = PluginStatus.ERROR
                logger.error(f"Failed to initialize plugin: {plugin_name}")
                return None
            
        except Exception as e:
            logger.error(f"Error loading plugin {plugin_name}: {e}")
            return None
    
    def load_all(self, context: PluginContext) -> List[BasePlugin]:
        """
        Load all discovered plugins.
        
        Args:
            context: Plugin context to pass during initialization
        
        Returns:
            List of successfully loaded plugins
        """
        loaded = []
        
        for metadata in self.discover():
            if metadata.enabled:
                plugin = self.load(metadata.name, context)
                if plugin:
                    loaded.append(plugin)
        
        return loaded
    
    def activate_all(self) -> int:
        """
        Activate all loaded plugins.
        
        Returns:
            Number of successfully activated plugins
        """
        activated = 0
        
        for plugin in self.registry.get_all():
            if plugin.status == PluginStatus.LOADED:
                try:
                    if plugin.activate():
                        plugin.status = PluginStatus.ACTIVE
                        activated += 1
                        logger.info(f"Activated plugin: {plugin.name}")
                except Exception as e:
                    plugin.status = PluginStatus.ERROR
                    logger.error(f"Failed to activate plugin {plugin.name}: {e}")
        
        return activated


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def get_registry() -> PluginRegistry:
    """Get the plugin registry singleton."""
    return PluginRegistry.get_instance()


def fire_hook(event: str, **kwargs) -> List[Any]:
    """Fire a plugin hook event."""
    return get_registry().fire_hook(event, **kwargs)


async def fire_hook_async(event: str, **kwargs) -> List[Any]:
    """Fire a plugin hook event asynchronously."""
    return await get_registry().fire_hook_async(event, **kwargs)
