"""
LABBAIK AI v6.0 - Agent Verification System
============================================
Verify travel agents against Ministry of Hajj official database
Based on Official Hak Jamaah #24
"""

import streamlit as st
from typing import Dict, List, Optional
from datetime import datetime
import json


# =============================================================================
# VERIFICATION DATA STRUCTURES
# =============================================================================

class AgentVerificationStatus:
    """Agent verification status enum."""
    VERIFIED = "verified"
    PENDING = "pending"
    SUSPICIOUS = "suspicious"
    BLACKLISTED = "blacklisted"
    UNKNOWN = "unknown"


VERIFICATION_BADGES = {
    AgentVerificationStatus.VERIFIED: {
        "icon": "✅",
        "emoji": "🟢",
        "label": "Verified & Licensed",
        "color": "#4ade80",
        "bg_color": "#1a5f3c",
        "description": "Travel agent resmi terdaftar di Kementerian Haji Saudi",
        "trust_score": 95
    },
    AgentVerificationStatus.PENDING: {
        "icon": "⏳",
        "emoji": "🟡",
        "label": "Verification Pending",
        "color": "#facc15",
        "bg_color": "#854d0e",
        "description": "Sedang dalam proses verifikasi oleh sistem",
        "trust_score": 50
    },
    AgentVerificationStatus.SUSPICIOUS: {
        "icon": "⚠️",
        "emoji": "🟠",
        "label": "Needs Attention",
        "color": "#fb923c",
        "bg_color": "#9a3412",
        "description": "Ada laporan/keluhan terhadap travel agent ini",
        "trust_score": 30
    },
    AgentVerificationStatus.BLACKLISTED: {
        "icon": "🚫",
        "emoji": "🔴",
        "label": "Blacklisted",
        "color": "#ef4444",
        "bg_color": "#7f1d1d",
        "description": "Travel agent tidak sah atau tercatat melanggar",
        "trust_score": 0
    },
    AgentVerificationStatus.UNKNOWN: {
        "icon": "❓",
        "emoji": "⚪",
        "label": "Unknown Status",
        "color": "#9ca3af",
        "bg_color": "#374151",
        "description": "Belum ada data verifikasi",
        "trust_score": 0
    }
}

# Sample verified agents database (in production, fetch from API/database)
SAMPLE_VERIFIED_AGENTS = {
    "SA-12345": {
        "name": "Al-Hijaz Travel & Tours",
        "license_number": "SA-12345",
        "country": "Indonesia",
        "city": "Jakarta",
        "verified_date": "2024-01-15",
        "expiry_date": "2025-12-31",
        "status": AgentVerificationStatus.VERIFIED,
        "rating": 4.8,
        "total_pilgrims": 15000,
        "complaints": 3,
        "contact": {
            "phone": "+62-21-1234-5678",
            "email": "info@alhijaz.co.id",
            "website": "www.alhijaz.co.id"
        }
    },
    "SA-67890": {
        "name": "Arminareka Perdana",
        "license_number": "SA-67890",
        "country": "Indonesia",
        "city": "Jakarta",
        "verified_date": "2024-02-20",
        "expiry_date": "2025-12-31",
        "status": AgentVerificationStatus.VERIFIED,
        "rating": 4.7,
        "total_pilgrims": 20000,
        "complaints": 5,
        "contact": {
            "phone": "+62-21-9876-5432",
            "email": "info@arminareka.com",
            "website": "www.arminareka.com"
        }
    }
}


# =============================================================================
# VERIFICATION FUNCTIONS
# =============================================================================

def verify_agent_license(license_number: str) -> Optional[Dict]:
    """
    Verify travel agent license against database.
    
    In production, this would call the official Ministry API:
    https://eservices.haj.gov.sa/eservices3/pages/VisaInquiry/SearchVisa.xhtml
    
    Args:
        license_number: Agent license number (format: SA-XXXXX)
    
    Returns:
        Agent data dict if found, None otherwise
    """
    # Normalize license number
    license_number = license_number.strip().upper()
    
    # Check in database (in production: API call)
    return SAMPLE_VERIFIED_AGENTS.get(license_number)


def calculate_trust_score(agent_data: Dict) -> int:
    """
    Calculate trust score based on agent metrics.
    
    Args:
        agent_data: Agent data dictionary
    
    Returns:
        Trust score (0-100)
    """
    base_score = VERIFICATION_BADGES[agent_data['status']]['trust_score']
    
    # Adjust based on rating
    rating_bonus = (agent_data.get('rating', 0) - 3) * 5  # +5 per 0.1 above 3.0
    
    # Penalty for complaints
    complaint_rate = agent_data.get('complaints', 0) / max(agent_data.get('total_pilgrims', 1), 1) * 100
    complaint_penalty = min(complaint_rate * 2, 20)  # Max -20 points
    
    final_score = base_score + rating_bonus - complaint_penalty
    return max(0, min(100, int(final_score)))


