"""
LABBAIK AI v6.0 - Super Boom Edition
=====================================
Platform Perencanaan Umrah AI #1 Indonesia
By MS Hadianto

Main entry point - compatible with Streamlit Cloud deployment
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

# Import pages
from ui.pages.home import render_home_page
from ui.pages.chat import render_chat_page
from ui.pages.simulator import render_simulator_page
from ui.pages.umrah_mandiri import render_umrah_mandiri_page
from ui.pages.umrah_bareng import render_umrah_bareng_page
from ui.pages.booking import render_booking_page

# Initialize session state
def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "current_page": "home",
        "user": None,
        "is_authenticated": False,
        "chat_messages": [],
        "visitor_counted": False,
        "xp": 0,
        "level": 1,
        "achievements": [],
        "daily_challenges_completed": [],
        "theme": "dark",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Track visitor (simple version - upgrade with DB later)
def track_visitor():
    """Track unique visitors."""
    if not st.session_state.get("visitor_counted"):
        st.session_state.visitor_counted = True
        # TODO: Integrate with Neon DB visitor_stats table

# Price Intelligence Health Indicator
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

# Sidebar navigation
def render_sidebar():
    """Render sidebar with navigation and branding."""
    with st.sidebar:
        # Logo & Brand
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 3rem;">🕋</div>
            <h2 style="color: #d4af37; margin: 0;">LABBAIK AI</h2>
            <p style="color: #888; font-size: 0.85rem;">Platform Umrah Cerdas</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Price Intelligence Status (with fallback)
        render_price_health()
        
        st.markdown("---")
        
        # Navigation Menu
        st.markdown("### 🧭 Menu")
        
        menu_items = [
            ("🏠", "Beranda", "home"),
            ("🤖", "AI Assistant", "chat"),
            ("💰", "Simulasi Biaya", "simulator"),
            ("👥", "Umrah Bareng", "umrah_bareng"),
            ("🧭", "Umrah Mandiri", "umrah_mandiri"),
            ("📦", "Booking", "booking"),
        ]
        
        for icon, label, page_key in menu_items:
            if st.button(f"{icon} {label}", key=f"nav_{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()
        
        st.markdown("---")
        
        # Gamification Stats
        st.markdown("### 🏆 Progress Anda")
        level = st.session_state.get("level", 1)
        xp = st.session_state.get("xp", 0)
        xp_for_next = level * 100
        
        st.markdown(f"**Level {level}** - {get_level_title(level)}")
        st.progress(min(xp / xp_for_next, 1.0))
        st.caption(f"{xp}/{xp_for_next} XP")
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <p style="color: #666; font-size: 0.75rem;">
                v6.0.0 - Super Boom Edition<br>
                © 2025 MS Hadianto
            </p>
        </div>
        """, unsafe_allow_html=True)

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

# Page router
def render_page():
    """Render the current page based on session state."""
    page = st.session_state.get("current_page", "home")
    
    page_map = {
        "home": render_home_page,
        "chat": render_chat_page,
        "simulator": render_simulator_page,
        "umrah_mandiri": render_umrah_mandiri_page,
        "umrah_bareng": render_umrah_bareng_page,
        "booking": render_booking_page,
    }
    
    renderer = page_map.get(page, render_home_page)
    renderer()

# Main app
def main():
    """Main application entry point."""
    # Initialize
    init_session_state()
    track_visitor()
    
    # Award XP for visiting (once per session per page)
    page = st.session_state.get("current_page", "home")
    visit_key = f"visited_{page}"
    if not st.session_state.get(visit_key):
        st.session_state[visit_key] = True
        add_xp(5, f"Mengunjungi {page}")
    
    # Render sidebar
    render_sidebar()
    
    # Render main content
    render_page()

if __name__ == "__main__":
    main()