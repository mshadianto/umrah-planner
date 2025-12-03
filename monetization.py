"""
LABBAIK Monetization Module
Handles premium features and sponsorships
"""

import streamlit as st
from typing import Dict, List, Optional
from datetime import datetime


# Sponsorship packages
SPONSORSHIP_TIERS = {
    "bronze": {
        "name": "Bronze Partner",
        "price": 2_500_000,
        "duration": "1 bulan",
        "benefits": [
            "Logo di footer",
            "1 slot featured package",
            "Basic analytics"
        ],
        "color": "#CD7F32"
    },
    "silver": {
        "name": "Silver Partner",
        "price": 5_000_000,
        "duration": "1 bulan",
        "benefits": [
            "Logo di sidebar",
            "3 slot featured package",
            "Priority listing",
            "Monthly report"
        ],
        "color": "#C0C0C0"
    },
    "gold": {
        "name": "Gold Partner",
        "price": 10_000_000,
        "duration": "1 bulan",
        "benefits": [
            "Logo di homepage",
            "5 slot featured package",
            "Top priority listing",
            "Weekly report",
            "Dedicated support",
            "Custom branding"
        ],
        "color": "#FFD700"
    }
}


def render_monetization_sidebar():
    """Render monetization info in sidebar"""
    
    with st.sidebar.expander("💼 Kerjasama Bisnis", expanded=False):
        st.markdown("""
        **Tertarik kerjasama?**
        
        LABBAIK membuka kerjasama dengan:
        - Travel Agent
        - Hotel Partner
        - Sponsor
        
        📧 partner@labbaik.id
        """)


def render_monetization_page():
    """Render full monetization/partnership page"""
    
    st.header("🤝 Kerjasama & Partnership")
    
    st.markdown("""
    LABBAIK membuka kesempatan kerjasama dengan berbagai pihak untuk memberikan 
    layanan terbaik bagi jamaah umrah Indonesia.
    """)
    
    # Partnership tiers
    st.subheader("📊 Paket Kerjasama")
    
    cols = st.columns(3)
    
    for i, (tier_id, tier) in enumerate(SPONSORSHIP_TIERS.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%);
                        border-radius: 15px; padding: 20px; text-align: center;
                        border: 2px solid {tier['color']}40; height: 350px;">
                <div style="font-size: 2rem; margin-bottom: 10px;">
                    {"🥉" if tier_id == "bronze" else "🥈" if tier_id == "silver" else "🥇"}
                </div>
                <div style="color: {tier['color']}; font-size: 1.2rem; font-weight: 700;">
                    {tier['name']}
                </div>
                <div style="color: #D4AF37; font-size: 1.5rem; font-weight: 700; margin: 15px 0;">
                    Rp {tier['price']:,.0f}
                </div>
                <div style="color: #888; font-size: 0.85rem; margin-bottom: 15px;">
                    {tier['duration']}
                </div>
                <div style="text-align: left; color: #E8E8E8; font-size: 0.85rem;">
                    {"".join([f"<div style='margin-bottom: 5px;'>✓ {b}</div>" for b in tier['benefits']])}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Pilih {tier['name']}", key=f"select_{tier_id}", use_container_width=True):
                st.info(f"Untuk memilih {tier['name']}, silakan hubungi partner@labbaik.id")
    
    st.markdown("---")
    
    # Contact form
    st.subheader("📬 Hubungi Kami")
    
    with st.form("partnership_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("🏢 Nama Perusahaan")
            contact_name = st.text_input("👤 Nama Kontak")
        
        with col2:
            email = st.text_input("📧 Email")
            phone = st.text_input("📱 No. Telepon")
        
        partnership_type = st.selectbox(
            "📋 Jenis Kerjasama",
            ["Travel Agent Partner", "Hotel Partner", "Sponsor/Advertiser", "Lainnya"]
        )
        
        message = st.text_area("💬 Pesan")
        
        submitted = st.form_submit_button("📤 Kirim", use_container_width=True)
        
        if submitted:
            if not company_name or not email:
                st.error("Mohon isi nama perusahaan dan email")
            else:
                st.success("✅ Terima kasih! Tim kami akan menghubungi Anda dalam 1x24 jam.")


def render_premium_badge(tier: str = "free"):
    """Render premium badge for users"""
    
    badges = {
        "free": ("🆓", "Free", "#888"),
        "starter": ("⭐", "Starter", "#4CAF50"),
        "pro": ("🌟", "Pro", "#2196F3"),
        "enterprise": ("💎", "Enterprise", "#9C27B0")
    }
    
    icon, name, color = badges.get(tier, badges["free"])
    
    st.markdown(f"""
    <span style="background: {color}20; color: {color}; padding: 3px 10px; 
                 border-radius: 12px; font-size: 0.8rem; font-weight: 600;">
        {icon} {name}
    </span>
    """, unsafe_allow_html=True)


def check_feature_access(feature: str, user_tier: str = "free") -> bool:
    """Check if user has access to a feature based on tier"""
    
    feature_access = {
        "basic_simulation": ["free", "starter", "pro", "enterprise"],
        "ai_assistant": ["free", "starter", "pro", "enterprise"],
        "package_comparison": ["starter", "pro", "enterprise"],
        "detailed_report": ["pro", "enterprise"],
        "api_access": ["enterprise"],
        "white_label": ["enterprise"]
    }
    
    allowed_tiers = feature_access.get(feature, ["enterprise"])
    return user_tier in allowed_tiers


def render_upgrade_prompt(feature_name: str):
    """Render upgrade prompt for locked features"""
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D1F3D 100%);
                border-radius: 15px; padding: 20px; text-align: center;
                border: 2px dashed #9C27B050;">
        <div style="font-size: 2rem; margin-bottom: 10px;">🔒</div>
        <div style="color: white; font-size: 1.1rem; font-weight: 600; margin-bottom: 10px;">
            Fitur {feature_name} Terkunci
        </div>
        <div style="color: #C9A86C; margin-bottom: 15px;">
            Upgrade ke paket Pro untuk mengakses fitur ini
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("⬆️ Upgrade Sekarang", use_container_width=True):
        st.info("Fitur upgrade akan segera tersedia!")
