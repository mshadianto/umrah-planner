"""
================================================================================
لَبَّيْكَ LABBAIK - Main Application
================================================================================

Labbaik Allahumma Labbaik - Aku Datang Memenuhi Panggilan-Mu

Copyright (c) 2025 MS Hadianto. All Rights Reserved.

This software is proprietary and confidential. Unauthorized copying,
modification, distribution, or use of this software is strictly prohibited.

See LICENSE and COPYRIGHT files for full terms.

================================================================================
Platform: AI-Powered Umrah Planning Platform
Version:  3.1.0
Codename: Labbaik
Author:   MS Hadianto
Email:    sopian.hadianto@gmail.com
Website:  labbaik.ai
GitHub:   https://github.com/mshadianto
================================================================================

Version: 3.1.0
Updated: 2025-12-02
Changes: Added Makkah/Madinah duration options in Buat Rencana + UAH video tutorial + Budget Finder feature
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Import modules
from config import (
    app_config, llm_config, SCENARIO_TEMPLATES, 
    DEPARTURE_CITIES, SEASONS
)
from agents import AgentOrchestrator
from scenarios import ScenarioPlanner
from utils import format_currency, format_duration
from features import render_additional_features
from booking import render_booking_features
from version import (
    __version__, DEVELOPER, APP_INFO, CHANGELOG, TECH_STACK,
    get_version_badge, get_developer_card, get_changelog_markdown, get_app_age
)
from monetization import (
    render_monetization_page, render_monetization_sidebar,
    render_quick_quote_widget, init_monetization_state, PRICING_TIERS
)
from auth import (
    init_user_database, is_logged_in, get_current_user, get_user_role_info,
    render_login_page, render_user_badge, render_upgrade_prompt,
    render_admin_dashboard, has_permission, check_limit, increment_usage,
    USER_ROLES, logout_user
)
from visitor_tracker import (
    track_page_view, get_visitor_count, get_page_view_count,
    get_visitor_stats, render_visitor_stats, render_analytics_dashboard
)

# ============================================
# LABBAIK BRAND CONSTANTS
# ============================================

BRAND = {
    "name": "LABBAIK",
    "arabic": "لَبَّيْكَ",
    "talbiyah": "لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ",
    "tagline": "Panggilan-Nya, Langkahmu",
    "description": "Platform AI Perencanaan Umrah #1 Indonesia",
    "full_tagline": "Labbaik Allahumma Labbaik - Aku Datang Memenuhi Panggilan-Mu",
    "version": "3.2.0",
}

COLORS = {
    "black": "#1A1A1A",
    "gold": "#D4AF37",
    "gold_light": "#F5E6C8",
    "green": "#006B3C",
    "white": "#FFFFFF",
    "sand": "#C9A86C",
    "blue": "#1E3A5F",
    "gray": "#666666",
}

CONTACT = {
    "email": "sopian.hadianto@gmail.com",
    "whatsapp": "+62 815 9658 833",
    "website": "labbaik.ai",
}

# ============================================
# HOTEL PRICES CONFIGURATION (for Buat Rencana)
# ============================================

HOTEL_PRICES = {
    "ekonomis": {
        "makkah": {"name": "Hotel Bintang 2-3 (1-2 km dari Haram)", "price": 800000},
        "madinah": {"name": "Hotel Bintang 2-3 (500m-1 km dari Nabawi)", "price": 600000}
    },
    "standard": {
        "makkah": {"name": "Hotel Bintang 3-4 (500m-1 km dari Haram)", "price": 1500000},
        "madinah": {"name": "Hotel Bintang 3-4 (300-500m dari Nabawi)", "price": 1000000}
    },
    "premium": {
        "makkah": {"name": "Hotel Bintang 4-5 (200-500m dari Haram)", "price": 2500000},
        "madinah": {"name": "Hotel Bintang 4-5 (100-300m dari Nabawi)", "price": 1800000}
    },
    "vip": {
        "makkah": {"name": "Hotel Bintang 5 (View Ka'bah, <200m)", "price": 5000000},
        "madinah": {"name": "Hotel Bintang 5 (View Masjid Nabawi, <100m)", "price": 3500000}
    }
}

ADDITIONAL_COSTS = {
    "ekonomis": {"flight": 8000000, "visa": 500000, "transport": 500000, "meals": 300000},
    "standard": {"flight": 12000000, "visa": 500000, "transport": 800000, "meals": 500000},
    "premium": {"flight": 18000000, "visa": 500000, "transport": 1200000, "meals": 800000},
    "vip": {"flight": 30000000, "visa": 500000, "transport": 2000000, "meals": 1500000}
}

# Page configuration
st.set_page_config(
    page_title=f"{BRAND['name']} - {BRAND['description']}",
    page_icon="🕋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# LABBAIK Brand CSS
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Noto+Naskh+Arabic:wght@400;500;600;700&display=swap');
    
    /* ===== CSS Variables ===== */
    :root {{
        --brand-black: {COLORS['black']};
        --brand-gold: {COLORS['gold']};
        --brand-gold-light: {COLORS['gold_light']};
        --brand-green: {COLORS['green']};
        --brand-white: {COLORS['white']};
        --brand-sand: {COLORS['sand']};
        --brand-blue: {COLORS['blue']};
        --brand-gray: {COLORS['gray']};
    }}
    
    /* ===== Sidebar ===== */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['black']} 0%, #2D2D2D 100%);
    }}
    
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] .stRadio label {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] hr {{
        border-color: #333 !important;
    }}
    
    /* ===== Buttons ===== */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['gold']} 0%, {COLORS['sand']} 100%);
        color: {COLORS['black']};
        border: none;
        border-radius: 25px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
        transform: translateY(-2px);
    }}
    
    .stButton > button[kind="secondary"] {{
        background: transparent;
        border: 2px solid {COLORS['gold']};
        color: {COLORS['gold']};
    }}
    
    /* ===== Metrics ===== */
    [data-testid="stMetricValue"] {{
        color: {COLORS['gold']} !important;
        font-weight: 700;
    }}
    
    /* ===== Tabs ===== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {COLORS['gold']};
        color: {COLORS['black']};
    }}
    
    /* ===== Headers ===== */
    .main-header {{
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        font-weight: bold;
        color: {COLORS['black']};
        text-align: center;
        padding: 1rem;
    }}
    
    .sub-header {{
        font-size: 1.2rem;
        color: {COLORS['gray']};
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    /* ===== Brand Header ===== */
    .labbaik-hero {{
        background: linear-gradient(135deg, {COLORS['black']} 0%, #2D2D2D 50%, {COLORS['black']} 100%);
        padding: 40px 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
    }}
    
    .labbaik-arabic {{
        font-family: 'Noto Naskh Arabic', serif;
        font-size: 3rem;
        color: {COLORS['gold']};
        text-shadow: 0 2px 15px rgba(212, 175, 55, 0.3);
        margin-bottom: 8px;
    }}
    
    .labbaik-name {{
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        letter-spacing: 0.3em;
        margin-bottom: 8px;
    }}
    
    .labbaik-tagline {{
        color: {COLORS['sand']};
        font-size: 1rem;
    }}
    
    /* ===== Cards ===== */
    .metric-card {{
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border: 2px solid #E0E0E0;
        transition: all 0.3s ease;
    }}
    
    .metric-card:hover {{
        border-color: {COLORS['gold']};
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.15);
        transform: translateY(-3px);
    }}
    
    .metric-card h3 {{
        color: {COLORS['black']};
        margin-bottom: 0.5rem;
    }}
    
    .metric-card p {{
        color: {COLORS['gray']};
        font-size: 0.9rem;
    }}
    
    /* ===== Feature Card ===== */
    .feature-card {{
        background: white;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        border: 2px solid #E0E0E0;
        transition: all 0.3s ease;
        height: 100%;
    }}
    
    .feature-card:hover {{
        border-color: {COLORS['gold']};
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.2);
        transform: translateY(-5px);
    }}
    
    .feature-icon {{
        font-size: 2.5rem;
        margin-bottom: 12px;
    }}
    
    .feature-title {{
        font-weight: 700;
        color: {COLORS['black']};
        margin-bottom: 8px;
    }}
    
    .feature-desc {{
        color: {COLORS['gray']};
        font-size: 0.9rem;
    }}
    
    /* ===== Highlight Boxes ===== */
    .highlight-box {{
        background-color: rgba(212, 175, 55, 0.1);
        border-left: 4px solid {COLORS['gold']};
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }}
    
    .warning-box {{
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }}
    
    .success-box {{
        background-color: rgba(0, 107, 60, 0.1);
        border-left: 4px solid {COLORS['green']};
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }}
    
    /* ===== Gold Accent ===== */
    .gold-text {{
        color: {COLORS['gold']};
    }}
    
    .gold-bg {{
        background: linear-gradient(135deg, {COLORS['gold']} 0%, {COLORS['sand']} 100%);
        color: {COLORS['black']};
    }}
    
    /* ===== Stats Bar ===== */
    .stats-bar {{
        background: {COLORS['black']};
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
    }}
    
    .stat-item {{
        text-align: center;
    }}
    
    .stat-value {{
        font-size: 1.8rem;
        font-weight: 800;
        color: {COLORS['gold']};
    }}
    
    .stat-label {{
        font-size: 0.85rem;
        color: {COLORS['sand']};
    }}
    
    /* ===== Footer ===== */
    .labbaik-footer {{
        background: linear-gradient(135deg, {COLORS['black']} 0%, #2D2D2D 100%);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin-top: 40px;
    }}
    
    /* ===== Animations ===== */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(15px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.8; }}
    }}
    
    .animate-fadeIn {{
        animation: fadeIn 0.5s ease-out;
    }}
    
    .animate-pulse {{
        animation: pulse 2s infinite;
    }}
</style>
""", unsafe_allow_html=True)


# ============================================
# SESSION STATE INITIALIZATION
# ============================================

def init_session_state():
    """Initialize session state variables"""
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = None
    if "scenario_planner" not in st.session_state:
        st.session_state.scenario_planner = ScenarioPlanner()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_scenario" not in st.session_state:
        st.session_state.current_scenario = None
    if "initialized" not in st.session_state:
        st.session_state.initialized = False


def initialize_system():
    """Initialize the AI system"""
    if st.session_state.orchestrator is None:
        with st.spinner("🔄 Menginisialisasi sistem AI..."):
            try:
                st.session_state.orchestrator = AgentOrchestrator()
                result = st.session_state.orchestrator.initialize()
                st.session_state.initialized = True
                return result
            except Exception as e:
                st.error(f"Error initializing system: {str(e)}")
                return None
    return {"status": "already_initialized"}


