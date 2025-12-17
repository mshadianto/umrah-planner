"""
LABBAIK AI v6.0 - Emergency Contact Hub
========================================
24/7 Emergency contacts and SOS system
Based on Official Hak Jamaah #23, #28, #29
"""

import streamlit as st
from typing import Dict, List
from datetime import datetime


# =============================================================================
# EMERGENCY CONTACT DATA
# =============================================================================

EMERGENCY_CONTACTS = {
    "saudi_ministry": {
        "category": "🏛️ Kementerian Haji Saudi",
        "priority": 1,
        "contacts": [
            {
                "name": "Ministry of Hajj & Umrah Hotline",
                "phone": "+966920002814",
                "whatsapp": "+966920002814",
                "email": "mohcc@haj.gov.sa",
                "available": "24/7",
                "languages": ["العربية", "English", "Bahasa Indonesia"],
                "description": "Hotline resmi untuk semua pertanyaan & darurat jamaah umrah"
            }
        ]
    },
    "indonesian_embassy": {
        "category": "🇮🇩 Kedutaan Indonesia",
        "priority": 2,
        "contacts": [
            {
                "name": "KBRI Riyadh",
                "phone": "+966-11-488-2800",
                "emergency": "+966-50-527-7436",
                "email": "konsulerriyadh@kemlu.go.id",
                "address": "Al Maather St, Ar Rawdah, Riyadh",
                "available": "24/7 (Emergency)",
                "description": "Kedutaan Besar RI di Riyadh untuk bantuan warga negara"
            },
            {
                "name": "KJRI Jeddah",
                "phone": "+966-12-660-1000",
                "emergency": "+966-50-501-9882",
                "email": "kjrijeddah@kemlu.go.id",
                "address": "Al Hamra District, Jeddah",
                "available": "24/7 (Emergency)",
                "description": "Konsulat Jenderal RI di Jeddah"
            }
        ]
    },
    "emergency_services": {
        "category": "🚨 Layanan Darurat Saudi",
        "priority": 1,
        "contacts": [
            {
                "name": "Police / Kepolisian",
                "phone": "999",
                "description": "Panggilan darurat untuk keamanan, pencurian, kecelakaan"
            },
            {
                "name": "Ambulance / Ambulans",
                "phone": "997",
                "description": "Darurat medis, kecelakaan, kondisi kritis"
            },
            {
                "name": "Civil Defense / Pemadam Kebakaran",
                "phone": "998",
                "description": "Kebakaran, bencana alam, penyelamatan"
            },
            {
                "name": "Traffic Accidents",
                "phone": "993",
                "description": "Kecelakaan lalu lintas"
            }
        ]
    },
    "hospitals": {
        "category": "🏥 Rumah Sakit Utama",
        "priority": 3,
        "contacts": [
            {
                "name": "Makkah Haram Emergency",
                "phone": "+966-12-5564-999",
                "location": "Makkah",
                "description": "Unit darurat di sekitar Masjidil Haram"
            },
            {
                "name": "King Abdullah Medical City",
                "phone": "+966-12-549-9999",
                "location": "Makkah",
                "description": "RS pemerintah besar di Makkah"
            },
            {
                "name": "Madinah Haram Emergency",
                "phone": "+966-14-848-8888",
                "location": "Madinah",
                "description": "Unit darurat di sekitar Masjid Nabawi"
            },
            {
                "name": "King Fahd Hospital",
                "phone": "+966-14-822-2222",
                "location": "Madinah",
                "description": "RS pemerintah besar di Madinah"
            }
        ]
    },
    "travel_agent": {
        "category": "🏢 Travel Agent Anda",
        "priority": 1,
        "contacts": [
            {
                "name": "Koordinator Kelompok",
                "phone": "Lihat di kartu jamaah Anda",
                "description": "Hubungi pertama kali untuk masalah apapun"
            },
            {
                "name": "Kantor Pusat Indonesia",
                "phone": "Sesuai travel agent Anda",
                "description": "Hotline travel agent di Indonesia"
            }
        ]
    }
}

SOS_QUICK_ACTIONS = [
    {
        "icon": "🏥",
        "title": "Sakit/Cedera",
        "action": "call_ambulance",
        "primary_number": "997",
        "steps": [
            "1. Panggil ambulans: 997",
            "2. Hubungi koordinator kelompok",
            "3. Siapkan kartu asuransi",
            "4. Catat lokasi & kondisi"
        ]
    },
    {
        "icon": "🚨",
        "title": "Keamanan/Pencurian",
        "action": "call_police",
        "primary_number": "999",
        "steps": [
            "1. Panggil polisi: 999",
            "2. Jangan tinggalkan lokasi",
            "3. Hubungi KBRI/KJRI",
            "4. Buat laporan tertulis"
        ]
    },
    {
        "icon": "👤",
        "title": "Tersesat/Hilang",
        "action": "report_lost",
        "primary_number": "+966920002814",
        "steps": [
            "1. Tetap di tempat ramai",
            "2. Hubungi koordinator",
            "3. Aktifkan GPS/share location",
            "4. Cari petugas terdekat"
        ]
    },
    {
        "icon": "📱",
        "title": "Kehilangan Dokumen",
        "action": "report_documents",
        "primary_number": "+966-11-488-2800",
        "steps": [
            "1. Lapor ke polisi (999)",
            "2. Hubungi KBRI/KJRI",
            "3. Siapkan foto/copy dokumen",
            "4. Urus dokumen pengganti"
        ]
    }
]


# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_emergency_header():
    """Render emergency hub header."""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%); 
                padding: 2rem; border-radius: 15px; margin-bottom: 2rem;
                border: 3px solid #fca5a5; animation: pulse 2s infinite;">
        <div style="text-align: center;">
            <div style="font-size: 4rem;">🆘</div>
            <h1 style="color: #fff; margin: 0.5rem 0;">Emergency Contact Hub</h1>
            <p style="color: #fecaca; font-size: 1.2rem;">
                Kontak Darurat 24/7 untuk Jamaah Umrah
            </p>
        </div>
    </div>
    
    <style>
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    </style>
    """, unsafe_allow_html=True)


def render_quick_sos_buttons():
    """Render quick SOS action buttons."""
    st.markdown("## ⚡ Aksi Cepat Darurat")
    
    cols = st.columns(4)
    
    for idx, sos in enumerate(SOS_QUICK_ACTIONS):
        with cols[idx]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
                        padding: 1.5rem; border-radius: 12px; text-align: center;
                        border: 2px solid #fca5a5; cursor: pointer; min-height: 180px;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">{sos['icon']}</div>
                <h3 style="color: #fca5a5; margin: 0.5rem 0; font-size: 1rem;">
                    {sos['title']}
                </h3>
                <div style="background: #dc2626; color: #fff; padding: 0.5rem;
                            border-radius: 8px; font-weight: bold; margin-top: 1rem;">
                    📞 {sos['primary_number']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"📋 Panduan", key=f"sos_{idx}", use_container_width=True):
                st.session_state[f"show_sos_{sos['action']}"] = True
        
        # Show steps if button clicked
        if st.session_state.get(f"show_sos_{sos['action']}"):
            with cols[idx]:
                with st.expander("📝 Langkah-Langkah", expanded=True):
                    for step in sos['steps']:
                        st.markdown(f"- {step}")


def render_emergency_contacts_by_category():
    """Render all emergency contacts organized by category."""
    st.markdown("---")
    st.markdown("## 📞 Daftar Kontak Lengkap")
    
    # Sort by priority
    sorted_categories = sorted(
        EMERGENCY_CONTACTS.items(),
        key=lambda x: x[1]['priority']
    )
    
    for cat_key, cat_data in sorted_categories:
        st.markdown(f"### {cat_data['category']}")
        
        for contact in cat_data['contacts']:
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1.5rem; border-radius: 10px;
                                margin-bottom: 1rem; border-left: 4px solid #d4af37;">
                        <h4 style="color: #d4af37; margin: 0 0 0.5rem 0;">
                            {contact['name']}
                        </h4>
                        <p style="color: #ccc; margin: 0.3rem 0;">
                            {contact.get('description', '')}
                        </p>
                    """, unsafe_allow_html=True)
                    
                    # Contact details
                    if 'phone' in contact:
                        st.markdown(f"""
                        <p style="color: #4ade80; margin: 0.5rem 0;">
                            📞 <strong>Phone:</strong> {contact['phone']}
                        </p>
                        """, unsafe_allow_html=True)
                    
                    if 'emergency' in contact:
                        st.markdown(f"""
                        <p style="color: #ef4444; margin: 0.5rem 0;">
                            🚨 <strong>Emergency:</strong> {contact['emergency']}
                        </p>
                        """, unsafe_allow_html=True)
                    
                    if 'whatsapp' in contact:
                        st.markdown(f"""
                        <p style="color: #22c55e; margin: 0.5rem 0;">
                            💬 <strong>WhatsApp:</strong> {contact['whatsapp']}
                        </p>
                        """, unsafe_allow_html=True)
                    
                    if 'email' in contact:
                        st.markdown(f"""
                        <p style="color: #60a5fa; margin: 0.5rem 0;">
                            📧 <strong>Email:</strong> {contact['email']}
                        </p>
                        """, unsafe_allow_html=True)
                    
                    if 'address' in contact:
                        st.markdown(f"""
                        <p style="color: #aaa; margin: 0.5rem 0;">
                            📍 <strong>Address:</strong> {contact['address']}
                        </p>
                        """, unsafe_allow_html=True)
                    
                    if 'available' in contact:
                        st.markdown(f"""
                        <p style="color: #facc15; margin: 0.5rem 0;">
                            ⏰ <strong>Available:</strong> {contact['available']}
                        </p>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    if 'phone' in contact and contact['phone'] not in ["Lihat di kartu jamaah Anda", "Sesuai travel agent Anda"]:
                        if st.button(f"📞 Call", key=f"call_{contact['name']}", use_container_width=True):
                            st.success(f"Calling {contact['phone']}...")
                    
                    if 'whatsapp' in contact:
                        if st.button(f"💬 WhatsApp", key=f"wa_{contact['name']}", use_container_width=True):
                            st.success(f"Opening WhatsApp...")


def render_emergency_tips():
    """Render emergency preparation tips."""
    st.markdown("---")
    st.markdown("## 💡 Tips Persiapan Darurat")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✅ Persiapan Sebelum Berangkat:**
        
        1. ✅ Simpan semua nomor darurat di HP
        2. ✅ Foto/scan semua dokumen penting
        3. ✅ Share lokasi real-time dengan keluarga
        4. ✅ Catat nomor koordinator kelompok
        5. ✅ Siapkan kartu asuransi di tempat mudah
        6. ✅ Pelajari beberapa frasa Arab dasar
        7. ✅ Bawa obat-obatan pribadi + resep
        8. ✅ Install app translator di HP
        """)
    
    with col2:
        st.info("""
        **📱 App Wajib Install:**
        
        - 🕋 **Nusuk**: Izin umrah & Raudhah
        - 🗺️ **Google Maps**: Navigasi
        - 💬 **WhatsApp**: Komunikasi keluarga
        - 📞 **Tawakkalna**: App COVID Saudi
        - 🏥 **Sehhaty**: Rekam medis Saudi
        - 💰 **Currency Converter**: Konversi SAR-IDR
        - 📖 **Al-Quran**: Ibadah
        - 🔊 **Google Translate**: Penerjemah
        """)


