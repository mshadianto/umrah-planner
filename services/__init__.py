"""
LABBAIK AI v6.0 - Services Package
=================================
Business logic services.
"""

from services.ai.chat_service import (
    GroqChatService,
    OpenAIChatService,
    UnifiedChatService,
)
from services.ai.rag_service import (
    RAGService,
    LocalEmbeddingService,
    ChromaVectorStore,
)
from services.ai.base import (
    ChatMessage,
    ChatCompletionRequest,
    ChatCompletionResponse,
    AIServiceFactory,
)

# Database services
from services.database.repository import (
    DatabaseConnection,
    get_db,
    BaseRepository,
    UserRepository,
    ChatRepository,
    BookingRepository,
)

# Cost services
from services.cost.calculator import (
    calculate_umrah_cost,
    compare_packages,
    compare_seasons,
    get_season_type,
)

# Auth services - may not exist yet
try:
    from services.auth.auth_service import (
        AuthService,
        get_auth_service,
        PasswordService,
        TokenService,
        AuthResult,
    )
except ImportError:
    AuthService = None
    get_auth_service = None

# Notification services
try:
    from services.notification.notification_service import (
        NotificationService as NotifService,
        get_notification_service,
        EmailSender,
        NotificationMessage,
        NotificationResult,
    )
except ImportError:
    NotifService = None
    get_notification_service = None

# Data services (new centralized layer)
try:
    from services.data_service import (
        Database,
        DataStore,
        UserService,
        TripService,
        BookingService,
        ChatService,
        SimulationService,
        NotificationService,
        AnalyticsService,
        init_database,
        db,
        store,
    )
except ImportError:
    Database = None
    DataStore = None
    UserService = None
    TripService = None
    BookingService = None
    ChatService = None
    SimulationService = None
    NotificationService = None
    AnalyticsService = None
    init_database = None
    db = None
    store = None

# State manager
try:
    from services.state_manager import (
        StateManager,
        StateKeys,
        state_manager,
        init_state,
    )
except ImportError:
    StateManager = None
    StateKeys = None
    state_manager = None
    init_state = None

__all__ = [
    # AI Services
    "GroqChatService",
    "OpenAIChatService",
    "UnifiedChatService",
    "RAGService",
    "LocalEmbeddingService",
    "ChromaVectorStore",
    "ChatMessage",
    "ChatCompletionRequest",
    "ChatCompletionResponse",
    "AIServiceFactory",
    
    # Database
    "DatabaseConnection",
    "get_db",
    "BaseRepository",
    "UserRepository",
    "ChatRepository",
    "BookingRepository",
    
    # Cost
    "calculate_umrah_cost",
    "compare_packages",
    "compare_seasons",
    "get_season_type",
    
    # Auth
    "AuthService",
    "get_auth_service",
    "PasswordService",
    "TokenService",
    "AuthResult",
    
    # Notification (old)
    "NotifService",
    "get_notification_service",
    "EmailSender",
    "NotificationMessage",
    "NotificationResult",
    
    # Data services (new)
    "Database",
    "DataStore",
    "UserService",
    "TripService",
    "BookingService",
    "ChatService",
    "SimulationService",
    "NotificationService",
    "AnalyticsService",
    "init_database",
    "db",
    "store",
    
    # State manager
    "StateManager",
    "StateKeys",
    "state_manager",
    "init_state",
]
