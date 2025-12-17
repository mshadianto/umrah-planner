"""
LABBAIK AI v6.0 - Hak Jamaah Umrah Page
========================================
Official Pilgrim Rights Charter based on Ministry of Hajj & Umrah document
Dokumen Resmi: وثيقة حقوق المعتمرين ١٤٤٦ هـ
"""

import streamlit as st
from datetime import datetime
from typing import List, Dict

# =============================================================================
# OFFICIAL 29 RIGHTS DATA (from Ministry document)
# =============================================================================

OFFICIAL_RIGHTS = [
    {
        "no": 1,
        "title": "Pelayanan dengan Amanah",
        "description": "Semua pihak dalam ekosistem umrah wajib melayani jamaah dengan amanah dan ikhlas",
        "icon": "🤝",
        "category": "trust"
    },
    {
        "no": 2,
        "title": "Tracking Status Visa",
        "description": "Jamaah dapat melacak status pengajuan visa melalui platform resmi visa.mofa.gov.sa",
        "icon": "📋",
        "category": "visa"
    },
    {
        "no": 3,
        "title": "Edukasi & Panduan",
        "description": "Travel agent wajib memberikan edukasi lengkap tentang peraturan dan panduan selama di Saudi Arabia",
        "icon": "📚",
        "category": "education"
    },
    {
        "no": 4,
        "title": "Transparansi Paket",
        "description": "Jamaah berhak melihat detail lengkap layanan dalam paket sebelum melakukan pembayaran",
        "icon": "🔍",
        "category": "transparency"
    },
    {
        "no": 5,
        "title": "Penjemputan di Bandara",
        "description": "Jamaah akan dijemput di bandara (udara/darat/laut) dan diantar ke penginapan sesuai program",
        "icon": "✈️",
        "category": "service"
    },
    {
        "no": 6,
        "title": "Asuransi Komprehensif",
        "description": "Asuransi berlaku 90 hari meliputi: kesehatan, kecelakaan, delay penerbangan, pemulangan jenazah, COVID-19",
        "icon": "🏥",
        "category": "insurance"
    },
    {
        "no": 7,
        "title": "Izin Umrah & Raudhah",
        "description": "Travel agent akan menerbitkan izin umrah dan salat di Raudhah sesuai ketersediaan waktu pemesanan",
        "icon": "🕋",
        "category": "permit"
    },
    {
        "no": 8,
        "title": "Umrah Berulang",
        "description": "Jamaah dapat melakukan umrah berkali-kali selama masa tinggal (kecuali Ramadan: 1x saja)",
        "icon": "🔄",
        "category": "permit"
    },
    {
        "no": 9,
        "title": "Izin Raudhah Setahun Sekali",
        "description": "Jamaah berhak mendapat 1 izin salat di Raudhah setiap 365 hari (jika tersedia)",
        "icon": "🕌",
        "category": "permit"
    },
    {
        "no": 10,
        "title": "Pemenuhan Layanan Kontrak",
        "description": "Travel agent bertanggung jawab memenuhi SEMUA layanan (penginapan, transport, dll) sesuai kontrak tanpa biaya tambahan",
        "icon": "✅",
        "category": "service"
    },
    {
        "no": 11,
        "title": "Verifikasi Kesiapan Layanan",
        "description": "Travel agent wajib memastikan semua layanan siap SEBELUM jamaah berangkat",
        "icon": "🔐",
        "category": "service"
    },
    {
        "no": 12,
        "title": "Transportasi Pribadi",
        "description": "Jamaah dapat meminta layanan transport pribadi sesuai ketersediaan",
        "icon": "🚗",
        "category": "service"
    },
    {
        "no": 13,
        "title": "Panduan Jamaah Tersesat",
        "description": "Jamaah yang tersesat akan dibimbing kembali ke penginapan",
        "icon": "🧭",
        "category": "service"
    },
    {
        "no": 14,
        "title": "Koordinasi Kelompok",
        "description": "Travel agent mengatur jamaah dalam kelompok dengan petugas khusus yang mendampingi hingga selesai ibadah",
        "icon": "👥",
        "category": "service"
    },
    {
        "no": 15,
        "title": "Kunjungan Kota Lain",
        "description": "Jamaah bebas mengunjungi kota lain di Saudi selama masa tinggal dengan koordinasi travel agent",
        "icon": "🗺️",
        "category": "freedom"
    },
    {
        "no": 16,
        "title": "Durasi Tinggal 3 Bulan",
        "description": "Masa tinggal maksimal 3 bulan sejak kedatangan atau paling lambat 1 Dzulqa'dah",
        "icon": "📅",
        "category": "visa"
    },
    {
        "no": 17,
        "title": "Mulai Penerbitan Visa",
        "description": "Visa mulai diterbitkan tanggal 14 Dzulhijjah setiap tahun",
        "icon": "📆",
        "category": "visa"
    },
    {
        "no": 18,
        "title": "Mulai Program di Makkah",
        "description": "Program umrah di Makkah dimulai tanggal 16 Dzulhijjah",
        "icon": "🕋",
        "category": "timeline"
    },
    {
        "no": 19,
        "title": "Batas Penerbitan Visa",
        "description": "Batas akhir penerbitan visa dan masuk Saudi: 15 Syawal",
        "icon": "⏰",
        "category": "visa"
    },
    {
        "no": 20,
        "title": "Batas Keberangkatan",
        "description": "Batas akhir meninggalkan Saudi: 1 Dzulqa'dah",
        "icon": "🛫",
        "category": "timeline"
    },
    {
        "no": 21,
        "title": "Masa Berlaku Visa",
        "description": "Visa berlaku 3 bulan sejak penerbitan atau maksimal masuk 15 Syawal (mana yang lebih awal)",
        "icon": "📋",
        "category": "visa"
    },
    {
        "no": 22,
        "title": "Periode Pengajuan Visa",
        "description": "Pengajuan visa dibuka 14 Dzulhijjah hingga 15 Syawal tahun berikutnya",
        "icon": "📝",
        "category": "visa"
    },
    {
        "no": 23,
        "title": "Layanan Darurat",
        "description": "Jamaah berhak mendapat bantuan penuh dari travel agent untuk insiden/kecelakaan/sakit/meninggal",
        "icon": "🆘",
        "category": "emergency"
    },
    {
        "no": 24,
        "title": "Verifikasi Travel Agent",
        "description": "Jamaah dapat memverifikasi travel agent resmi melalui portal Kemenag Haji Saudi",
        "icon": "✔️",
        "category": "verification"
    },
    {
        "no": 25,
        "title": "Akses Platform Nusuk",
        "description": "Jamaah dapat mengakses berbagai jenis visa umrah melalui platform Nusuk (www.nusuk.sa)",
        "icon": "📱",
        "category": "platform"
    },
    {
        "no": 26,
        "title": "Pengaturan Keberangkatan",
        "description": "Travel agent mengatur jadwal keberangkatan ke bandara agar jamaah tiba tepat waktu",
        "icon": "🛬",
        "category": "service"
    },
    {
        "no": 27,
        "title": "Hak Asasi Manusia",
        "description": "Semua hak yang diakui Komisi HAM Saudi Arabia berlaku untuk jamaah umrah",
        "icon": "⚖️",
        "category": "rights"
    },
    {
        "no": 28,
        "title": "Akses Keamanan",
        "description": "Jamaah berhak menghubungi pihak keamanan jika menghadapi masalah selama di Saudi",
        "icon": "🚨",
        "category": "security"
    },
    {
        "no": 29,
        "title": "Hak Komplain & Feedback",
        "description": "Jamaah dapat menilai layanan, mengajukan keluhan, dan memberikan saran melalui email/hotline 24/7",
        "icon": "📞",
        "category": "feedback"
    }
]

