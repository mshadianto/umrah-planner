"""
LABBAIK AI v6.0 - Super Boom Edition
=====================================
Platform Perencanaan Umrah AI #1 Indonesia
By MS Hadianto

Main entry point - compatible with Streamlit Cloud deployment

NEW FEATURES (PilgrimPal-Inspired):
- 📊 Crowd Prediction
- 🆘 SOS Emergency
- 📍 Group Tracking
- 🕋 3D Manasik
- 🔍 Smart Comparison
- 📈 Analytics Dashboard
"""

import streamlit as st
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="LABBAIK AI - Platform Umrah Cerdas",
    page_icon="🕋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://labbaik.cloud/help',
        'Report a bug': 'https://labbaik.cloud/feedback',
        'About': 'LABBAIK AI v6.0 - Platform Perencanaan Umrah AI #1 Indonesia'
    }
)

# =============================================================================
# IMPORTS - Core Pages
# =============================================================================
from ui.pages.home import render_home_page
from ui.pages.chat import render_chat_page
from ui.pages.simulator import render_simulator_page
from ui.pages.umrah_mandiri import render_umrah_mandiri_page
from ui.pages.umrah_bareng import render_umrah_bareng_page
from ui.pages.booking import render_booking_page

# =============================================================================
# IMPORTS - New Features (with fallbacks)
# =============================================================================

# Crowd Prediction
try:
    from features.crowd_prediction import (
        render_crowd_prediction_page,
        render_crowd_widget,
    )
    HAS_CROWD_PREDICTION = True
except ImportError:
    HAS_CROWD_PREDICTION = False
    def render_crowd_prediction_page():
        st.warning("⚠️ Fitur Crowd Prediction belum tersedia")
    def render_crowd_widget(location="makkah", compact=True):
        pass

# SOS Emergency
try:
    from features.sos_emergency import (
        render_sos_page,
        render_sos_button,
    )
    HAS_SOS = True
except ImportError:
    HAS_SOS = False
    def render_sos_page():
        st.warning("⚠️ Fitur SOS Emergency belum tersedia")
    def render_sos_button(size="small"):
        pass

# Group Tracking
try:
    from features.group_tracking import (
        render_group_tracking_page,
        render_tracking_mini_widget,
    )
    HAS_TRACKING = True
except ImportError:
    HAS_TRACKING = False
    def render_group_tracking_page():
        st.warning("⚠️ Fitur Group Tracking belum tersedia")
    def render_tracking_mini_widget():
        pass

# 3D Manasik
try:
    from features.manasik_3d import (
        render_manasik_page,
        render_manasik_mini_widget,
    )
    HAS_MANASIK = True
except ImportError:
    HAS_MANASIK = False
    def render_manasik_page():
        st.warning("⚠️ Fitur 3D Manasik belum tersedia")
    def render_manasik_mini_widget():
        pass

# Smart Comparison
try:
    from features.smart_comparison import render_smart_comparison_page
    HAS_COMPARISON = True
except ImportError:
    HAS_COMPARISON = False
    def render_smart_comparison_page():
        st.warning("⚠️ Fitur Smart Comparison belum tersedia")

# Analytics Dashboard
try:
    from services.analytics.dashboard import render_analytics_dashboard
    HAS_ANALYTICS = True
except ImportError:
    HAS_ANALYTICS = False
    def render_analytics_dashboard():
        st.warning("⚠️ Fitur Analytics Dashboard belum tersedia")

# WhatsApp / WAHA Integration
try:
    from services.whatsapp import (
        render_whatsapp_settings,
        render_whatsapp_status,
        get_whatsapp_service,
    )
    HAS_WHATSAPP = True
except ImportError:
    HAS_WHATSAPP = False
    def render_whatsapp_settings():
        st.warning("⚠️ WhatsApp Integration belum tersedia")
    def render_whatsapp_status():
        pass
    def get_whatsapp_service():
        return None

# Doa Player (Coming Soon)
HAS_DOA_PLAYER = False
def render_doa_player_page():
    st.markdown("# 🤲 Doa & Dzikir")
    st.info("🚧 Fitur ini sedang dalam pengembangan...")
    st.markdown("""
    **Coming Soon:**
    - Audio doa Umrah & Haji
    - Dzikir pagi & petang
    - Bacaan thawaf & sa'i
    - Mode offline
    """)

# WhatsApp Service (WAHA)
try:
    from features.whatsapp_service import (
        render_whatsapp_settings,
        render_whatsapp_status,
        WhatsAppService,
    )
    HAS_WHATSAPP = True
except ImportError:
    HAS_WHATSAPP = False
    def render_whatsapp_settings():
        st.warning("⚠️ Fitur WhatsApp belum tersedia")
    def render_whatsapp_status():
        pass

# Doa Player
try:
    from features.doa_player import (
        render_doa_player_page,
        render_doa_mini_widget,
    )
    HAS_DOA_PLAYER = True
