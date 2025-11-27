"""
🚀 Landing Page - High Converting
=================================
Landing page yang dioptimasi untuk konversi

Copyright (c) 2025 MS Hadianto. All Rights Reserved.
"""

import streamlit as st
from datetime import datetime, timedelta
import random

def render_landing_page():
    """Render high-converting landing page"""
    
    # Custom CSS for landing page
    st.markdown("""
    <style>
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #1e3c72 100%);
        padding: 60px 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    .hero-section::before {
        content: "🕋";
        position: absolute;
        font-size: 200px;
        opacity: 0.1;
        right: -30px;
        top: -30px;
    }
    .hero-title {
        color: #FFD700;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .hero-subtitle {
        color: white;
        font-size: 1.3em;
        margin-bottom: 20px;
    }
    .hero-cta {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #1e3c72 !important;
        padding: 15px 40px;
        border-radius: 30px;
        font-size: 1.2em;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
        transition: transform 0.3s;
    }
    .hero-cta:hover {
        transform: scale(1.05);
    }
    
    /* Stats Bar */
    .stats-bar {
        display: flex;
        justify-content: space-around;
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: -40px 20px 30px 20px;
        position: relative;
        z-index: 10;
    }
    .stat-item {
        text-align: center;
    }
    .stat-number {
        font-size: 2em;
        font-weight: bold;
        color: #1e3c72;
    }
    .stat-label {
        color: #666;
        font-size: 0.9em;
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        height: 100%;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .feature-icon {
        font-size: 3em;
        margin-bottom: 15px;
    }
    .feature-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #1e3c72;
        margin-bottom: 10px;
    }
    .feature-desc {
        color: #666;
        font-size: 0.95em;
    }
    
    /* Testimonial */
    .testimonial-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 15px;
    }
    .testimonial-text {
        font-style: italic;
        color: #333;
        margin-bottom: 15px;
    }
    .testimonial-author {
        font-weight: bold;
        color: #1e3c72;
    }
    .testimonial-rating {
        color: #FFD700;
    }
    
    /* Pricing Card */
    .pricing-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .pricing-popular {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #1e3c72;
        padding: 5px 20px;
        position: absolute;
        top: 15px;
        right: -30px;
        transform: rotate(45deg);
        font-size: 0.8em;
        font-weight: bold;
    }
    .pricing-title {
        font-size: 1.5em;
        font-weight: bold;
        color: #1e3c72;
        margin-bottom: 10px;
    }
    .pricing-price {
        font-size: 2.5em;
        font-weight: bold;
        color: #2a5298;
    }
    .pricing-period {
        color: #666;
        font-size: 0.9em;
    }
    .pricing-features {
        text-align: left;
        margin: 20px 0;
    }
    .pricing-feature {
        padding: 8px 0;
        border-bottom: 1px solid #eee;
    }
    
    /* CTA Section */
    .cta-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 50px 30px;
        border-radius: 20px;
        text-align: center;
        margin: 30px 0;
    }
    .cta-title {
        color: white;
        font-size: 2em;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .cta-subtitle {
        color: #eee;
        font-size: 1.1em;
        margin-bottom: 25px;
    }
    
    /* Trust Badges */
    .trust-badges {
        display: flex;
        justify-content: center;
        gap: 30px;
        flex-wrap: wrap;
        padding: 20px;
    }
    .trust-badge {
        text-align: center;
        opacity: 0.8;
    }
    
    /* Countdown */
    .countdown-bar {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .countdown-title {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .countdown-timer {
        font-size: 1.5em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Countdown Timer (Creates urgency)
    promo_end = datetime.now() + timedelta(days=3)
    st.markdown(f"""
    <div class="countdown-bar">
        <div class="countdown-title">🔥 PROMO SPESIAL BERAKHIR DALAM:</div>
        <div class="countdown-timer">3 Hari : 12 Jam : 45 Menit</div>
        <div>Diskon hingga 15% untuk pendaftaran hari ini!</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🕋 Umrah Planner AI</div>
        <div class="hero-subtitle">
            Platform Cerdas #1 Indonesia untuk Perencanaan Umrah<br>
            <strong>Hemat Waktu, Hemat Biaya, Ibadah Maksimal</strong>
        </div>
        <div style="color: #eee; margin: 20px 0;">
            ✅ Bandingkan 100+ Paket Umrah &nbsp;&nbsp;
            ✅ AI Assistant 24/7 &nbsp;&nbsp;
            ✅ Harga Terbaik Dijamin
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Bar
    st.markdown("""
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-number">15,000+</div>
            <div class="stat-label">Jamaah Terbantu</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">50+</div>
            <div class="stat-label">Travel Partner</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">4.9 ⭐</div>
            <div class="stat-label">Rating Pengguna</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">Rp 5M+</div>
            <div class="stat-label">Hemat Rata-rata</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick CTA
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 MULAI PERENCANAAN GRATIS", use_container_width=True, type="primary"):
            st.session_state.page = "ai_chat"
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Features Section
    st.markdown("## ✨ Kenapa Pilih Umrah Planner AI?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Assistant 24/7</div>
            <div class="feature-desc">
                Tanya apapun tentang umrah kapanpun. 
                AI kami siap membantu perencanaan Anda.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💰</div>
            <div class="feature-title">Hemat Hingga 30%</div>
            <div class="feature-desc">
                Bandingkan harga dari 50+ travel agent. 
                Dapatkan harga terbaik untuk budget Anda.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📋</div>
            <div class="feature-title">Perencanaan Lengkap</div>
            <div class="feature-desc">
                Dari estimasi biaya, jadwal, packing list, 
                hingga doa & manasik. Semua dalam satu aplikasi.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">✈️</div>
            <div class="feature-title">Booking Terintegrasi</div>
            <div class="feature-desc">
                Booking tiket, hotel, dan paket langsung 
                dari platform kami dengan harga spesial.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <div class="feature-title">Travel Agent Terpercaya</div>
            <div class="feature-desc">
                Semua partner kami memiliki izin PPIU resmi 
                dari Kementerian Agama RI.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📱</div>
            <div class="feature-title">Akses Kapan Saja</div>
            <div class="feature-desc">
                Aplikasi web yang bisa diakses dari HP, 
                tablet, atau laptop. Tanpa perlu install.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Social Proof - Testimonials
    st.markdown("## 💬 Apa Kata Jamaah Kami?")
    
    testimonials = [
        {
            "text": "Alhamdulillah, dengan Umrah Planner saya bisa membandingkan banyak paket dan hemat hampir Rp 7 juta! Sangat membantu untuk perencanaan pertama kali.",
            "author": "Ibu Fatimah, Jakarta",
            "rating": "⭐⭐⭐⭐⭐"
        },
        {
            "text": "AI-nya sangat pintar! Saya tanya tentang waktu terbaik umrah, langsung dijawab lengkap dengan pertimbangan cuaca dan keramaian. Recommended!",
            "author": "Bapak Ahmad, Surabaya", 
            "rating": "⭐⭐⭐⭐⭐"
        },
        {
            "text": "Proses booking sangat mudah. Tim support juga fast response. Paket yang saya dapat sesuai budget dan kualitasnya memuaskan.",
            "author": "Ibu Siti, Bandung",
            "rating": "⭐⭐⭐⭐⭐"
        }
    ]
    
    cols = st.columns(3)
    for i, testimonial in enumerate(testimonials):
        with cols[i]:
            st.markdown(f"""
            <div class="testimonial-card">
                <div class="testimonial-rating">{testimonial['rating']}</div>
                <div class="testimonial-text">"{testimonial['text']}"</div>
                <div class="testimonial-author">— {testimonial['author']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Pricing Section
    st.markdown("## 💎 Pilih Paket Anda")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="pricing-card">
            <div class="pricing-title">🆓 Gratis</div>
            <div class="pricing-price">Rp 0</div>
            <div class="pricing-period">Selamanya</div>
            <div class="pricing-features">
                <div class="pricing-feature">✅ 5 Chat AI / hari</div>
                <div class="pricing-feature">✅ Simulasi biaya dasar</div>
                <div class="pricing-feature">✅ Bandingkan 2 skenario</div>
                <div class="pricing-feature">❌ Simpan rencana</div>
                <div class="pricing-feature">❌ Export PDF</div>
                <div class="pricing-feature">❌ Priority support</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Mulai Gratis", use_container_width=True):
            st.session_state.page = "register"
    
    with col2:
        st.markdown("""
        <div class="pricing-card" style="border: 3px solid #FFD700; transform: scale(1.05);">
            <div class="pricing-popular">POPULER</div>
            <div class="pricing-title">⭐ Premium</div>
            <div class="pricing-price">Rp 149K</div>
            <div class="pricing-period">/ bulan</div>
            <div class="pricing-features">
                <div class="pricing-feature">✅ Chat AI Unlimited</div>
                <div class="pricing-feature">✅ Simulasi biaya lengkap</div>
                <div class="pricing-feature">✅ Bandingkan unlimited</div>
                <div class="pricing-feature">✅ Simpan 20 rencana</div>
                <div class="pricing-feature">✅ Export PDF</div>
                <div class="pricing-feature">✅ Diskon 10% booking</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔥 Pilih Premium", use_container_width=True, type="primary"):
            st.session_state.page = "subscribe"
            st.session_state.selected_plan = "premium"
    
    with col3:
        st.markdown("""
        <div class="pricing-card">
            <div class="pricing-title">👑 VIP Elite</div>
            <div class="pricing-price">Rp 499K</div>
            <div class="pricing-period">/ bulan</div>
            <div class="pricing-features">
                <div class="pricing-feature">✅ Semua fitur Premium</div>
                <div class="pricing-feature">✅ Dedicated assistant</div>
                <div class="pricing-feature">✅ Konsultasi via call</div>
                <div class="pricing-feature">✅ Cashback 5%</div>
                <div class="pricing-feature">✅ Free airport transfer</div>
                <div class="pricing-feature">✅ Diskon 15% booking</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pilih VIP", use_container_width=True):
            st.session_state.page = "subscribe"
            st.session_state.selected_plan = "vip"
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Lead Capture Section
    st.markdown("""
    <div class="cta-section">
        <div class="cta-title">📞 Mau Konsultasi Gratis?</div>
        <div class="cta-subtitle">
            Isi form di bawah dan travel agent berpengalaman kami<br>
            akan menghubungi Anda dalam 1x24 jam!
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Lead Form
    with st.form("landing_lead_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nama Lengkap *")
            phone = st.text_input("No. WhatsApp *", placeholder="08xxxxxxxxxx")
        
        with col2:
            city = st.selectbox("Kota", [
                "Jakarta", "Bandung", "Surabaya", "Medan", 
                "Makassar", "Semarang", "Yogyakarta", "Lainnya"
            ])
            travel_month = st.selectbox("Rencana Berangkat", [
                "Januari 2025", "Februari 2025", "Maret 2025",
                "Ramadhan 2025", "Setelah Lebaran 2025", "Belum Pasti"
            ])
        
        num_people = st.slider("Jumlah Jamaah", 1, 20, 2)
        
        submitted = st.form_submit_button("📩 DAPATKAN PENAWARAN TERBAIK", use_container_width=True)
        
        if submitted:
            if name and phone:
                # Save lead
                lead_data = {
                    "id": f"LEAD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000,9999)}",
                    "name": name,
                    "phone": phone,
                    "city": city,
                    "num_people": num_people,
                    "travel_month": travel_month,
                    "source": "landing_page",
                    "created_at": datetime.now().isoformat()
                }
                
                if 'leads' not in st.session_state:
                    st.session_state.leads = []
                st.session_state.leads.append(lead_data)
                
                st.success("✅ Terima kasih! Tim kami akan menghubungi Anda segera.")
                st.balloons()
            else:
                st.error("Mohon isi nama dan nomor WhatsApp")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Trust Section
    st.markdown("## 🏆 Dipercaya Oleh")
    
    st.markdown("""
    <div class="trust-badges">
        <div class="trust-badge">
            <div style="font-size: 2em;">🏛️</div>
            <div>Terdaftar di<br><strong>Kemenkumham</strong></div>
        </div>
        <div class="trust-badge">
            <div style="font-size: 2em;">🕌</div>
            <div>Partner dengan<br><strong>50+ PPIU</strong></div>
        </div>
        <div class="trust-badge">
            <div style="font-size: 2em;">🔒</div>
            <div>Pembayaran<br><strong>100% Aman</strong></div>
        </div>
        <div class="trust-badge">
            <div style="font-size: 2em;">⭐</div>
            <div>Rating<br><strong>4.9/5.0</strong></div>
        </div>
        <div class="trust-badge">
            <div style="font-size: 2em;">👥</div>
            <div>Sudah Digunakan<br><strong>15,000+ Jamaah</strong></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # FAQ Section
    st.markdown("## ❓ Pertanyaan Umum")
    
    with st.expander("Apakah Umrah Planner AI gratis?"):
        st.write("""
        Ya! Anda bisa menggunakan fitur dasar secara gratis, termasuk:
        - 5 chat AI per hari
        - Simulasi biaya dasar
        - Bandingkan 2 skenario
        
        Untuk fitur lebih lengkap, Anda bisa upgrade ke Premium atau VIP.
        """)
    
    with st.expander("Bagaimana cara kerja AI Assistant?"):
        st.write("""
        AI Assistant kami menggunakan teknologi terbaru (RAG + LLM) yang dilatih 
        khusus dengan data umrah terkini. Anda bisa bertanya tentang:
        - Estimasi biaya berdasarkan preferensi
        - Waktu terbaik untuk umrah
        - Perbandingan paket dan travel agent
        - Tips dan panduan manasik
        """)
    
    with st.expander("Apakah travel agent yang direkomendasikan terpercaya?"):
        st.write("""
        Ya, semua travel agent partner kami telah memiliki:
        - Izin PPIU resmi dari Kementerian Agama RI
        - Rating minimal 4.5/5.0
        - Track record minimal 3 tahun
        - Verifikasi legalitas oleh tim kami
        """)
    
    with st.expander("Bagaimana jika saya tidak puas dengan layanan?"):
        st.write("""
        Kami menyediakan garansi kepuasan:
        - Untuk subscription: Refund 100% dalam 7 hari pertama
        - Untuk booking: Sesuai kebijakan travel agent terkait
        - Support 24/7 via WhatsApp untuk bantuan
        """)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Final CTA
    st.markdown("""
    <div class="cta-section">
        <div class="cta-title">🕋 Wujudkan Impian Umrah Anda!</div>
        <div class="cta-subtitle">
            Mulai perencanaan sekarang dan dapatkan harga terbaik<br>
            untuk perjalanan ibadah Anda
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 MULAI SEKARANG - GRATIS!", use_container_width=True, type="primary"):
            st.session_state.page = "ai_chat"
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>© 2025 Umrah Planner AI by MS Hadianto. All Rights Reserved.</p>
        <p>
            <a href="#" style="color: #666; margin: 0 10px;">Syarat & Ketentuan</a> |
            <a href="#" style="color: #666; margin: 0 10px;">Kebijakan Privasi</a> |
            <a href="#" style="color: #666; margin: 0 10px;">Kontak</a>
        </p>
        <p>📧 sopian.hadianto@gmail.com | 📱 +62 815 9658 833</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_landing_page()
