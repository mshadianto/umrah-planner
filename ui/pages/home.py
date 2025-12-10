"""
LABBAIK AI v6.0 - Home Page (Super WOW Edition)
===============================================
Stunning landing page with hero section, features showcase,
testimonials, stats counter, and interactive elements.
"""

import streamlit as st
from datetime import datetime, date, timedelta
import random

# =============================================================================
# PAGE CONFIG & STYLING
# =============================================================================

def inject_custom_css():
    """Inject custom CSS for stunning visuals."""
    st.markdown("""
    <style>
    /* Hero gradient background */
    .hero-section {
        background: linear-gradient(135deg, #1a5f3c 0%, #2d8659 50%, #3ba876 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Stats counter */
    .stats-container {
        display: flex;
        justify-content: space-around;
        padding: 2rem;
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        margin: 2rem 0;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1a5f3c;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Testimonial cards */
    .testimonial-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin: 1rem 0;
    }
    
    /* CTA button */
    .cta-button {
        background: linear-gradient(135deg, #ffd700 0%, #ffb700 100%);
        color: #1a1a1a !important;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: 700;
        text-decoration: none;
        display: inline-block;
        transition: transform 0.3s ease;
    }
    
    .cta-button:hover {
        transform: scale(1.05);
    }
    
    /* Floating animation */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #1a5f3c 0%, #3ba876 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# COMPONENTS
# =============================================================================

def render_hero_section():
    """Render hero section with call-to-action - BLACK GOLD theme."""
    
    # CSS only
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');
    
    .hero-section-v6 {
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 50%, #0d0d0d 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        text-align: center;
        color: white;
        border: 1px solid #d4af37;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.2);
    }
    
    .arabic-calligraphy-v6 {
        font-family: 'Amiri', serif;
        font-size: 2.2rem;
        color: #d4af37;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
    }
    
    .brand-name-v6 {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: 0.8rem;
        margin-bottom: 0.3rem;
        color: #d4af37;
    }
    
    .tagline-v6 {
        font-size: 1.2rem;
        color: #d4af37;
        margin-bottom: 0.3rem;
    }
    
    .subtitle-v6 {
        font-size: 0.95rem;
        color: #888;
        margin-bottom: 1rem;
    }
    
    .version-badge-v6 {
        display: inline-block;
        background: linear-gradient(135deg, #d4af37 0%, #f4d03f 50%, #d4af37 100%);
        color: #1a1a1a;
        padding: 0.4rem 1.2rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    .stat-card-v6 {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border: 1px solid #d4af37;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
    }
    
    .stat-icon-v6 { font-size: 1.5rem; }
    .stat-label-v6 { font-size: 0.75rem; color: #888; margin-top: 0.3rem; }
    .stat-value-v6 { font-size: 1.3rem; font-weight: bold; color: #d4af37; }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero content
    st.markdown("""
    <div class="hero-section-v6">
        <div class="arabic-calligraphy-v6">لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ</div>
        <div class="brand-name-v6">L A B B A I K</div>
        <div class="tagline-v6">Panggilan-Nya, Langkahmu</div>
        <div class="subtitle-v6">Platform Perencanaan Umrah AI #1 Indonesia</div>
        <div class="version-badge-v6">v6.0.0 - Super Boom Edition</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats using Streamlit columns
    col1, col2, col3, col4 = st.columns(4)
    
    stats = [
        ("🕋", "Panduan Manasik", "8 Rukun"),
        ("💰", "Budget Simulator", "Real-time"),
        ("👥", "Smart Matching", "AI-Powered"),
        ("🤲", "Koleksi Doa", "20+ Doa"),
    ]
    
    for col, (icon, label, value) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div class="stat-card-v6">
                <div class="stat-icon-v6">{icon}</div>
                <div class="stat-value-v6">{value}</div>
                <div class="stat-label-v6">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("")  # Spacer
    
    # CTA Buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🤖 AI Chat", type="primary", use_container_width=True):
            st.session_state.current_page = "chat"
            st.rerun()
    
    with col2:
        if st.button("💰 Simulasi Biaya", use_container_width=True):
            st.session_state.current_page = "simulator"
            st.rerun()
    
    with col3:
        if st.button("🧭 Umrah Mandiri", use_container_width=True):
            st.session_state.current_page = "umrah_mandiri"
            st.rerun()
    
    with col4:
        if st.button("👥 Umrah Bareng", use_container_width=True):
            st.session_state.current_page = "umrah_bareng"
            st.rerun()


def render_stats_counter():
    """Render animated stats counter."""
    
    # Skip - stats already in hero section
    pass


def render_3_pilar_framework():
    """Render Framework 3 Pilar Umrah Mandiri section - BLACK GOLD theme."""
    
    st.markdown("---")
    st.markdown("## 🏛️ Framework 3 Pilar Umrah Mandiri")
    st.caption("Sistem persiapan umrah mandiri yang komprehensif:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
             padding: 1.5rem; border-radius: 15px; text-align: center; height: 200px;
             border-top: 4px solid #d4af37; border: 1px solid #333;">
            <div style="font-size: 3rem;">📋</div>
            <h3 style="color: #d4af37; margin: 0.5rem 0;">Administrasi & Persiapan</h3>
            <p style="color: #888; font-size: 0.9rem;">Dokumen, legalitas, dan kesiapan sebelum keberangkatan</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
             padding: 1.5rem; border-radius: 15px; text-align: center; height: 200px;
             border-top: 4px solid #d4af37; border: 1px solid #333;">
            <div style="font-size: 3rem;">🏨</div>
            <h3 style="color: #d4af37; margin: 0.5rem 0;">Logistik & Akomodasi</h3>
            <p style="color: #888; font-size: 0.9rem;">Kenyamanan fisik dan efisiensi biaya</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
             padding: 1.5rem; border-radius: 15px; text-align: center; height: 200px;
             border-top: 4px solid #d4af37; border: 1px solid #333;">
            <div style="font-size: 3rem;">🚀</div>
            <h3 style="color: #d4af37; margin: 0.5rem 0;">Eksekusi di Lapangan</h3>
            <p style="color: #888; font-size: 0.9rem;">Survival tools setelah mendarat</p>
        </div>
        """, unsafe_allow_html=True)
    
    # CTA to Umrah Mandiri
    st.markdown("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🧭 Buka Panduan Umrah Mandiri", type="primary", use_container_width=True):
            st.session_state.current_page = "umrah_mandiri"
            st.rerun()


def render_features_showcase():
    """Render features showcase section - SUPER ENHANCED for Umrah Jamaah."""
    
    st.markdown("## ✨ Fitur Super Lengkap untuk Jemaah Umrah")
    st.caption("Semua tools yang Anda butuhkan dari persiapan hingga pulang ke tanah air")
    
    # UMRAH MANDIRI FEATURES
    st.markdown("### 🧭 Umrah Mandiri - Panduan Lengkap DIY")
    
    mandiri_features = [
        {
            "icon": "📿",
            "title": "Virtual Manasik Simulator",
            "description": "Latihan 8 rukun umrah interaktif dengan visualisasi langkah demi langkah. Lengkap dengan doa Arab, latin, dan artinya.",
            "highlight": "8 Langkah Interaktif"
        },
        {
            "icon": "🏛️",
            "title": "3 Pilar Framework",
            "description": "Checklist persiapan komprehensif: Administrasi (paspor, visa), Logistik (hotel, transport), Eksekusi (apps, survival kit).",
            "highlight": "15+ Checklist Items"
        },
        {
            "icon": "💰",
            "title": "AI Budget Optimizer",
            "description": "Hitung estimasi biaya detail: tiket, hotel Makkah & Madinah, transport, makan. Dengan tips hemat hingga 30%!",
            "highlight": "Smart Cost Calculation"
        },
        {
            "icon": "🌡️",
            "title": "Weather & Crowd Prediction",
            "description": "Info cuaca real-time Makkah & Madinah. Prediksi keramaian Thawaf per jam untuk hindari antrian panjang.",
            "highlight": "Best Time Recommendation"
        },
        {
            "icon": "🤲",
            "title": "Koleksi Doa Lengkap",
            "description": "50+ doa umrah dengan teks Arab, transliterasi latin, dan terjemahan. Kategori: Thawaf, Sa'i, Zamzam, dll.",
            "highlight": "Arabic + Latin + Arti"
        },
        {
            "icon": "🗺️",
            "title": "Peta Lokasi Penting",
            "description": "POI Makkah (Masjidil Haram, Jabal Nur, Mina, Arafah) dan Madinah (Masjid Nabawi, Raudhah, Quba, Uhud).",
            "highlight": "Interactive Map Guide"
        },
    ]
    
    for i in range(0, len(mandiri_features), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(mandiri_features):
                f = mandiri_features[i + j]
                with col:
                    with st.container(border=True):
                        st.markdown(f"### {f['icon']} {f['title']}")
                        st.write(f['description'])
                        st.info(f"✨ {f['highlight']}")
    
    st.markdown("---")
    
    # UMRAH BARENG FEATURES
    st.markdown("### 👥 Umrah Bareng - Cari Teman Perjalanan")
    
    bareng_features = [
        {
            "icon": "🎯",
            "title": "Smart Matching System",
            "description": "AI matching berdasarkan budget, tanggal, kota asal, gender, dan preferensi perjalanan. Match score hingga 100%!",
            "highlight": "AI-Powered Matching"
        },
        {
            "icon": "🏆",
            "title": "Trip Leader Verified",
            "description": "Lihat profil leader dengan rating, jumlah jamaah yang pernah dipimpin, dan review dari peserta sebelumnya.",
            "highlight": "Trusted Leaders"
        },
        {
            "icon": "💬",
            "title": "Group Chat & Discussion",
            "description": "Diskusi langsung dengan calon teman perjalanan. Koordinasi jadwal, meeting point, dan persiapan bersama.",
            "highlight": "Real-time Communication"
        },
        {
            "icon": "📋",
            "title": "Trip Management",
            "description": "Kelola trip dari pembuatan hingga keberangkatan. Track member, RSVP status, dan payment confirmation.",
            "highlight": "End-to-End Management"
        },
        {
            "icon": "⭐",
            "title": "Review & Rating System",
            "description": "Beri dan baca review pengalaman perjalanan. Bantu jamaah lain menemukan partner terbaik.",
            "highlight": "Community Trust"
        },
        {
            "icon": "🏅",
            "title": "Leaderboard & Badges",
            "description": "Kumpulkan badge: First Timer, Explorer, Community Helper. Naik peringkat di leaderboard jamaah!",
            "highlight": "Gamification"
        },
    ]
    
    for i in range(0, len(bareng_features), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(bareng_features):
                f = bareng_features[i + j]
                with col:
                    with st.container(border=True):
                        st.markdown(f"### {f['icon']} {f['title']}")
                        st.write(f['description'])
                        st.success(f"✨ {f['highlight']}")
    
    st.markdown("---")
    
    # TOOLS & UTILITIES
    st.markdown("### 🛠️ Tools & Utilities")
    
    tools_features = [
        {
            "icon": "🤖",
            "title": "AI Chat Assistant",
            "description": "Tanya apa saja tentang umrah 24/7. Dari syarat visa, tips packing, hingga rekomendasi hotel terbaik.",
            "highlight": "24/7 AI Support"
        },
        {
            "icon": "🐷",
            "title": "Tabungan Tracker",
            "description": "Set target tabungan umrah, track progress harian, dan dapatkan motivasi untuk mencapai goal Anda.",
            "highlight": "Goal Tracking"
        },
        {
            "icon": "⏰",
            "title": "Countdown Timer",
            "description": "Hitung mundur ke hari H keberangkatan. Dengan milestone reminder: 6 bulan, 3 bulan, 1 bulan, dll.",
            "highlight": "Smart Reminders"
        },
        {
            "icon": "🆘",
            "title": "Emergency SOS",
            "description": "Daftar kontak darurat lengkap: Polisi Saudi (999), Ambulance (997), KBRI Riyadh, KJRI Jeddah.",
            "highlight": "Safety First"
        },
        {
            "icon": "🎯",
            "title": "Daily Challenges",
            "description": "Tantangan harian: baca doa, pelajari frasa Arab, checklist persiapan. Dapatkan XP dan naik level!",
            "highlight": "Stay Motivated"
        },
        {
            "icon": "🏆",
            "title": "Achievement System",
            "description": "Unlock 10+ achievements: Langkah Pertama, Master Planner, Manasik Pro, Istiqomah 7 Hari, dll.",
            "highlight": "10+ Achievements"
        },
    ]
    
    for i in range(0, len(tools_features), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(tools_features):
                f = tools_features[i + j]
                with col:
                    with st.container(border=True):
                        st.markdown(f"### {f['icon']} {f['title']}")
                        st.write(f['description'])
                        st.warning(f"✨ {f['highlight']}")


def render_package_preview():
    """Render package preview section."""
    
    st.markdown("---")
    st.markdown("## 📦 Pilihan Paket Umrah")
    st.caption("Dari ekonomis hingga VIP, sesuaikan dengan kebutuhan Anda")
    
    packages = [
        {
            "name": "Backpacker",
            "icon": "🎒",
            "price": "18 Juta",
            "features": ["Hotel Bintang 3", "Tanpa makan", "Bus sharing"],
            "color": "#28a745"
        },
        {
            "name": "Reguler",
            "icon": "⭐",
            "price": "25 Juta",
            "features": ["Hotel Bintang 4", "Makan 3x", "Transport full"],
            "color": "#007bff",
            "popular": True
        },
        {
            "name": "Plus",
            "icon": "🌟",
            "price": "35 Juta",
            "features": ["Hotel Bintang 5", "Makan premium", "Transport VIP"],
            "color": "#6f42c1"
        },
        {
            "name": "VIP",
            "icon": "👑",
            "price": "55 Juta",
            "features": ["Suite room", "Fine dining", "Private car"],
            "color": "#fd7e14"
        },
    ]
    
    cols = st.columns(4)
    
    for col, pkg in zip(cols, packages):
        with col:
            with st.container(border=True):
                if pkg.get("popular"):
                    st.markdown("🔥 **POPULER**")
                
                st.markdown(f"### {pkg['icon']} {pkg['name']}")
                st.markdown(f"## Rp {pkg['price']}")
                st.caption("per orang")
                
                for feature in pkg['features']:
                    st.markdown(f"✓ {feature}")
                
                if st.button("Lihat Detail", key=f"pkg_{pkg['name']}", use_container_width=True):
                    st.session_state.current_page = "booking"
                    st.rerun()


def render_testimonials():
    """Render testimonials section."""
    
    st.markdown("---")
    st.markdown("## 💬 Apa Kata Mereka")
    st.caption("Testimoni jamaah yang telah menggunakan LABBAIK")
    
    testimonials = [
        {
            "name": "Budi Santoso",
            "location": "Jakarta",
            "rating": 5,
            "text": "AI Assistant sangat membantu! Semua pertanyaan saya tentang umrah dijawab dengan detail. Simulasi biayanya juga akurat.",
            "avatar": "👨"
        },
        {
            "name": "Siti Nurhaliza",
            "location": "Surabaya",
            "rating": 5,
            "text": "Fitur Umrah Bareng luar biasa! Saya menemukan teman perjalanan yang cocok dan kami jadi sahabat sampai sekarang.",
            "avatar": "👩"
        },
        {
            "name": "Ahmad Fauzi",
            "location": "Bandung",
            "rating": 5,
            "text": "Proses booking sangat mudah. Dari pemilihan paket sampai pembayaran, semuanya lancar. Recommended!",
            "avatar": "👨"
        },
        {
            "name": "Fatimah Zahra",
            "location": "Medan",
            "rating": 5,
            "text": "Knowledge base-nya lengkap banget. Saya jadi lebih paham tentang tata cara umrah sebelum berangkat.",
            "avatar": "👩"
        },
    ]
    
    cols = st.columns(2)
    
    for i, t in enumerate(testimonials):
        with cols[i % 2]:
            with st.container(border=True):
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    st.markdown(f"### {t['avatar']}")
                
                with col2:
                    st.markdown(f"**{t['name']}**")
                    st.caption(f"📍 {t['location']}")
                
                st.write(f'"{t["text"]}"')
                st.markdown("⭐" * t['rating'])


def render_upcoming_trips():
    """Render upcoming public trips section."""
    
    st.markdown("---")
    st.markdown("## 🗓️ Trip Umrah Terdekat")
    st.caption("Gabung dengan trip yang sudah terjadwal")
    
    trips = [
        {
            "title": "Umrah Ramadan 2025",
            "date": "15 Mar 2025",
            "duration": "14 hari",
            "slots": 12,
            "price": "35 Juta",
            "leader": "Ustadz Ahmad"
        },
        {
            "title": "Umrah Liburan Sekolah",
            "date": "20 Jun 2025",
            "duration": "10 hari",
            "slots": 8,
            "price": "28 Juta",
            "leader": "Ustadzah Siti"
        },
        {
            "title": "Umrah Akhir Tahun",
            "date": "25 Dec 2025",
            "duration": "12 hari",
            "slots": 15,
            "price": "30 Juta",
            "leader": "Ustadz Budi"
        },
    ]
    
    cols = st.columns(3)
    
    for col, trip in zip(cols, trips):
        with col:
            with st.container(border=True):
                st.markdown(f"### {trip['title']}")
                st.caption(f"📅 {trip['date']} · ⏱️ {trip['duration']}")
                
                st.markdown(f"👨‍🏫 **Leader:** {trip['leader']}")
                st.markdown(f"💰 **Mulai** Rp {trip['price']}")
                
                st.progress(1 - (trip['slots'] / 30))
                st.caption(f"🎫 {trip['slots']} slot tersisa")
                
                if st.button("Gabung", key=f"trip_{trip['title']}", type="primary", use_container_width=True):
                    st.session_state.current_page = "umrah_bareng"
                    st.rerun()


def render_quick_chat():
    """Render quick AI chat widget."""
    
    st.markdown("---")
    st.markdown("## 🤖 Tanya AI Sekarang")
    st.caption("Punya pertanyaan tentang umrah? Tanya langsung!")
    
    # Quick questions
    quick_questions = [
        "Apa syarat umrah?",
        "Berapa biaya umrah?",
        "Kapan waktu terbaik umrah?",
        "Apa yang harus dibawa?",
        "Bagaimana tata cara ihram?",
    ]
    
    st.markdown("**Pertanyaan populer:**")
    cols = st.columns(5)
    
    for col, q in zip(cols, quick_questions):
        with col:
            if st.button(q, key=f"quick_{q}", use_container_width=True):
                st.session_state.quick_question = q
                st.session_state.current_page = "chat"
                st.rerun()
    
    # Custom question
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_question = st.text_input(
            "Atau ketik pertanyaan Anda:",
            placeholder="Contoh: Apa saja rukun umrah?",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("Tanya 🚀", type="primary", use_container_width=True):
            if user_question:
                st.session_state.quick_question = user_question
                st.session_state.current_page = "chat"
                st.rerun()


def render_partners():
    """Render partners/trust badges section."""
    
    st.markdown("---")
    st.markdown("## 🤝 Dipercaya Oleh")
    
    partners = [
        "✈️ Garuda Indonesia",
        "🏨 Accor Hotels",
        "🕋 Saudi Airlines",
        "🏦 Bank Syariah Indonesia",
        "📋 Kemenag RI",
    ]
    
    cols = st.columns(5)
    
    for col, partner in zip(cols, partners):
        with col:
            st.markdown(f"**{partner}**")


def render_newsletter():
    """Render newsletter subscription section."""
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📬 Dapatkan Info Terbaru")
        st.caption("Promo, tips umrah, dan jadwal keberangkatan langsung ke inbox Anda")
    
    with col2:
        email = st.text_input("Email", placeholder="email@anda.com", label_visibility="collapsed")
        if st.button("Subscribe", type="primary", use_container_width=True):
            if email and "@" in email:
                st.success("✅ Terima kasih telah subscribe!")
            else:
                st.error("Email tidak valid")


def render_footer():
    """Render footer section."""
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 🕋 LABBAIK AI")
        st.caption("Platform Cerdas untuk Perjalanan Umrah")
        st.caption("© 2025 MS Hadianto")
    
    with col2:
        st.markdown("**Fitur**")
        st.caption("AI Assistant")
        st.caption("Cost Simulator")
        st.caption("Umrah Bareng")
        st.caption("Knowledge Base")
    
    with col3:
        st.markdown("**Bantuan**")
        st.caption("FAQ")
        st.caption("Kontak Kami")
        st.caption("Syarat & Ketentuan")
        st.caption("Kebijakan Privasi")
    
    with col4:
        st.markdown("**Ikuti Kami**")
        st.caption("📱 Instagram")
        st.caption("💬 WhatsApp")
        st.caption("▶️ YouTube")
        st.caption("💼 LinkedIn")


# =============================================================================
# MAIN PAGE RENDERER
# =============================================================================

def render_home_page():
    """Main home page renderer."""
    
    # Inject CSS
    inject_custom_css()
    
    # Render sections
    render_hero_section()
    render_3_pilar_framework()  # New 3 Pilar section
    render_features_showcase()
    render_package_preview()
    render_upcoming_trips()
    render_testimonials()
    render_quick_chat()
    render_partners()
    render_newsletter()
    render_footer()


# Export
__all__ = ["render_home_page"]