CONTACT_INFO = {
    "ministry_hotline": "+966920002814",
    "ministry_email": "mohcc@haj.gov.sa",
    "verification_url": "https://eservices.haj.gov.sa/eservices3/pages/VisaInquiry/SearchVisa.xhtml",
    "nusuk_url": "https://www.nusuk.sa/ar",
    "visa_portal": "https://visa.mofa.gov.sa"
}


# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_header():
    """Render page header with official branding."""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a5f3c 0%, #2d8659 100%); 
                padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;
                border: 2px solid #d4af37;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">📜</div>
        <h1 style="color: #d4af37; margin: 0;">Hak Jamaah Umrah</h1>
        <p style="color: #fff; font-size: 1.1rem; margin-top: 0.5rem;">
            وثيقة حقوق المعتمرين ١٤٤٦ هـ
        </p>
        <p style="color: #d4af37; font-size: 0.9rem;">
            Dokumen Resmi Kementerian Haji & Umrah Saudi Arabia
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_intro():
    """Render introduction section."""
    st.markdown("## 📋 Tentang Dokumen Ini")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Dokumen **Hak Jamaah Umrah** diterbitkan resmi oleh **Kementerian Haji dan Umrah 
        Kerajaan Saudi Arabia** untuk melindungi hak-hak jamaah internasional.
        
        **Tujuan Dokumen:**
        - ✅ Memastikan pelayanan berkualitas tinggi
        - ✅ Melindungi jamaah dari praktik tidak etis
        - ✅ Memberikan panduan jelas tentang hak & kewajiban
        - ✅ Meningkatkan transparansi industri umrah
        """)
    
    with col2:
        st.info("""
        **📊 Statistik:**
        - 29 Hak Resmi
        - 8 Kategori
        - Berlaku untuk semua jamaah
        - Ditegakkan oleh hukum Saudi
        """)


def render_rights_by_category():
    """Render rights organized by category."""
    st.markdown("---")
    st.markdown("## 🗂️ Hak-Hak Berdasarkan Kategori")
    
    # Group rights by category
    categories = {}
    for right in OFFICIAL_RIGHTS:
        cat = right['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(right)
    
    # Category names in Indonesian
    category_names = {
        "trust": "🤝 Amanah & Kepercayaan",
        "visa": "📋 Visa & Dokumentasi",
        "education": "📚 Edukasi & Panduan",
        "transparency": "🔍 Transparansi",
        "service": "✅ Layanan & Fasilitas",
        "insurance": "🏥 Asuransi & Perlindungan",
        "permit": "🕋 Izin Umrah & Ibadah",
        "freedom": "🗺️ Kebebasan Bergerak",
        "timeline": "📅 Jadwal & Timeline",
        "emergency": "🆘 Layanan Darurat",
        "verification": "✔️ Verifikasi Travel Agent",
        "platform": "📱 Platform Digital",
        "rights": "⚖️ Hak Asasi Manusia",
        "security": "🚨 Keamanan",
        "feedback": "📞 Komplain & Feedback"
    }
    
    # Create tabs for each category
    cat_keys = list(categories.keys())
    cat_tabs = st.tabs([category_names.get(cat, cat.title()) for cat in cat_keys])
    
    for tab, cat_key in zip(cat_tabs, cat_keys):
        with tab:
            rights_in_cat = categories[cat_key]
            
            for right in rights_in_cat:
                with st.container():
                    col1, col2 = st.columns([1, 20])
                    
                    with col1:
                        st.markdown(f"<div style='font-size: 2rem;'>{right['icon']}</div>", 
                                  unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                                    padding: 1rem; border-radius: 10px; border-left: 4px solid #d4af37;'>
                            <h4 style='color: #d4af37; margin: 0;'>
                                Hak #{right['no']}: {right['title']}
                            </h4>
                            <p style='color: #ccc; margin-top: 0.5rem;'>
                                {right['description']}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("")


def render_all_rights_list():
    """Render complete list of all 29 rights."""
    st.markdown("---")
    st.markdown("## 📜 Daftar Lengkap 29 Hak Jamaah")
    
    # Split into 3 columns for better readability
    col1, col2, col3 = st.columns(3)
    
    columns = [col1, col2, col3]
    rights_per_col = len(OFFICIAL_RIGHTS) // 3 + 1
    
    for idx, right in enumerate(OFFICIAL_RIGHTS):
        col_idx = idx // rights_per_col
        with columns[col_idx]:
            st.markdown(f"""
            <div style='background: #1a1a1a; padding: 0.8rem; margin-bottom: 0.5rem;
                        border-radius: 8px; border: 1px solid #333;'>
                <div style='color: #d4af37; font-weight: bold;'>
                    {right['icon']} #{right['no']}
                </div>
                <div style='color: #aaa; font-size: 0.85rem; margin-top: 0.3rem;'>
                    {right['title']}
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_official_contacts():
    """Render official contact information."""
    st.markdown("---")
    st.markdown("## 📞 Kontak Resmi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1a5f3c 0%, #2d8659 100%);
                    padding: 1.5rem; border-radius: 10px; border: 1px solid #4ade80;'>
            <h3 style='color: #d4af37; margin-top: 0;'>🏛️ Kementerian Haji Saudi</h3>
            <p style='color: #fff;'>
                <strong>📞 Hotline 24/7:</strong><br>
                +966920002814
            </p>
            <p style='color: #fff;'>
                <strong>📧 Email:</strong><br>
                mohcc@haj.gov.sa
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                    padding: 1.5rem; border-radius: 10px; border: 1px solid #d4af37;'>
            <h3 style='color: #d4af37; margin-top: 0;'>🔗 Portal Resmi</h3>
            <p style='color: #ccc;'>
                <strong>Verifikasi Travel Agent:</strong><br>
                <a href='https://eservices.haj.gov.sa' target='_blank' 
                   style='color: #4ade80;'>eservices.haj.gov.sa</a>
            </p>
            <p style='color: #ccc;'>
                <strong>Platform Nusuk:</strong><br>
                <a href='https://www.nusuk.sa' target='_blank' 
                   style='color: #4ade80;'>www.nusuk.sa</a>
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_download_section():
    """Render PDF download section."""
    st.markdown("---")
    st.markdown("## 📥 Download Dokumen Resmi")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info("""
        📄 **Dokumen PDF Resmi**
        
        Download dokumen asli dalam bahasa Arab dari Kementerian Haji & Umrah 
        Kerajaan Saudi Arabia.
        
        - Dokumen resmi berkas PDF
        - Bahasa: العربية (Arab)
        - Ukuran: ~500KB
        - Tahun: ١٤٤٦ هـ (1446 H)
        """)
        
        # Note: In production, you would serve the actual PDF file
        st.button("📥 Download PDF Resmi", type="primary", use_container_width=True)
        st.caption("*File PDF harus ditempatkan di folder assets/docs/")


def render_disclaimer():
    """Render disclaimer and notes."""
    st.markdown("---")
    st.warning("""
    ⚠️ **Catatan Penting:**
    
    - Dokumen ini adalah terjemahan non-resmi untuk keperluan informatif
    - Untuk versi resmi, silakan lihat dokumen bahasa Arab dari Kementerian
    - Hak dan kewajiban dapat berubah sesuai regulasi terbaru
    - Hubungi travel agent resmi untuk informasi detail dan terkini
    """)


# =============================================================================
# MAIN PAGE RENDERER
# =============================================================================

def render_hak_jamaah_page():
    """Main page renderer for Hak Jamaah Umrah."""
    
    # Track page view
    try:
        from services.analytics import track_page
        track_page("hak_jamaah")
    except:
        pass
    
    # Render components
    render_header()
    render_intro()
    render_rights_by_category()
    render_all_rights_list()
    render_official_contacts()
    render_download_section()
    render_disclaimer()
    
    # Footer with action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠 Kembali ke Beranda", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
    
    with col2:
        if st.button("🔍 Cek Paket Compliance", use_container_width=True):
            st.session_state.current_page = "simulator"
            st.rerun()
    
    with col3:
        if st.button("🆘 Emergency Hub", use_container_width=True):
            st.session_state.current_page = "sos"
            st.rerun()


# Export
__all__ = ["render_hak_jamaah_page", "OFFICIAL_RIGHTS", "CONTACT_INFO"]