except ImportError:
    HAS_DOA_PLAYER = False
    def render_doa_player_page():
        st.warning("⚠️ Fitur Doa Player belum tersedia")
    def render_doa_mini_widget():
        pass
except ImportError:
    HAS_ANALYTICS = False
    def render_analytics_dashboard():
        st.warning("⚠️ Fitur Analytics Dashboard belum tersedia")

# Page Tracking
try:
    from services.analytics import track_page
    HAS_TRACKING_SERVICE = True
except ImportError:
    HAS_TRACKING_SERVICE = False
    def track_page(page_name):
        pass


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        # Navigation
        "current_page": "home",
        
        # Authentication
        "user": None,
        "is_authenticated": False,
        
        # Chat
        "chat_messages": [],
        
        # Visitor tracking
        "visitor_counted": False,
        
        # Gamification
        "xp": 0,
        "level": 1,
        "achievements": [],
        "daily_challenges_completed": [],
        
        # Theme
        "theme": "dark",
        
        # SOS Emergency
        "sos_contacts": [],
        "sos_user_info": {},
        "sos_triggered": False,
        
        # Group Tracking
        "tracking_groups": {},
        "current_group_id": None,
        "my_member_id": None,
        
        # Manasik Progress
        "manasik_progress": {},
        
        # Analytics
        "tracked_pages": set(),
        
        # Crowd Prediction
        "crowd_location": "makkah",
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =============================================================================
# VISITOR TRACKING
# =============================================================================

def track_visitor():
    """Track unique visitors."""
    if not st.session_state.get("visitor_counted"):
        st.session_state.visitor_counted = True
        
        # Track with analytics service
        if HAS_TRACKING_SERVICE:
            try:
                track_page("home")
            except:
                pass


# =============================================================================
# GAMIFICATION SYSTEM
# =============================================================================

def get_level_title(level: int) -> str:
    """Get title based on level."""
    titles = {
        1: "Pemula",
        2: "Pelajar",
        3: "Praktisi",
        4: "Ahli",
        5: "Master",
        6: "Guru",
        7: "Ulama",
        8: "Syaikh",
        9: "Mufti",
        10: "Grand Master"
    }
    return titles.get(level, "Legend")


def add_xp(amount: int, reason: str = ""):
    """Add XP and check for level up."""
    st.session_state.xp = st.session_state.get("xp", 0) + amount
    
    # Check level up
    current_level = st.session_state.get("level", 1)
    xp_needed = current_level * 100
    
    if st.session_state.xp >= xp_needed and current_level < 10:
        st.session_state.level = current_level + 1
        st.session_state.xp = st.session_state.xp - xp_needed
        st.toast(f"🎉 Level Up! Sekarang Level {st.session_state.level}!", icon="⬆️")
    
    if reason:
        st.toast(f"🎯 +{amount} poin! {reason}", icon="✨")


# =============================================================================
# PRICE INTELLIGENCE HEALTH
# =============================================================================

def render_price_health():
    """Render Price Intelligence health status."""
    try:
        from services.price.monitoring import render_health_indicator
        render_health_indicator()
    except ImportError:
        # Fallback jika module belum ada
        db_status = "🟢 Online" if os.getenv("DATABASE_URL") else "🟡 Offline Mode"
        st.caption(f"Status: {db_status}")
    except Exception:
        # Silent fallback
        st.caption("📊 Mode offline")


# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================