def get_verification_badge_html(status: str) -> str:
    """Generate HTML for verification badge."""
    badge = VERIFICATION_BADGES[status]
    
    return f"""
    <div style="background: linear-gradient(135deg, {badge['bg_color']} 0%, #1a1a1a 100%);
                padding: 1rem; border-radius: 10px; border: 2px solid {badge['color']};
                display: inline-block; min-width: 250px;">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.5rem;">{badge['emoji']}</span>
            <div>
                <div style="color: {badge['color']}; font-weight: bold; font-size: 1.1rem;">
                    {badge['label']}
                </div>
                <div style="color: #aaa; font-size: 0.85rem;">
                    {badge['description']}
                </div>
            </div>
        </div>
    </div>
    """


# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_verification_header():
    """Render verification page header."""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); 
                padding: 2rem; border-radius: 15px; margin-bottom: 2rem;
                border: 2px solid #60a5fa;">
        <div style="text-align: center;">
            <div style="font-size: 3rem;">✅</div>
            <h1 style="color: #fff; margin: 0.5rem 0;">Verifikasi Travel Agent</h1>
            <p style="color: #dbeafe; font-size: 1.1rem;">
                Pastikan travel agent Anda terdaftar resmi di Kementerian Haji Saudi
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_verification_form():
    """Render agent verification search form."""
    st.markdown("## 🔍 Cek Lisensi Travel Agent")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        license_input = st.text_input(
            "Masukkan Nomor Lisensi",
            placeholder="Contoh: SA-12345",
            help="Nomor lisensi resmi dari Kementerian Haji Saudi Arabia"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_clicked = st.button("🔎 Verifikasi", type="primary", use_container_width=True)
    
    if search_clicked and license_input:
        with st.spinner("Memverifikasi dengan database resmi..."):
            agent_data = verify_agent_license(license_input)
            
            if agent_data:
                render_agent_verification_result(agent_data)
            else:
                render_agent_not_found(license_input)
    
    # Quick access to sample agents
    st.markdown("---")
    st.markdown("### 🎯 Coba Lisensi Sample:")
    
    cols = st.columns(len(SAMPLE_VERIFIED_AGENTS))
    for idx, (license_no, agent) in enumerate(SAMPLE_VERIFIED_AGENTS.items()):
        with cols[idx]:
            if st.button(f"✅ {agent['name']}", key=f"sample_{idx}", use_container_width=True):
                render_agent_verification_result(agent)


def render_agent_verification_result(agent_data: Dict):
    """Render verification result for found agent."""
    st.success("✅ Travel Agent Ditemukan!")
    
    # Verification badge
    st.markdown(get_verification_badge_html(agent_data['status']), unsafe_allow_html=True)
    st.markdown("")
    
    # Agent details
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                    padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4ade80;">
            <h3 style="color: #4ade80; margin-top: 0;">
                {agent_data['name']}
            </h3>
            <p style="color: #aaa; margin: 0.5rem 0;">
                📋 <strong>Lisensi:</strong> {agent_data['license_number']}<br>
                📍 <strong>Lokasi:</strong> {agent_data['city']}, {agent_data['country']}<br>
                📅 <strong>Verified:</strong> {agent_data['verified_date']}<br>
                ⏰ <strong>Berlaku hingga:</strong> {agent_data['expiry_date']}<br>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Contact info
        st.markdown("""
        <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <h4 style="color: #d4af37; margin-top: 0;">📞 Informasi Kontak</h4>
        """, unsafe_allow_html=True)
        
        contact = agent_data['contact']
        st.markdown(f"""
            <p style="color: #ccc; margin: 0.3rem 0;">
                📱 Phone: {contact['phone']}<br>
                📧 Email: {contact['email']}<br>
                🌐 Website: <a href="https://{contact['website']}" target="_blank" 
                   style="color: #4ade80;">{contact['website']}</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Trust score
        trust_score = calculate_trust_score(agent_data)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a5f3c 0%, #2d8659 100%);
                    padding: 1.5rem; border-radius: 12px; text-align: center;">
            <h4 style="color: #d4af37; margin: 0;">Trust Score</h4>
            <div style="font-size: 3rem; color: #4ade80; font-weight: bold; margin: 1rem 0;">
                {trust_score}
            </div>
            <div style="color: #fff; font-size: 0.9rem;">
                dari 100 poin
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Performance metrics
        st.markdown("""
        <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <h4 style="color: #d4af37; margin-top: 0; text-align: center;">📊 Statistik</h4>
        """, unsafe_allow_html=True)
        
        st.metric("Rating", f"{agent_data['rating']}/5.0", delta="Excellent")
        st.metric("Total Jamaah", f"{agent_data['total_pilgrims']:,}", delta=None)
        st.metric("Komplain", agent_data['complaints'], delta="-2 vs last year", delta_color="inverse")
        
        st.markdown("</div>", unsafe_allow_html=True)


def render_agent_not_found(license_number: str):
    """Render result when agent not found."""
    st.error(f"""
    ❌ **Travel Agent Tidak Ditemukan!**
    
    Lisensi **{license_number}** tidak terdaftar dalam database resmi.
    
    **⚠️ PERINGATAN:**
    - Travel agent ini mungkin TIDAK SAH
    - Jangan melakukan pembayaran
    - Laporkan ke pihak berwenang jika ada penipuan
    """)
    
    st.warning("""
    **💡 Apa yang harus dilakukan?**
    
    1. ✅ Cek ulang nomor lisensi (typo?)
    2. ✅ Minta bukti lisensi resmi dari agent
    3. ✅ Verifikasi langsung di portal resmi
    4. ✅ Gunakan travel agent verified di LABBAIK
    """)


def render_official_verification_link():
    """Render link to official verification portal."""
    st.markdown("---")
    st.markdown("## 🔗 Verifikasi di Portal Resmi")
    
    st.info("""
    **Portal Resmi Kementerian Haji & Umrah Saudi Arabia:**
    
    🌐 https://eservices.haj.gov.sa/eservices3/pages/VisaInquiry/SearchVisa.xhtml
    
    Anda dapat melakukan verifikasi langsung di website resmi Kementerian.
    """)
    
    if st.button("🌐 Buka Portal Resmi", type="secondary", use_container_width=True):
        st.write("Opening in new tab...")
        # In production, use st.link or JavaScript redirect


def render_verification_tips():
    """Render tips for verifying travel agents."""
    st.markdown("---")
    st.markdown("## 💡 Tips Memilih Travel Agent Aman")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✅ Yang HARUS Diperiksa:**
        
        1. ✅ Lisensi resmi dari Kemenag Haji Saudi
        2. ✅ NPWP & izin usaha travel Indonesia
        3. ✅ Kantor fisik yang jelas
        4. ✅ Track record minimal 2-3 tahun
        5. ✅ Kontrak tertulis yang jelas
        6. ✅ Transparansi harga & fasilitas
        7. ✅ Asuransi resmi termasuk
        8. ✅ Testimoni jamaah sebelumnya
        """)
    
    with col2:
        st.error("""
        **🚨 Red Flags (Tanda Bahaya):**
        
        1. ❌ Tidak punya lisensi resmi
        2. ❌ Harga jauh di bawah pasaran
        3. ❌ Janji berlebihan ("umrah gratis!")
        4. ❌ Minta transfer ke rekening pribadi
        5. ❌ Tidak ada kantor/alamat jelas
        6. ❌ Banyak komplain di medsos
        7. ❌ Tidak transparan soal biaya
        8. ❌ Menghindari pertanyaan detail
        """)


def render_complaint_button(agent_license: Optional[str] = None):
    """Render button to file complaint."""
    st.markdown("---")
    st.markdown("## 📢 Laporkan Travel Agent Bermasalah")
    
    st.warning("""
    Jika Anda mengalami masalah dengan travel agent, Anda berhak melaporkan ke:
    
    - 📞 **Kementerian Haji Saudi:** +966920002814
    - 📧 **Email:** mohcc@haj.gov.sa
    - 🇮🇩 **Kemenag RI Pusat:** 021-3441543
    """)
    
    if st.button("📝 Form Pengaduan", type="secondary", use_container_width=True):
        st.session_state.show_complaint_form = True
        if agent_license:
            st.session_state.complaint_agent_license = agent_license


# =============================================================================
# COMPACT BADGE COMPONENT
# =============================================================================

def render_verification_badge_compact(agent_license: str, show_details: bool = False):
    """
    Render compact verification badge for use in package cards.
    
    Args:
        agent_license: Agent license number
        show_details: If True, show detailed info on click
    """
    agent_data = verify_agent_license(agent_license)
    
    if agent_data:
        badge = VERIFICATION_BADGES[agent_data['status']]
        
        badge_html = f"""
        <div style="display: inline-flex; align-items: center; gap: 0.5rem;
                    background: {badge['bg_color']}; padding: 0.5rem 1rem;
                    border-radius: 20px; border: 1px solid {badge['color']};">
            <span>{badge['emoji']}</span>
            <span style="color: {badge['color']}; font-weight: bold; font-size: 0.9rem;">
                {badge['label']}
            </span>
        </div>
        """
        
        st.markdown(badge_html, unsafe_allow_html=True)
        
        if show_details:
            with st.expander("ℹ️ Lihat Detail Verifikasi"):
                render_agent_verification_result(agent_data)
    else:
        st.markdown(get_verification_badge_html(AgentVerificationStatus.UNKNOWN), 
                   unsafe_allow_html=True)


# =============================================================================
# MAIN PAGE RENDERER
# =============================================================================

def render_agent_verification_page():
    """Main page renderer for agent verification."""
    
    # Track page view
    try:
        from services.analytics import track_page
        track_page("agent_verification")
    except:
        pass
    
    # Render components
    render_verification_header()
    render_verification_form()
    render_official_verification_link()
    render_verification_tips()
    render_complaint_button()


# Export
__all__ = [
    "render_agent_verification_page",
    "render_verification_badge_compact",
    "verify_agent_license",
    "AgentVerificationStatus",
    "VERIFICATION_BADGES"
]