def render_emergency_scenarios():
    """Render common emergency scenarios and solutions."""
    st.markdown("---")
    st.markdown("## 🎯 Panduan Situasi Darurat")
    
    scenarios = [
        {
            "title": "Sakit Mendadak",
            "steps": [
                "1. Hubungi ambulans (997) atau koordinator",
                "2. Jika bisa berjalan, cari klinik terdekat",
                "3. Tunjukkan kartu asuransi (cashless)",
                "4. Simpan semua kuitansi/dokumen",
                "5. Lapor ke travel agent untuk follow-up"
            ],
            "icon": "🏥"
        },
        {
            "title": "Passport/Visa Hilang",
            "steps": [
                "1. Lapor polisi (999) - minta surat kehilangan",
                "2. Hubungi KBRI/KJRI segera",
                "3. Siapkan foto/copy dokumen",
                "4. Urus Surat Perjalanan Laksana Paspor (SPLP)",
                "5. Koordinasi travel agent untuk reschedule"
            ],
            "icon": "📕"
        },
        {
            "title": "Uang/Kartu Hilang/Dicuri",
            "steps": [
                "1. Lapor polisi (999)",
                "2. Block kartu ATM/credit card segera",
                "3. Hubungi bank di Indonesia",
                "4. Minta bantuan dana darurat dari keluarga",
                "5. Travel agent bantu koordinasi"
            ],
            "icon": "💰"
        },
        {
            "title": "Terpisah dari Kelompok",
            "steps": [
                "1. TETAP DI TEMPAT yang ramai/aman",
                "2. Hubungi koordinator kelompok",
                "3. Share lokasi GPS via WhatsApp",
                "4. Tanyakan ke petugas terdekat",
                "5. Cari ke hotel/bus jika ingat lokasi"
            ],
            "icon": "👥"
        }
    ]
    
    for scenario in scenarios:
        with st.expander(f"{scenario['icon']} {scenario['title']}"):
            for step in scenario['steps']:
                st.markdown(f"**{step}**")
            st.markdown("")


def render_save_emergency_contacts():
    """Render button to save/download emergency contacts."""
    st.markdown("---")
    st.markdown("## 💾 Simpan Kontak Darurat")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📱 Export to VCF", use_container_width=True):
            st.info("Feature coming soon: Download all contacts as .vcf file")
    
    with col2:
        if st.button("📄 Export to PDF", use_container_width=True):
            st.info("Feature coming soon: Download contact list as PDF")
    
    with col3:
        if st.button("📧 Email to Me", use_container_width=True):
            st.info("Feature coming soon: Send contact list to your email")


# =============================================================================
# MAIN PAGE RENDERER
# =============================================================================

def render_emergency_hub_page():
    """Main page renderer for emergency contact hub."""
    
    # Track page view
    try:
        from services.analytics import track_page
        track_page("emergency_hub")
    except:
        pass
    
    # Render components
    render_emergency_header()
    render_quick_sos_buttons()
    render_emergency_contacts_by_category()
    render_emergency_tips()
    render_emergency_scenarios()
    render_save_emergency_contacts()
    
    # Footer warning
    st.markdown("---")
    st.error("""
    ⚠️ **PENTING:**
    
    - Simpan screenshot halaman ini di HP Anda
    - Jangan panik - ikuti prosedur dengan tenang
    - Selalu prioritaskan keselamatan jiwa
    - Hubungi koordinator kelompok terlebih dahulu
    - Simpan bukti untuk klaim asuransi
    """)


# Export
__all__ = [
    "render_emergency_hub_page",
    "EMERGENCY_CONTACTS",
    "SOS_QUICK_ACTIONS"
]