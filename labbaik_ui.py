"""
================================================================================
لَبَّيْكَ LABBAIK - Brand UI Components
================================================================================

Simple, ready-to-use UI components for LABBAIK branding.
Just import and use - no complex setup required.

Usage:
    from labbaik_ui import inject_brand_css, render_sidebar_brand, render_footer

Copyright (c) 2025 MS Hadianto. All Rights Reserved.
================================================================================
"""

import streamlit as st

# ============================================
# BRAND CONSTANTS
# ============================================

BRAND_NAME = "LABBAIK"
BRAND_ARABIC = "لَبَّيْكَ"
BRAND_TAGLINE = "Panggilan-Nya, Langkahmu"
BRAND_DESCRIPTION = "Platform AI Perencanaan Umrah #1 Indonesia"

# Colors
BLACK = "#1A1A1A"
GOLD = "#D4AF37"
GREEN = "#006B3C"
WHITE = "#FFFFFF"
SAND = "#C9A86C"

# Contact
EMAIL = "sopian.hadianto@gmail.com"
WHATSAPP = "+62 815 9658 833"
WEBSITE = "labbaik.ai"

# ============================================
# CSS INJECTION
# ============================================

def inject_brand_css():
    """Inject LABBAIK brand CSS into Streamlit app"""
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Noto+Naskh+Arabic:wght@400;600&display=swap');
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {BLACK} 0%, #2D2D2D 100%);
    }}
    
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    /* Gold buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {GOLD} 0%, {SAND} 100%);
        color: {BLACK};
        border: none;
        border-radius: 25px;
        font-weight: 600;
    }}
    
    .stButton > button:hover {{
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
        transform: translateY(-2px);
    }}
    
    /* Metrics gold */
    [data-testid="stMetricValue"] {{
        color: {GOLD} !important;
        font-weight: 700;
    }}
    
    /* Tabs */
    .stTabs [aria-selected="true"] {{
        background: {GOLD};
        color: {BLACK};
    }}
    
    /* Brand header class */
    .labbaik-header {{
        background: linear-gradient(135deg, {BLACK} 0%, #2D2D2D 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }}
    
    .labbaik-arabic {{
        font-family: 'Noto Naskh Arabic', serif;
        font-size: 2.5rem;
        color: {GOLD};
        text-shadow: 0 2px 10px rgba(212, 175, 55, 0.3);
    }}
    
    .labbaik-name {{
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        letter-spacing: 0.3em;
        margin-top: 8px;
    }}
    
    .labbaik-tagline {{
        color: {SAND};
        font-size: 0.9rem;
        margin-top: 8px;
    }}
    
    /* Card styling */
    .labbaik-card {{
        background: white;
        border-radius: 15px;
        padding: 20px;
        border: 2px solid #E0E0E0;
        transition: all 0.3s ease;
    }}
    
    .labbaik-card:hover {{
        border-color: {GOLD};
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.15);
    }}
    
    /* Gold accent text */
    .gold-text {{
        color: {GOLD};
        font-weight: 600;
    }}
    </style>
    """, unsafe_allow_html=True)

# ============================================
# UI COMPONENTS
# ============================================

def render_sidebar_brand():
    """Render brand header in sidebar"""
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 15px; border-bottom: 1px solid #333; margin-bottom: 15px;">
        <div style="font-family: 'Noto Naskh Arabic', serif; font-size: 1.8rem; color: {GOLD};">
            {BRAND_ARABIC}
        </div>
        <div style="font-size: 1.2rem; font-weight: 700; color: white; letter-spacing: 0.25em; margin-top: 5px;">
            {BRAND_NAME}
        </div>
        <div style="font-size: 0.75rem; color: {SAND}; margin-top: 8px;">
            {BRAND_TAGLINE}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_page_header(title: str = None, subtitle: str = None):
    """Render branded page header"""
    title = title or f"🕋 {BRAND_NAME}"
    subtitle = subtitle or BRAND_DESCRIPTION
    
    st.markdown(f"""
    <div class="labbaik-header">
        <div class="labbaik-arabic">{BRAND_ARABIC}</div>
        <div class="labbaik-name">{BRAND_NAME}</div>
        <div class="labbaik-tagline">{BRAND_TAGLINE}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #666;'>{subtitle}</p>", unsafe_allow_html=True)

def render_simple_header():
    """Render simple text header (less prominent)"""
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <span style="font-family: 'Noto Naskh Arabic', serif; color: {GOLD}; font-size: 1.5rem;">
            {BRAND_ARABIC}
        </span>
        <span style="color: {BLACK}; font-weight: 700; letter-spacing: 0.2em; margin-left: 10px;">
            {BRAND_NAME}
        </span>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Render branded footer"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {BLACK} 0%, #2D2D2D 100%);
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin-top: 40px;
    ">
        <div style="font-family: 'Noto Naskh Arabic', serif; color: {GOLD}; font-size: 1.5rem;">
            {BRAND_ARABIC}
        </div>
        <div style="color: white; font-weight: 700; letter-spacing: 0.25em; margin: 10px 0;">
            {BRAND_NAME}
        </div>
        <div style="color: {SAND}; font-size: 0.9rem; margin-bottom: 15px;">
            {BRAND_TAGLINE}
        </div>
        <div style="color: #888; font-size: 0.8rem;">
            📧 {EMAIL} | 📱 {WHATSAPP} | 🌐 {WEBSITE}
        </div>
        <div style="color: #666; font-size: 0.75rem; margin-top: 15px; border-top: 1px solid #333; padding-top: 15px;">
            © 2025 {BRAND_NAME}. Hak Cipta Dilindungi.
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar_footer():
    """Render compact footer for sidebar"""
    st.markdown(f"""
    <div style="text-align: center; font-size: 0.7rem; color: #888; padding: 15px 0;">
        <span style="color: {GOLD};">لَبَّيْكَ</span> {BRAND_NAME}<br>
        {BRAND_TAGLINE}<br><br>
        © 2025 | v3.0.0
    </div>
    """, unsafe_allow_html=True)

def render_gold_metric(label: str, value: str, delta: str = None):
    """Render a metric with gold styling"""
    delta_html = f"<div style='color: {GREEN}; font-size: 0.8rem;'>{delta}</div>" if delta else ""
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {BLACK} 0%, #2D2D2D 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
    ">
        <div style="color: #999; font-size: 0.85rem;">{label}</div>
        <div style="color: {GOLD}; font-size: 2rem; font-weight: 800;">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def render_feature_card(icon: str, title: str, description: str):
    """Render a feature card"""
    st.markdown(f"""
    <div class="labbaik-card">
        <div style="font-size: 2.5rem; text-align: center;">{icon}</div>
        <h4 style="text-align: center; color: {BLACK}; margin: 10px 0;">{title}</h4>
        <p style="text-align: center; color: #666; font-size: 0.9rem;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_cta_button(text: str = "Mulai Sekarang", url: str = "#"):
    """Render a gold CTA button (HTML version)"""
    st.markdown(f"""
    <div style="text-align: center; margin: 20px 0;">
        <a href="{url}" style="
            display: inline-block;
            background: linear-gradient(135deg, {GOLD} 0%, {SAND} 100%);
            color: {BLACK};
            padding: 15px 40px;
            border-radius: 30px;
            font-weight: 700;
            text-decoration: none;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
            transition: all 0.3s ease;
        ">🕋 {text}</a>
    </div>
    """, unsafe_allow_html=True)

def render_stats_bar():
    """Render statistics bar"""
    col1, col2, col3, col4 = st.columns(4)
    
    stats = [
        ("👥", "15,000+", "Jamaah Terbantu"),
        ("🤝", "50+", "Travel Partner"),
        ("⭐", "4.9", "Rating"),
        ("💰", "30%", "Hemat"),
    ]
    
    for col, (icon, value, label) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div style="
                background: {BLACK};
                padding: 15px;
                border-radius: 10px;
                text-align: center;
            ">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div style="color: {GOLD}; font-size: 1.5rem; font-weight: 800;">{value}</div>
                <div style="color: {SAND}; font-size: 0.75rem;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# PAGE CONFIG HELPER
# ============================================

def get_page_config():
    """Get Streamlit page config for LABBAIK"""
    return {
        "page_title": f"{BRAND_NAME} - {BRAND_DESCRIPTION}",
        "page_icon": "🕋",
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }

# ============================================
# QUICK SETUP FUNCTION
# ============================================

def setup_labbaik_branding():
    """One-line setup for LABBAIK branding"""
    inject_brand_css()
    
def setup_labbaik_sidebar():
    """Setup sidebar with LABBAIK branding"""
    render_sidebar_brand()
