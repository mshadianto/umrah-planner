"""
LABBAIK AI v6.0 - Main Application (Super WOW Edition)
======================================================
Integrated platform for Umrah planning with AI assistance,
cost simulation, trip matching, and booking.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from datetime import datetime

# =============================================================================
# PAGE CONFIG (Must be first Streamlit command)
# =============================================================================

st.set_page_config(
    page_title="LABBAIK AI - Platform Umrah Cerdas",
    page_icon="🕋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://labbaik.streamlit.app/help",
        "Report a bug": "https://github.com/labbaik/issues",
        "About": "LABBAIK AI v6.0 - Platform Cerdas untuk Perjalanan Umrah"
    }
)

# =============================================================================
# SERVICE IMPORTS (with fallbacks)
# =============================================================================

# Try importing state manager
try:
    from services.state_manager import state_manager, init_state, StateKeys
    STATE_MANAGER_AVAILABLE = True
except ImportError:
    STATE_MANAGER_AVAILABLE = False
    state_manager = None

# Try importing data services
try:
    from services.data_service import (
        init_database,
        UserService,
        TripService,
        AnalyticsService,
        db,
    )
    DATA_SERVICES_AVAILABLE = True
except ImportError:
    DATA_SERVICES_AVAILABLE = False
    init_database = None
    db = None

# =============================================================================
# CUSTOM CSS
# =============================================================================

def inject_global_css():
    """Inject global CSS styling."""
    st.markdown("""
    <style>
    /* Global styles */
    .main {
        padding-top: 1rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a5f3c 0%, #2d8659 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stButton button {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255,255,255,0.2);
        border-color: rgba(255,255,255,0.5);
    }
    
    /* Primary button */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #1a5f3c 0%, #2d8659 100%);
        border: none;
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #1a5f3c 0%, #3ba876 100%);
    }
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# SESSION STATE INITIALIZATION (Fallback if state_manager not available)
# =============================================================================

