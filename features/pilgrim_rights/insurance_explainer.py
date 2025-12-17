"""
LABBAIK AI v6.0 - Insurance Coverage Explainer
===============================================
Comprehensive insurance breakdown based on Official Hak Jamaah #6
90-day comprehensive coverage for all pilgrims
"""

import streamlit as st
from typing import Dict, List
from datetime import datetime, timedelta


# =============================================================================
# INSURANCE COVERAGE DATA (Based on Official Document)
# =============================================================================

INSURANCE_COVERAGE = {
    "medical": {
        "icon": "🏥",
        "title": "Layanan Kesehatan Lengkap",
        "description": "Perawatan medis di seluruh fasilitas kesehatan Saudi Arabia",
        "benefits": [
            "✅ Rumah sakit & klinik pemerintah (gratis penuh)",
            "✅ Rumah sakit & klinik swasta terakreditasi",
            "✅ Konsultasi dokter umum & spesialis",
            "✅ Rawat inap (ICU, operasi, dll)",
            "✅ Obat-obatan resep dokter",
            "✅ Pemeriksaan laboratorium & radiologi",
            "✅ Ambulans & emergency transport"
        ],
        "coverage": "Unlimited (tanpa batas)",
        "color": "#4ade80"
    },
    "covid": {
        "icon": "😷",
        "title": "Perlindungan COVID-19",
        "description": "Biaya penuh untuk perawatan dan karantina COVID-19",
        "benefits": [
            "✅ Tes COVID-19 (PCR/Antigen)",
            "✅ Perawatan jika positif COVID",
            "✅ Biaya karantina mandiri",
            "✅ Biaya isolasi di fasilitas kesehatan",
            "✅ Obat & perawatan komplikasi",
            "✅ Follow-up treatment"
        ],
        "coverage": "Full coverage",
        "color": "#60a5fa"
    },
    "accident": {
        "icon": "🚑",
        "title": "Kecelakaan & Bencana",
        "description": "Perlindungan untuk kecelakaan dan bencana alam",
        "benefits": [
            "✅ Kecelakaan lalu lintas",
            "✅ Kecelakaan di hotel/tempat umum",
            "✅ Cedera saat ibadah (jatuh, terinjak, dll)",
            "✅ Bencana alam (gempa, banjir, dll)",
            "✅ Santunan cacat tetap",
            "✅ Santunan meninggal dunia"
        ],
        "coverage": "Sesuai polis standar",
        "color": "#fb923c"
    },
    "flight": {
        "icon": "✈️",
        "title": "Delay & Pembatalan Penerbangan",
        "description": "Kompensasi untuk masalah penerbangan",
        "benefits": [
            "✅ Biaya hotel jika delay >6 jam",
            "✅ Biaya makan selama delay",
            "✅ Kompensasi pembatalan sepihak",
            "✅ Rebooking ke penerbangan lain",
            "✅ Bagasi hilang/rusak",
            "✅ Dokumen perjalanan hilang"
        ],
        "coverage": "Sesuai ketentuan maskapai",
        "color": "#a78bfa"
    },
    "repatriation": {
        "icon": "🕊️",
        "title": "Pemulangan Jenazah",
        "description": "Biaya penuh pemulangan jika meninggal dunia",
        "benefits": [
            "✅ Pengurusan dokumen kematian",
            "✅ Perawatan & preservasi jenazah",
            "✅ Peti jenazah standar internasional",
            "✅ Tiket kargo udara ke Indonesia",
            "✅ Handling di bandara tujuan",
            "✅ Administrasi & koordinasi keluarga"
        ],
        "coverage": "Full coverage",
        "color": "#f472b6"
    },
    "assistance": {
        "icon": "📞",
        "title": "Bantuan 24/7",
        "description": "Layanan bantuan sepanjang waktu",
        "benefits": [
            "✅ Hotline darurat 24/7",
            "✅ Koordinasi dengan travel agent",
            "✅ Bantuan administrasi rumah sakit",
            "✅ Penerjemah medis (Arab-Indonesia)",
            "✅ Koordinasi dengan keluarga di Indonesia",
            "✅ Rekomendasi fasilitas kesehatan"
        ],
        "coverage": "Unlimited",
        "color": "#facc15"
    }
}

INSURANCE_SPECS = {
    "validity": "90 hari sejak masuk Saudi Arabia",
    "activation": "Otomatis aktif saat visa disetujui",
    "provider": "Perusahaan asuransi terakreditasi Saudi",
    "claim_process": "Langsung di rumah sakit (cashless) atau reimburse",
    "coverage_area": "Seluruh wilayah Saudi Arabia",
    "premium": "SUDAH TERMASUK dalam harga paket umrah"
}

EXCLUSIONS = [
    "❌ Penyakit yang sudah ada sebelum keberangkatan (pre-existing)",
    "❌ Cedera akibat aktivitas ekstrem (parkour, balap, dll)",
    "❌ Penyalahgunaan obat-obatan terlarang",
    "❌ Tindakan kriminal atau melanggar hukum Saudi",
    "❌ Perawatan kosmetik/estetika",
    "❌ Pemeriksaan check-up rutin (tanpa indikasi medis)"
]


# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_insurance_header():
    """Render insurance section header."""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); 
                padding: 2rem; border-radius: 15px; margin-bottom: 2rem;
                border: 2px solid #60a5fa;">
        <div style="font-size: 3rem; text-align: center;">🏥</div>
        <h2 style="color: #fff; text-align: center; margin: 0.5rem 0;">
            Asuransi Komprehensif 90 Hari
        </h2>
        <p style="color: #dbeafe; text-align: center; font-size: 1.1rem;">
            Perlindungan lengkap selama perjalanan umrah Anda
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_coverage_card(coverage_type: str, data: Dict):
    """Render individual coverage card."""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;
                border-left: 5px solid {data['color']};">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="font-size: 2.5rem; margin-right: 1rem;">{data['icon']}</div>
            <div>
                <h3 style="color: {data['color']}; margin: 0;">{data['title']}</h3>
                <p style="color: #aaa; margin: 0.3rem 0 0 0; font-size: 0.9rem;">
                    {data['description']}
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Benefits list
    cols = st.columns([1, 3])
    with cols[1]:
        for benefit in data['benefits']:
            st.markdown(f"<p style='color: #ccc; margin: 0.3rem 0;'>{benefit}</p>", 
                       unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: #1a1a1a; padding: 0.8rem; border-radius: 8px; 
                    margin-top: 1rem; border: 1px solid {data['color']};">
            <strong style="color: {data['color']};">Limit Coverage:</strong>
            <span style="color: #fff;"> {data['coverage']}</span>
        </div>
        """, unsafe_allow_html=True)


def render_all_coverages():
    """Render all insurance coverages."""
    st.markdown("## 🛡️ Cakupan Asuransi Lengkap")
    
    for coverage_type, data in INSURANCE_COVERAGE.items():
        render_coverage_card(coverage_type, data)


def render_insurance_specs():
    """Render insurance specifications."""
    st.markdown("---")
    st.markdown("## 📋 Spesifikasi Asuransi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a5f3c 0%, #2d8659 100%);
                    padding: 1.5rem; border-radius: 10px;">
            <h4 style="color: #d4af37; margin-top: 0;">✅ Detail Polis</h4>
        """, unsafe_allow_html=True)
        
        for key, value in INSURANCE_SPECS.items():
            label = key.replace("_", " ").title()
            st.markdown(f"""
            <div style="margin-bottom: 0.8rem;">
                <strong style="color: #4ade80;">{label}:</strong><br>
                <span style="color: #fff;">{value}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #991b1b 0%, #dc2626 100%);
                    padding: 1.5rem; border-radius: 10px;">
            <h4 style="color: #fca5a5; margin-top: 0;">⚠️ Pengecualian</h4>
        """, unsafe_allow_html=True)
        
        for exclusion in EXCLUSIONS:
            st.markdown(f"""
            <p style="color: #fecaca; margin: 0.5rem 0;">{exclusion}</p>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


def render_claim_process():
    """Render claim process guide."""
    st.markdown("---")
    st.markdown("## 📝 Cara Klaim Asuransi")
    
    steps = [
        {
            "no": "1",
            "title": "Segera Hubungi Hotline",
            "desc": "Hubungi hotline asuransi atau travel agent saat terjadi insiden",
            "icon": "📞"
        },
        {
            "no": "2",
            "title": "Dapatkan Perawatan",
            "desc": "Pergi ke rumah sakit/klinik rekanan (cashless) atau RS terdekat",
            "icon": "🏥"
        },
        {
            "no": "3",
            "title": "Simpan Dokumen",
            "desc": "Kumpulkan semua dokumen: kuitansi, resep, hasil lab, surat dokter",
            "icon": "📄"
        },
        {
            "no": "4",
            "title": "Submit Klaim",
            "desc": "Serahkan dokumen ke travel agent atau submit online",
            "icon": "✉️"
        },
        {
            "no": "5",
            "title": "Proses Verifikasi",
            "desc": "Perusahaan asuransi akan verifikasi (1-7 hari kerja)",
            "icon": "🔍"
        },
        {
            "no": "6",
            "title": "Terima Reimbursement",
            "desc": "Dana ditransfer ke rekening Anda (jika tidak cashless)",
            "icon": "💰"
        }
    ]
    
    cols = st.columns(3)
    for idx, step in enumerate(steps):
        col_idx = idx % 3
        with cols[col_idx]:
            st.markdown(f"""
            <div style="background: #1a1a1a; padding: 1.5rem; border-radius: 10px;
                        text-align: center; margin-bottom: 1rem; 
                        border: 2px solid #d4af37; min-height: 200px;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">{step['icon']}</div>
                <div style="background: #d4af37; color: #000; width: 40px; height: 40px;
                            border-radius: 50%; display: flex; align-items: center;
                            justify-content: center; margin: 0 auto 0.5rem; font-weight: bold;">
                    {step['no']}
                </div>
                <h4 style="color: #d4af37; margin: 0.5rem 0;">{step['title']}</h4>
                <p style="color: #aaa; font-size: 0.85rem; margin: 0;">
                    {step['desc']}
                </p>
            </div>
            """, unsafe_allow_html=True)


def render_emergency_contacts():
    """Render emergency insurance contacts."""
    st.markdown("---")
    st.markdown("## 🆘 Kontak Darurat Asuransi")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **📞 Hotline Asuransi**
        
        +966-XX-XXXX-XXXX
        (24 jam, 7 hari/minggu)
        
        *Hubungi travel agent untuk nomor spesifik
        """)
    
    with col2:
        st.info("""
        **🏥 Rumah Sakit Rekanan**
        
        Daftar lengkap RS rekanan
        tersedia di kartu asuransi
        
        *Request dari travel agent
        """)
    
    with col3:
        st.info("""
        **📧 Email Klaim**
        
        claims@insurance.sa
        
        *Email khusus untuk submit dokumen klaim
        """)


