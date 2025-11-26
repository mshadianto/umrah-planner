"""
🕋 Umrah Planner AI - Main Application
======================================
RAG Agentic AI untuk Simulasi Biaya Perjalanan Umrah

Developed by: MS Hadianto
Email: sopian.hadianto@gmail.com
GitHub: https://github.com/mshadianto
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

# Page configuration
st.set_page_config(
    page_title=app_config.app_name,
    page_icon="🕋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        padding: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .highlight-box {
        background-color: #e3f2fd;
        border-left: 4px solid #1E88E5;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }
    .warning-box {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
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
    """Render sidebar with settings and navigation"""
    with st.sidebar:
        st.markdown("# 🕋")
        st.title("Umrah Planner")
        st.markdown(get_version_badge(), unsafe_allow_html=True)
        st.markdown("---")
        
        # User tier badge
        init_monetization_state()
        render_monetization_sidebar()
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "📍 Navigasi",
            [
                "🏠 Beranda",
                "💰 Simulasi Biaya",
                "📊 Perbandingan Skenario",
                "📅 Analisis Waktu",
                "🤖 Chat AI",
                "📋 Buat Rencana",
                "✈️ Booking & Reservasi",
                "🧰 Tools & Fitur",
                "💼 Business Hub",
                "⚙️ Pengaturan",
                "ℹ️ Tentang Aplikasi"
            ]
        )
        
        st.markdown("---")
        
        # Quick quote widget
        render_quick_quote_widget()
        
        st.markdown("---")
        
        # Quick info
        st.markdown("### 📌 Info Cepat")
        st.info(f"""
        **Provider LLM:** {llm_config.provider.upper()}
        **Model:** {llm_config.groq_model if llm_config.provider == 'groq' else llm_config.openai_model}
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        tips = [
            "Booking 3-4 bulan sebelumnya untuk harga terbaik",
            "Hindari Ramadhan jika budget terbatas",
            "Pilih hotel dekat Haram untuk jamaah lansia",
            "Bawa obat pribadi yang cukup",
            "Download peta offline sebelum berangkat",
            "Tukar uang ke Riyal sebelum berangkat",
        ]
        st.caption(tips[datetime.now().second % len(tips)])
        
        # Footer
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; font-size: 0.75rem; color: #888;">
            Made with ❤️ by<br>
            <strong>{DEVELOPER['name']}</strong><br>
            v{__version__}
        </div>
        """, unsafe_allow_html=True)
        
        return page


def render_home():
    """Render home page"""
    st.markdown('<h1 class="main-header">🕋 Umrah Planner AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Asisten Cerdas untuk Perencanaan Perjalanan Umrah Anda</p>', unsafe_allow_html=True)
    
    # Version badge
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1rem;">
        {get_version_badge()}
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards - Row 1
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>💰 Simulasi Biaya</h3>
            <p>Hitung estimasi biaya umrah dengan berbagai skenario</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Scenario Planning</h3>
            <p>Bandingkan opsi Ekonomis, Standard, Premium, dan VIP</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🤖 AI Assistant</h3>
            <p>Konsultasi dengan AI untuk pertanyaan seputar umrah</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature cards - Row 2 (NEW)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>✈️ Booking Tiket</h3>
            <p>Cari & bandingkan harga tiket pesawat</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🏨 Hotel & Akomodasi</h3>
            <p>Temukan hotel terbaik di Makkah & Madinah</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📦 Paket Travel</h3>
            <p>Bandingkan paket dari berbagai travel agent</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick start
    st.markdown("### 🚀 Mulai Cepat")
    
    col1, col2 = st.columns(2)
    
    with col1:
        scenario = st.selectbox(
            "Pilih Skenario",
            ["ekonomis", "standard", "premium", "vip"],
            format_func=lambda x: SCENARIO_TEMPLATES[x]["name"]
        )
    
    with col2:
        num_people = st.number_input(
            "Jumlah Jamaah",
            min_value=1,
            max_value=50,
            value=1
        )
    
    if st.button("🔍 Lihat Estimasi Cepat", use_container_width=True):
        template = SCENARIO_TEMPLATES[scenario]
        planner = st.session_state.scenario_planner
        result = planner.create_scenario(scenario, num_people)
        
        st.markdown("### 📋 Estimasi Cepat")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Estimasi Minimum",
                format_currency(result.estimated_min)
            )
        
        with col2:
            st.metric(
                "Estimasi Maksimum",
                format_currency(result.estimated_max)
            )
        
        with col3:
            st.metric(
                "Per Orang",
                format_currency(result.estimated_min / num_people)
            )
        
        # Features
        st.markdown("#### ✨ Fasilitas Termasuk:")
        for feature in result.features:
            st.markdown(f"• {feature}")
    
    # Why choose us section
    st.markdown("---")
    st.markdown("### 🌟 Mengapa Umrah Planner AI?")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <h1>🤖</h1>
            <strong>AI-Powered</strong>
            <p style="font-size: 0.85rem;">Didukung teknologi AI terdepan</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <h1>📊</h1>
            <strong>Data Akurat</strong>
            <p style="font-size: 0.85rem;">Estimasi biaya berdasarkan data real</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center;">
            <h1>🇮🇩</h1>
            <strong>Lokal Indonesia</strong>
            <p style="font-size: 0.85rem;">Disesuaikan untuk jamaah Indonesia</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center;">
            <h1>🆓</h1>
            <strong>100% Gratis</strong>
            <p style="font-size: 0.85rem;">Gunakan tanpa biaya apapun</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Lead capture CTA
    st.markdown("---")
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    ">
        <h2 style="margin: 0;">🎯 Dapatkan Penawaran Terbaik GRATIS!</h2>
        <p style="font-size: 1.1rem; margin: 1rem 0;">
            Travel agent terpercaya siap memberikan penawaran khusus untuk Anda
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("home_lead_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                lead_name = st.text_input("Nama", placeholder="Nama lengkap")
            with col_b:
                lead_phone = st.text_input("WhatsApp", placeholder="08xxxxxxxxxx")
            
            if st.form_submit_button("📞 Hubungi Saya", use_container_width=True, type="primary"):
                if lead_name and lead_phone:
                    st.success(f"✅ Terima kasih {lead_name}! Tim kami akan menghubungi Anda segera.")
                else:
                    st.error("Mohon isi nama dan nomor WhatsApp")
    
    # Partner logos
    st.markdown("---")
    st.markdown("### 🤝 Partner Travel Terpercaya")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    partners = ["🏢 Patuna", "🕌 Al Khalid", "⭐ Arminareka", "🌙 Maktour", "☪️ Ebad"]
    for i, partner in enumerate(partners):
        with [col1, col2, col3, col4, col5][i]:
            st.markdown(f"""
            <div style="
                background: #f5f5f5;
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
            ">
                <strong>{partner}</strong>
            </div>
            """, unsafe_allow_html=True)


def render_cost_simulation():
    """Render cost simulation page"""
    st.header("💰 Simulasi Biaya Umrah")
    
    # Input form
    with st.form("cost_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            scenario = st.selectbox(
                "Skenario Paket",
                ["ekonomis", "standard", "premium", "vip"],
                format_func=lambda x: SCENARIO_TEMPLATES[x]["name"]
            )
            
            num_people = st.number_input(
                "Jumlah Jamaah",
                min_value=1,
                max_value=50,
                value=2
            )
            
            duration = st.slider(
                "Durasi (hari)",
                min_value=7,
                max_value=21,
                value=SCENARIO_TEMPLATES[scenario]["duration_days"]
            )
        
        with col2:
            departure_city = st.selectbox(
                "Kota Keberangkatan",
                DEPARTURE_CITIES
            )
            
            departure_month = st.selectbox(
                "Bulan Keberangkatan",
                range(1, 13),
                format_func=lambda x: [
                    "Januari", "Februari", "Maret", "April",
                    "Mei", "Juni", "Juli", "Agustus",
                    "September", "Oktober", "November", "Desember"
                ][x-1]
            )
            
            special_requests = st.text_area(
                "Permintaan Khusus (opsional)",
                placeholder="Misal: jamaah lansia, butuh kursi roda, dll."
            )
        
        submitted = st.form_submit_button("🔍 Hitung Biaya", use_container_width=True)
    
    if submitted:
        with st.spinner("⏳ Menghitung estimasi biaya..."):
            # Create scenario
            planner = st.session_state.scenario_planner
            result = planner.create_scenario(
                scenario_type=scenario,
                num_people=num_people,
                duration_days=duration,
                departure_month=departure_month
            )
            
            st.session_state.current_scenario = result
        
        # Display results
        st.markdown("---")
        st.subheader("📊 Hasil Simulasi")
        
        # Key metrics
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
        
        # Season warning
        season_info = None
        for season in SEASONS.values():
            if departure_month in season["months"]:
                season_info = season
                break
        
        if season_info and season_info["multiplier"] > 1:
            st.markdown(f"""
            <div class="warning-box">
                ⚠️ <strong>Perhatian:</strong> Bulan {departure_month} termasuk musim {season_info['name']} 
                dengan kenaikan harga sekitar {int((season_info['multiplier']-1)*100)}%
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed breakdown visualization
        st.markdown("### 📈 Visualisasi Biaya")
        
        # Create breakdown chart
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
            fig = px.pie(
                df, 
                values="Estimasi", 
                names="Komponen",
                title="Distribusi Biaya",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                df,
                x="Komponen",
                y="Estimasi",
                title="Breakdown per Komponen",
                color="Komponen",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Features included
        st.markdown("### ✨ Fasilitas Termasuk")
        cols = st.columns(2)
        for i, feature in enumerate(result.features):
            cols[i % 2].markdown(f"✅ {feature}")
        
        # Notes
        if result.notes:
            st.markdown("### 📝 Catatan")
            for note in result.notes:
                st.markdown(note)
        
        # AI Analysis
        if st.session_state.orchestrator:
            st.markdown("### 🤖 Analisis AI")
            
            if st.button("💡 Dapatkan Saran AI"):
                with st.spinner("AI sedang menganalisis..."):
                    response = st.session_state.orchestrator.financial_agent.calculate_cost(
                        scenario=scenario,
                        num_people=num_people,
                        duration_days=duration,
                        departure_month=departure_month
                    )
                    st.markdown(response["response"])


def render_scenario_comparison():
    """Render scenario comparison page"""
    st.header("📊 Perbandingan Skenario")
    
    # Parameters
    col1, col2 = st.columns(2)
    
    with col1:
        num_people = st.number_input(
            "Jumlah Jamaah",
            min_value=1,
            max_value=50,
            value=1,
            key="compare_people"
        )
    
    with col2:
        duration = st.slider(
            "Durasi (hari)",
            min_value=7,
            max_value=21,
            value=12,
            key="compare_duration"
        )
    
    if st.button("🔍 Bandingkan Semua Skenario", use_container_width=True):
        planner = st.session_state.scenario_planner
        
        # Create all scenarios
        scenarios_data = []
        for stype in ["ekonomis", "standard", "premium", "vip"]:
            scenario = planner.create_scenario(
                scenario_type=stype,
                num_people=num_people,
                duration_days=duration
            )
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
        
        # Display comparison table
        st.markdown("### 📋 Tabel Perbandingan")
        st.dataframe(
            df.style.format({
                "Min (Rp)": "{:,.0f}",
                "Max (Rp)": "{:,.0f}"
            }),
            use_container_width=True
        )
        
        # Price comparison chart
        st.markdown("### 💰 Perbandingan Harga")
        
        fig = go.Figure()
        
        for scenario in scenarios_data:
            fig.add_trace(go.Bar(
                name=scenario["Skenario"],
                x=[scenario["Skenario"]],
                y=[(scenario["Min (Rp)"] + scenario["Max (Rp)"]) / 2],
                error_y=dict(
                    type='data',
                    symmetric=False,
                    array=[scenario["Max (Rp)"] - (scenario["Min (Rp)"] + scenario["Max (Rp)"]) / 2],
                    arrayminus=[(scenario["Min (Rp)"] + scenario["Max (Rp)"]) / 2 - scenario["Min (Rp)"]]
                )
            ))
        
        fig.update_layout(
            title="Range Harga per Skenario",
            yaxis_title="Estimasi Biaya (Rp)",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendation
        st.markdown("""
        <div class="highlight-box">
            <h4>💡 Rekomendasi</h4>
            <ul>
                <li><strong>Budget < Rp 35 juta:</strong> Pilih Ekonomis</li>
                <li><strong>Keseimbangan:</strong> Pilih Standard</li>
                <li><strong>Prioritas Kenyamanan:</strong> Pilih Premium</li>
                <li><strong>Pengalaman Terbaik:</strong> Pilih VIP</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


def render_time_analysis():
    """Render time analysis page"""
    st.header("📅 Analisis Waktu Terbaik Umrah")
    
    priority = st.selectbox(
        "Prioritas Anda",
        ["balanced", "cost", "crowd"],
        format_func=lambda x: {
            "balanced": "🎯 Seimbang (Harga & Keramaian)",
            "cost": "💰 Prioritas Hemat Biaya",
            "crowd": "👥 Prioritas Hindari Keramaian"
        }[x]
    )
    
    if st.button("📊 Analisis Waktu Terbaik", use_container_width=True):
        planner = st.session_state.scenario_planner
        analysis = planner.analyze_best_time(priority)
        
        # Best months
        st.markdown("### ✅ Bulan Terbaik untuk Umrah")
        
        cols = st.columns(3)
        for i, month_data in enumerate(analysis["best_months"]):
            with cols[i]:
                st.markdown(f"""
                <div class="success-box">
                    <h4>#{i+1} {month_data['month_name']}</h4>
                    <p>🌡️ Cuaca: {month_data['weather']}</p>
                    <p>💰 Multiplier: {month_data['price_multiplier']}x</p>
                    <p>👥 Keramaian: {month_data['crowd_level']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Avoid months
        st.markdown("### ⚠️ Bulan yang Perlu Dipertimbangkan")
        
        cols = st.columns(3)
        for i, month_data in enumerate(analysis["avoid_months"]):
            with cols[i]:
                st.markdown(f"""
                <div class="warning-box">
                    <h4>{month_data['month_name']}</h4>
                    <p>🌡️ Cuaca: {month_data['weather']}</p>
                    <p>💰 Multiplier: {month_data['price_multiplier']}x</p>
                    <p>👥 Keramaian: {month_data['crowd_level']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Full year chart
        st.markdown("### 📈 Analisis Sepanjang Tahun")
        
        df = pd.DataFrame(analysis["analysis"])
        
        fig = px.line(
            df,
            x="month_name",
            y="recommendation_score",
            title="Skor Rekomendasi per Bulan",
            markers=True
        )
        fig.update_layout(xaxis_title="Bulan", yaxis_title="Skor Rekomendasi")
        st.plotly_chart(fig, use_container_width=True)
        
        # Tips
        st.markdown("### 💡 Tips")
        for note in analysis["notes"]:
            st.markdown(f"• {note}")


def render_ai_chat():
    """Render AI chat page"""
    st.header("🤖 Chat dengan AI Assistant")
    
    # Initialize orchestrator if needed
    if st.session_state.orchestrator is None:
        st.warning("⚠️ Sistem AI belum diinisialisasi.")
        if st.button("🔄 Inisialisasi Sistem"):
            initialize_system()
            st.rerun()
        return
    
    # Chat interface
    st.markdown("Tanyakan apa saja tentang umrah kepada AI Assistant!")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ketik pertanyaan Anda..."):
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })
        st.chat_message("user").write(prompt)
        
        # Get AI response
        with st.spinner("🤔 AI sedang berpikir..."):
            try:
                response = st.session_state.orchestrator.chat(prompt)
                ai_response = response["response"]
            except Exception as e:
                ai_response = f"Maaf, terjadi error: {str(e)}"
        
        # Add AI response to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": ai_response
        })
        st.chat_message("assistant").write(ai_response)
    
    # Quick questions
    st.markdown("---")
    st.markdown("### 💡 Pertanyaan Cepat")
    
    quick_questions = [
        "Apa saja rukun umrah?",
        "Bagaimana tips hemat biaya umrah?",
        "Kapan waktu terbaik untuk umrah?",
        "Apa yang harus dipersiapkan sebelum umrah?",
        "Bagaimana memilih travel umrah yang terpercaya?",
    ]
    
    cols = st.columns(2)
    for i, q in enumerate(quick_questions):
        if cols[i % 2].button(q, key=f"quick_{i}"):
            st.session_state.chat_history.append({"role": "user", "content": q})
            st.rerun()
    
    # Clear chat
    if st.button("🗑️ Hapus Riwayat Chat"):
        st.session_state.chat_history = []
        if st.session_state.orchestrator:
            st.session_state.orchestrator.reset_conversations()
        st.rerun()


def render_create_plan():
    """Render create plan page"""
    st.header("📋 Buat Rencana Umrah Lengkap")
    
    if st.session_state.orchestrator is None:
        st.warning("⚠️ Sistem AI belum diinisialisasi.")
        if st.button("🔄 Inisialisasi Sistem"):
            initialize_system()
            st.rerun()
        return
    
    with st.form("plan_form"):
        st.markdown("### 📝 Detail Perjalanan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            scenario = st.selectbox(
                "Skenario Paket",
                ["ekonomis", "standard", "premium", "vip"],
                format_func=lambda x: SCENARIO_TEMPLATES[x]["name"]
            )
            
            num_people = st.number_input(
                "Jumlah Jamaah",
                min_value=1,
                max_value=50,
                value=2
            )
            
            duration = st.slider(
                "Durasi (hari)",
                min_value=7,
                max_value=21,
                value=12
            )
        
        with col2:
            departure_month = st.selectbox(
                "Bulan Keberangkatan",
                range(1, 13),
                format_func=lambda x: [
                    "Januari", "Februari", "Maret", "April",
                    "Mei", "Juni", "Juli", "Agustus",
                    "September", "Oktober", "November", "Desember"
                ][x-1]
            )
            
            special_requests = st.text_area(
                "Permintaan Khusus",
                placeholder="Misal: jamaah lansia, butuh kursi roda, vegetarian, dll."
            )
        
        submitted = st.form_submit_button("🚀 Buat Rencana Lengkap", use_container_width=True)
    
    if submitted:
        with st.spinner("⏳ AI sedang menyusun rencana lengkap..."):
            try:
                result = st.session_state.orchestrator.create_complete_plan(
                    scenario=scenario,
                    num_people=num_people,
                    duration_days=duration,
                    departure_month=departure_month,
                    special_requests=special_requests if special_requests else None
                )
                
                # Display results
                st.markdown("---")
                st.success("✅ Rencana berhasil dibuat!")
                
                # Financial summary
                st.markdown("### 💰 Ringkasan Biaya")
                if "calculation" in result["results"]["financial"]:
                    calc = result["results"]["financial"]["calculation"]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Minimum", format_currency(calc["total_min"]))
                    with col2:
                        st.metric("Total Maksimum", format_currency(calc["total_max"]))
                
                st.markdown(result["results"]["financial"]["response"])
                
                # Itinerary
                st.markdown("### 📅 Itinerary")
                st.markdown(result["results"]["itinerary"]["response"])
                
                # Requirements
                st.markdown("### 📋 Persyaratan")
                st.markdown(result["results"]["requirements"]["response"])
                
                # Tips
                st.markdown("### 💡 Tips")
                st.markdown(result["results"]["tips"]["response"])
                
            except Exception as e:
                st.error(f"Error: {str(e)}")


def render_settings():
    """Render settings page"""
    st.header("⚙️ Pengaturan")
    
    st.markdown("### 🔑 Konfigurasi API")
    
    provider = st.selectbox(
        "LLM Provider",
        ["groq", "openai"],
        index=0 if llm_config.provider == "groq" else 1
    )
    
    if provider == "groq":
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            value=llm_config.groq_api_key[:10] + "..." if llm_config.groq_api_key else ""
        )
        st.info("💡 Dapatkan API key gratis di https://console.groq.com")
    else:
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=llm_config.openai_api_key[:10] + "..." if llm_config.openai_api_key else ""
        )
        st.info("💡 Dapatkan API key di https://platform.openai.com")
    
    st.markdown("### 📊 Status Sistem")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Status Inisialisasi",
            "✅ Aktif" if st.session_state.initialized else "❌ Belum Aktif"
        )
    
    with col2:
        if st.session_state.orchestrator:
            stats = st.session_state.orchestrator.get_agent_status()
            st.metric(
                "Dokumen Knowledge Base",
                stats["rag_retriever"]["total_documents"]
            )
    
    if st.button("🔄 Reinisialisasi Sistem"):
        st.session_state.orchestrator = None
        st.session_state.initialized = False
        initialize_system()
        st.rerun()
    
    st.markdown("### ℹ️ Informasi Aplikasi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **{APP_INFO['name']}** v{__version__}
        
        {APP_INFO['tagline']}
        
        **Developer:** {DEVELOPER['name']}
        **Email:** {DEVELOPER['email']}
        """)
    
    with col2:
        st.info(f"""
        **Repository:**
        {APP_INFO['repository']}
        
        **Demo:**
        {APP_INFO['demo_url']}
        
        **License:** {APP_INFO['license']}
        """)


def render_about():
    """Render about page with developer info"""
    st.markdown('<h1 class="main-header">ℹ️ Tentang Aplikasi</h1>', unsafe_allow_html=True)
    
    # App info card
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
    ">
        <h1 style="margin: 0;">🕋 {APP_INFO['name']}</h1>
        <p style="font-size: 1.2rem; margin: 0.5rem 0;">{APP_INFO['tagline']}</p>
        <p style="
            background: rgba(255,255,255,0.2);
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        ">Version {__version__}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["👨‍💻 Developer", "📋 Changelog", "🔧 Tech Stack", "📊 Stats"])
    
    with tab1:
        st.markdown(get_developer_card(), unsafe_allow_html=True)
        
        st.markdown("### 📧 Kontak")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"📧 **Email**\n\n{DEVELOPER['email']}")
        with col2:
            wa_link = f"https://wa.me/{DEVELOPER['whatsapp']}"
            st.markdown(f"💬 **WhatsApp**\n\n[Chat]({wa_link})")
        with col3:
            st.markdown(f"🔗 **GitHub**\n\n[mshadianto]({DEVELOPER['github']})")
        with col4:
            st.markdown(f"💼 **LinkedIn**\n\n[Profile]({DEVELOPER['linkedin']})")
        
        st.markdown("---")
        st.markdown("### 🎯 Keahlian Developer")
        st.markdown("""
        - 📊 Governance, Risk & Compliance (GRC)
        - 🔍 Internal Audit & Quality Assurance
        - 🤖 AI-Powered Solutions
        - 📋 Corporate Governance Advisory
        - 💻 Full-Stack Development
        """)
    
    with tab2:
        st.markdown(get_changelog_markdown())
    
    with tab3:
        st.markdown("### 🔧 Technology Stack")
        
        for category, techs in TECH_STACK.items():
            st.markdown(f"#### {category.replace('_', ' ').title()}")
            for name, version, desc in techs:
                st.markdown(f"- **{name}** `{version}` - {desc}")
        
        st.markdown("---")
        st.markdown("### 📦 Source Code")
        st.code(f"git clone {APP_INFO['repository']}.git", language="bash")
        st.markdown(f"[📂 View on GitHub]({APP_INFO['repository']})")
    
    with tab4:
        st.markdown("### 📊 Application Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📅 Released", get_app_age())
        with col2:
            st.metric("🔄 Version", __version__)
        with col3:
            st.metric("📦 Modules", "8+")
        
        st.markdown("---")
        st.markdown("### 🌟 Features")
        
        features = [
            ("💰 Cost Simulation", "Simulate umrah costs with multiple scenarios"),
            ("📊 Scenario Comparison", "Compare economic, standard, premium, VIP packages"),
            ("🤖 AI Chat", "RAG-powered chatbot for umrah guidance"),
            ("✈️ Flight Search", "Search and compare flight prices"),
            ("🏨 Hotel Booking", "Find hotels in Makkah & Madinah"),
            ("📦 Package Comparison", "Compare travel agent packages"),
            ("🛂 Visa Tracker", "Track visa processing status"),
            ("💳 Payment Calculator", "Calculate installment plans"),
            ("✅ Preparation Checklist", "Interactive preparation checklist"),
            ("📿 Doa & Manasik", "Complete prayer and ritual guide"),
        ]
        
        col1, col2 = st.columns(2)
        for i, (name, desc) in enumerate(features):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"**{name}**\n\n{desc}")
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: #f5f5f5; border-radius: 10px;">
        <p>📜 Licensed under {APP_INFO['license']}</p>
        <p>Made with ❤️ in Indonesia 🇮🇩</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application entry point"""
    init_session_state()
    
    # Sidebar navigation
    page = render_sidebar()
    
    # Initialize system on first load
    if not st.session_state.initialized:
        # Check if API key is available
        if llm_config.groq_api_key or llm_config.openai_api_key:
            initialize_system()
    
    # Route to appropriate page
    if "Beranda" in page:
        render_home()
    elif "Simulasi Biaya" in page:
        render_cost_simulation()
    elif "Perbandingan" in page:
        render_scenario_comparison()
    elif "Analisis Waktu" in page:
        render_time_analysis()
    elif "Chat AI" in page:
        render_ai_chat()
    elif "Buat Rencana" in page:
        render_create_plan()
    elif "Booking" in page:
        st.header("✈️ Booking & Reservasi")
        st.markdown("Cari penerbangan, hotel, transportasi, dan paket travel terbaik")
        render_booking_features()
    elif "Tools" in page:
        st.header("🧰 Tools & Fitur Jamaah")
        render_additional_features()
    elif "Business" in page:
        st.header("💼 Business Hub")
        st.markdown("Monetisasi, partnership, dan fitur premium")
        render_monetization_page()
    elif "Pengaturan" in page:
        render_settings()
    elif "Tentang" in page:
        render_about()


if __name__ == "__main__":
    main()
