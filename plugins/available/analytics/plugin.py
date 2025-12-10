"""
LABBAIK AI v6.0 - Analytics Plugin
==================================
User analytics and behavior tracking plugin.
"""

from __future__ import annotations
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum

from plugins.base import (
    BasePlugin,
    PluginMetadata,
    PluginStatus,
    PluginPriority,
    PluginHook,
    HookEvents,
    PluginContext,
)

logger = logging.getLogger(__name__)


# =============================================================================
# ANALYTICS DATA MODELS
# =============================================================================

class EventType(str, Enum):
    """Analytics event types."""
    PAGE_VIEW = "page_view"
    CHAT_START = "chat_start"
    CHAT_MESSAGE = "chat_message"
    COST_SIMULATION = "cost_simulation"
    BOOKING_START = "booking_start"
    BOOKING_COMPLETE = "booking_complete"
    USER_LOGIN = "user_login"
    USER_REGISTER = "user_register"
    FEATURE_USE = "feature_use"
    ERROR = "error"


@dataclass
class AnalyticsEvent:
    """Single analytics event."""
    event_type: EventType
    user_id: Optional[str]
    session_id: str
    timestamp: datetime
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type.value,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat(),
            "properties": self.properties,
        }


@dataclass
class UserAnalytics:
    """User analytics summary."""
    user_id: str
    total_sessions: int = 0
    total_page_views: int = 0
    total_chats: int = 0
    total_simulations: int = 0
    total_bookings: int = 0
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    avg_session_duration: float = 0  # in minutes
    favorite_features: List[str] = field(default_factory=list)


@dataclass
class DailyStats:
    """Daily statistics."""
    date: str
    active_users: int = 0
    new_users: int = 0
    page_views: int = 0
    chat_messages: int = 0
    simulations: int = 0
    bookings: int = 0
    errors: int = 0


# =============================================================================
# ANALYTICS SERVICE
# =============================================================================