def init_session_state():
    """Initialize all session state variables."""
    
    # Use state manager if available
    if STATE_MANAGER_AVAILABLE and state_manager:
        state_manager.initialize()
        return
    
    # Fallback initialization
    defaults = {
        "current_page": "home",
        "user": None,
        "is_authenticated": False,
        "points": 0,
        "badges": [],
        "theme": "light",
        "show_login": False,
        "last_page": None,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =============================================================================
# NAVIGATION
# =============================================================================

def render_sidebar_navigation():
    """Render sidebar with navigation."""
    
    with st.sidebar:
        # Logo & branding
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="font-size: 2rem; margin: 0;">🕋</h1>
            <h2 style="font-size: 1.5rem; margin: 0;">LABBAIK AI</h2>
            <p style="font-size: 0.8rem; opacity: 0.8;">Platform Umrah Cerdas</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Database status indicator
        if DATA_SERVICES_AVAILABLE and db:
            mode = "🟢 Connected" if not db.is_mock else "🟡 Demo Mode"
        else:
            mode = "🟡 Offline Mode"
        st.caption(f"Status: {mode}")
        
        st.divider()
        
        # Navigation menu
        st.markdown("### 🧭 Menu")
        
        menu_items = [
            ("🏠 Beranda", "home"),
            ("🤖 AI Assistant", "chat"),
            ("💰 Simulasi Biaya", "simulator"),
            ("👥 Umrah Bareng", "umrah_bareng"),
            ("🧭 Umrah Mandiri", "umrah_mandiri"),
            ("📦 Booking", "booking"),
            ("📚 Panduan", "guide"),
        ]
        
        current_page = st.session_state.get("current_page", "home")
        
        for label, page_id in menu_items:
            is_active = current_page == page_id
            btn_type = "primary" if is_active else "secondary"
            
            if st.button(label, key=f"nav_{page_id}", use_container_width=True, type=btn_type):
                st.session_state.current_page = page_id
                st.rerun()
        
        st.divider()
        
        # User section
        if st.session_state.get("is_authenticated"):
            st.markdown("### 👤 Profil")
            
            user = st.session_state.get("user") or {}
            st.markdown(f"**{user.get('name', 'User')}**")
            st.caption(f"⭐ {st.session_state.get('points', 0)} poin")
            
            # Badges
            badges = st.session_state.get("badges", [])
            if badges:
                badge_icons = " ".join([b.get("icon", "🏅") for b in badges[:5]])
                st.markdown(f"🏅 {badge_icons}")
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.is_authenticated = False
                st.session_state.user = None
                st.rerun()
        else:
            st.markdown("### 🔐 Akun")
            
            if st.button("🔑 Login", use_container_width=True):
                st.session_state.show_login = True
            
            if st.button("📝 Daftar", use_container_width=True):
                st.session_state.show_register = True
        
        st.divider()
        
        # Platform stats
        st.markdown("### 📊 Statistik")
        if DATA_SERVICES_AVAILABLE:
            try:
                stats = AnalyticsService.get_platform_stats()
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Users", stats.get("total_users", "10K+"))
                with col2:
                    st.metric("Trips", stats.get("total_trips", "500+"))
            except:
                st.caption("10K+ jamaah terlayani")
        else:
            st.caption("10K+ jamaah terlayani")
        
        # Footer
        st.markdown("""
        <div style="text-align: center; font-size: 0.7rem; opacity: 0.7; margin-top: 2rem;">
            <p>LABBAIK AI v6.0</p>
            <p>© 2025 MS Hadianto</p>
        </div>
        """, unsafe_allow_html=True)


def render_login_modal():
    """Render login modal."""
    
    if st.session_state.get("show_login"):
        with st.container(border=True):
            st.markdown("### 🔑 Login")
            
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Masuk", type="primary", use_container_width=True):
                    if email and password:
                        # Use state manager if available
                        if STATE_MANAGER_AVAILABLE and state_manager:
                            success, msg = state_manager.login(email, password)
                        else:
                            # Fallback mock login
                            st.session_state.is_authenticated = True
                            st.session_state.user = {
                                "id": "user_1",
                                "name": email.split("@")[0].title(),
                                "email": email
                            }
                            success, msg = True, "Login berhasil"
                        
                        if success:
                            st.success(f"✅ {msg}")
                            st.session_state.show_login = False
                            award_points(50, "Login bonus")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
                    else:
                        st.error("Email dan password harus diisi")
            
            with col2:
                if st.button("Batal", use_container_width=True):
                    st.session_state.show_login = False
                    st.rerun()


# =============================================================================
# PAGE RENDERERS
# =============================================================================

def render_home_page():
    """Render home page."""
    try:
        from ui.pages.home import render_home_page as render
        render()
    except ImportError as e:
        st.error(f"Error loading home page: {e}")
        render_fallback_home()


def render_chat_page():
    """Render chat page."""
    try:
        from ui.pages.chat import render_chat_page as render
        render()
    except ImportError as e:
        st.error(f"Error loading chat page: {e}")
        st.info("💬 Chat dengan AI Assistant")
        st.text_input("Tanya seputar umrah...")


def render_simulator_page():
    """Render simulator page."""
    try:
        from ui.pages.simulator import render_simulator_page as render
        render()
    except ImportError as e:
        st.error(f"Error loading simulator page: {e}")
        st.info("💰 Simulasi Biaya Umrah")


def render_umrah_bareng_page():
    """Render umrah bareng page."""
    try:
        from ui.pages.umrah_bareng import render_umrah_bareng_page as render
        render()
    except ImportError as e:
        st.error(f"Error loading umrah bareng page: {e}")
        st.info("👥 Temukan teman perjalanan umrah")


def render_umrah_mandiri_page():
    """Render umrah mandiri page."""
    try:
        from ui.pages.umrah_mandiri import render_umrah_mandiri_page as render
        render()
    except ImportError as e:
        st.error(f"Error loading umrah mandiri page: {e}")
        st.info("🧭 Panduan Umrah Mandiri dengan 3 Pilar Framework")


def render_booking_page():
    """Render booking page."""
    try:
        from ui.pages.booking import render_booking_page as render
        render()
    except ImportError as e:
        st.error(f"Error loading booking page: {e}")
        st.info("📦 Booking Paket Umrah")


def render_guide_page():
    """Render knowledge base / guide page."""
    st.markdown("# 📚 Panduan Umrah")
    st.caption("Semua yang perlu Anda ketahui tentang ibadah umrah")
    
    tabs = st.tabs(["📋 Persiapan", "🕋 Tata Cara", "🗣️ Bahasa Arab", "💡 Tips"])
    
    with tabs[0]:
        st.markdown("""
        ## Persiapan Umrah
        
        ### Dokumen yang Diperlukan
        1. **Paspor** - Minimal berlaku 7 bulan
        2. **Pas foto** - 4x6 background putih
        3. **Kartu vaksin** - Meningitis & COVID-19
        4. **KTP** - Untuk verifikasi
        """)
    
    with tabs[1]:
        st.markdown("""
        ## Tata Cara Umrah
        
        ### Rukun Umrah
        1. **Ihram** - Niat dan berpakaian ihram
        2. **Thawaf** - Mengelilingi Ka'bah 7 kali
        3. **Sa'i** - Berjalan Shafa-Marwah 7 kali
        4. **Tahallul** - Mencukur/memotong rambut
        """)
    
    with tabs[2]:
        st.markdown("""
        ## Frasa Bahasa Arab Penting
        
        | Indonesia | Arab | Transliterasi |
        |-----------|------|---------------|
        | Terima kasih | شكراً | Syukran |
        | Sama-sama | عفواً | 'Afwan |
        | Permisi | لو سمحت | Law samaht |
        """)
    
    with tabs[3]:
        st.markdown("""
        ## Tips Praktis
        
        - ✅ Siapkan dokumen 2 bulan sebelumnya
        - ✅ Bawa obat-obatan pribadi
        - ✅ Gunakan sandal yang nyaman
        - ✅ Bawa payung untuk perjalanan
        """)


def render_fallback_home():
    """Fallback home page if module not loaded."""
    st.markdown("# 🕋 LABBAIK AI")
    st.markdown("### Platform Cerdas untuk Perjalanan Umrah")
    
    st.info("Selamat datang di LABBAIK AI! Silakan pilih menu di sidebar untuk memulai.")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🤖 Chat AI", use_container_width=True, type="primary"):
            st.session_state.current_page = "chat"
            st.rerun()
    
    with col2:
        if st.button("💰 Simulasi", use_container_width=True):
            st.session_state.current_page = "simulator"
            st.rerun()
    
    with col3:
        if st.button("👥 Umrah Bareng", use_container_width=True):
            st.session_state.current_page = "umrah_bareng"
            st.rerun()
    
    with col4:
        if st.button("📦 Booking", use_container_width=True):
            st.session_state.current_page = "booking"
            st.rerun()
    
    # Quick stats
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Jamaah", "10,000+")
    with col2:
        st.metric("✈️ Trips", "500+")
    with col3:
        st.metric("⭐ Rating", "4.9")
    with col4:
        st.metric("🤖 AI Chat", "24/7")


# =============================================================================
# GAMIFICATION
# =============================================================================

def award_points(points: int, reason: str):
    """Award points to user."""
    if STATE_MANAGER_AVAILABLE and state_manager:
        state_manager.add_points(points, reason)
    else:
        current = st.session_state.get("points", 0)
        st.session_state.points = current + points
        st.toast(f"🎉 +{points} poin! {reason}")
        check_badges()


def check_badges():
    """Check and award badges."""
    points = st.session_state.get("points", 0)
    badges = st.session_state.get("badges", [])
    badge_ids = [b.get("id") for b in badges]
    
    badge_definitions = [
        {"id": "first_visit", "name": "First Visit", "icon": "🌟", "threshold": 10},
        {"id": "explorer", "name": "Explorer", "icon": "🔍", "threshold": 100},
        {"id": "learner", "name": "Learner", "icon": "📚", "threshold": 500},
        {"id": "planner", "name": "Planner", "icon": "📋", "threshold": 1000},
        {"id": "champion", "name": "Champion", "icon": "🏆", "threshold": 5000},
    ]
    
    for badge in badge_definitions:
        if points >= badge["threshold"] and badge["id"] not in badge_ids:
            badges.append(badge)
            st.balloons()
            st.toast(f"🏅 Badge baru: {badge['icon']} {badge['name']}")
    
    st.session_state.badges = badges


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    
    # Initialize
    init_session_state()
    inject_global_css()
    
    # Initialize database if available
    if DATA_SERVICES_AVAILABLE and init_database:
        init_database()
    
    # Navigation
    render_sidebar_navigation()
    
    # Login modal
    if st.session_state.get("show_login"):
        render_login_modal()
    
    # Page routing
    page = st.session_state.get("current_page", "home")
    
    page_renderers = {
        "home": render_home_page,
        "chat": render_chat_page,
        "simulator": render_simulator_page,
        "umrah_bareng": render_umrah_bareng_page,
        "umrah_mandiri": render_umrah_mandiri_page,
        "booking": render_booking_page,
        "guide": render_guide_page,
    }
    
    renderer = page_renderers.get(page, render_home_page)
    renderer()
    
    # Award points for visiting pages
    last_page = st.session_state.get("last_page")
    if last_page != page:
        award_points(5, f"Mengunjungi {page}")
        st.session_state.last_page = page


if __name__ == "__main__":
    main()