def render_sidebar():
    """Render sidebar with navigation, widgets, and branding."""
    with st.sidebar:
        # =====================================================================
        # Logo & Brand
        # =====================================================================
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 3rem;">🕋</div>
            <h2 style="color: #d4af37; margin: 0;">LABBAIK AI</h2>
            <p style="color: #888; font-size: 0.85rem;">Platform Umrah Cerdas</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # =====================================================================
        # 🆘 SOS Emergency Button (Always Visible)
        # =====================================================================
        if HAS_SOS:
            if st.button("🆘 DARURAT / SOS", key="sos_sidebar_main", use_container_width=True, type="primary"):
                st.session_state.current_page = "sos"
                st.rerun()
            st.markdown("")
        
        # =====================================================================
        # Price Intelligence Status
        # =====================================================================
        render_price_health()
        
        st.markdown("---")
        
        # =====================================================================
        # 🧭 Main Navigation Menu
        # =====================================================================
        st.markdown("### 🧭 Menu Utama")
        
        main_menu = [
            ("🏠", "Beranda", "home"),
            ("🤖", "AI Assistant", "chat"),
            ("💰", "Simulasi Biaya", "simulator"),
            ("👥", "Umrah Bareng", "umrah_bareng"),
            ("🧭", "Umrah Mandiri", "umrah_mandiri"),
            ("📦", "Booking", "booking"),
        ]
        
        for icon, label, page_key in main_menu:
            is_active = st.session_state.get("current_page") == page_key
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon} {label}", key=f"nav_{page_key}", use_container_width=True, type=btn_type):
                st.session_state.current_page = page_key
                st.rerun()
        
        st.markdown("---")
        
        # =====================================================================
        # ✨ New Features Menu (PilgrimPal-Inspired)
        # =====================================================================
        st.markdown("### ✨ Fitur Baru")
        
        new_features = [
            ("📊", "Prediksi Keramaian", "crowd", HAS_CROWD_PREDICTION),
            ("📍", "Group Tracking", "tracking", HAS_TRACKING),
            ("🕋", "Manasik 3D", "manasik", HAS_MANASIK),
            ("🤲", "Doa & Dzikir", "doa", HAS_DOA_PLAYER),
            ("🔍", "Bandingkan Paket", "compare", HAS_COMPARISON),
            ("📱", "WhatsApp", "whatsapp", HAS_WHATSAPP),
            ("📈", "Analytics", "analytics", HAS_ANALYTICS),
        ]
        
        for icon, label, page_key, is_available in new_features:
            if is_available:
                is_active = st.session_state.get("current_page") == page_key
                if st.button(f"{icon} {label}", key=f"nav_{page_key}", use_container_width=True):
                    st.session_state.current_page = page_key
                    st.rerun()
        
        st.markdown("---")
        
        # =====================================================================
        # 📊 Quick Widgets
        # =====================================================================
        st.markdown("### 📊 Quick Info")
        
        # WhatsApp Status
        if HAS_WHATSAPP:
            try:
                render_whatsapp_status()
            except:
                pass
        
        # Crowd Widget
        if HAS_CROWD_PREDICTION:
            try:
                render_crowd_widget("makkah", compact=True)
            except:
                pass
        
        # Group Tracking Widget
        if HAS_TRACKING:
            try:
                render_tracking_mini_widget()
            except:
                pass
        
        # Manasik Progress Widget
        if HAS_MANASIK:
            try:
                render_manasik_mini_widget()
            except:
                pass
        
        # Doa Mini Widget
        if HAS_DOA_PLAYER:
            try:
                render_doa_mini_widget()
            except:
                pass
        
        st.markdown("---")
        
        # =====================================================================
        # 🏆 Gamification Stats
        # =====================================================================
        st.markdown("### 🏆 Progress Anda")
        
        level = st.session_state.get("level", 1)
        xp = st.session_state.get("xp", 0)
        xp_for_next = level * 100
        
        st.markdown(f"**Level {level}** - {get_level_title(level)}")
        st.progress(min(xp / xp_for_next, 1.0))
        st.caption(f"{xp}/{xp_for_next} XP")
        
        # Achievement badges
        achievements = st.session_state.get("achievements", [])
        if achievements:
            badges = " ".join(achievements[:5])
            st.caption(f"🎖️ {badges}")
        
        st.markdown("---")
        
        # =====================================================================
        # Footer
        # =====================================================================
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <p style="color: #666; font-size: 0.75rem;">
                v6.0.0 - Super Boom Edition<br>
                © 2025 MS Hadianto
            </p>
            <p style="color: #444; font-size: 0.65rem;">
                Inspired by PilgrimPal<br>
                Powered by AI
            </p>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# PAGE ROUTER
# =============================================================================

def render_page():
    """Render the current page based on session state."""
    page = st.session_state.get("current_page", "home")
    
    # Track page view
    if HAS_TRACKING_SERVICE:
        try:
            track_page(page)
        except:
            pass
    
    # Page mapping
    page_map = {
        # Core pages
        "home": render_home_page,
        "chat": render_chat_page,
        "simulator": render_simulator_page,
        "umrah_mandiri": render_umrah_mandiri_page,
        "umrah_bareng": render_umrah_bareng_page,
        "booking": render_booking_page,
        
        # New feature pages
        "crowd": render_crowd_prediction_page,
        "sos": render_sos_page,
        "tracking": render_group_tracking_page,
        "manasik": render_manasik_page,
        "compare": render_smart_comparison_page,
        "analytics": render_analytics_dashboard,
        "whatsapp": render_whatsapp_settings,
        "doa": render_doa_player_page,
    }
    
    renderer = page_map.get(page, render_home_page)
    
    try:
        renderer()
    except Exception as e:
        st.error(f"❌ Error rendering page: {str(e)}")
        st.info("Kembali ke beranda...")
        if st.button("🏠 Ke Beranda"):
            st.session_state.current_page = "home"
            st.rerun()


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    # Initialize session state
    init_session_state()
    
    # Track visitor
    track_visitor()
    
    # Award XP for visiting (once per session per page)
    page = st.session_state.get("current_page", "home")
    visit_key = f"visited_{page}"
    if not st.session_state.get(visit_key):
        st.session_state[visit_key] = True
        add_xp(5, f"Mengunjungi {page}")
    
    # Check for SOS trigger from any page
    if st.session_state.get("sos_triggered") and st.session_state.get("current_page") != "sos":
        st.session_state.current_page = "sos"
        st.rerun()
    
    # Render sidebar
    render_sidebar()
    
    # Render main content
    render_page()


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
