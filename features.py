"""
Fitur Tambahan untuk Jamaah Umrah
=================================
Checklist, Kalkulator Tabungan, Doa & Manasik, dll
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json


# ============================================
# 1. CHECKLIST PERSIAPAN UMRAH
# ============================================

CHECKLIST_DATA = {
    "dokumen": {
        "title": "📄 Dokumen Penting",
        "items": [
            ("Paspor (masa berlaku min. 6 bulan)", True),
            ("Fotokopi paspor 5 lembar", True),
            ("Foto 4x6 background putih (10 lembar)", True),
            ("Kartu Keluarga (KK) asli + fotokopi", True),
            ("KTP asli + fotokopi", True),
            ("Buku Nikah (jika sudah menikah)", True),
            ("Akta Kelahiran (untuk anak < 18 thn)", False),
            ("Surat Izin Mahram (wanita < 45 thn)", False),
            ("Kartu Vaksin Meningitis", True),
            ("Sertifikat Vaksin COVID-19", True),
            ("Tiket Pesawat (print/digital)", True),
            ("Voucher Hotel", True),
            ("Bukti Asuransi Perjalanan", True),
        ]
    },
    "pakaian": {
        "title": "👕 Pakaian & Perlengkapan Ibadah",
        "items": [
            ("Kain Ihram (pria) - 2 set", True),
            ("Mukena putih (wanita) - 3 set", True),
            ("Baju muslim harian - 5 set", True),
            ("Pakaian dalam secukupnya", True),
            ("Sandal jepit (untuk thawaf)", True),
            ("Sepatu nyaman untuk jalan", True),
            ("Kaos kaki", True),
            ("Jaket tipis (untuk AC)", True),
            ("Sajadah travel", False),
            ("Tasbih", False),
            ("Al-Quran kecil", False),
            ("Buku Doa Umrah", True),
        ]
    },
    "kesehatan": {
        "title": "💊 Kesehatan & Obat-obatan",
        "items": [
            ("Obat pribadi (jika ada)", True),
            ("Obat sakit kepala/demam", True),
            ("Obat maag/pencernaan", True),
            ("Obat flu & batuk", True),
            ("Vitamin & suplemen", True),
            ("Masker (banyak)", True),
            ("Hand sanitizer", True),
            ("Minyak angin/balsem", True),
            ("Plester luka", True),
            ("Sunblock/sunscreen", True),
            ("Lip balm", True),
            ("Kacamata hitam", False),
        ]
    },
    "elektronik": {
        "title": "📱 Elektronik & Gadget",
        "items": [
            ("Handphone + charger", True),
            ("Power bank", True),
            ("Adapter universal", True),
            ("Kabel data cadangan", False),
            ("Earphone", False),
            ("Kamera (opsional)", False),
        ]
    },
    "lainnya": {
        "title": "🎒 Perlengkapan Lainnya",
        "items": [
            ("Koper ukuran sesuai", True),
            ("Tas kecil/selempang", True),
            ("Tas pinggang (untuk uang)", True),
            ("Payung lipat", True),
            ("Botol minum", True),
            ("Snack ringan dari Indonesia", False),
            ("Uang tunai SAR", True),
            ("Uang tunai IDR (untuk di bandara)", True),
            ("Gembok koper", True),
            ("Luggage tag", True),
        ]
    }
}


def render_checklist():
    """Render interactive checklist"""
    st.markdown("### ✅ Checklist Persiapan Umrah")
    st.markdown("Centang item yang sudah disiapkan:")
    
    # Initialize checklist state
    if "checklist_state" not in st.session_state:
        st.session_state.checklist_state = {}
    
    total_items = 0
    checked_items = 0
    
    for category_key, category_data in CHECKLIST_DATA.items():
        with st.expander(category_data["title"], expanded=True):
            for item, is_required in category_data["items"]:
                item_key = f"{category_key}_{item}"
                total_items += 1
                
                # Add required badge
                label = f"{item} {'🔴' if is_required else '⚪'}"
                
                checked = st.checkbox(
                    label,
                    key=item_key,
                    value=st.session_state.checklist_state.get(item_key, False)
                )
                
                st.session_state.checklist_state[item_key] = checked
                if checked:
                    checked_items += 1
    
    # Progress
    progress = checked_items / total_items if total_items > 0 else 0
    st.markdown("---")
    st.markdown(f"### 📊 Progress: {checked_items}/{total_items} ({progress*100:.0f}%)")
    st.progress(progress)
    
    if progress == 1.0:
        st.balloons()
        st.success("🎉 Alhamdulillah! Semua persiapan sudah lengkap!")
    elif progress >= 0.8:
        st.info("👍 Hampir selesai! Tinggal sedikit lagi.")
    elif progress >= 0.5:
        st.warning("⚠️ Masih ada beberapa item yang perlu disiapkan.")
    else:
        st.error("📋 Masih banyak yang perlu disiapkan. Semangat!")


# ============================================
# 2. KALKULATOR TABUNGAN UMRAH
# ============================================

def render_savings_calculator():
    """Render savings calculator"""
    st.markdown("### 💰 Kalkulator Tabungan Umrah")
    st.markdown("Rencanakan tabungan Anda untuk berangkat umrah:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        target_cost = st.number_input(
            "Target Biaya Umrah (Rp)",
            min_value=20_000_000,
            max_value=200_000_000,
            value=35_000_000,
            step=1_000_000,
            format="%d"
        )
        
        current_savings = st.number_input(
            "Tabungan Saat Ini (Rp)",
            min_value=0,
            max_value=200_000_000,
            value=5_000_000,
            step=500_000,
            format="%d"
        )
    
    with col2:
        target_date = st.date_input(
            "Target Tanggal Berangkat",
            value=datetime.now() + timedelta(days=365),
            min_value=datetime.now() + timedelta(days=30)
        )
        
        savings_frequency = st.selectbox(
            "Frekuensi Menabung",
            options=["Harian", "Mingguan", "Bulanan"],
            index=2
        )
    
    # Calculate
    remaining = target_cost - current_savings
    days_left = (target_date - datetime.now().date()).days
    weeks_left = days_left // 7
    months_left = days_left // 30
    
    if remaining > 0 and days_left > 0:
        daily_savings = remaining / days_left
        weekly_savings = remaining / max(weeks_left, 1)
        monthly_savings = remaining / max(months_left, 1)
        
        st.markdown("---")
        st.markdown("### 📈 Rencana Tabungan")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Harian",
                f"Rp {daily_savings:,.0f}",
                delta=f"{days_left} hari lagi"
            )
        
        with col2:
            st.metric(
                "Mingguan",
                f"Rp {weekly_savings:,.0f}",
                delta=f"{weeks_left} minggu lagi"
            )
        
        with col3:
            st.metric(
                "Bulanan",
                f"Rp {monthly_savings:,.0f}",
                delta=f"{months_left} bulan lagi"
            )
        
        # Progress bar
        progress = current_savings / target_cost
        st.markdown(f"**Progress Tabungan: {progress*100:.1f}%**")
        st.progress(min(progress, 1.0))
        
        # Tips
        st.markdown("---")
        st.markdown("### 💡 Tips Menabung")
        
        if monthly_savings > 5_000_000:
            st.warning(f"""
            ⚠️ Target tabungan bulanan cukup tinggi (Rp {monthly_savings:,.0f}/bulan).
            
            **Saran:**
            - Pertimbangkan untuk menunda 3-6 bulan
            - Cari penghasilan tambahan
            - Pilih paket umrah yang lebih ekonomis
            """)
        else:
            st.success(f"""
            ✅ Target tabungan realistis! 
            
            **Tips:**
            - Sisihkan di awal gajian (pay yourself first)
            - Buat rekening khusus tabungan umrah
            - Gunakan auto-debet untuk konsistensi
            - Investasikan di deposito/reksadana untuk hasil lebih
            """)
    
    elif remaining <= 0:
        st.success("🎉 Alhamdulillah! Dana sudah mencukupi. Saatnya booking!")
    else:
        st.error("⚠️ Target tanggal sudah lewat. Silakan pilih tanggal baru.")


# ============================================
# 3. COUNTDOWN TIMER
# ============================================

def render_countdown():
    """Render countdown to departure"""
    st.markdown("### ⏰ Countdown Keberangkatan")
    
    departure_date = st.date_input(
        "Tanggal Keberangkatan",
        value=datetime.now() + timedelta(days=90),
        min_value=datetime.now()
    )
    
    days_left = (departure_date - datetime.now().date()).days
    
    if days_left > 0:
        weeks = days_left // 7
        remaining_days = days_left % 7
        
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1e5128 0%, #4e9f3d 100%); border-radius: 15px; color: white;">
            <h1 style="font-size: 4rem; margin: 0;">{days_left}</h1>
            <p style="font-size: 1.5rem;">Hari Menuju Tanah Suci</p>
            <p style="font-size: 1rem;">({weeks} minggu {remaining_days} hari)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Milestones
        st.markdown("#### 📌 Milestone Persiapan")
        
        milestones = [
            (90, "Booking tiket & hotel"),
            (60, "Urus visa & vaksinasi"),
            (30, "Siapkan perlengkapan"),
            (14, "Medical check-up"),
            (7, "Packing & cek dokumen"),
            (3, "Konfirmasi semua booking"),
            (1, "Istirahat & persiapan mental"),
        ]
        
        for days, task in milestones:
            if days_left >= days:
                st.checkbox(f"H-{days}: {task}", key=f"milestone_{days}")
            else:
                st.markdown(f"~~H-{days}: {task}~~ ✅")
    
    elif days_left == 0:
        st.balloons()
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: gold; border-radius: 15px;">
            <h1>🕋 HARI INI!</h1>
            <p>Selamat menunaikan ibadah umrah!</p>
            <p>لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Masukkan tanggal keberangkatan yang akan datang.")


# ============================================
# 4. DOA & MANASIK GUIDE
# ============================================

DOA_MANASIK = {
    "niat_ihram": {
        "title": "1️⃣ Niat Ihram Umrah",
        "arabic": "لَبَّيْكَ اللَّهُمَّ عُمْرَةً",
        "latin": "Labbaika Allahumma 'Umratan",
        "arti": "Aku memenuhi panggilan-Mu ya Allah untuk umrah",
        "keterangan": "Diucapkan saat memasuki miqat"
    },
    "talbiyah": {
        "title": "2️⃣ Talbiyah",
        "arabic": "لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيكَ لَكَ لَبَّيْكَ، إِنَّ الْحَمْدَ وَالنِّعْمَةَ لَكَ وَالْمُلْكَ، لَا شَرِيكَ لَكَ",
        "latin": "Labbaika Allahumma labbaik, labbaika laa syariika laka labbaik, innal hamda wan ni'mata laka wal mulk, laa syariika lak",
        "arti": "Aku memenuhi panggilan-Mu ya Allah, aku memenuhi panggilan-Mu. Aku memenuhi panggilan-Mu, tidak ada sekutu bagi-Mu. Sesungguhnya segala puji, nikmat, dan kerajaan adalah milik-Mu. Tidak ada sekutu bagi-Mu.",
        "keterangan": "Dibaca sepanjang perjalanan hingga sampai Masjidil Haram"
    },
    "masuk_masjid": {
        "title": "3️⃣ Doa Masuk Masjidil Haram",
        "arabic": "بِسْمِ اللهِ وَالصَّلاَةُ وَالسَّلاَمُ عَلَى رَسُولِ اللهِ، اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ",
        "latin": "Bismillahi was-shalatu was-salamu 'ala Rasulillah, Allahumma aftah li abwaba rahmatik",
        "arti": "Dengan nama Allah, shalawat dan salam atas Rasulullah, Ya Allah bukakanlah untukku pintu-pintu rahmat-Mu",
        "keterangan": "Masuk dengan kaki kanan"
    },
    "melihat_kabah": {
        "title": "4️⃣ Doa Melihat Ka'bah",
        "arabic": "اللَّهُمَّ زِدْ هَذَا الْبَيْتَ تَشْرِيفًا وَتَعْظِيمًا وَتَكْرِيمًا وَمَهَابَةً، وَزِدْ مَنْ شَرَّفَهُ وَكَرَّمَهُ مِمَّنْ حَجَّهُ أَوِ اعْتَمَرَهُ تَشْرِيفًا وَتَكْرِيمًا وَتَعْظِيمًا وَبِرًّا",
        "latin": "Allahumma zid hadhal baita tasyrifan wa ta'zhiman wa takriman wa mahabah, wa zid man syarrafahu wa karramahu mimman hajjahu awi'tamarahu tasyrifan wa takriman wa ta'zhiman wa birra",
        "arti": "Ya Allah, tambahkanlah kemuliaan, keagungan, kehormatan dan kewibawaan pada rumah ini (Ka'bah), dan tambahkanlah kemuliaan, kehormatan, keagungan dan kebaikan kepada orang yang memuliakannya dari orang-orang yang berhaji atau berumrah ke sana.",
        "keterangan": "Saat pertama kali melihat Ka'bah, angkat tangan berdoa"
    },
    "thawaf": {
        "title": "5️⃣ Doa Memulai Thawaf (di Hajar Aswad)",
        "arabic": "بِسْمِ اللهِ وَاللهُ أَكْبَرُ",
        "latin": "Bismillahi wallahu akbar",
        "arti": "Dengan nama Allah, dan Allah Maha Besar",
        "keterangan": "Istilam (menghadap) Hajar Aswad di setiap putaran"
    },
    "rukun_yamani": {
        "title": "6️⃣ Doa Antara Rukun Yamani dan Hajar Aswad",
        "arabic": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ",
        "latin": "Rabbana atina fid-dunya hasanah wa fil-akhirati hasanah wa qina 'adzaban-nar",
        "arti": "Ya Tuhan kami, berilah kami kebaikan di dunia dan kebaikan di akhirat, dan lindungilah kami dari siksa api neraka",
        "keterangan": "Dibaca di setiap putaran thawaf"
    },
    "sai_shafa": {
        "title": "7️⃣ Doa di Bukit Shafa",
        "arabic": "إِنَّ الصَّفَا وَالْمَرْوَةَ مِنْ شَعَائِرِ اللهِ، أَبْدَأُ بِمَا بَدَأَ اللهُ بِهِ",
        "latin": "Innash-shafa wal-marwata min sya'a'irillah, abda'u bima bada'allahu bihi",
        "arti": "Sesungguhnya Shafa dan Marwah adalah sebagian dari syi'ar Allah. Aku memulai dengan apa yang Allah mulai dengannya.",
        "keterangan": "Dibaca saat pertama naik ke Shafa"
    },
    "tahallul": {
        "title": "8️⃣ Doa Setelah Tahallul",
        "arabic": "اَلْحَمْدُ لِلّٰهِ الَّذِيْ قَضٰى عَنَّا نُسُكَنَا",
        "latin": "Alhamdulillahil-ladzi qadha 'anna nusukana",
        "arti": "Segala puji bagi Allah yang telah menyelesaikan ibadah kami",
        "keterangan": "Setelah potong/cukur rambut"
    }
}


def render_doa_manasik():
    """Render doa and manasik guide"""
    st.markdown("### 📿 Panduan Doa & Manasik Umrah")
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📖 Doa-Doa Umrah", "🚶 Tata Cara Manasik", "🎥 Video Tutorial"])
    
    with tab1:
        for key, doa in DOA_MANASIK.items():
            with st.expander(doa["title"], expanded=False):
                st.markdown(f"""
                <div style="text-align: right; font-size: 1.5rem; font-family: 'Traditional Arabic', serif; line-height: 2; background: #f5f5f5; padding: 1rem; border-radius: 10px;">
                    {doa["arabic"]}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"**Latin:** *{doa['latin']}*")
                st.markdown(f"**Arti:** {doa['arti']}")
                st.info(f"📌 {doa['keterangan']}")
    
    with tab2:
        st.markdown("""
        #### 🕋 Urutan Manasik Umrah
        
        1. **Ihram dari Miqat**
           - Mandi sunnah
           - Pakai pakaian ihram
           - Niat umrah
           - Mulai membaca talbiyah
        
        2. **Thawaf (7 putaran)**
           - Mulai dari Hajar Aswad
           - Putaran 1-3: Ramal (jalan cepat) untuk pria
           - Putaran 4-7: Jalan biasa
           - Selesai dengan istilam Hajar Aswad
        
        3. **Shalat 2 Rakaat di Maqam Ibrahim**
           - Rakaat 1: Al-Kafirun
           - Rakaat 2: Al-Ikhlas
        
        4. **Minum Air Zamzam**
           - Berdoa sesuai hajat
        
        5. **Sa'i (7 kali)**
           - Mulai dari Shafa ke Marwah (1)
           - Marwah ke Shafa (2)
           - Berakhir di Marwah (7)
           - Pria: berlari kecil di area lampu hijau
        
        6. **Tahallul**
           - Pria: cukur/potong rambut
           - Wanita: potong ujung rambut ±3cm
        
        7. **Selesai - Keluar dari Ihram** ✅
        """)
    
    with tab3:
        st.markdown("#### 🎥 Video Panduan Manasik")
        st.video("https://www.youtube.com/watch?v=TRYDkDwqJv0")
        st.caption("Video panduan manasik umrah lengkap")