def render_sidebar():
    """Render sidebar with LABBAIK branding and navigation"""
    with st.sidebar:
        sidebar_header = f"""
<div style="text-align: center; padding: 25px 15px; border-bottom: 1px solid #333; margin-bottom: 15px;">
    <div style="font-family: 'Noto Naskh Arabic', serif; font-size: 2rem; color: {COLORS['gold']}; text-shadow: 0 2px 10px rgba(212, 175, 55, 0.3);">{BRAND['arabic']}</div>
    <div style="font-size: 1.3rem; font-weight: 700; color: white; letter-spacing: 0.25em; margin-top: 5px;">{BRAND['name']}</div>
    <div style="font-size: 0.8rem; color: {COLORS['sand']}; margin-top: 8px; font-style: italic;">{BRAND['tagline']}</div>
    <div style="margin-top: 10px;">
        <span style="background: linear-gradient(135deg, {COLORS['gold']} 0%, {COLORS['sand']} 100%); color: {COLORS['black']}; padding: 3px 10px; border-radius: 12px; font-size: 0.7rem; font-weight: 600;">v{BRAND['version']}</span>
    </div>
</div>
"""
        st.markdown(sidebar_header, unsafe_allow_html=True)
        
        init_user_database()
        init_monetization_state()
        render_user_badge()
        
        st.markdown("---")
        
        user = get_current_user()
        
        if not is_logged_in():
            nav_items = [
                "🏠 Beranda",
                "ℹ️ Tentang Aplikasi",
                "🔐 Login / Register",
            ]
        else:
            nav_items = [
                "🏠 Beranda",
                "💰 Simulasi Biaya",
                "💵 Cari Paket by Budget",
                "🤝 Umrah Bareng",
                "📊 Perbandingan Skenario",
                "📅 Analisis Waktu",
                "🤖 Chat AI",
                "📋 Buat Rencana",
                "✈️ Booking & Reservasi",
                "🧰 Tools & Fitur",
            ]
            
            if user and user.get("role") in ["admin", "superadmin"]:
                nav_items.append("📊 Analytics")
                nav_items.append("💼 Business Hub")
                nav_items.append("🛡️ Admin Dashboard")
            
            nav_items.append("👤 Profil Saya")
            nav_items.extend([
                "⚙️ Pengaturan",
                "ℹ️ Tentang Aplikasi"
            ])
        
        page = st.radio("📍 Navigasi", nav_items)
        
        st.markdown("---")
        render_quick_quote_widget()
        st.markdown("---")
        
        quick_info = f"""
<div style="background: rgba(212, 175, 55, 0.1); padding: 12px; border-radius: 10px; border: 1px solid {COLORS['gold']}40;">
    <div style="font-size: 0.85rem; font-weight: 600; color: {COLORS['gold']}; margin-bottom: 8px;">📌 Info Cepat</div>
    <div style="font-size: 0.75rem; color: {COLORS['sand']};">
        <strong>Provider:</strong> {llm_config.provider.upper()}<br>
        <strong>Model:</strong> {llm_config.groq_model if llm_config.provider == 'groq' else llm_config.openai_model}
    </div>
</div>
"""
        st.markdown(quick_info, unsafe_allow_html=True)
        
        if is_logged_in():
            user = get_current_user()
            if user and user.get("role") in ["admin", "superadmin"]:
                st.markdown("---")
                stats = get_visitor_stats()
                visitor_stats_html = f"""
<div style="background: rgba(0, 107, 60, 0.1); padding: 12px; border-radius: 10px; border: 1px solid {COLORS['green']}40;">
    <div style="font-size: 0.85rem; font-weight: 600; color: {COLORS['green']}; margin-bottom: 8px;">📊 Visitor Stats (Real-time)</div>
    <div style="font-size: 0.75rem; color: {COLORS['sand']};">
        <strong>Total:</strong> {stats['total_visitors']:,} visitors<br>
        <strong>Views:</strong> {stats['total_views']:,} page views<br>
        <strong>Today:</strong> {stats['today_visitors']:,} visitors
    </div>
</div>
"""
                st.markdown(visitor_stats_html, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"<div style='font-size: 0.85rem; font-weight: 600; color: {COLORS['gold']};'>💡 Tips</div>", unsafe_allow_html=True)
        tips = [
            "Booking 3-4 bulan sebelumnya untuk harga terbaik",
            "Hindari Ramadhan jika budget terbatas",
            "Pilih hotel dekat Haram untuk jamaah lansia",
            "Bawa obat pribadi yang cukup",
            "Download peta offline sebelum berangkat",
            "Tukar uang ke Riyal sebelum berangkat",
        ]
        st.caption(tips[datetime.now().second % len(tips)])
        
        sidebar_footer = f"""
<div style="text-align: center; padding: 15px 0;">
    <div style="font-family: 'Noto Naskh Arabic', serif; color: {COLORS['gold']}; font-size: 1rem;">{BRAND['arabic']}</div>
    <div style="color: white; font-weight: 600; letter-spacing: 0.15em; font-size: 0.85rem; margin: 5px 0;">{BRAND['name']}</div>
    <div style="color: {COLORS['sand']}; font-size: 0.7rem;">{BRAND['tagline']}</div>
    <div style="color: #666; font-size: 0.65rem; margin-top: 10px;">
        © 2025 {CONTACT['website']}<br>
        Made with ❤️ by {DEVELOPER['name']}
    </div>
</div>
"""
        st.markdown("---")
        st.markdown(sidebar_footer, unsafe_allow_html=True)
        
        return page