class AnalyticsService:
    """In-memory analytics service."""
    
    def __init__(self):
        self._events: List[AnalyticsEvent] = []
        self._user_stats: Dict[str, UserAnalytics] = {}
        self._daily_stats: Dict[str, DailyStats] = {}
        self._session_starts: Dict[str, datetime] = {}
    
    def track(
        self,
        event_type: EventType,
        user_id: str = None,
        session_id: str = "anonymous",
        properties: Dict[str, Any] = None
    ) -> AnalyticsEvent:
        """
        Track an analytics event.
        
        Args:
            event_type: Type of event
            user_id: User ID (optional)
            session_id: Session ID
            properties: Additional event properties
        
        Returns:
            Created event
        """
        event = AnalyticsEvent(
            event_type=event_type,
            user_id=user_id,
            session_id=session_id,
            timestamp=datetime.utcnow(),
            properties=properties or {}
        )
        
        self._events.append(event)
        self._update_stats(event)
        
        logger.debug(f"Tracked event: {event_type.value} for user {user_id}")
        return event
    
    def _update_stats(self, event: AnalyticsEvent):
        """Update statistics based on event."""
        # Update daily stats
        today = event.timestamp.strftime("%Y-%m-%d")
        if today not in self._daily_stats:
            self._daily_stats[today] = DailyStats(date=today)
        
        daily = self._daily_stats[today]
        
        if event.event_type == EventType.PAGE_VIEW:
            daily.page_views += 1
        elif event.event_type == EventType.CHAT_MESSAGE:
            daily.chat_messages += 1
        elif event.event_type == EventType.COST_SIMULATION:
            daily.simulations += 1
        elif event.event_type == EventType.BOOKING_COMPLETE:
            daily.bookings += 1
        elif event.event_type == EventType.ERROR:
            daily.errors += 1
        
        # Update user stats
        if event.user_id:
            if event.user_id not in self._user_stats:
                self._user_stats[event.user_id] = UserAnalytics(
                    user_id=event.user_id,
                    first_seen=event.timestamp
                )
                daily.new_users += 1
            
            user = self._user_stats[event.user_id]
            user.last_seen = event.timestamp
            
            if event.event_type == EventType.PAGE_VIEW:
                user.total_page_views += 1
            elif event.event_type == EventType.CHAT_MESSAGE:
                user.total_chats += 1
            elif event.event_type == EventType.COST_SIMULATION:
                user.total_simulations += 1
            elif event.event_type == EventType.BOOKING_COMPLETE:
                user.total_bookings += 1
    
    def get_user_analytics(self, user_id: str) -> Optional[UserAnalytics]:
        """Get analytics for a specific user."""
        return self._user_stats.get(user_id)
    
    def get_daily_stats(self, date: str = None) -> Optional[DailyStats]:
        """Get stats for a specific day."""
        if date is None:
            date = datetime.utcnow().strftime("%Y-%m-%d")
        return self._daily_stats.get(date)
    
    def get_stats_range(
        self,
        start_date: datetime,
        end_date: datetime = None
    ) -> List[DailyStats]:
        """Get stats for a date range."""
        if end_date is None:
            end_date = datetime.utcnow()
        
        result = []
        current = start_date
        
        while current <= end_date:
            date_str = current.strftime("%Y-%m-%d")
            if date_str in self._daily_stats:
                result.append(self._daily_stats[date_str])
            current += timedelta(days=1)
        
        return result
    
    def get_top_users(self, limit: int = 10) -> List[UserAnalytics]:
        """Get most active users."""
        users = list(self._user_stats.values())
        users.sort(key=lambda u: u.total_page_views + u.total_chats, reverse=True)
        return users[:limit]
    
    def get_feature_usage(self) -> Dict[str, int]:
        """Get feature usage statistics."""
        usage = defaultdict(int)
        
        for event in self._events:
            if event.event_type == EventType.FEATURE_USE:
                feature = event.properties.get("feature", "unknown")
                usage[feature] += 1
        
        return dict(usage)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get overall analytics summary."""
        total_events = len(self._events)
        total_users = len(self._user_stats)
        
        today = datetime.utcnow().strftime("%Y-%m-%d")
        today_stats = self.get_daily_stats(today) or DailyStats(date=today)
        
        # Calculate 7-day stats
        week_ago = datetime.utcnow() - timedelta(days=7)
        week_stats = self.get_stats_range(week_ago)
        
        week_page_views = sum(s.page_views for s in week_stats)
        week_chats = sum(s.chat_messages for s in week_stats)
        week_simulations = sum(s.simulations for s in week_stats)
        
        return {
            "total_events": total_events,
            "total_users": total_users,
            "today": {
                "page_views": today_stats.page_views,
                "chat_messages": today_stats.chat_messages,
                "simulations": today_stats.simulations,
                "bookings": today_stats.bookings,
                "new_users": today_stats.new_users,
            },
            "last_7_days": {
                "page_views": week_page_views,
                "chat_messages": week_chats,
                "simulations": week_simulations,
            }
        }


# =============================================================================
# ANALYTICS PLUGIN
# =============================================================================

class AnalyticsPlugin(BasePlugin):
    """
    Analytics and user behavior tracking plugin.
    
    Features:
    - Page view tracking
    - Chat analytics
    - Conversion tracking
    - User journey mapping
    - Admin dashboard widget
    """
    
    def __init__(self):
        metadata = PluginMetadata(
            name="analytics",
            version="1.0.0",
            description="User analytics and behavior tracking",
            author="LABBAIK AI Team",
            dependencies=[],
            config_schema={
                "track_anonymous": True,
                "retention_days": 90,
            }
        )
        super().__init__(metadata)
        
        self.analytics: Optional[AnalyticsService] = None
    
    def initialize(self, context: PluginContext) -> bool:
        """Initialize the analytics plugin."""
        try:
            self.context = context
            self.analytics = AnalyticsService()
            
            logger.info("Analytics plugin initialized")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize analytics plugin: {e}")
            return False
    
    def activate(self) -> bool:
        """Activate the analytics plugin."""
        self.status = PluginStatus.ACTIVE
        logger.info("Analytics plugin activated")
        return True
    
    def deactivate(self) -> bool:
        """Deactivate the analytics plugin."""
        self.status = PluginStatus.LOADED
        logger.info("Analytics plugin deactivated")
        return True
    
    # =========================================================================
    # HOOK HANDLERS
    # =========================================================================
    
    @PluginHook(HookEvents.USER_LOGIN, priority=PluginPriority.HIGH)
    def on_user_login(self, user_id: str, **kwargs):
        """Track user login."""
        if self.analytics:
            self.analytics.track(
                EventType.USER_LOGIN,
                user_id=user_id,
                properties={"method": kwargs.get("method", "email")}
            )
    
    @PluginHook(HookEvents.PAGE_RENDERED, priority=PluginPriority.NORMAL)
    def on_page_view(self, page: str, **kwargs):
        """Track page views."""
        if self.analytics:
            user_id = self.context.user.get("id") if self.context else None
            self.analytics.track(
                EventType.PAGE_VIEW,
                user_id=user_id,
                properties={"page": page}
            )
    
    @PluginHook(HookEvents.CHAT_MESSAGE_SENT, priority=PluginPriority.LOW)
    def on_chat_message(self, user_id: str, message: str, **kwargs):
        """Track chat messages."""
        if self.analytics:
            self.analytics.track(
                EventType.CHAT_MESSAGE,
                user_id=user_id,
                properties={
                    "message_length": len(message),
                    "is_first_message": kwargs.get("is_first", False)
                }
            )
    
    @PluginHook(HookEvents.COST_CALCULATED, priority=PluginPriority.LOW)
    def on_cost_simulation(self, user_id: str, result: Dict, **kwargs):
        """Track cost simulations."""
        if self.analytics:
            self.analytics.track(
                EventType.COST_SIMULATION,
                user_id=user_id,
                properties={
                    "total_per_person": result.get("total_per_person", 0),
                    "traveler_count": result.get("input", {}).get("traveler_count", 1),
                    "package_type": result.get("input", {}).get("package_type", "unknown"),
                }
            )
    
    @PluginHook(HookEvents.BOOKING_CREATED, priority=PluginPriority.LOW)
    def on_booking_created(self, user_id: str, booking_id: str, **kwargs):
        """Track booking creation."""
        if self.analytics:
            self.analytics.track(
                EventType.BOOKING_START,
                user_id=user_id,
                properties={"booking_id": booking_id}
            )
    
    @PluginHook(HookEvents.BOOKING_CONFIRMED, priority=PluginPriority.LOW)
    def on_booking_confirmed(self, user_id: str, booking_id: str, **kwargs):
        """Track booking completion."""
        if self.analytics:
            self.analytics.track(
                EventType.BOOKING_COMPLETE,
                user_id=user_id,
                properties={
                    "booking_id": booking_id,
                    "total_value": kwargs.get("total_value", 0)
                }
            )
    
    # =========================================================================
    # PUBLIC METHODS
    # =========================================================================
    
    def track_feature_use(self, user_id: str, feature: str):
        """Track feature usage."""
        if self.analytics:
            self.analytics.track(
                EventType.FEATURE_USE,
                user_id=user_id,
                properties={"feature": feature}
            )
    
    def track_error(self, user_id: str, error_type: str, error_message: str):
        """Track errors."""
        if self.analytics:
            self.analytics.track(
                EventType.ERROR,
                user_id=user_id,
                properties={
                    "error_type": error_type,
                    "error_message": error_message[:200]  # Truncate
                }
            )
    
    def get_user_analytics(self, user_id: str) -> Optional[Dict]:
        """Get user analytics as dict."""
        if self.analytics:
            user_stats = self.analytics.get_user_analytics(user_id)
            if user_stats:
                return {
                    "user_id": user_stats.user_id,
                    "total_sessions": user_stats.total_sessions,
                    "total_page_views": user_stats.total_page_views,
                    "total_chats": user_stats.total_chats,
                    "total_simulations": user_stats.total_simulations,
                    "total_bookings": user_stats.total_bookings,
                    "first_seen": user_stats.first_seen.isoformat() if user_stats.first_seen else None,
                    "last_seen": user_stats.last_seen.isoformat() if user_stats.last_seen else None,
                }
        return None
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data for admin dashboard."""
        if self.analytics:
            return self.analytics.get_summary()
        return {}
    
    # =========================================================================
    # UI RENDERING
    # =========================================================================
    
    def render_ui(self, location: str = "admin"):
        """Render analytics UI component."""
        import streamlit as st
        
        if location == "admin":
            self._render_admin_dashboard(st)
        elif location == "sidebar":
            self._render_sidebar_widget(st)
    
    def _render_admin_dashboard(self, st):
        """Render full admin analytics dashboard."""
        st.markdown("### 📊 Analytics Dashboard")
        
        if not self.analytics:
            st.warning("Analytics not initialized")
            return
        
        summary = self.analytics.get_summary()
        
        # Today's stats
        st.markdown("#### Today")
        col1, col2, col3, col4 = st.columns(4)
        
        today = summary.get("today", {})
        with col1:
            st.metric("Page Views", today.get("page_views", 0))
        with col2:
            st.metric("Chat Messages", today.get("chat_messages", 0))
        with col3:
            st.metric("Simulations", today.get("simulations", 0))
        with col4:
            st.metric("Bookings", today.get("bookings", 0))
        
        st.divider()
        
        # Last 7 days
        st.markdown("#### Last 7 Days")
        col1, col2, col3 = st.columns(3)
        
        week = summary.get("last_7_days", {})
        with col1:
            st.metric("Page Views", week.get("page_views", 0))
        with col2:
            st.metric("Chat Messages", week.get("chat_messages", 0))
        with col3:
            st.metric("Simulations", week.get("simulations", 0))
        
        st.divider()
        
        # Summary
        st.markdown("#### Overall")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Events", summary.get("total_events", 0))
        with col2:
            st.metric("Total Users", summary.get("total_users", 0))
        
        # Top users
        st.markdown("#### Top Users")
        top_users = self.analytics.get_top_users(5)
        
        if top_users:
            user_data = [
                {
                    "User ID": u.user_id[:8] + "...",
                    "Page Views": u.total_page_views,
                    "Chats": u.total_chats,
                    "Simulations": u.total_simulations,
                }
                for u in top_users
            ]
            st.dataframe(user_data, use_container_width=True)
        else:
            st.info("No user data yet")
    
    def _render_sidebar_widget(self, st):
        """Render compact sidebar analytics widget."""
        st.markdown("#### 📊 Quick Stats")
        
        if not self.analytics:
            return
        
        summary = self.analytics.get_summary()
        today = summary.get("today", {})
        
        st.caption(f"📄 Views: {today.get('page_views', 0)}")
        st.caption(f"💬 Chats: {today.get('chat_messages', 0)}")
        st.caption(f"👥 Users: {summary.get('total_users', 0)}")