# ============================================
# 5. KONVERTER MATA UANG
# ============================================

def render_currency_converter():
    """Render currency converter"""
    st.markdown("### 💱 Konverter Mata Uang")
    
    # Exchange rates (approximate)
    RATES = {
        "IDR_TO_SAR": 0.000242,  # 1 IDR = 0.000242 SAR
        "SAR_TO_IDR": 4130,      # 1 SAR = 4130 IDR
        "IDR_TO_USD": 0.0000645, # 1 IDR = 0.0000645 USD
        "USD_TO_IDR": 15500,     # 1 USD = 15500 IDR
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        from_currency = st.selectbox(
            "Dari",
            options=["IDR (Rupiah)", "SAR (Riyal)", "USD (Dollar)"],
            index=0
        )
        amount = st.number_input(
            "Jumlah",
            min_value=0.0,
            value=1000000.0,
            step=100000.0,
            format="%.0f"
        )
    
    with col2:
        to_currency = st.selectbox(
            "Ke",
            options=["SAR (Riyal)", "IDR (Rupiah)", "USD (Dollar)"],
            index=0
        )
    
    # Convert
    from_code = from_currency.split()[0]
    to_code = to_currency.split()[0]
    
    if from_code == to_code:
        result = amount
    elif from_code == "IDR" and to_code == "SAR":
        result = amount * RATES["IDR_TO_SAR"]
    elif from_code == "SAR" and to_code == "IDR":
        result = amount * RATES["SAR_TO_IDR"]
    elif from_code == "IDR" and to_code == "USD":
        result = amount * RATES["IDR_TO_USD"]
    elif from_code == "USD" and to_code == "IDR":
        result = amount * RATES["USD_TO_IDR"]
    elif from_code == "SAR" and to_code == "USD":
        result = amount * RATES["SAR_TO_IDR"] * RATES["IDR_TO_USD"]
    elif from_code == "USD" and to_code == "SAR":
        result = amount * RATES["USD_TO_IDR"] * RATES["IDR_TO_SAR"]
    else:
        result = amount
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; padding: 1.5rem; background: #e8f5e9; border-radius: 10px;">
        <h2 style="margin: 0; color: #1e5128;">
            {amount:,.0f} {from_code} = {result:,.2f} {to_code}
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick reference
    st.markdown("---")
    st.markdown("#### 📊 Referensi Cepat")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("1 SAR", f"Rp {RATES['SAR_TO_IDR']:,.0f}")
    with col2:
        st.metric("1 USD", f"Rp {RATES['USD_TO_IDR']:,.0f}")
    with col3:
        st.metric("Rp 1 Juta", f"{1000000 * RATES['IDR_TO_SAR']:,.2f} SAR")
    
    st.caption("⚠️ Kurs bersifat estimasi. Cek kurs terkini sebelum penukaran.")


# ============================================
# 6. KONTAK DARURAT
# ============================================

def render_emergency_contacts():
    """Render emergency contacts"""
    st.markdown("### 🆘 Kontak Darurat")
    
    contacts = {
        "Indonesia": [
            ("🏛️ KBRI Riyadh", "+966-11-488-2800", "Alamat: Riyadh, Saudi Arabia"),
            ("🏛️ KJRI Jeddah", "+966-12-667-6270", "Alamat: Jeddah, Saudi Arabia"),
            ("✈️ Garuda Indonesia Jeddah", "+966-12-283-0303", "Bandara King Abdulaziz"),
        ],
        "Saudi Arabia": [
            ("🚔 Polisi", "999", "Keadaan darurat"),
            ("🚑 Ambulans", "997", "Keadaan darurat medis"),
            ("🚒 Pemadam Kebakaran", "998", "Kebakaran"),
            ("🏥 RS King Faisal (Makkah)", "+966-12-553-3300", "Rumah sakit utama"),
            ("🏥 RS King Fahd (Madinah)", "+966-14-839-0001", "Rumah sakit utama"),
        ],
        "Travel Agent": [
            ("📞 Travel Agent Anda", "...", "Isi nomor travel agent Anda"),
            ("👤 Muthawwif/Guide", "...", "Isi nomor muthawwif Anda"),
        ]
    }
    
    for category, items in contacts.items():
        st.markdown(f"#### 📌 {category}")
        for name, number, note in items:
            col1, col2, col3 = st.columns([2, 1, 2])
            with col1:
                st.markdown(f"**{name}**")
            with col2:
                st.code(number)
            with col3:
                st.caption(note)
        st.markdown("---")
    
    st.warning("""
    **💡 Tips Penting:**
    - Simpan semua nomor di HP sebelum berangkat
    - Catat nomor kamar hotel Anda
    - Bawa fotokopi paspor di dompet terpisah
    - Install aplikasi: **Eatmarna**, **Tawakkalna**, **WhatsApp**
    """)


# ============================================
# 7. CUACA MAKKAH & MADINAH
# ============================================

def render_weather_info():
    """Render weather information"""
    st.markdown("### 🌡️ Info Cuaca Makkah & Madinah")
    
    # Monthly average temperatures
    weather_data = {
        "Bulan": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"],
        "Makkah (°C)": [24, 25, 28, 32, 36, 38, 39, 38, 37, 33, 29, 25],
        "Madinah (°C)": [18, 20, 24, 29, 34, 37, 38, 38, 35, 30, 24, 19],
    }
    
    import pandas as pd
    df = pd.DataFrame(weather_data)
    
    # Line chart
    st.line_chart(df.set_index("Bulan"))
    
    # Current month recommendation
    current_month = datetime.now().month
    months_id = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
                 "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    
    makkah_temp = weather_data["Makkah (°C)"][current_month - 1]
    madinah_temp = weather_data["Madinah (°C)"][current_month - 1]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            f"🕋 Makkah ({months_id[current_month-1]})",
            f"{makkah_temp}°C",
            delta="Panas" if makkah_temp > 35 else "Nyaman" if makkah_temp > 28 else "Sejuk"
        )
    
    with col2:
        st.metric(
            f"🕌 Madinah ({months_id[current_month-1]})",
            f"{madinah_temp}°C",
            delta="Panas" if madinah_temp > 35 else "Nyaman" if madinah_temp > 28 else "Sejuk"
        )
    
    # Recommendations
    st.markdown("---")
    st.markdown("#### 👕 Rekomendasi Pakaian")
    
    if makkah_temp > 35:
        st.warning("""
        🌡️ **Cuaca Panas!**
        - Pakai baju berbahan tipis & menyerap keringat
        - Bawa payung untuk teduh
        - Minum air minimal 3 liter/hari
        - Hindari aktivitas siang (11:00-15:00)
        - Sunscreen SPF 50+
        """)
    elif makkah_temp > 28:
        st.info("""
        ☀️ **Cuaca Hangat**
        - Pakaian tipis tapi sopan
        - Jaket tipis untuk AC
        - Tetap bawa payung
        - Minum air yang cukup
        """)
    else:
        st.success("""
        🌤️ **Cuaca Nyaman**
        - Waktu terbaik untuk umrah!
        - Bawa jaket untuk malam hari
        - Cuaca ideal untuk ibadah
        """)


# ============================================
# MAIN RENDER FUNCTION
# ============================================

def render_additional_features():
    """Main function to render all additional features"""
    
    feature = st.selectbox(
        "Pilih Fitur",
        options=[
            "✅ Checklist Persiapan",
            "💰 Kalkulator Tabungan",
            "⏰ Countdown Keberangkatan",
            "📿 Doa & Manasik",
            "💱 Konverter Mata Uang",
            "🆘 Kontak Darurat",
            "🌡️ Info Cuaca",
        ],
        index=0
    )
    
    st.markdown("---")
    
    if "Checklist" in feature:
        render_checklist()
    elif "Tabungan" in feature:
        render_savings_calculator()
    elif "Countdown" in feature:
        render_countdown()
    elif "Doa" in feature:
        render_doa_manasik()
    elif "Konverter" in feature:
        render_currency_converter()
    elif "Kontak" in feature:
        render_emergency_contacts()
    elif "Cuaca" in feature:
        render_weather_info()