def render_home():
    """Render home page with LABBAIK branding"""
    track_page_view("Home")
    
    hero_html = f"""
<div class="labbaik-hero animate-fadeIn">
    <div class="labbaik-arabic">{BRAND['talbiyah']}</div>
    <div class="labbaik-name">{BRAND['name']}</div>
    <div class="labbaik-tagline">{BRAND['tagline']}</div>
    <p style="color: {COLORS['sand']}; margin-top: 15px; font-size: 1.1rem;">{BRAND['description']}</p>
</div>
"""
    st.markdown(hero_html, unsafe_allow_html=True)
    
    stats_bar_html = f"""
<div style="background: {COLORS['black']}; padding: 20px; border-radius: 12px; margin: 20px 0;">
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <td style="text-align: center; padding: 10px;">
                <div style="font-size: 1.5rem;">🤖</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: {COLORS['gold']};">24/7</div>
                <div style="font-size: 0.85rem; color: {COLORS['sand']};">AI Assistant</div>
            </td>
            <td style="text-align: center; padding: 10px;">
                <div style="font-size: 1.5rem;">🏙️</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: {COLORS['gold']};">10+</div>
                <div style="font-size: 0.85rem; color: {COLORS['sand']};">Kota Keberangkatan</div>
            </td>
            <td style="text-align: center; padding: 10px;">
                <div style="font-size: 1.5rem;">📊</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: {COLORS['gold']};">5+</div>
                <div style="font-size: 0.85rem; color: {COLORS['sand']};">Skenario Paket</div>
            </td>
            <td style="text-align: center; padding: 10px;">
                <div style="font-size: 1.5rem;">🆓</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: {COLORS['gold']};">GRATIS</div>
                <div style="font-size: 0.85rem; color: {COLORS['sand']};">Beta Access</div>
            </td>
        </tr>
    </table>
</div>
"""
    st.markdown(stats_bar_html, unsafe_allow_html=True)
    
    if not is_logged_in():
        login_cta = f"""
<div style="background: linear-gradient(135deg, {COLORS['gold']}22, {COLORS['sand']}22); border: 2px solid {COLORS['gold']}; border-radius: 15px; padding: 30px; text-align: center; margin: 30px 0;">
    <h3 style="color: {COLORS['black']}; margin-bottom: 10px;">🔐 Login untuk Akses Penuh</h3>
    <p style="color: {COLORS['gray']};">Daftar GRATIS atau login untuk mengakses semua fitur perencanaan umrah</p>
</div>
"""
        st.markdown(login_cta, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔑 Login / Register Sekarang", type="primary", use_container_width=True):
                st.session_state.nav_to_login = True
                st.rerun()
        
        st.markdown("---")
        st.markdown(f"<h3 style='text-align: center; color: {COLORS['black']}; margin: 30px 0 20px;'>✨ Fitur yang Akan Anda Dapatkan</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""<div class="feature-card"><div class="feature-icon">🤖</div><div class="feature-title">AI Assistant 24/7</div><div class="feature-desc">Tanya apapun tentang umrah, AI siap membantu kapan saja</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="feature-card"><div class="feature-icon">💰</div><div class="feature-title">Simulasi Biaya</div><div class="feature-desc">Hitung estimasi biaya dengan berbagai skenario</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div class="feature-card"><div class="feature-icon">📊</div><div class="feature-title">Bandingkan Paket</div><div class="feature-desc">Bandingkan opsi Ekonomis, Standard, Premium, VIP</div></div>""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""<div class="feature-card"><div class="feature-icon">🤝</div><div class="feature-title">Umrah Bareng</div><div class="feature-desc">Cari teman umrah dengan kriteria yang cocok</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="feature-card"><div class="feature-icon">✈️</div><div class="feature-title">Booking Terintegrasi</div><div class="feature-desc">Pesan tiket pesawat dan hotel dalam satu platform</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div class="feature-card"><div class="feature-icon">🏨</div><div class="feature-title">Hotel & Akomodasi</div><div class="feature-desc">Temukan hotel terbaik di Makkah & Madinah</div></div>""", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"<h3 style='text-align: center; color: {COLORS['black']};'>🌟 Mengapa LABBAIK?</h3>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""<div style="text-align: center; padding: 15px;"><div style="font-size: 2.5rem;">🤖</div><div style="font-weight: 700; color: #1A1A1A;">AI-Powered</div><div style="font-size: 0.85rem; color: #666;">Teknologi AI terdepan</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div style="text-align: center; padding: 15px;"><div style="font-size: 2.5rem;">📊</div><div style="font-weight: 700; color: #1A1A1A;">Data Akurat</div><div style="font-size: 0.85rem; color: #666;">Estimasi biaya real</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div style="text-align: center; padding: 15px;"><div style="font-size: 2.5rem;">🇮🇩</div><div style="font-weight: 700; color: #1A1A1A;">Lokal Indonesia</div><div style="font-size: 0.85rem; color: #666;">Untuk jamaah Indonesia</div></div>""", unsafe_allow_html=True)
        with col4:
            st.markdown("""<div style="text-align: center; padding: 15px;"><div style="font-size: 2.5rem;">💯</div><div style="font-weight: 700; color: #1A1A1A;">100% Gratis</div><div style="font-size: 0.85rem; color: #666;">Daftar tanpa biaya</div></div>""", unsafe_allow_html=True)
        
    else:
        user = get_current_user()
        role_info = get_user_role_info()
        
        welcome_html = f"""
<div style="background: linear-gradient(135deg, {role_info['color']}22, {role_info['color']}11); border-left: 4px solid {role_info['color']}; padding: 15px 20px; border-radius: 0 10px 10px 0; margin-bottom: 20px;">
    <span style="font-size: 1.5rem;">{role_info['badge']}</span>
    <span style="font-weight: 600; margin-left: 10px;">Assalamualaikum, {user.get('name', 'User')}!</span>
    <span style="color: {COLORS['gray']}; margin-left: 10px;">({role_info['name']})</span>
</div>
"""
        st.markdown(welcome_html, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='color: {COLORS['black']}; margin: 20px 0;'>✨ Fitur Utama</h3>", unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown("""<div class="feature-card"><div class="feature-icon">🤖</div><div class="feature-title">AI Assistant</div><div class="feature-desc">Tanya apapun tentang umrah</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="feature-card"><div class="feature-icon">💰</div><div class="feature-title">Simulasi Biaya</div><div class="feature-desc">Hitung estimasi biaya</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div class="feature-card"><div class="feature-icon">💵</div><div class="feature-title">Cari by Budget</div><div class="feature-desc">Paket sesuai dana</div></div>""", unsafe_allow_html=True)
        with col4:
            st.markdown("""<div class="feature-card"><div class="feature-icon">🤝</div><div class="feature-title">Umrah Bareng</div><div class="feature-desc">Cari teman umrah</div></div>""", unsafe_allow_html=True)
        with col5:
            st.markdown("""<div class="feature-card"><div class="feature-icon">📊</div><div class="feature-title">Bandingkan</div><div class="feature-desc">Ekonomis - VIP</div></div>""", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"### 🚀 Mulai Perencanaan Umrah Anda")
        
        col1, col2 = st.columns(2)
        with col1:
            scenario = st.selectbox("Pilih Skenario", ["ekonomis", "standard", "premium", "vip"], format_func=lambda x: SCENARIO_TEMPLATES[x]["name"])
        with col2:
            num_people = st.number_input("Jumlah Jamaah", min_value=1, max_value=50, value=1)
        
        if st.button("🔍 Lihat Estimasi Cepat", use_container_width=True):
            planner = st.session_state.scenario_planner
            result = planner.create_scenario(scenario, num_people)
            
            st.markdown("### 📋 Estimasi Cepat")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Estimasi Minimum", format_currency(result.estimated_min))
            with col2:
                st.metric("Estimasi Maksimum", format_currency(result.estimated_max))
            with col3:
                st.metric("Per Orang", format_currency(result.estimated_min / num_people))
            
            st.markdown("#### ✨ Fasilitas Termasuk:")
            for feature in result.features:
                st.markdown(f"• {feature}")


def render_cost_simulation():
    """Render cost simulation page"""
    st.header("💰 Simulasi Biaya Umrah")
    
    with st.form("cost_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            scenario = st.selectbox("Skenario Paket", ["ekonomis", "standard", "premium", "vip"], format_func=lambda x: SCENARIO_TEMPLATES[x]["name"])
            num_people = st.number_input("Jumlah Jamaah", min_value=1, max_value=50, value=2)
            duration = st.slider("Durasi (hari)", min_value=7, max_value=21, value=SCENARIO_TEMPLATES[scenario]["duration_days"])
        
        with col2:
            departure_city = st.selectbox("Kota Keberangkatan", DEPARTURE_CITIES)
            departure_month = st.selectbox("Bulan Keberangkatan", range(1, 13), format_func=lambda x: ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"][x-1])
            special_requests = st.text_area("Permintaan Khusus (opsional)", placeholder="Misal: jamaah lansia, butuh kursi roda, dll.")
        
        submitted = st.form_submit_button("🔍 Hitung Biaya", use_container_width=True)
    
    if submitted:
        with st.spinner("⏳ Menghitung estimasi biaya..."):
            planner = st.session_state.scenario_planner
            result = planner.create_scenario(scenario_type=scenario, num_people=num_people, duration_days=duration, departure_month=departure_month)
            st.session_state.current_scenario = result
        
        st.markdown("---")
        st.subheader("📊 Hasil Simulasi")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Minimum", format_currency(result.estimated_min))
        with col2:
            st.metric("Total Maksimum", format_currency(result.estimated_max))
        with col3:
            st.metric("Per Orang (Min)", format_currency(result.estimated_min / num_people))
        with col4:
            avg = (result.estimated_min + result.estimated_max) / 2
            st.metric("Rata-rata Total", format_currency(avg))
        
        season_info = None
        for season in SEASONS.values():
            if departure_month in season["months"]:
                season_info = season
                break
        
        if season_info and season_info["multiplier"] > 1:
            st.markdown(f"""<div class="warning-box">⚠️ <strong>Perhatian:</strong> Bulan {departure_month} termasuk musim {season_info['name']} dengan kenaikan harga sekitar {int((season_info['multiplier']-1)*100)}%</div>""", unsafe_allow_html=True)
        
        st.markdown("### 📈 Visualisasi Biaya")
        
        components = [
            {"Komponen": "Tiket Pesawat", "Estimasi": result.estimated_max * 0.25},
            {"Komponen": "Hotel Makkah", "Estimasi": result.estimated_max * 0.30},
            {"Komponen": "Hotel Madinah", "Estimasi": result.estimated_max * 0.15},
            {"Komponen": "Makan", "Estimasi": result.estimated_max * 0.10},
            {"Komponen": "Transportasi", "Estimasi": result.estimated_max * 0.08},
            {"Komponen": "Visa & Handling", "Estimasi": result.estimated_max * 0.07},
            {"Komponen": "Lainnya", "Estimasi": result.estimated_max * 0.05},
        ]
        df = pd.DataFrame(components)
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(df, values="Estimasi", names="Komponen", title="Distribusi Biaya", color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(df, x="Komponen", y="Estimasi", title="Breakdown per Komponen", color="Komponen", color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### ✨ Fasilitas Termasuk")
        cols = st.columns(2)
        for i, feature in enumerate(result.features):
            cols[i % 2].markdown(f"✅ {feature}")
        
        if result.notes:
            st.markdown("### 📝 Catatan")
            for note in result.notes:
                st.markdown(note)


def render_scenario_comparison():
    """Render scenario comparison page"""
    st.header("📊 Perbandingan Skenario")
    
    col1, col2 = st.columns(2)
    with col1:
        num_people = st.number_input("Jumlah Jamaah", min_value=1, max_value=50, value=1, key="compare_people")
    with col2:
        duration = st.slider("Durasi (hari)", min_value=7, max_value=21, value=12, key="compare_duration")
    
    if st.button("🔍 Bandingkan Semua Skenario", use_container_width=True):
        planner = st.session_state.scenario_planner
        
        scenarios_data = []
        for stype in ["ekonomis", "standard", "premium", "vip"]:
            scenario = planner.create_scenario(scenario_type=stype, num_people=num_people, duration_days=duration)
            scenarios_data.append({
                "Skenario": SCENARIO_TEMPLATES[stype]["name"],
                "Hotel Makkah": f"⭐ {scenario.hotel_star_makkah}",
                "Hotel Madinah": f"⭐ {scenario.hotel_star_madinah}",
                "Jarak ke Haram": scenario.hotel_distance_makkah,
                "Makan": scenario.meal_type.replace("_", " ").title(),
                "Min (Rp)": scenario.estimated_min,
                "Max (Rp)": scenario.estimated_max,
            })
        
        df = pd.DataFrame(scenarios_data)
        
        st.markdown("### 📋 Tabel Perbandingan")
        st.dataframe(df.style.format({"Min (Rp)": "{:,.0f}", "Max (Rp)": "{:,.0f}"}), use_container_width=True)
        
        st.markdown("### 💰 Perbandingan Harga")
        fig = go.Figure()
        for scenario in scenarios_data:
            fig.add_trace(go.Bar(name=scenario["Skenario"], x=[scenario["Skenario"]], y=[(scenario["Min (Rp)"] + scenario["Max (Rp)"]) / 2], error_y=dict(type='data', symmetric=False, array=[scenario["Max (Rp)"] - (scenario["Min (Rp)"] + scenario["Max (Rp)"]) / 2], arrayminus=[(scenario["Min (Rp)"] + scenario["Max (Rp)"]) / 2 - scenario["Min (Rp)"]])))
        fig.update_layout(title="Range Harga per Skenario", yaxis_title="Estimasi Biaya (Rp)", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""<div class="highlight-box"><h4>💡 Rekomendasi</h4><ul><li><strong>Budget < Rp 35 juta:</strong> Pilih Ekonomis</li><li><strong>Keseimbangan:</strong> Pilih Standard</li><li><strong>Prioritas Kenyamanan:</strong> Pilih Premium</li><li><strong>Pengalaman Terbaik:</strong> Pilih VIP</li></ul></div>""", unsafe_allow_html=True)


def render_time_analysis():
    """Render time analysis page"""
    st.header("📅 Analisis Waktu Terbaik Umrah")
    
    priority = st.selectbox("Prioritas Anda", ["balanced", "cost", "crowd"], format_func=lambda x: {"balanced": "🎯 Seimbang (Harga & Keramaian)", "cost": "💰 Prioritas Hemat Biaya", "crowd": "👥 Prioritas Hindari Keramaian"}[x])
    
    if st.button("📊 Analisis Waktu Terbaik", use_container_width=True):
        planner = st.session_state.scenario_planner
        analysis = planner.analyze_best_time(priority)
        
        st.markdown("### ✅ Bulan Terbaik untuk Umrah")
        cols = st.columns(3)
        for i, month_data in enumerate(analysis["best_months"]):
            with cols[i]:
                st.markdown(f"""<div class="success-box"><h4>#{i+1} {month_data['month_name']}</h4><p>🌡️ Cuaca: {month_data['weather']}</p><p>💰 Multiplier: {month_data['price_multiplier']}x</p><p>👥 Keramaian: {month_data['crowd_level']}</p></div>""", unsafe_allow_html=True)
        
        st.markdown("### ⚠️ Bulan yang Perlu Dipertimbangkan")
        cols = st.columns(3)
        for i, month_data in enumerate(analysis["avoid_months"]):
            with cols[i]:
                st.markdown(f"""<div class="warning-box"><h4>{month_data['month_name']}</h4><p>🌡️ Cuaca: {month_data['weather']}</p><p>💰 Multiplier: {month_data['price_multiplier']}x</p><p>👥 Keramaian: {month_data['crowd_level']}</p></div>""", unsafe_allow_html=True)
        
        st.markdown("### 📈 Analisis Sepanjang Tahun")
        df = pd.DataFrame(analysis["analysis"])
        fig = px.line(df, x="month_name", y="recommendation_score", title="Skor Rekomendasi per Bulan", markers=True)
        fig.update_layout(xaxis_title="Bulan", yaxis_title="Skor Rekomendasi")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 💡 Tips")
        for note in analysis["notes"]:
            st.markdown(f"• {note}")


def render_ai_chat():
    """Render AI chat page"""
    st.header("🤖 Chat dengan AI Assistant")
    
    if st.session_state.orchestrator is None:
        st.warning("⚠️ Sistem AI belum diinisialisasi.")
        if st.button("🔄 Inisialisasi Sistem"):
            initialize_system()
            st.rerun()
        return
    
    st.markdown("Tanyakan apa saja tentang umrah kepada AI Assistant!")
    
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])
    
    if prompt := st.chat_input("Ketik pertanyaan Anda..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        with st.spinner("🤔 AI sedang berpikir..."):
            try:
                response = st.session_state.orchestrator.chat(prompt)
                ai_response = response["response"]
            except Exception as e:
                ai_response = f"Maaf, terjadi error: {str(e)}"
        
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        st.chat_message("assistant").write(ai_response)
    
    st.markdown("---")
    st.markdown("### 💡 Pertanyaan Cepat")
    
    quick_questions = ["Apa saja rukun umrah?", "Bagaimana tips hemat biaya umrah?", "Kapan waktu terbaik untuk umrah?", "Apa yang harus dipersiapkan sebelum umrah?", "Bagaimana memilih travel umrah yang terpercaya?"]
    
    cols = st.columns(2)
    for i, q in enumerate(quick_questions):
        if cols[i % 2].button(q, key=f"quick_{i}"):
            st.session_state.chat_history.append({"role": "user", "content": q})
            st.rerun()
    
    if st.button("🗑️ Hapus Riwayat Chat"):
        st.session_state.chat_history = []
        if st.session_state.orchestrator:
            st.session_state.orchestrator.reset_conversations()
        st.rerun()


def render_create_plan():
    """Render create plan page with Makkah/Madinah duration selection - v3.1.0"""
    st.header("📋 Buat Rencana Umrah Lengkap")
    
    if st.session_state.orchestrator is None:
        st.warning("⚠️ Sistem AI belum diinisialisasi.")
        if st.button("🔄 Inisialisasi Sistem"):
            initialize_system()
            st.rerun()
        return
    
    st.markdown("### 📝 Detail Perjalanan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        scenario = st.selectbox("Skenario Paket", ["ekonomis", "standard", "premium", "vip"], format_func=lambda x: SCENARIO_TEMPLATES[x]["name"], key="plan_scenario")
        num_people = st.number_input("Jumlah Jamaah", min_value=1, max_value=50, value=2, key="plan_num_people")
        departure_month = st.selectbox("Bulan Keberangkatan", range(1, 13), format_func=lambda x: ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"][x-1], key="plan_departure_month")
    
    with col2:
        st.markdown("#### 🕋 Durasi Menginap")
        nights_makkah = st.slider("🕋 Lama di Mekkah (malam)", min_value=2, max_value=10, value=4, key="nights_makkah", help="Pilih jumlah malam menginap di Mekkah")
        nights_madinah = st.slider("🕌 Lama di Madinah (malam)", min_value=2, max_value=10, value=3, key="nights_madinah", help="Pilih jumlah malam menginap di Madinah")
        total_duration = nights_makkah + nights_madinah + 2
        st.info(f"📅 **Total Durasi:** {total_duration} hari ({nights_makkah} malam Mekkah + {nights_madinah} malam Madinah + 2 hari transit)")
    
    st.markdown("---")
    st.markdown("### 💰 Preview Biaya Akomodasi")
    
    hotel_makkah = HOTEL_PRICES[scenario]["makkah"]
    hotel_madinah = HOTEL_PRICES[scenario]["madinah"]
    additional = ADDITIONAL_COSTS[scenario]
    
    cost_makkah = hotel_makkah["price"] * nights_makkah
    cost_madinah = hotel_madinah["price"] * nights_madinah
    cost_accommodation = cost_makkah + cost_madinah
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""<div style="background: #fff3e0; padding: 15px; border-radius: 10px; border-left: 4px solid #e65100;"><div style="font-weight: 700; color: #e65100; margin-bottom: 8px;">🕋 Hotel Mekkah</div><div style="font-size: 0.85rem; color: #666; margin-bottom: 5px;">{hotel_makkah['name']}</div><div style="font-size: 0.8rem; color: #888;">Rp {hotel_makkah['price']:,}/malam × {nights_makkah} malam</div><div style="font-size: 1.2rem; font-weight: 700; color: #e65100; margin-top: 8px;">Rp {cost_makkah:,}</div></div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""<div style="background: #e8f5e9; padding: 15px; border-radius: 10px; border-left: 4px solid #2e7d32;"><div style="font-weight: 700; color: #2e7d32; margin-bottom: 8px;">🕌 Hotel Madinah</div><div style="font-size: 0.85rem; color: #666; margin-bottom: 5px;">{hotel_madinah['name']}</div><div style="font-size: 0.8rem; color: #888;">Rp {hotel_madinah['price']:,}/malam × {nights_madinah} malam</div><div style="font-size: 1.2rem; font-weight: 700; color: #2e7d32; margin-top: 8px;">Rp {cost_madinah:,}</div></div>""", unsafe_allow_html=True)
    
    with col3:
        total_accommodation = cost_accommodation * num_people
        st.markdown(f"""<div style="background: linear-gradient(135deg, #1A1A1A 0%, #333 100%); padding: 15px; border-radius: 10px;"><div style="font-weight: 700; color: #D4AF37; margin-bottom: 8px;">💰 Total Akomodasi</div><div style="font-size: 0.85rem; color: #C9A86C; margin-bottom: 5px;">Per orang: Rp {cost_accommodation:,}</div><div style="font-size: 0.8rem; color: #888;">× {num_people} jamaah</div><div style="font-size: 1.2rem; font-weight: 700; color: #D4AF37; margin-top: 8px;">Rp {total_accommodation:,}</div></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    special_requests = st.text_area("Permintaan Khusus", placeholder="Misal: jamaah lansia, butuh kursi roda, vegetarian, dll.", key="plan_special_requests")
    
    if st.button("🚀 Buat Rencana Lengkap", use_container_width=True, type="primary"):
        with st.spinner("⏳ AI sedang menyusun rencana lengkap..."):
            try:
                duration_info = f"\n\nDurasi menginap:\n- Mekkah: {nights_makkah} malam\n- Madinah: {nights_madinah} malam\n- Total: {total_duration} hari"
                enhanced_requests = (special_requests or "") + duration_info
                
                result = st.session_state.orchestrator.create_complete_plan(scenario=scenario, num_people=num_people, duration_days=total_duration, departure_month=departure_month, special_requests=enhanced_requests if enhanced_requests.strip() else None)
                
                st.markdown("---")
                st.success("✅ Rencana berhasil dibuat!")
                
                st.markdown("### 📊 Ringkasan Perjalanan")
                sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
                with sum_col1:
                    st.metric("👥 Jamaah", f"{num_people} orang")
                with sum_col2:
                    st.metric("🕋 Mekkah", f"{nights_makkah} malam")
                with sum_col3:
                    st.metric("🕌 Madinah", f"{nights_madinah} malam")
                with sum_col4:
                    st.metric("📅 Total", f"{total_duration} hari")
                
                st.markdown("### 💰 Rincian Biaya Per Orang")
                
                flight_cost = additional["flight"]
                visa_cost = additional["visa"]
                transport_cost = additional["transport"]
                meals_cost = additional["meals"] * total_duration
                
                total_per_person = cost_accommodation + flight_cost + visa_cost + transport_cost + meals_cost
                grand_total = total_per_person * num_people
                
                cost_items = [("✈️ Tiket Pesawat PP", flight_cost), ("🕋 Hotel Mekkah", cost_makkah), ("🕌 Hotel Madinah", cost_madinah), ("📄 Visa & Handling", visa_cost), ("🚐 Transportasi Lokal", transport_cost), (f"🍽️ Makan ({total_duration} hari)", meals_cost)]
                
                for item_name, item_cost in cost_items:
                    st.markdown(f"""<div style="display: flex; justify-content: space-between; padding: 8px 12px; background: #f9f9f9; border-radius: 5px; margin: 4px 0;"><span>{item_name}</span><span style="font-weight: 600;">Rp {item_cost:,}</span></div>""", unsafe_allow_html=True)
                
                st.markdown("---")
                total_col1, total_col2 = st.columns(2)
                with total_col1:
                    st.markdown(f"""<div style="background: #e3f2fd; padding: 20px; border-radius: 10px; text-align: center;"><div style="font-size: 0.9rem; color: #1565c0;">Per Orang</div><div style="font-size: 1.8rem; font-weight: 700; color: #1565c0;">Rp {total_per_person:,}</div></div>""", unsafe_allow_html=True)
                with total_col2:
                    st.markdown(f"""<div style="background: linear-gradient(135deg, #1A1A1A 0%, #333 100%); padding: 20px; border-radius: 10px; text-align: center;"><div style="font-size: 0.9rem; color: #D4AF37;">GRAND TOTAL ({num_people} orang)</div><div style="font-size: 1.8rem; font-weight: 700; color: #D4AF37;">Rp {grand_total:,}</div></div>""", unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 💡 Analisis AI - Keuangan")
                if "calculation" in result["results"]["financial"]:
                    calc = result["results"]["financial"]["calculation"]
                    ai_col1, ai_col2 = st.columns(2)
                    with ai_col1:
                        st.metric("Estimasi AI Min", format_currency(calc["total_min"]))
                    with ai_col2:
                        st.metric("Estimasi AI Max", format_currency(calc["total_max"]))
                st.markdown(result["results"]["financial"]["response"])
                
                st.markdown("### 📅 Itinerary")
                st.markdown(result["results"]["itinerary"]["response"])
                
                st.markdown("### 📋 Persyaratan")
                st.markdown(result["results"]["requirements"]["response"])
                
                st.markdown("### 💡 Tips")
                st.markdown(result["results"]["tips"]["response"])
                
            except Exception as e:
                st.error(f"Error: {str(e)}")


def render_budget_finder():
    """Render budget finder page - Find packages based on available budget v3.1.0"""
    st.header("💵 Cari Paket Sesuai Budget")
    st.markdown("Masukkan dana yang Anda miliki, kami akan carikan paket terbaik untuk Anda!")
    
    # Budget input
    col1, col2 = st.columns(2)
    
    with col1:
        budget = st.number_input(
            "💰 Budget Anda (Rp)",
            min_value=10_000_000,
            max_value=500_000_000,
            value=35_000_000,
            step=1_000_000,
            format="%d",
            help="Masukkan total dana yang Anda siapkan untuk umrah"
        )
    
    with col2:
        num_people = st.number_input(
            "👥 Jumlah Jamaah",
            min_value=1,
            max_value=50,
            value=1,
            help="Berapa orang yang akan berangkat?"
        )
    
    budget_per_person = budget / num_people
    
    st.markdown("---")
    
    # Display budget per person
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1A1A1A 0%, #333 100%); padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;">
        <div style="color: #C9A86C; font-size: 0.9rem;">Budget Per Orang</div>
        <div style="color: #D4AF37; font-size: 2rem; font-weight: 700;">Rp {budget_per_person:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Analyze what packages are available
    st.markdown("### 📊 Analisis Paket yang Tersedia")
    
    # Package thresholds (minimum budget per person for each scenario)
    PACKAGE_THRESHOLDS = {
        "ekonomis": {
            "min_budget": 20_000_000,
            "max_budget": 35_000_000,
            "base_duration": 9,  # minimum days
            "max_duration": 12,
        },
        "standard": {
            "min_budget": 35_000_000,
            "max_budget": 50_000_000,
            "base_duration": 9,
            "max_duration": 14,
        },
        "premium": {
            "min_budget": 50_000_000,
            "max_budget": 80_000_000,
            "base_duration": 10,
            "max_duration": 14,
        },
        "vip": {
            "min_budget": 80_000_000,
            "max_budget": 200_000_000,
            "base_duration": 12,
            "max_duration": 21,
        }
    }
    
    available_packages = []
    partial_packages = []
    
    # Hotel star mapping for each scenario
    HOTEL_STARS = {
        "ekonomis": "2-3",
        "standard": "3-4", 
        "premium": "4-5",
        "vip": "5"
    }
    
    for scenario_key, threshold in PACKAGE_THRESHOLDS.items():
        template = SCENARIO_TEMPLATES[scenario_key]
        hotel_makkah = HOTEL_PRICES[scenario_key]["makkah"]
        hotel_madinah = HOTEL_PRICES[scenario_key]["madinah"]
        additional = ADDITIONAL_COSTS[scenario_key]
        hotel_star = HOTEL_STARS.get(scenario_key, "3")
        
        # Calculate minimum cost for this package (base duration)
        base_nights_makkah = 4
        base_nights_madinah = 3
        base_total_days = base_nights_makkah + base_nights_madinah + 2
        
        min_accommodation = (hotel_makkah["price"] * base_nights_makkah) + (hotel_madinah["price"] * base_nights_madinah)
        min_total = min_accommodation + additional["flight"] + additional["visa"] + additional["transport"] + (additional["meals"] * base_total_days)
        
        # Calculate maximum possible duration with this budget
        if budget_per_person >= min_total:
            # Calculate how many extra nights can be afforded
            remaining_budget = budget_per_person - min_total
            extra_night_cost = hotel_makkah["price"] + additional["meals"]  # Cost per extra night
            extra_nights = int(remaining_budget / extra_night_cost)
            max_possible_nights = min(base_nights_makkah + base_nights_madinah + extra_nights, threshold["max_duration"] - 2)
            
            # Distribute extra nights
            extra_makkah = min(extra_nights // 2, 6)  # Max 10 nights in Makkah
            extra_madinah = min(extra_nights - extra_makkah, 7)  # Max 10 nights in Madinah
            
            final_makkah = base_nights_makkah + extra_makkah
            final_madinah = base_nights_madinah + extra_madinah
            final_duration = final_makkah + final_madinah + 2
            
            # Recalculate actual cost
            actual_accommodation = (hotel_makkah["price"] * final_makkah) + (hotel_madinah["price"] * final_madinah)
            actual_total = actual_accommodation + additional["flight"] + additional["visa"] + additional["transport"] + (additional["meals"] * final_duration)
            
            available_packages.append({
                "scenario": scenario_key,
                "name": template["name"],
                "hotel_star": hotel_star,
                "nights_makkah": final_makkah,
                "nights_madinah": final_madinah,
                "duration": final_duration,
                "total_cost": actual_total,
                "remaining": budget_per_person - actual_total,
                "hotel_makkah": hotel_makkah["name"],
                "hotel_madinah": hotel_madinah["name"],
                "features": ["Visa Umrah", "Transportasi", "Muthawwif", "Air Zamzam 5L"],
                "flight_class": "Economy" if scenario_key in ["ekonomis", "standard"] else "Business" if scenario_key == "vip" else "Economy Plus",
                "meals": "Prasmanan" if scenario_key in ["ekonomis"] else "Buffet Hotel" if scenario_key == "standard" else "Full Board Premium",
            })
        elif budget_per_person >= threshold["min_budget"] * 0.7:
            # Partial - almost enough
            shortage = min_total - budget_per_person
            partial_packages.append({
                "scenario": scenario_key,
                "name": template["name"],
                "shortage": shortage,
                "min_required": min_total,
            })
    
    # Display available packages
    if available_packages:
        st.success(f"✅ **{len(available_packages)} Paket Tersedia** untuk budget Anda!")
        
        for i, pkg in enumerate(available_packages):
            # Determine card color based on scenario
            colors = {
                "ekonomis": ("#4CAF50", "#E8F5E9"),
                "standard": ("#2196F3", "#E3F2FD"),
                "premium": ("#FF9800", "#FFF3E0"),
                "vip": ("#D4AF37", "#FFF8E1"),
            }
            accent_color, bg_color = colors.get(pkg["scenario"], ("#666", "#f5f5f5"))
            
            st.markdown(f"""
            <div style="background: {bg_color}; border: 2px solid {accent_color}; border-radius: 15px; padding: 20px; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <div>
                        <span style="background: {accent_color}; color: white; padding: 5px 15px; border-radius: 20px; font-weight: 700;">
                            {'🌟' if pkg['scenario'] == 'vip' else '⭐' if pkg['scenario'] == 'premium' else '✨'} {pkg['name']}
                        </span>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 0.8rem; color: #666;">Estimasi Biaya/Orang</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: {accent_color};">Rp {pkg['total_cost']:,.0f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Package details in columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                **🕋 Mekkah**  
                {pkg['nights_makkah']} malam  
                _{pkg['hotel_makkah'][:30]}..._
                """)
            
            with col2:
                st.markdown(f"""
                **🕌 Madinah**  
                {pkg['nights_madinah']} malam  
                _{pkg['hotel_madinah'][:30]}..._
                """)
            
            with col3:
                st.markdown(f"""
                **📅 Durasi**  
                {pkg['duration']} hari  
                _Termasuk transit_
                """)
            
            with col4:
                if pkg['remaining'] > 0:
                    st.markdown(f"""
                    **💰 Sisa Budget**  
                    Rp {pkg['remaining']:,.0f}  
                    _Untuk oleh-oleh_
                    """)
                else:
                    st.markdown(f"""
                    **💰 Status**  
                    Pas Budget  
                    _Sesuai dana_
                    """)
            
            # Expandable details
            with st.expander(f"📋 Lihat Detail Paket {pkg['name']}"):
                detail_col1, detail_col2 = st.columns(2)
                
                with detail_col1:
                    st.markdown("**✈️ Penerbangan**")
                    st.markdown(f"- Kelas: {pkg['flight_class']}")
                    st.markdown(f"- Rute: PP Indonesia - Jeddah/Madinah")
                    
                    st.markdown("**🏨 Akomodasi**")
                    st.markdown(f"- Hotel Bintang: ⭐ {pkg['hotel_star']}")
                    st.markdown(f"- Mekkah: {pkg['hotel_makkah']}")
                    st.markdown(f"- Madinah: {pkg['hotel_madinah']}")
                
                with detail_col2:
                    st.markdown("**🍽️ Konsumsi**")
                    st.markdown(f"- Tipe: {pkg['meals']}")
                    st.markdown(f"- {pkg['duration']} hari full board")
                    
                    st.markdown("**📦 Termasuk**")
                    st.markdown("- ✅ Visa Umrah")
                    st.markdown("- ✅ Transportasi lokal")
                    st.markdown("- ✅ Muthawwif/Guide")
                    st.markdown("- ✅ Air Zamzam 5L")
                
                # Cost breakdown
                st.markdown("---")
                st.markdown("**💰 Rincian Biaya Per Orang:**")
                
                additional = ADDITIONAL_COSTS[pkg["scenario"]]
                hotel_m = HOTEL_PRICES[pkg["scenario"]]["makkah"]["price"] * pkg["nights_makkah"]
                hotel_d = HOTEL_PRICES[pkg["scenario"]]["madinah"]["price"] * pkg["nights_madinah"]
                
                breakdown_data = [
                    ("✈️ Tiket Pesawat PP", additional["flight"]),
                    ("🕋 Hotel Mekkah", hotel_m),
                    ("🕌 Hotel Madinah", hotel_d),
                    ("📄 Visa & Handling", additional["visa"]),
                    ("🚐 Transportasi", additional["transport"]),
                    (f"🍽️ Makan ({pkg['duration']} hari)", additional["meals"] * pkg["duration"]),
                ]
                
                for item, cost in breakdown_data:
                    st.markdown(f"- {item}: **Rp {cost:,.0f}**")
                
                st.markdown(f"**TOTAL: Rp {pkg['total_cost']:,.0f}**")
            
            st.markdown("---")
        
        # Summary for multiple people
        if num_people > 1:
            best_pkg = available_packages[0]  # Recommend the first available (usually ekonomis)
            total_for_group = best_pkg["total_cost"] * num_people
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1A1A1A 0%, #333 100%); padding: 25px; border-radius: 15px; margin-top: 20px;">
                <div style="text-align: center;">
                    <div style="color: #C9A86C; font-size: 1rem; margin-bottom: 10px;">💡 Rekomendasi untuk {num_people} Jamaah</div>
                    <div style="color: white; font-size: 1.2rem; margin-bottom: 15px;">Paket <strong style="color: #D4AF37;">{best_pkg['name']}</strong></div>
                    <table style="margin: 0 auto; color: white;">
                        <tr>
                            <td style="padding: 10px 30px; text-align: center;">
                                <div style="font-size: 0.8rem; color: #888;">Per Orang</div>
                                <div style="font-size: 1.3rem; font-weight: 700; color: #D4AF37;">Rp {best_pkg['total_cost']:,.0f}</div>
                            </td>
                            <td style="padding: 10px 30px; text-align: center;">
                                <div style="font-size: 0.8rem; color: #888;">Total {num_people} Orang</div>
                                <div style="font-size: 1.3rem; font-weight: 700; color: #D4AF37;">Rp {total_for_group:,.0f}</div>
                            </td>
                            <td style="padding: 10px 30px; text-align: center;">
                                <div style="font-size: 0.8rem; color: #888;">Sisa Budget</div>
                                <div style="font-size: 1.3rem; font-weight: 700; color: #4CAF50;">Rp {budget - total_for_group:,.0f}</div>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # No packages available
        st.warning("⚠️ Budget belum mencukupi untuk paket umrah reguler.")
        
        # Show what's needed
        min_ekonomis = 20_000_000
        shortage = min_ekonomis - budget_per_person
        
        st.markdown(f"""
        <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 20px; border-radius: 0 10px 10px 0;">
            <h4 style="color: #e65100; margin-top: 0;">💡 Saran untuk Anda</h4>
            <p>Budget per orang: <strong>Rp {budget_per_person:,.0f}</strong></p>
            <p>Minimum untuk Paket Ekonomis: <strong>Rp {min_ekonomis:,.0f}</strong></p>
            <p>Kekurangan: <strong style="color: #e65100;">Rp {shortage:,.0f}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📈 Opsi yang Bisa Anda Lakukan:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **💰 Tambah Tabungan**
            - Target tambahan: Rp {:,.0f}
            - Jika menabung Rp 1 juta/bulan: {} bulan lagi
            - Jika menabung Rp 2 juta/bulan: {} bulan lagi
            """.format(
                shortage,
                int(shortage / 1_000_000) + 1,
                int(shortage / 2_000_000) + 1
            ))
        
        with col2:
            st.markdown("""
            **🤝 Opsi Lain**
            - Cari promo early bird
            - Berangkat di low season (Januari-Februari)
            - Gabung dengan grup besar untuk diskon
            - Cicilan dari travel agent
            """)
        
        # Show partial packages (almost affordable)
        if partial_packages:
            st.markdown("### 📦 Paket yang Hampir Terjangkau")
            for pkg in partial_packages:
                st.info(f"**{pkg['name']}** - Kurang Rp {pkg['shortage']:,.0f} (Minimum: Rp {pkg['min_required']:,.0f})")
    
    # Tips section
    st.markdown("---")
    st.markdown("### 💡 Tips Mendapatkan Harga Terbaik")
    
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.markdown("""
        **🗓️ Waktu Booking**
        - Book 3-4 bulan sebelumnya
        - Hindari musim haji & Ramadhan
        - Cari promo akhir tahun
        
        **✈️ Penerbangan**
        - Flexible date = harga lebih murah
        - Transit 1x bisa hemat 20-30%
        - Cek berbagai maskapai
        """)
    
    with tips_col2:
        st.markdown("""
        **🏨 Akomodasi**
        - Hotel agak jauh = lebih murah
        - Sharing room untuk hemat
        - Weekday lebih murah dari weekend
        
        **👥 Grup**
        - Grup 10+ orang dapat diskon
        - Gabung open trip
        - Tanya promo travel agent
        """)


# ============================================
# UMRAH BARENG - OPEN TRIP FEATURE
# ============================================

def init_umrah_bareng_state():
    """Initialize Umrah Bareng session state"""
    if "open_trips" not in st.session_state:
        # Sample data for demonstration
        st.session_state.open_trips = [
            {
                "id": "OT001",
                "creator_name": "Ahmad Fauzi",
                "creator_phone": "+62812xxxx1234",
                "creator_city": "Jakarta",
                "title": "Umrah Bareng Keluarga Muda",
                "departure_date": "2025-03-15",
                "departure_city": "Jakarta (CGK)",
                "package_type": "standard",
                "budget_per_person": 38000000,
                "duration_days": 12,
                "nights_makkah": 5,
                "nights_madinah": 4,
                "current_members": 4,
                "max_members": 10,
                "gender_preference": "Campuran (Keluarga)",
                "age_preference": "25-40 tahun",
                "special_notes": "Fokus ibadah, tidak banyak shopping. Ada anak kecil.",
                "amenities": ["Muthawwif Indonesia", "Kursi Roda Tersedia", "Menu Indonesia"],
                "status": "open",
                "created_at": "2025-01-15",
                "whatsapp_group": "https://chat.whatsapp.com/xxx",
            },
            {
                "id": "OT002",
                "creator_name": "Hj. Siti Aminah",
                "creator_phone": "+62813xxxx5678",
                "creator_city": "Surabaya",
                "title": "Umrah Khusus Ibu-Ibu",
                "departure_date": "2025-04-10",
                "departure_city": "Surabaya (SUB)",
                "package_type": "premium",
                "budget_per_person": 55000000,
                "duration_days": 14,
                "nights_makkah": 6,
                "nights_madinah": 5,
                "current_members": 8,
                "max_members": 15,
                "gender_preference": "Wanita Only",
                "age_preference": "40+ tahun",
                "special_notes": "Tempo santai, banyak ziarah. Cocok untuk lansia.",
                "amenities": ["Ustadzah Pendamping", "Hotel Dekat Haram", "Wheelchair Friendly"],
                "status": "open",
                "created_at": "2025-01-10",
                "whatsapp_group": "https://chat.whatsapp.com/yyy",
            },
            {
                "id": "OT003",
                "creator_name": "Rizky Pratama",
                "creator_phone": "+62857xxxx9012",
                "creator_city": "Bandung",
                "title": "Umrah Backpacker Style",
                "departure_date": "2025-02-20",
                "departure_city": "Jakarta (CGK)",
                "package_type": "ekonomis",
                "budget_per_person": 25000000,
                "duration_days": 9,
                "nights_makkah": 4,
                "nights_madinah": 3,
                "current_members": 3,
                "max_members": 8,
                "gender_preference": "Pria Only",
                "age_preference": "20-35 tahun",
                "special_notes": "Budget terbatas tapi semangat tinggi! Siap jalan kaki.",
                "amenities": ["Guide Lokal", "Sharing Room"],
                "status": "open",
                "created_at": "2025-01-20",
                "whatsapp_group": "https://chat.whatsapp.com/zzz",
            },
        ]


def render_umrah_bareng():
    """Render Umrah Bareng (Open Trip) feature"""
    init_umrah_bareng_state()
    
    st.header("🤝 Umrah Bareng - Open Trip")
    st.markdown("Cari teman perjalanan umrah atau buat open trip sendiri!")
    
    # Stats bar
    total_trips = len(st.session_state.open_trips)
    open_trips = len([t for t in st.session_state.open_trips if t["status"] == "open"])
    total_slots = sum([t["max_members"] - t["current_members"] for t in st.session_state.open_trips if t["status"] == "open"])
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1A1A1A 0%, #333 100%); padding: 20px; border-radius: 15px; margin-bottom: 20px;">
        <table style="width: 100%; color: white;">
            <tr>
                <td style="text-align: center; padding: 10px;">
                    <div style="font-size: 2rem; font-weight: 700; color: #D4AF37;">{total_trips}</div>
                    <div style="font-size: 0.85rem; color: #C9A86C;">Total Open Trip</div>
                </td>
                <td style="text-align: center; padding: 10px;">
                    <div style="font-size: 2rem; font-weight: 700; color: #4CAF50;">{open_trips}</div>
                    <div style="font-size: 0.85rem; color: #C9A86C;">Masih Tersedia</div>
                </td>
                <td style="text-align: center; padding: 10px;">
                    <div style="font-size: 2rem; font-weight: 700; color: #2196F3;">{total_slots}</div>
                    <div style="font-size: 0.85rem; color: #C9A86C;">Slot Kosong</div>
                </td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Cari Open Trip", "➕ Buat Open Trip", "📋 Trip Saya"])
    
    # ===== TAB 1: CARI OPEN TRIP =====
    with tab1:
        st.markdown("### 🔍 Cari Open Trip yang Cocok")
        
        # Filters
        with st.expander("🎯 Filter Pencarian", expanded=True):
            filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
            
            with filter_col1:
                filter_budget = st.select_slider(
                    "💰 Budget Maksimal",
                    options=[20, 30, 40, 50, 60, 80, 100],
                    value=50,
                    format_func=lambda x: f"Rp {x} juta"
                )
            
            with filter_col2:
                filter_package = st.selectbox(
                    "📦 Tipe Paket",
                    options=["Semua", "ekonomis", "standard", "premium", "vip"],
                    format_func=lambda x: "Semua Paket" if x == "Semua" else SCENARIO_TEMPLATES.get(x, {}).get("name", x.title())
                )
            
            with filter_col3:
                filter_gender = st.selectbox(
                    "👥 Preferensi Gender",
                    options=["Semua", "Campuran (Keluarga)", "Pria Only", "Wanita Only"]
                )
            
            with filter_col4:
                filter_city = st.selectbox(
                    "🏙️ Kota Keberangkatan",
                    options=["Semua"] + DEPARTURE_CITIES
                )
        
        # Filter results
        filtered_trips = st.session_state.open_trips.copy()
        
        if filter_budget:
            filtered_trips = [t for t in filtered_trips if t["budget_per_person"] <= filter_budget * 1_000_000]
        
        if filter_package != "Semua":
            filtered_trips = [t for t in filtered_trips if t["package_type"] == filter_package]
        
        if filter_gender != "Semua":
            filtered_trips = [t for t in filtered_trips if t["gender_preference"] == filter_gender]
        
        if filter_city != "Semua":
            filtered_trips = [t for t in filtered_trips if filter_city in t["departure_city"]]
        
        # Only show open trips
        filtered_trips = [t for t in filtered_trips if t["status"] == "open"]
        
        st.markdown(f"**Ditemukan {len(filtered_trips)} open trip**")
        st.markdown("---")
        
        # Display trips
        if filtered_trips:
            for trip in filtered_trips:
                slots_left = trip["max_members"] - trip["current_members"]
                progress = trip["current_members"] / trip["max_members"]
                
                # Package colors
                pkg_colors = {
                    "ekonomis": ("#4CAF50", "🟢"),
                    "standard": ("#2196F3", "🔵"),
                    "premium": ("#FF9800", "🟠"),
                    "vip": ("#D4AF37", "🟡"),
                }
                pkg_color, pkg_emoji = pkg_colors.get(trip["package_type"], ("#666", "⚪"))
                
                st.markdown(f"""
                <div style="background: white; border: 2px solid {pkg_color}; border-radius: 15px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
                        <div>
                            <span style="background: {pkg_color}; color: white; padding: 3px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;">
                                {pkg_emoji} {SCENARIO_TEMPLATES.get(trip['package_type'], {}).get('name', trip['package_type'].title())}
                            </span>
                            <h3 style="margin: 10px 0 5px 0; color: #1A1A1A;">{trip['title']}</h3>
                            <p style="color: #666; margin: 0; font-size: 0.9rem;">oleh {trip['creator_name']} • {trip['creator_city']}</p>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.8rem; color: #888;">Budget/Orang</div>
                            <div style="font-size: 1.4rem; font-weight: 700; color: {pkg_color};">Rp {trip['budget_per_person']:,}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Trip details
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"📅 **Berangkat**\n\n{trip['departure_date']}")
                
                with col2:
                    st.markdown(f"✈️ **Dari**\n\n{trip['departure_city']}")
                
                with col3:
                    st.markdown(f"⏱️ **Durasi**\n\n{trip['duration_days']} hari")
                
                with col4:
                    st.markdown(f"👥 **Slot**\n\n{trip['current_members']}/{trip['max_members']} ({slots_left} sisa)")
                
                # Progress bar
                st.progress(progress)
                
                # Expandable details
                with st.expander("📋 Lihat Detail & Gabung"):
                    detail_col1, detail_col2 = st.columns(2)
                    
                    with detail_col1:
                        st.markdown("**🕋 Itinerary:**")
                        st.markdown(f"- Mekkah: {trip['nights_makkah']} malam")
                        st.markdown(f"- Madinah: {trip['nights_madinah']} malam")
                        
                        st.markdown("**👥 Preferensi:**")
                        st.markdown(f"- Gender: {trip['gender_preference']}")
                        st.markdown(f"- Usia: {trip['age_preference']}")
                    
                    with detail_col2:
                        st.markdown("**✨ Fasilitas Khusus:**")
                        for amenity in trip["amenities"]:
                            st.markdown(f"- ✅ {amenity}")
                        
                        st.markdown("**📝 Catatan:**")
                        st.markdown(f"_{trip['special_notes']}_")
                    
                    st.markdown("---")
                    
                    # Contact buttons
                    btn_col1, btn_col2, btn_col3 = st.columns(3)
                    
                    with btn_col1:
                        st.markdown(f"[💬 Hubungi via WhatsApp](https://wa.me/{trip['creator_phone'].replace('+', '')}?text=Halo%20kak,%20saya%20tertarik%20dengan%20open%20trip%20{trip['title']})")
                    
                    with btn_col2:
                        if trip.get("whatsapp_group"):
                            st.markdown(f"[👥 Join Grup WA]({trip['whatsapp_group']})")
                    
                    with btn_col3:
                        if st.button(f"❤️ Simpan Trip", key=f"save_{trip['id']}"):
                            st.success("Trip disimpan!")
                
                st.markdown("---")
        else:
            st.info("🔍 Tidak ada open trip yang sesuai filter. Coba ubah kriteria pencarian atau buat open trip sendiri!")
    
    # ===== TAB 2: BUAT OPEN TRIP =====
    with tab2:
        st.markdown("### ➕ Buat Open Trip Baru")
        st.markdown("Ajak jamaah lain untuk umrah bareng dengan kriteria yang Anda tentukan!")
        
        with st.form("create_open_trip"):
            st.markdown("#### 📝 Informasi Dasar")
            
            col1, col2 = st.columns(2)
            
            with col1:
                trip_title = st.text_input(
                    "Judul Open Trip *",
                    placeholder="Contoh: Umrah Bareng Keluarga Muda"
                )
                
                creator_name = st.text_input(
                    "Nama Anda *",
                    placeholder="Nama yang akan ditampilkan"
                )
                
                creator_phone = st.text_input(
                    "No. WhatsApp *",
                    placeholder="+62812xxxxxxxx"
                )
            
            with col2:
                creator_city = st.selectbox(
                    "Kota Anda *",
                    options=["Jakarta", "Surabaya", "Bandung", "Medan", "Makassar", "Semarang", "Yogyakarta", "Lainnya"]
                )
                
                departure_city = st.selectbox(
                    "Kota Keberangkatan *",
                    options=DEPARTURE_CITIES
                )
                
                departure_date = st.date_input(
                    "Tanggal Keberangkatan *",
                    min_value=datetime.now()
                )
            
            st.markdown("---")
            st.markdown("#### 📦 Detail Paket")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                package_type = st.selectbox(
                    "Tipe Paket *",
                    options=["ekonomis", "standard", "premium", "vip"],
                    format_func=lambda x: SCENARIO_TEMPLATES[x]["name"]
                )
                
                budget_per_person = st.number_input(
                    "Budget per Orang (Rp) *",
                    min_value=20_000_000,
                    max_value=200_000_000,
                    value=35_000_000,
                    step=1_000_000
                )
            
            with col2:
                duration_days = st.number_input(
                    "Durasi (hari) *",
                    min_value=7,
                    max_value=21,
                    value=12
                )
                
                nights_makkah = st.number_input(
                    "Malam di Mekkah *",
                    min_value=2,
                    max_value=10,
                    value=5
                )
            
            with col3:
                nights_madinah = st.number_input(
                    "Malam di Madinah *",
                    min_value=2,
                    max_value=10,
                    value=4
                )
                
                max_members = st.number_input(
                    "Maksimal Peserta *",
                    min_value=2,
                    max_value=50,
                    value=10
                )
            
            st.markdown("---")
            st.markdown("#### 👥 Preferensi Peserta")
            
            col1, col2 = st.columns(2)
            
            with col1:
                gender_preference = st.selectbox(
                    "Preferensi Gender",
                    options=["Campuran (Keluarga)", "Pria Only", "Wanita Only"]
                )
                
                age_preference = st.selectbox(
                    "Rentang Usia",
                    options=["Semua Usia", "20-35 tahun", "25-40 tahun", "35-50 tahun", "40+ tahun", "50+ tahun"]
                )
            
            with col2:
                amenities = st.multiselect(
                    "Fasilitas Khusus",
                    options=[
                        "Muthawwif Indonesia",
                        "Ustadz/Ustadzah Pendamping",
                        "Hotel Dekat Haram",
                        "Kursi Roda Tersedia",
                        "Wheelchair Friendly",
                        "Menu Indonesia",
                        "Sharing Room",
                        "Private Room",
                        "City Tour",
                        "Oleh-oleh Tour"
                    ]
                )
            
            special_notes = st.text_area(
                "Catatan Khusus",
                placeholder="Jelaskan lebih detail tentang trip Anda...",
                max_chars=500
            )
            
            whatsapp_group = st.text_input(
                "Link Grup WhatsApp (opsional)",
                placeholder="https://chat.whatsapp.com/..."
            )
            
            st.markdown("---")
            
            submitted = st.form_submit_button("🚀 Buat Open Trip", use_container_width=True)
            
            if submitted:
                if trip_title and creator_name and creator_phone:
                    # Create new trip
                    new_trip = {
                        "id": f"OT{len(st.session_state.open_trips) + 1:03d}",
                        "creator_name": creator_name,
                        "creator_phone": creator_phone,
                        "creator_city": creator_city,
                        "title": trip_title,
                        "departure_date": str(departure_date),
                        "departure_city": departure_city,
                        "package_type": package_type,
                        "budget_per_person": budget_per_person,
                        "duration_days": duration_days,
                        "nights_makkah": nights_makkah,
                        "nights_madinah": nights_madinah,
                        "current_members": 1,  # Creator is first member
                        "max_members": max_members,
                        "gender_preference": gender_preference,
                        "age_preference": age_preference,
                        "special_notes": special_notes,
                        "amenities": amenities,
                        "status": "open",
                        "created_at": str(datetime.now().date()),
                        "whatsapp_group": whatsapp_group,
                    }
                    
                    st.session_state.open_trips.append(new_trip)
                    st.success("✅ Open Trip berhasil dibuat!")
                    st.balloons()
                    
                    st.markdown(f"""
                    <div style="background: #e8f5e9; border: 2px solid #4CAF50; border-radius: 10px; padding: 20px; margin-top: 20px;">
                        <h4 style="color: #2e7d32; margin-top: 0;">🎉 Open Trip Anda Sudah Live!</h4>
                        <p><strong>ID:</strong> {new_trip['id']}</p>
                        <p><strong>Judul:</strong> {new_trip['title']}</p>
                        <p>Jamaah lain sekarang bisa melihat dan bergabung dengan open trip Anda.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("❌ Mohon lengkapi semua field yang wajib (*)")
    
    # ===== TAB 3: TRIP SAYA =====
    with tab3:
        st.markdown("### 📋 Open Trip yang Saya Buat")
        
        user = get_current_user()
        
        if user:
            # Filter trips created by current user (by name for demo)
            my_trips = [t for t in st.session_state.open_trips if t["creator_name"] == user.get("name", "")]
            
            if my_trips:
                for trip in my_trips:
                    slots_left = trip["max_members"] - trip["current_members"]
                    
                    st.markdown(f"""
                    <div style="background: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <strong>{trip['title']}</strong><br>
                                <small>📅 {trip['departure_date']} • 👥 {trip['current_members']}/{trip['max_members']} peserta</small>
                            </div>
                            <div>
                                <span style="background: {'#4CAF50' if trip['status'] == 'open' else '#666'}; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.8rem;">
                                    {'🟢 Open' if trip['status'] == 'open' else '⚫ Closed'}
                                </span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("✏️ Edit", key=f"edit_{trip['id']}"):
                            st.info("Fitur edit akan segera hadir!")
                    with col2:
                        if st.button("🔴 Tutup", key=f"close_{trip['id']}"):
                            trip["status"] = "closed"
                            st.success("Trip ditutup")
                            st.rerun()
                    with col3:
                        if st.button("🗑️ Hapus", key=f"delete_{trip['id']}"):
                            st.session_state.open_trips.remove(trip)
                            st.success("Trip dihapus")
                            st.rerun()
            else:
                st.info("Anda belum membuat open trip. Buat sekarang di tab 'Buat Open Trip'!")
        else:
            st.warning("🔐 Login untuk melihat open trip yang Anda buat.")
    
    # Info section
    st.markdown("---")
    st.markdown("### 💡 Tentang Umrah Bareng")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🤝 Apa itu Umrah Bareng?**
        
        Platform untuk mencari teman perjalanan umrah dengan kriteria yang cocok:
        - Budget yang sama
        - Jadwal yang sesuai
        - Preferensi yang mirip
        - Dapat diskon grup
        """)
    
    with col2:
        st.markdown("""
        **✨ Keuntungan:**
        
        - 💰 Lebih hemat dengan grup
        - 👥 Dapat teman perjalanan
        - 🕋 Ibadah lebih nyaman
        - 📱 Koordinasi mudah via WhatsApp
        """)
    
    st.warning("""
    **⚠️ Disclaimer:** LABBAIK hanya memfasilitasi pertemuan antar calon jamaah. 
    Segala transaksi dan koordinasi dilakukan langsung antar peserta dan travel agent terpilih. 
    Pastikan memilih travel agent resmi berizin.
    """)


def render_settings():
    """Render settings page"""
    st.header("⚙️ Pengaturan")
    
    st.markdown("### 🔑 Konfigurasi API")
    
    provider = st.selectbox("LLM Provider", ["groq", "openai"], index=0 if llm_config.provider == "groq" else 1)
    
    if provider == "groq":
        api_key = st.text_input("Groq API Key", type="password", value=llm_config.groq_api_key[:10] + "..." if llm_config.groq_api_key else "")
        st.info("💡 Dapatkan API key gratis di https://console.groq.com")
    else:
        api_key = st.text_input("OpenAI API Key", type="password", value=llm_config.openai_api_key[:10] + "..." if llm_config.openai_api_key else "")
        st.info("💡 Dapatkan API key di https://platform.openai.com")
    
    st.markdown("### 📊 Status Sistem")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Status Inisialisasi", "✅ Aktif" if st.session_state.initialized else "❌ Belum Aktif")
    with col2:
        if st.session_state.orchestrator:
            stats = st.session_state.orchestrator.get_agent_status()
            st.metric("Dokumen Knowledge Base", stats["rag_retriever"]["total_documents"])
    
    if st.button("🔄 Reinisialisasi Sistem"):
        st.session_state.orchestrator = None
        st.session_state.initialized = False
        initialize_system()
        st.rerun()
    
    st.markdown("### ℹ️ Informasi Aplikasi")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"""**{APP_INFO['name']}** v{__version__}\n\n{APP_INFO['tagline']}\n\n**Developer:** {DEVELOPER['name']}\n**Email:** {DEVELOPER['email']}""")
    with col2:
        st.info(f"""**Repository:**\n{APP_INFO['repository']}\n\n**Demo:**\n{APP_INFO['demo_url']}\n\n**License:** {APP_INFO['license']}""")


def render_about():
    """Render about page with LABBAIK branding"""
    
    about_header = f"""
<div style="background: linear-gradient(135deg, {COLORS['black']} 0%, #2D2D2D 50%, {COLORS['black']} 100%); color: white; padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 30px;">
    <div style="font-family: 'Noto Naskh Arabic', serif; font-size: 2.5rem; color: {COLORS['gold']}; text-shadow: 0 2px 15px rgba(212, 175, 55, 0.4);">{BRAND['talbiyah']}</div>
    <div style="font-size: 2rem; font-weight: 700; letter-spacing: 0.3em; margin: 15px 0;">{BRAND['name']}</div>
    <div style="color: {COLORS['sand']}; font-size: 1.1rem; margin-bottom: 15px;">{BRAND['tagline']}</div>
    <div style="color: {COLORS['sand']}; font-size: 0.95rem;">{BRAND['description']}</div>
    <div style="margin-top: 20px;"><span style="background: linear-gradient(135deg, {COLORS['gold']} 0%, {COLORS['sand']} 100%); color: {COLORS['black']}; padding: 8px 20px; border-radius: 20px; font-weight: 700;">Version {BRAND['version']}</span></div>
</div>
"""
    st.markdown(about_header, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["👨‍💻 Developer", "📋 Changelog", "🔧 Tech Stack", "📊 Stats"])
    
    with tab1:
        st.markdown(get_developer_card(), unsafe_allow_html=True)
        st.markdown("### 📧 Kontak")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"📧 **Email**\n\n{DEVELOPER['email']}")
        with col2:
            st.markdown(f"💬 **WhatsApp**\n\n[Chat](https://wa.me/{DEVELOPER['whatsapp']})")
        with col3:
            st.markdown(f"🔗 **GitHub**\n\n[mshadianto]({DEVELOPER['github']})")
        with col4:
            st.markdown(f"💼 **LinkedIn**\n\n[Profile]({DEVELOPER['linkedin']})")
    
    with tab2:
        st.markdown(get_changelog_markdown())
    
    with tab3:
        st.markdown("### 🔧 Technology Stack")
        for category, techs in TECH_STACK.items():
            st.markdown(f"#### {category.replace('_', ' ').title()}")
            for name, version, desc in techs:
                st.markdown(f"- **{name}** `{version}` - {desc}")
    
    with tab4:
        st.markdown("### 📊 Application Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📅 Released", get_app_age())
        with col2:
            st.metric("🔄 Version", __version__)
        with col3:
            st.metric("📦 Modules", "8+")


def render_labbaik_footer():
    """Render LABBAIK branded footer"""
    stats = get_visitor_stats()
    visitor_str = f"{stats['total_visitors']:,}"
    views_str = f"{stats['total_views']:,}"
    
    st.markdown("""<div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); padding: 40px 40px 0 40px; border-radius: 20px 20px 0 0; text-align: center; margin-top: 50px;"><div style="font-family: 'Noto Naskh Arabic', serif; font-size: 1.8rem; color: #D4AF37;">لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ</div><div style="font-size: 1.3rem; font-weight: 700; color: white; letter-spacing: 0.25em; margin: 12px 0;">LABBAIK</div><div style="color: #C9A86C; font-size: 0.95rem; margin-bottom: 20px;">Panggilan-Nya, Langkahmu</div></div>""", unsafe_allow_html=True)
    
    st.markdown(f"""<div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); padding: 0 40px; text-align: center;"><table style="margin: 0 auto; border-collapse: separate; border-spacing: 20px 0;"><tr><td style="background: rgba(212, 175, 55, 0.15); padding: 12px 24px; border-radius: 20px; text-align: center;"><div style="color: #D4AF37; font-size: 0.75rem; opacity: 0.8;">Total Pengunjung</div><div style="color: #D4AF37; font-size: 1.5rem; font-weight: 700;">{visitor_str}</div></td><td style="background: rgba(0, 107, 60, 0.15); padding: 12px 24px; border-radius: 20px; text-align: center;"><div style="color: #C9A86C; font-size: 0.75rem; opacity: 0.8;">Total Page Views</div><div style="color: #C9A86C; font-size: 1.5rem; font-weight: 700;">{views_str}</div></td></tr></table></div>""", unsafe_allow_html=True)
    
    st.markdown("""<div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); padding: 20px 40px; text-align: center;"><div style="color: #888; font-size: 0.85rem;">📧 sopian.hadianto@gmail.com | 📱 +62 815 9658 833 | 🌐 labbaik.ai</div></div>""", unsafe_allow_html=True)
    
    st.markdown("""<div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); padding: 0 40px; text-align: center;"><div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px 20px; margin: 0 auto; max-width: 600px;"><div style="color: #D4AF37; font-size: 0.8rem; font-weight: 600; margin-bottom: 8px;">⚠️ Disclaimer</div><div style="color: #aaa; font-size: 0.75rem; line-height: 1.6;">Aplikasi ini dikembangkan oleh non-developer dengan memanfaatkan teknologi AI (Claude, Gemini, dll). Informasi yang disajikan bersifat simulasi dan estimasi. Untuk keputusan perjalanan umrah, selalu konsultasikan dengan travel agent resmi berizin.</div></div></div>""", unsafe_allow_html=True)
    
    st.markdown("""<div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); padding: 20px 40px 40px 40px; border-radius: 0 0 20px 20px; text-align: center;"><div style="border-top: 1px solid #333; padding-top: 20px; color: #666; font-size: 0.8rem;">© 2025 LABBAIK. Hak Cipta Dilindungi.<br><span style="color: #D4AF37;">Made with ❤️ &amp; AI by MS Hadianto</span><br><span style="color: #555; font-size: 0.7rem;">v3.1.0 Beta • Powered by Streamlit &amp; Groq AI</span></div></div>""", unsafe_allow_html=True)


def render_user_profile():
    """Render user profile page"""
    user = get_current_user()
    
    if not user:
        st.warning("🔐 Silakan login untuk melihat profil")
        render_login_page()
        return
    
    st.header("👤 Profil Saya")
    role_info = get_user_role_info()
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""<div style="background: linear-gradient(135deg, {role_info['color']}88, {role_info['color']}44); padding: 2rem; border-radius: 15px; text-align: center; border: 3px solid {role_info['color']};"><div style="font-size: 4rem;">{role_info['badge']}</div><h2>{user['name']}</h2><p style="color: {role_info['color']}; font-weight: bold;">{role_info['name']}</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("### 📋 Informasi Akun")
        st.markdown(f"""| Field | Value |\n|-------|-------|\n| **Username** | @{user['username']} |\n| **Email** | {user['email']} |\n| **Phone** | {user.get('phone', '-')} |\n| **Member Since** | {user.get('created_at', '-')[:10]} |\n| **Last Login** | {user.get('last_login', '-')[:16] if user.get('last_login') else '-'} |\n| **Status** | {'✅ Active' if user.get('status') == 'active' else '❌ Inactive'} |""")
    
    st.markdown("---")
    if st.button("🚪 Logout", type="secondary"):
        logout_user()
        st.rerun()


def main():
    """Main application entry point"""
    init_session_state()
    
    if "show_login_page" not in st.session_state:
        st.session_state.show_login_page = False
    
    if st.session_state.get("nav_to_login"):
        st.session_state.nav_to_login = False
        st.session_state.show_login_page = True
    
    if st.session_state.show_login_page and not is_logged_in():
        st.markdown(f"""<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, {COLORS['black']} 0%, #2D2D2D 100%); border-radius: 10px; margin-bottom: 20px;"><div style="font-family: 'Noto Naskh Arabic', serif; font-size: 1.5rem; color: {COLORS['gold']};">{BRAND['arabic']}</div><div style="font-size: 1rem; font-weight: 700; color: white; letter-spacing: 0.2em;">{BRAND['name']}</div></div>""", unsafe_allow_html=True)
        render_login_page()
        if st.button("← Kembali ke Beranda"):
            st.session_state.show_login_page = False
            st.rerun()
        return
    
    if is_logged_in():
        st.session_state.show_login_page = False
    
    page = render_sidebar()
    
    if not st.session_state.initialized:
        if llm_config.groq_api_key or llm_config.openai_api_key:
            initialize_system()
    
    if "Beranda" in page:
        render_home()
        render_labbaik_footer()
    elif "Simulasi Biaya" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Cost Simulation")
            render_cost_simulation()
    elif "Cari Paket by Budget" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Budget Finder")
            render_budget_finder()
    elif "Umrah Bareng" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Umrah Bareng")
            render_umrah_bareng()
    elif "Perbandingan" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Scenario Comparison")
            render_scenario_comparison()
    elif "Analisis Waktu" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Time Analysis")
            render_time_analysis()
    elif "Chat AI" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("AI Chat")
            render_ai_chat()
    elif "Buat Rencana" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Create Plan")
            render_create_plan()
    elif "Booking" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Booking")
            st.markdown(f"""<div style="text-align: center; margin-bottom: 20px;"><span style="font-family: 'Noto Naskh Arabic', serif; color: {COLORS['gold']}; font-size: 1.5rem;">{BRAND['arabic']}</span><span style="font-weight: 700; letter-spacing: 0.15em; margin-left: 10px;">{BRAND['name']}</span></div>""", unsafe_allow_html=True)
            st.header("✈️ Booking & Reservasi")
            render_booking_features()
    elif "Tools" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Tools")
            st.markdown(f"""<div style="text-align: center; margin-bottom: 20px;"><span style="font-family: 'Noto Naskh Arabic', serif; color: {COLORS['gold']}; font-size: 1.5rem;">{BRAND['arabic']}</span><span style="font-weight: 700; letter-spacing: 0.15em; margin-left: 10px;">{BRAND['name']}</span></div>""", unsafe_allow_html=True)
            st.header("🧰 Tools & Fitur Jamaah")
            render_additional_features()
    elif "Analytics" in page:
        user = get_current_user()
        if not user or user.get("role") not in ["admin", "superadmin"]:
            st.error("🚫 Akses Ditolak")
        else:
            track_page_view("Analytics")
            st.header("📊 Analytics Dashboard")
            render_analytics_dashboard()
    elif "Business" in page:
        user = get_current_user()
        if not user or user.get("role") not in ["admin", "superadmin"]:
            st.error("🚫 Akses Ditolak")
        else:
            track_page_view("Business Hub")
            st.header("💼 Business Hub")
            render_monetization_page()
    elif "Login" in page:
        track_page_view("Login")
        render_login_page()
    elif "Admin" in page:
        track_page_view("Admin Dashboard")
        render_admin_dashboard()
    elif "Profil" in page:
        track_page_view("Profile")
        render_user_profile()
    elif "Pengaturan" in page:
        track_page_view("Settings")
        render_settings()
    elif "Tentang" in page:
        track_page_view("About")
        render_about()
        render_labbaik_footer()


if __name__ == "__main__":
    main()