def render_insurance_calculator():
    """Render insurance value calculator."""
    st.markdown("---")
    st.markdown("## 💰 Nilai Manfaat Asuransi Anda")
    
    st.info("""
    Asuransi komprehensif 90 hari senilai **Rp 2.000.000 - Rp 5.000.000** 
    **SUDAH TERMASUK** dalam harga paket umrah Anda!
    """)
    
    # Interactive calculator
    with st.expander("🧮 Hitung Estimasi Nilai Manfaat"):
        duration = st.slider("Durasi Umrah (hari)", 9, 30, 12)
        
        # Calculate potential savings
        hospital_visit = 5000000  # Rp 5 juta if need hospital
        covid_treatment = 15000000  # Rp 15 juta if COVID positive
        repatriation = 50000000  # Rp 50 juta if need repatriation
        
        st.markdown(f"""
        ### Estimasi Perlindungan Finansial:
        
        **Tanpa Asuransi, Anda berisiko bayar:**
        - Rawat inap 1 hari: **Rp {hospital_visit:,}**
        - Perawatan COVID: **Rp {covid_treatment:,}**
        - Pemulangan jenazah: **Rp {repatriation:,}**
        
        **TOTAL RISIKO: Rp {(hospital_visit + covid_treatment + repatriation):,}**
        
        ---
        
        ✅ **Dengan asuransi: GRATIS / COVERED!**
        
        Hemat potensial: **Rp 70.000.000+** 💰
        """)


def render_insurance_tips():
    """Render insurance usage tips."""
    st.markdown("---")
    st.markdown("## 💡 Tips Memaksimalkan Asuransi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✅ DO:**
        - Simpan kartu asuransi di tempat mudah diakses
        - Foto/scan kartu asuransi di HP
        - Catat nomor hotline di kontak darurat
        - Bawa obat rutin dari Indonesia (dengan resep)
        - Periksa kesehatan sebelum berangkat
        - Minta travel agent untuk daftar RS rekanan
        """)
    
    with col2:
        st.error("""
        **❌ DON'T:**
        - Menyembunyikan penyakit kronis saat pendaftaran
        - Melakukan aktivitas berbahaya/ekstrem
        - Mengabaikan gejala penyakit kecil
        - Buang dokumen/kuitansi medis
        - Lupa lapor ke travel agent jika sakit
        - Menolak perawatan karena takut biaya
        """)


# =============================================================================
# MAIN COMPONENT RENDERER
# =============================================================================

def render_insurance_explainer(compact: bool = False):
    """
    Render insurance explainer component.
    
    Args:
        compact: If True, render compact version for sidebar/modal
    """
    if compact:
        # Compact version for sidebar widget
        st.markdown("### 🏥 Asuransi Komprehensif")
        st.success("""
        ✅ 90 hari coverage
        ✅ Medical unlimited
        ✅ COVID-19 covered
        ✅ Repatriasi gratis
        ✅ Hotline 24/7
        """)
        
        if st.button("📖 Lihat Detail Lengkap", use_container_width=True):
            st.session_state.show_insurance_detail = True
            st.rerun()
    
    else:
        # Full version for dedicated page/section
        render_insurance_header()
        render_all_coverages()
        render_insurance_specs()
        render_claim_process()
        render_emergency_contacts()
        render_insurance_calculator()
        render_insurance_tips()


def render_insurance_modal():
    """Render insurance info as modal dialog."""
    if st.session_state.get("show_insurance_detail"):
        with st.container():
            st.markdown("---")
            render_insurance_explainer(compact=False)
            
            if st.button("✖️ Tutup", type="secondary"):
                st.session_state.show_insurance_detail = False
                st.rerun()


# Export
__all__ = [
    "render_insurance_explainer",
    "render_insurance_modal",
    "INSURANCE_COVERAGE",
    "INSURANCE_SPECS"
]