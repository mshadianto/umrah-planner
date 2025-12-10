"""
LABBAIK AI v6.0 - Gamification Plugin
=====================================
Plugin untuk menambahkan fitur gamifikasi (badges, points, levels).
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

from plugins.base import (
    BasePlugin,
    PluginMetadata,
    PluginContext,
    PluginHook,
    HookEvents,
    PluginStatus,
)

logger = logging.getLogger(__name__)


# =============================================================================
# GAMIFICATION DATA CLASSES
# =============================================================================

class BadgeCategory(str, Enum):
    """Badge categories."""
    LEARNING = "learning"
    PLANNING = "planning"
    ENGAGEMENT = "engagement"
    SOCIAL = "social"
    ACHIEVEMENT = "achievement"


@dataclass
class Badge:
    """Represents a badge that can be earned."""
    id: str
    name: str
    name_ar: str  # Arabic name
    description: str
    icon: str
    category: BadgeCategory
    points: int
    requirements: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "name_ar": self.name_ar,
            "description": self.description,
            "icon": self.icon,
            "category": self.category.value,
            "points": self.points,
        }


@dataclass
class UserBadge:
    """Badge earned by a user."""
    badge_id: str
    earned_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserProgress:
    """User's gamification progress."""
    user_id: str
    total_points: int = 0
    level: int = 1
    badges: List[UserBadge] = field(default_factory=list)
    stats: Dict[str, int] = field(default_factory=dict)
    
    def add_badge(self, badge_id: str) -> UserBadge:
        """Add a badge to user's collection."""
        user_badge = UserBadge(
            badge_id=badge_id,
            earned_at=datetime.utcnow()
        )
        self.badges.append(user_badge)
        return user_badge
    
    def has_badge(self, badge_id: str) -> bool:
        """Check if user has a badge."""
        return any(b.badge_id == badge_id for b in self.badges)
    
    def add_points(self, points: int):
        """Add points and update level."""
        self.total_points += points
        self.level = self._calculate_level()
    
    def _calculate_level(self) -> int:
        """Calculate level based on points."""
        # Simple level calculation: 100 points per level
        return max(1, (self.total_points // 100) + 1)
    
    def increment_stat(self, stat_name: str, amount: int = 1):
        """Increment a stat counter."""
        self.stats[stat_name] = self.stats.get(stat_name, 0) + amount


# =============================================================================
# BADGE DEFINITIONS
# =============================================================================

BADGES = [
    Badge(
        id="newcomer",
        name="Jamaah Baru",
        name_ar="حاج جديد",
        description="Selamat datang di LABBAIK AI! Badge pertama Anda.",
        icon="🌟",
        category=BadgeCategory.ACHIEVEMENT,
        points=10,
        requirements={"action": "first_visit"}
    ),
    Badge(
        id="curious_learner",
        name="Pencari Ilmu",
        name_ar="طالب العلم",
        description="Mengajukan 10 pertanyaan tentang Umrah.",
        icon="📚",
        category=BadgeCategory.LEARNING,
        points=25,
        requirements={"questions_asked": 10}
    ),
    Badge(
        id="planner",
        name="Perencana Handal",
        name_ar="المخطط الماهر",
        description="Menyelesaikan simulasi biaya pertama.",
        icon="🧮",
        category=BadgeCategory.PLANNING,
        points=20,
        requirements={"simulations_completed": 1}
    ),
    Badge(
        id="expert_planner",
        name="Ahli Perencanaan",
        name_ar="خبير التخطيط",
        description="Menyelesaikan 10 simulasi biaya.",
        icon="🏆",
        category=BadgeCategory.PLANNING,
        points=50,
        requirements={"simulations_completed": 10}
    ),
    Badge(
        id="community_member",
        name="Anggota Komunitas",
        name_ar="عضو المجتمع",
        description="Bergabung dengan fitur Umrah Bareng.",
        icon="👥",
        category=BadgeCategory.SOCIAL,
        points=30,
        requirements={"action": "join_umrah_bareng"}
    ),
    Badge(
        id="knowledge_seeker",
        name="Penuntut Ilmu",
        name_ar="طالب المعرفة",
        description="Membaca semua panduan Umrah Mandiri.",
        icon="📖",
        category=BadgeCategory.LEARNING,
        points=40,
        requirements={"guides_completed": "all"}
    ),
    Badge(
        id="daily_visitor",
        name="Pengunjung Setia",
        name_ar="الزائر المخلص",
        description="Mengunjungi LABBAIK AI 7 hari berturut-turut.",
        icon="🔥",
        category=BadgeCategory.ENGAGEMENT,
        points=35,
        requirements={"consecutive_days": 7}
    ),
    Badge(
        id="arabic_learner",
        name="Murid Bahasa Arab",
        name_ar="دارس اللغة العربية",
        description="Mempelajari 20 frasa bahasa Arab.",
        icon="🗣️",
        category=BadgeCategory.LEARNING,
        points=30,
        requirements={"arabic_phrases_learned": 20}
    ),
]


# =============================================================================
# GAMIFICATION PLUGIN
# =============================================================================

class GamificationPlugin(BasePlugin):
    """
    Plugin untuk sistem gamifikasi.
    Menambahkan badges, points, dan levels untuk meningkatkan engagement.
    """
    
    def __init__(self, metadata: PluginMetadata = None):
        if metadata is None:
            metadata = PluginMetadata(
                name="gamification",
                version="1.0.0",
                description="Sistem gamifikasi dengan badges dan points",
                author="LABBAIK Team"
            )
        super().__init__(metadata)
        
        self._badges: Dict[str, Badge] = {b.id: b for b in BADGES}
        self._user_progress: Dict[str, UserProgress] = {}
        self._context: Optional[PluginContext] = None
    
    def initialize(self, context: PluginContext) -> bool:
        """Initialize gamification plugin."""
        self._context = context
        
        # Register hooks
        self.register_hook(HookEvents.USER_LOGIN, self._on_user_login)
        self.register_hook(HookEvents.CHAT_MESSAGE_SENT, self._on_chat_message)
        self.register_hook(HookEvents.COST_CALCULATED, self._on_cost_calculated)
        
        logger.info("Gamification plugin initialized")
        return True
    
    def activate(self) -> bool:
        """Activate gamification plugin."""
        self.status = PluginStatus.ACTIVE
        logger.info("Gamification plugin activated")
        return True
    
    def deactivate(self) -> bool:
        """Deactivate gamification plugin."""
        self.status = PluginStatus.LOADED
        logger.info("Gamification plugin deactivated")
        return True
    
    # =========================================================================
    # CORE METHODS
    # =========================================================================
    
    def get_user_progress(self, user_id: str) -> UserProgress:
        """Get or create user progress."""
        if user_id not in self._user_progress:
            self._user_progress[user_id] = UserProgress(user_id=user_id)
        return self._user_progress[user_id]
    
    def award_badge(self, user_id: str, badge_id: str) -> Optional[UserBadge]:
        """Award a badge to user if not already earned."""
        progress = self.get_user_progress(user_id)
        
        if progress.has_badge(badge_id):
            return None
        
        badge = self._badges.get(badge_id)
        if not badge:
            logger.warning(f"Badge not found: {badge_id}")
            return None
        
        user_badge = progress.add_badge(badge_id)
        progress.add_points(badge.points)
        
        logger.info(f"Awarded badge '{badge_id}' to user {user_id}")
        return user_badge
    
    def check_badges(self, user_id: str) -> List[UserBadge]:
        """Check and award all earned badges for user."""
        progress = self.get_user_progress(user_id)
        new_badges = []
        
        for badge_id, badge in self._badges.items():
            if progress.has_badge(badge_id):
                continue
            
            if self._check_badge_requirements(progress, badge):
                user_badge = self.award_badge(user_id, badge_id)
                if user_badge:
                    new_badges.append(user_badge)
        
        return new_badges
    
    def _check_badge_requirements(self, progress: UserProgress, badge: Badge) -> bool:
        """Check if user meets badge requirements."""
        reqs = badge.requirements
        
        # Check stat-based requirements
        for key, value in reqs.items():
            if key == "action":
                continue  # Actions are checked separately
            
            if key in progress.stats:
                if progress.stats[key] < value:
                    return False
            else:
                return False
        
        return True
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top users by points."""
        sorted_users = sorted(
            self._user_progress.values(),
            key=lambda x: x.total_points,
            reverse=True
        )[:limit]
        
        return [
            {
                "user_id": u.user_id,
                "points": u.total_points,
                "level": u.level,
                "badge_count": len(u.badges)
            }
            for u in sorted_users
        ]
    
    def get_all_badges(self) -> List[Badge]:
        """Get all available badges."""
        return list(self._badges.values())
    
    # =========================================================================
    # HOOK HANDLERS
    # =========================================================================
    
    @PluginHook(HookEvents.USER_LOGIN)
    def _on_user_login(self, user_id: str, **kwargs):
        """Handle user login event."""
        progress = self.get_user_progress(user_id)
        
        # Award newcomer badge on first visit
        if not progress.badges:
            self.award_badge(user_id, "newcomer")
        
        # Track consecutive days
        progress.increment_stat("login_days")
        
        # Check for new badges
        self.check_badges(user_id)
    
    @PluginHook(HookEvents.CHAT_MESSAGE_SENT)
    def _on_chat_message(self, user_id: str, message: str, **kwargs):
        """Handle chat message event."""
        progress = self.get_user_progress(user_id)
        progress.increment_stat("questions_asked")
        
        # Check for learning badges
        self.check_badges(user_id)
    
    @PluginHook(HookEvents.COST_CALCULATED)
    def _on_cost_calculated(self, user_id: str, **kwargs):
        """Handle cost simulation event."""
        progress = self.get_user_progress(user_id)
        progress.increment_stat("simulations_completed")
        
        # Check for planning badges
        self.check_badges(user_id)
    
    # =========================================================================
    # UI RENDERING
    # =========================================================================
    
    def render_ui(self):
        """Render gamification UI components."""
        import streamlit as st
        
        if "user_id" not in st.session_state:
            return
        
        user_id = st.session_state.user_id
        progress = self.get_user_progress(user_id)
        
        # Sidebar widget
        with st.sidebar:
            st.markdown("### 🏆 Progress Anda")
            
            # Level and points
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Level", progress.level)
            with col2:
                st.metric("Points", progress.total_points)
            
            # Progress bar to next level
            points_in_level = progress.total_points % 100
            st.progress(points_in_level / 100)
            st.caption(f"{points_in_level}/100 ke level {progress.level + 1}")
            
            # Recent badges
            if progress.badges:
                st.markdown("**Badge Terbaru:**")
                recent = progress.badges[-3:]
                badge_icons = ""
                for ub in recent:
                    badge = self._badges.get(ub.badge_id)
                    if badge:
                        badge_icons += f"{badge.icon} "
                st.markdown(badge_icons)
    
    def render_badges_page(self):
        """Render full badges page."""
        import streamlit as st
        
        st.header("🏆 Koleksi Badge")
        
        user_id = st.session_state.get("user_id")
        if not user_id:
            st.warning("Silakan login untuk melihat badge Anda.")
            return
        
        progress = self.get_user_progress(user_id)
        
        # Stats overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Points", progress.total_points)
        with col2:
            st.metric("Level", progress.level)
        with col3:
            st.metric("Badge Diperoleh", f"{len(progress.badges)}/{len(self._badges)}")
        
        st.divider()
        
        # Badge grid
        for category in BadgeCategory:
            category_badges = [b for b in self._badges.values() if b.category == category]
            if not category_badges:
                continue
            
            st.subheader(f"{category.value.title()}")
            
            cols = st.columns(4)
            for i, badge in enumerate(category_badges):
                with cols[i % 4]:
                    earned = progress.has_badge(badge.id)
                    
                    if earned:
                        st.markdown(f"### {badge.icon}")
                        st.markdown(f"**{badge.name}**")
                        st.caption(badge.description)
                        st.success(f"+{badge.points} pts ✓")
                    else:
                        st.markdown(f"### 🔒")
                        st.markdown(f"**{badge.name}**")
                        st.caption(badge.description)
                        st.info(f"+{badge.points} pts")
