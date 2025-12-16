"""
================================================================================
🕋 LABBAIK AI v6.0 - UMRAH MANDIRI SUPER BOOM EDITION
================================================================================
Gamification + Virtual Manasik + Budget AI + Weather + Daily Challenges
================================================================================
"""

import streamlit as st
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional

# =============================================================================
# 🎨 SUPER STYLING
# =============================================================================

SUPER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');

.hero-gradient {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
    padding: 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    border: 1px solid #d4af37;
}

.hero-gradient h1 { font-size: 2.5rem; margin-bottom: 0.5rem; color: #d4af37; }
.hero-gradient .arabic { font-size: 3rem; font-family: 'Amiri', serif; color: #d4af37; text-shadow: 0 0 20px rgba(212, 175, 55, 0.5); }

.xp-bar-container {
    background: #2d2d2d;
    border-radius: 20px;
    height: 30px;
    overflow: hidden;
    margin: 1rem 0;
    position: relative;
    border: 1px solid #d4af37;
}

.xp-bar-fill {
    background: linear-gradient(90deg, #d4af37, #f4d03f, #d4af37);
    height: 100%;
    border-radius: 20px;
    transition: width 0.5s ease;
}

.xp-bar-text {
    position: absolute;
    width: 100%;
    text-align: center;
    line-height: 30px;
    color: white;
    font-weight: bold;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}

.achievement-card {
    background: linear-gradient(145deg, #2d2d2d 0%, #1a1a1a 100%);
    border-radius: 15px;
    padding: 1rem;
    text-align: center;
    margin: 0.5rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    border: 1px solid #d4af37;
    color: white;
}

.achievement-card.locked {
    background: linear-gradient(145deg, #1a1a1a 0%, #0d0d0d 100%);
    opacity: 0.6;
    border-color: #444;
}

.weather-card {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    border-radius: 20px;
    padding: 1.5rem;
    color: white;
    text-align: center;
    border: 1px solid #d4af37;
}

.weather-temp { font-size: 4rem; font-weight: bold; color: #d4af37; }

.countdown-digit {
    background: linear-gradient(180deg, #1a1a1a 0%, #0d0d0d 100%);
    color: #d4af37;
    font-size: 2.5rem;
    font-weight: bold;
    padding: 0.75rem 1.25rem;
    border-radius: 10px;
    margin: 0.25rem;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    display: inline-block;
    border: 1px solid #d4af37;
}

.countdown-label {
    font-size: 0.75rem;
    color: #888;
    text-transform: uppercase;
    display: block;
    margin-top: 0.25rem;
}

.doa-arabic {
    font-size: 1.8rem;
    text-align: right;
    font-family: 'Amiri', serif;
    background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    border-right: 4px solid #d4af37;
    color: #d4af37;
}

.gold-text { color: #d4af37; }
.gold-border { border: 1px solid #d4af37; }
</style>
"""

# =============================================================================
# 🎮 GAMIFICATION DATA
# =============================================================================

LEVELS = [
    {"level": 1, "name": "Niat Suci", "min_xp": 0, "icon": "🌱"},
    {"level": 2, "name": "Pencari Ilmu", "min_xp": 100, "icon": "📚"},
    {"level": 3, "name": "Perencana Cermat", "min_xp": 300, "icon": "📝"},
    {"level": 4, "name": "Penabung Setia", "min_xp": 600, "icon": "💰"},
    {"level": 5, "name": "Siap Berangkat", "min_xp": 1000, "icon": "✈️"},
    {"level": 6, "name": "Muhrim Sejati", "min_xp": 1500, "icon": "🧕"},
    {"level": 7, "name": "Thawaf Champion", "min_xp": 2100, "icon": "🕋"},
    {"level": 8, "name": "Sa'i Warrior", "min_xp": 2800, "icon": "🏃"},
    {"level": 9, "name": "Jamaah Teladan", "min_xp": 3600, "icon": "⭐"},
    {"level": 10, "name": "Haji Mabrur", "min_xp": 5000, "icon": "👑"},
]

ACHIEVEMENTS = [
    {"id": "first_step", "name": "Langkah Pertama", "icon": "👣", "desc": "Mulai journey", "xp": 50, "cat": "journey"},
    {"id": "planner", "name": "Master Planner", "icon": "📋", "desc": "10 checklist selesai", "xp": 100, "cat": "journey"},
    {"id": "all_pillar", "name": "3 Pilar Complete", "icon": "🏛️", "desc": "Semua pilar selesai", "xp": 300, "cat": "journey"},
    {"id": "scholar", "name": "Pencari Ilmu", "icon": "📚", "desc": "Baca semua manasik", "xp": 150, "cat": "knowledge"},
    {"id": "budget_set", "name": "Budget Planner", "icon": "💰", "desc": "Hitung estimasi", "xp": 50, "cat": "financial"},
    {"id": "saver", "name": "Penabung Setia", "icon": "🐷", "desc": "Target tabungan", "xp": 75, "cat": "financial"},
    {"id": "passport", "name": "Paspor Ready", "icon": "🛂", "desc": "Checklist paspor", "xp": 100, "cat": "preparation"},
    {"id": "manasik_pro", "name": "Manasik Pro", "icon": "🕌", "desc": "Virtual manasik done", "xp": 150, "cat": "ibadah"},
    {"id": "streak_7", "name": "Istiqomah", "icon": "🔥", "desc": "7 hari streak", "xp": 250, "cat": "special"},
    {"id": "perfectionist", "name": "Perfectionist", "icon": "💎", "desc": "100% complete", "xp": 500, "cat": "special"},
]

DAILY_CHALLENGES = [
    {"id": "read_dua", "name": "Baca 1 Doa Umrah", "xp": 10, "icon": "📖"},
    {"id": "arabic", "name": "Pelajari 3 Frasa Arab", "xp": 15, "icon": "🗣️"},
    {"id": "checklist", "name": "Centang 3 Checklist", "xp": 20, "icon": "✅"},
    {"id": "save", "name": "Tabung Hari Ini", "xp": 25, "icon": "💰"},
    {"id": "talbiyah", "name": "Latihan Talbiyah", "xp": 20, "icon": "🎵"},
]

# =============================================================================
# 📿 VIRTUAL MANASIK DATA
# =============================================================================

MANASIK_STEPS = [
    {
        "step": 1, "title": "Niat & Persiapan", "icon": "🎯",
        "location": "Rumah / Hotel",
        "desc": "Niatkan umrah karena Allah. Persiapkan fisik, mental, dan spiritual.",
        "tips": ["Perbanyak istighfar", "Lunasi hutang", "Minta maaf keluarga"],
        "dua": "اَللّٰهُمَّ إِنِّيْ أُرِيْدُ الْعُمْرَةَ",
        "dua_latin": "Allahumma innii uridul 'umrah",
        "dua_arti": "Ya Allah, aku ingin melaksanakan umrah",
    },
    {
        "step": 2, "title": "Miqat & Ihram", "icon": "🧕",
        "location": "Bir Ali / Pesawat",
        "desc": "Mandi, wudhu, pakai pakaian ihram, niat umrah.",
        "tips": ["Pria: 2 kain putih tanpa jahitan", "Wanita: pakaian menutup aurat", "Pakai wangi sebelum ihram"],
        "dua": "لَبَّيْكَ اللّٰهُمَّ عُمْرَةً",
        "dua_latin": "Labbaik Allahumma 'umratan",
        "dua_arti": "Aku penuhi panggilan-Mu untuk umrah",
    },
    {
        "step": 3, "title": "Talbiyah", "icon": "🎵",
        "location": "Sejak Miqat",
        "desc": "Ucapkan talbiyah dengan suara keras (pria) hingga sampai Ka'bah.",
        "tips": ["Perbanyak sepanjang perjalanan", "Wanita dengan suara pelan", "Berhenti saat mulai thawaf"],
        "dua": "لَبَّيْكَ اللّٰهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيْكَ لَكَ لَبَّيْكَ",
        "dua_latin": "Labbaik Allahumma labbaik, labbaik laa syariika laka labbaik",
        "dua_arti": "Aku penuhi panggilan-Mu ya Allah",
    },
    {
        "step": 4, "title": "Thawaf", "icon": "🕋",
        "location": "Masjidil Haram",
        "desc": "Kelilingi Ka'bah 7 putaran berlawanan jarum jam.",
        "tips": ["Idhtiba (buka bahu kanan) untuk pria", "Raml 3 putaran pertama", "Mulai dari Hajar Aswad"],
        "dua": "بِسْمِ اللهِ وَاللهُ أَكْبَرُ",
        "dua_latin": "Bismillahi wallahu akbar",
        "dua_arti": "Dengan nama Allah, Allah Maha Besar",
    },
    {
        "step": 5, "title": "Sholat Maqam Ibrahim", "icon": "🙏",
        "location": "Belakang Maqam Ibrahim",
        "desc": "Sholat 2 rakaat sunnah thawaf.",
        "tips": ["Jika ramai, boleh di mana saja", "Baca Al-Kafirun & Al-Ikhlas"],
        "dua": "وَاتَّخِذُوا مِنْ مَقَامِ إِبْرَاهِيمَ مُصَلًّى",
        "dua_latin": "Wattakhidzu min maqami ibrahim mushalla",
        "dua_arti": "Jadikanlah Maqam Ibrahim tempat sholat",
    },
    {
        "step": 6, "title": "Minum Zamzam", "icon": "💧",
        "location": "Area Zamzam",
        "desc": "Minum air zamzam sambil berdoa.",
        "tips": ["Minum berdiri menghadap kiblat", "Berdoa sesuai hajat", "Minum sampai puas"],
        "dua": "اَللّٰهُمَّ إِنِّيْ أَسْأَلُكَ عِلْمًا نَافِعًا",
        "dua_latin": "Allahumma inni as'aluka 'ilman nafi'an",
        "dua_arti": "Ya Allah, aku memohon ilmu yang bermanfaat",
    },
    {
        "step": 7, "title": "Sa'i", "icon": "🏃",
        "location": "Shafa - Marwah",
        "desc": "Berjalan 7 kali antara Bukit Shafa dan Marwah.",
        "tips": ["Mulai dari Shafa", "Pria lari kecil di lampu hijau", "Selesai di Marwah"],
        "dua": "إِنَّ الصَّفَا وَالْمَرْوَةَ مِنْ شَعَائِرِ اللهِ",
        "dua_latin": "Innash shafa wal marwata min sya'airillah",
        "dua_arti": "Shafa dan Marwah adalah syiar Allah",
    },
    {
        "step": 8, "title": "Tahallul", "icon": "✂️",
        "location": "Sekitar Masjidil Haram",
        "desc": "Potong/cukur rambut untuk mengakhiri ihram.",
        "tips": ["Pria: cukur habis (afdhal)", "Wanita: potong ~3cm", "Larangan ihram selesai"],
        "dua": "اَلْحَمْدُ لِلّٰهِ الَّذِيْ قَضٰى عَنَّا نُسُكَنَا",
        "dua_latin": "Alhamdulillahilladzi qadha 'anna nusukana",
        "dua_arti": "Puji bagi Allah yang menyempurnakan ibadah kami",
    },
]

# =============================================================================
# 🏛️ 3 PILAR DATA
# =============================================================================

PILLAR_DATA = {
    "administrasi": {
        "title": "Pilar 1: Administrasi", "subtitle": "Pre-Departure", "icon": "📋", "color": "#1a5f3c",
        "tasks": [
            {"id": "passport", "name": "Paspor aktif >6 bulan", "xp": 50, "priority": "wajib", "icon": "🛂"},
            {"id": "photo", "name": "Foto 4x6 background putih", "xp": 10, "priority": "wajib", "icon": "📷"},
            {"id": "ticket", "name": "Tiket pesawat PP", "xp": 50, "priority": "wajib", "icon": "✈️"},
            {"id": "vaccine", "name": "Vaksin meningitis", "xp": 30, "priority": "wajib", "icon": "💉"},
            {"id": "insurance", "name": "Asuransi perjalanan", "xp": 20, "priority": "recommended", "icon": "🛡️"},
        ]
    },
    "logistik": {
        "title": "Pilar 2: Logistik", "subtitle": "Booking & Visa", "icon": "🏨", "color": "#2d8659",
        "tasks": [
            {"id": "visa", "name": "Visa umrah via Nusuk", "xp": 60, "priority": "wajib", "icon": "📄"},
            {"id": "hotel_makkah", "name": "Hotel Makkah booked", "xp": 50, "priority": "wajib", "icon": "🕋"},
            {"id": "hotel_madinah", "name": "Hotel Madinah booked", "xp": 50, "priority": "wajib", "icon": "🕌"},
            {"id": "raudhah", "name": "Slot Raudhah (wanita)", "xp": 40, "priority": "wajib", "icon": "💚"},
            {"id": "nusuk", "name": "Download & daftar Nusuk", "xp": 30, "priority": "wajib", "icon": "📱"},
        ]
    },
    "eksekusi": {
        "title": "Pilar 3: Eksekusi", "subtitle": "On-Site Survival", "icon": "🚀", "color": "#3ba876",
        "tasks": [
            {"id": "careem", "name": "Download Careem", "xp": 30, "priority": "wajib", "icon": "🚗"},
            {"id": "maps", "name": "Google Maps offline", "xp": 30, "priority": "wajib", "icon": "🗺️"},
            {"id": "riyal", "name": "Tukar Riyal tunai", "xp": 30, "priority": "wajib", "icon": "💵"},
            {"id": "powerbank", "name": "Powerbank charged", "xp": 10, "priority": "recommended", "icon": "🔋"},
            {"id": "medicine", "name": "Obat-obatan pribadi", "xp": 20, "priority": "wajib", "icon": "💊"},
        ]
    }
}

# =============================================================================
# 💰 BUDGET DATA
# =============================================================================

COST_COMPONENTS = {
    "flight": {
        "label": "✈️ Tiket Pesawat",
        "options": [
            {"name": "LCC Promo", "price": 5500000, "tips": "Book 2-3 bulan sebelumnya"},
            {"name": "LCC Regular", "price": 7000000, "tips": "Bagasi 20kg, no meal"},
            {"name": "Full Service", "price": 10000000, "tips": "Bagasi 30kg, meal included"},
            {"name": "Premium Airline", "price": 15000000, "tips": "Turkish, Emirates"},
        ]
    },
    "hotel_makkah": {
        "label": "🕋 Hotel Makkah",
        "per_night": True,
        "options": [
            {"name": "Budget (1km)", "price": 400000, "tips": "Jalan 15+ menit"},
            {"name": "Standard (500m)", "price": 700000, "tips": "Jalan 7-10 menit"},
            {"name": "Premium (200m)", "price": 1500000, "tips": "Dekat pintu"},
            {"name": "Luxury (50m)", "price": 3500000, "tips": "Clock Tower area"},
        ]
    },
    "hotel_madinah": {
        "label": "🕌 Hotel Madinah",
        "per_night": True,
        "options": [
            {"name": "Budget", "price": 350000, "tips": "Per malam"},
            {"name": "Standard", "price": 550000, "tips": "Per malam"},
            {"name": "Premium", "price": 1200000, "tips": "Dekat pintu"},
        ]
    },
    "transport": {
        "label": "🚗 Transport",
        "options": [
            {"name": "Budget (Bus+Train)", "price": 400000, "tips": "Total trip"},
            {"name": "Standard (Careem)", "price": 800000, "tips": "Total trip"},
            {"name": "Premium (Private)", "price": 2000000, "tips": "AC, guide"},
        ]
    },
    "meals": {
        "label": "🍽️ Makan",
        "per_day": True,
        "options": [
            {"name": "Hemat", "price": 100000, "tips": "Street food"},
            {"name": "Standard", "price": 200000, "tips": "Restaurant"},
            {"name": "Nyaman", "price": 350000, "tips": "Variety"},
        ]
    },
}

SAVING_TIPS = [
    {"tip": "Book tiket 2-3 bulan sebelumnya", "save": "Rp 2-3 juta", "icon": "✈️"},
    {"tip": "Pilih hotel 500m dari Haram", "save": "Rp 500K/malam", "icon": "🏨"},
    {"tip": "Gunakan HHR Train", "save": "Rp 300K", "icon": "🚄"},
    {"tip": "Umrah di luar Ramadan", "save": "30%", "icon": "📅"},
]

# =============================================================================
# 🌡️ WEATHER & OTHER DATA
# =============================================================================

WEATHER_DATA = {
    "makkah": {"temp": 38, "condition": "Cerah", "icon": "☀️", "humidity": 25},
    "madinah": {"temp": 35, "condition": "Cerah", "icon": "☀️", "humidity": 30},
}

CROWD_PREDICTION = [
    {"time": "00:00-03:00", "level": 2, "label": "Sepi", "color": "#28a745"},
    {"time": "03:00-06:00", "level": 3, "label": "Sedang", "color": "#ffc107"},
    {"time": "06:00-09:00", "level": 4, "label": "Ramai", "color": "#fd7e14"},
    {"time": "12:00-15:00", "level": 5, "label": "Sangat Ramai", "color": "#dc3545"},
    {"time": "18:00-21:00", "level": 5, "label": "Sangat Ramai", "color": "#dc3545"},
    {"time": "21:00-00:00", "level": 3, "label": "Sedang", "color": "#ffc107"},
]

EMERGENCY_CONTACTS = {
    "saudi": [
        {"name": "Police", "phone": "999", "icon": "👮"},
        {"name": "Ambulance", "phone": "997", "icon": "🚑"},
        {"name": "Fire", "phone": "998", "icon": "🚒"},
    ],
    "indonesia": [
        {"name": "KBRI Riyadh", "phone": "+966-11-488-2800", "icon": "🇮🇩"},
        {"name": "KJRI Jeddah", "phone": "+966-12-667-0826", "icon": "🇮🇩"},
    ],
}

DOA_COLLECTION = [
    # WAJIB
    {
        "name": "Talbiyah",
        "arabic": "لَبَّيْكَ اللّٰهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيْكَ لَكَ لَبَّيْكَ، إِنَّ الْحَمْدَ وَالنِّعْمَةَ لَكَ وَالْمُلْكَ، لَا شَرِيْكَ لَكَ",
        "latin": "Labbaik Allahumma labbaik, labbaik laa syariika laka labbaik, innal hamda wan ni'mata laka wal mulk, laa syariika lak",
        "meaning": "Aku penuhi panggilan-Mu ya Allah, tiada sekutu bagi-Mu. Segala puji, nikmat, dan kerajaan milik-Mu, tiada sekutu bagi-Mu",
        "when": "Sejak miqat hingga thawaf",
        "category": "wajib",
    },
    {
        "name": "Niat Umrah",
        "arabic": "اَللّٰهُمَّ إِنِّيْ أُرِيْدُ الْعُمْرَةَ فَيَسِّرْهَا لِيْ وَتَقَبَّلْهَا مِنِّيْ",
        "latin": "Allahumma innii uridul 'umrah, fayassirha lii wa taqabbalha minnii",
        "meaning": "Ya Allah, aku ingin umrah, mudahkanlah dan terimalah dariku",
        "when": "Saat niat ihram di miqat",
        "category": "wajib",
    },
    # THAWAF
    {
        "name": "Doa Mulai Thawaf (Hajar Aswad)",
        "arabic": "بِسْمِ اللهِ وَاللهُ أَكْبَرُ، اَللّٰهُمَّ إِيْمَانًا بِكَ وَتَصْدِيْقًا بِكِتَابِكَ",
        "latin": "Bismillahi wallahu akbar. Allahumma iimanan bika wa tashdiqan bikitabik",
        "meaning": "Dengan nama Allah, Allah Maha Besar. Ya Allah, dengan iman kepada-Mu dan membenarkan kitab-Mu",
        "when": "Saat melewati Hajar Aswad",
        "category": "thawaf",
    },
    {
        "name": "Doa Rukun Yamani",
        "arabic": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ",
        "latin": "Rabbana aatina fid dunya hasanah wa fil aakhirati hasanah wa qinaa 'adzaaban naar",
        "meaning": "Ya Tuhan kami, berilah kami kebaikan di dunia dan di akhirat, lindungi kami dari siksa neraka",
        "when": "Antara Rukun Yamani dan Hajar Aswad",
        "category": "thawaf",
    },
    {
        "name": "Doa Setelah Thawaf",
        "arabic": "اَللّٰهُمَّ قَنِّعْنِيْ بِمَا رَزَقْتَنِيْ وَبَارِكْ لِيْ فِيْهِ",
        "latin": "Allahumma qanni'nii bima razaqtanii wa baarik lii fiih",
        "meaning": "Ya Allah, jadikan aku puas dengan rizki yang Engkau berikan dan berkahilah",
        "when": "Setelah selesai 7 putaran thawaf",
        "category": "thawaf",
    },
    {
        "name": "Doa di Multazam",
        "arabic": "اَللّٰهُمَّ يَا رَبَّ الْبَيْتِ الْعَتِيْقِ، أَعْتِقْ رِقَابَنَا وَرِقَابَ آبَائِنَا وَأُمَّهَاتِنَا مِنَ النَّارِ",
        "latin": "Allahumma ya rabbal baytil 'atiq, a'tiq riqabana wa riqaba aba'ina wa ummahatina minan naar",
        "meaning": "Ya Allah Tuhan rumah tua ini, bebaskanlah kami, ayah dan ibu kami dari neraka",
        "when": "Saat berdoa di Multazam",
        "category": "thawaf",
    },
    # SA'I
    {
        "name": "Doa Naik Shafa",
        "arabic": "إِنَّ الصَّفَا وَالْمَرْوَةَ مِنْ شَعَائِرِ اللهِ",
        "latin": "Innash shafa wal marwata min sya'airillah",
        "meaning": "Sesungguhnya Shafa dan Marwah adalah syiar-syiar Allah",
        "when": "Saat naik ke Bukit Shafa",
        "category": "sai",
    },
    {
        "name": "Doa di Shafa",
        "arabic": "لَا إِلٰهَ إِلَّا اللهُ وَحْدَهُ لَا شَرِيْكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلٰى كُلِّ شَيْءٍ قَدِيْرٌ",
        "latin": "Laa ilaaha illallahu wahdahu laa syariika lah, lahul mulku wa lahul hamdu wa huwa 'ala kulli syai'in qadiir",
        "meaning": "Tiada Tuhan selain Allah, Esa, tiada sekutu. Milik-Nya kerajaan dan pujian, Maha Kuasa atas segala sesuatu",
        "when": "Saat di atas Bukit Shafa menghadap Ka'bah",
        "category": "sai",
    },
    {
        "name": "Doa Saat Sa'i",
        "arabic": "رَبِّ اغْفِرْ وَارْحَمْ وَأَنْتَ الْأَعَزُّ الْأَكْرَمُ",
        "latin": "Rabbighfir warham wa antal a'azzul akram",
        "meaning": "Ya Tuhanku, ampuni dan rahmatilah, Engkau Maha Mulia dan Maha Pemurah",
        "when": "Dibaca selama perjalanan sa'i",
        "category": "sai",
    },
    # ZAMZAM
    {
        "name": "Doa Minum Zamzam",
        "arabic": "اَللّٰهُمَّ إِنِّيْ أَسْأَلُكَ عِلْمًا نَافِعًا وَرِزْقًا وَاسِعًا وَشِفَاءً مِنْ كُلِّ دَاءٍ",
        "latin": "Allahumma inni as'aluka 'ilman nafi'an wa rizqan wasi'an wa syifa'an min kulli da'",
        "meaning": "Ya Allah, aku mohon ilmu bermanfaat, rizki yang luas, dan kesembuhan dari segala penyakit",
        "when": "Saat minum air zamzam",
        "category": "zamzam",
    },
    # MADINAH
    {
        "name": "Doa Masuk Masjid Nabawi",
        "arabic": "اَللّٰهُمَّ افْتَحْ لِيْ أَبْوَابَ رَحْمَتِكَ",
        "latin": "Allahummaftah lii abwaba rahmatik",
        "meaning": "Ya Allah, bukakanlah untukku pintu-pintu rahmat-Mu",
        "when": "Saat masuk Masjid Nabawi",
        "category": "madinah",
    },
    {
        "name": "Salam kepada Rasulullah",
        "arabic": "اَلسَّلَامُ عَلَيْكَ يَا رَسُوْلَ اللهِ، اَلسَّلَامُ عَلَيْكَ يَا نَبِيَّ اللهِ",
        "latin": "Assalamu 'alaika ya Rasulallah, assalamu 'alaika ya Nabiyyallah",
        "meaning": "Salam sejahtera atasmu wahai Rasulullah, salam sejahtera atasmu wahai Nabi Allah",
        "when": "Saat di depan makam Rasulullah SAW",
        "category": "madinah",
    },
    {
        "name": "Doa di Raudhah",
        "arabic": "اَللّٰهُمَّ اجْعَلْ فِيْ قَلْبِيْ نُوْرًا وَفِيْ سَمْعِيْ نُوْرًا وَفِيْ بَصَرِيْ نُوْرًا",
        "latin": "Allahummaj'al fii qalbii nuran wa fii sam'ii nuran wa fii basarii nuran",
        "meaning": "Ya Allah, jadikanlah cahaya di hatiku, pendengaranku, dan penglihatanku",
        "when": "Saat sholat di Raudhah",
        "category": "madinah",
    },
    # UMUM
    {
        "name": "Doa Perjalanan",
        "arabic": "سُبْحَانَ الَّذِيْ سَخَّرَ لَنَا هٰذَا وَمَا كُنَّا لَهُ مُقْرِنِيْنَ وَإِنَّا إِلٰى رَبِّنَا لَمُنْقَلِبُوْنَ",
        "latin": "Subhanalladzi sakhkhara lana hadza wa ma kunna lahu muqrinin, wa inna ila rabbina lamunqalibun",
        "meaning": "Maha Suci yang menundukkan ini untuk kami, padahal kami tidak mampu, dan kepada Tuhan kami akan kembali",
        "when": "Saat naik kendaraan/pesawat",
        "category": "umum",
    },
    {
        "name": "Doa Keluar Rumah",
        "arabic": "بِسْمِ اللهِ تَوَكَّلْتُ عَلَى اللهِ، لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللهِ",
        "latin": "Bismillahi tawakkaltu 'alallah, la hawla wa la quwwata illa billah",
        "meaning": "Dengan nama Allah aku bertawakkal, tiada daya dan kekuatan kecuali dengan Allah",
        "when": "Saat keluar rumah/hotel",
        "category": "umum",
    },
    {
        "name": "Doa Sebelum Tidur",
        "arabic": "بِاسْمِكَ اللّٰهُمَّ أَمُوْتُ وَأَحْيَا",
        "latin": "Bismika Allahumma amuutu wa ahya",
        "meaning": "Dengan nama-Mu ya Allah, aku mati dan hidup",
        "when": "Sebelum tidur di hotel",
        "category": "umum",
    },
    {
        "name": "Doa Bangun Tidur",
        "arabic": "اَلْحَمْدُ لِلّٰهِ الَّذِيْ أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُوْرُ",
        "latin": "Alhamdulillahilladzi ahyana ba'da ma amatana wa ilaihin nusyur",
        "meaning": "Segala puji bagi Allah yang menghidupkan kami setelah mematikan dan kepada-Nya kebangkitan",
        "when": "Saat bangun tidur",
        "category": "umum",
    },
    {
        "name": "Doa Mohon Keselamatan",
        "arabic": "اَللّٰهُمَّ إِنِّيْ أَسْأَلُكَ الْعَافِيَةَ فِي الدُّنْيَا وَالْآخِرَةِ",
        "latin": "Allahumma inni as'alukal 'afiyata fid dunya wal akhirah",
        "meaning": "Ya Allah, aku mohon keselamatan di dunia dan akhirat",
        "when": "Setiap saat",
        "category": "umum",
    },
    {
        "name": "Istighfar",
        "arabic": "أَسْتَغْفِرُ اللهَ الْعَظِيْمَ الَّذِيْ لَا إِلٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّوْمُ وَأَتُوْبُ إِلَيْهِ",
        "latin": "Astaghfirullahal 'azhim alladzi la ilaha illa huwal hayyul qayyum wa atubu ilaih",
        "meaning": "Aku mohon ampun kepada Allah Yang Maha Agung, tiada Tuhan selain Dia Yang Maha Hidup dan Maha Tegak, aku bertaubat kepada-Nya",
        "when": "Setiap saat, terutama di Tanah Suci",
        "category": "umum",
    },
    {
        "name": "Doa Tahallul",
        "arabic": "اَلْحَمْدُ لِلّٰهِ الَّذِيْ قَضٰى عَنَّا نُسُكَنَا",
        "latin": "Alhamdulillahilladzi qadha 'anna nusukana",
        "meaning": "Segala puji bagi Allah yang telah menyempurnakan ibadah kami",
        "when": "Setelah tahallul (potong rambut)",
        "category": "wajib",
    },
]

MAKKAH_POIS = [
    {"name": "Masjidil Haram", "icon": "🕋", "desc": "Ka'bah, Hajar Aswad"},
    {"name": "Jabal Nur", "icon": "🏔️", "desc": "Gua Hira"},
    {"name": "Jabal Tsur", "icon": "🗻", "desc": "Gua hijrah"},
    {"name": "Mina", "icon": "⛺", "desc": "Lempar jumrah"},
    {"name": "Arafah", "icon": "☀️", "desc": "Wukuf"},
    {"name": "Abraj Al-Bait", "icon": "🏨", "desc": "Clock Tower"},
]

MADINAH_POIS = [
    {"name": "Masjid Nabawi", "icon": "🕌", "desc": "Makam Rasulullah"},
    {"name": "Raudhah", "icon": "💚", "desc": "Taman surga"},
    {"name": "Masjid Quba", "icon": "🕌", "desc": "Masjid pertama"},
    {"name": "Jabal Uhud", "icon": "⛰️", "desc": "Perang Uhud"},
    {"name": "Makam Baqi", "icon": "🪦", "desc": "Pemakaman sahabat"},
]

# =============================================================================
# 🔧 SESSION STATE
# =============================================================================

def init_super_state():
    """Initialize all session state."""
    if "um_xp" not in st.session_state:
        st.session_state.um_xp = 0
    if "um_level" not in st.session_state:
        st.session_state.um_level = 1
    if "um_achievements" not in st.session_state:
        st.session_state.um_achievements = ["first_step"]
    if "um_daily_completed" not in st.session_state:
        st.session_state.um_daily_completed = []
    if "um_streak" not in st.session_state:
        st.session_state.um_streak = 0
    if "um_tasks" not in st.session_state:
        st.session_state.um_tasks = {"administrasi": [], "logistik": [], "eksekusi": []}
    if "um_departure_date" not in st.session_state:
        st.session_state.um_departure_date = None
    if "um_duration" not in st.session_state:
        st.session_state.um_duration = 9
    if "um_manasik_step" not in st.session_state:
        st.session_state.um_manasik_step = 0
    if "um_manasik_completed" not in st.session_state:
        st.session_state.um_manasik_completed = []
    if "um_savings" not in st.session_state:
        st.session_state.um_savings = {"target": 20000000, "current": 0, "history": []}


def add_xp(amount: int, reason: str = ""):
    """Add XP and check level up."""
    st.session_state.um_xp += amount
    for level_data in reversed(LEVELS):
        if st.session_state.um_xp >= level_data["min_xp"]:
            if st.session_state.um_level < level_data["level"]:
                st.session_state.um_level = level_data["level"]
                st.balloons()
                st.toast(f"🎉 Level Up! {level_data['name']}")
            break
    if reason:
        st.toast(f"+{amount} XP: {reason}")


def unlock_achievement(aid: str):
    """Unlock achievement."""
    if aid not in st.session_state.um_achievements:
        ach = next((a for a in ACHIEVEMENTS if a["id"] == aid), None)
        if ach:
            st.session_state.um_achievements.append(aid)
            add_xp(ach["xp"], f"🏆 {ach['name']}")
            st.balloons()


def get_current_level():
    """Get current level."""
    for lv in reversed(LEVELS):
        if st.session_state.um_xp >= lv["min_xp"]:
            return lv
    return LEVELS[0]


def get_next_level():
    """Get next level."""
    curr = get_current_level()
    for lv in LEVELS:
        if lv["level"] > curr["level"]:
            return lv
    return None


# =============================================================================
# 🎨 RENDER FUNCTIONS
# =============================================================================

def render_hero():
    """Render hero header - BLACK GOLD theme."""
    st.markdown(SUPER_CSS, unsafe_allow_html=True)
    st.markdown("""
    <div class="hero-gradient">
        <div class="arabic">🕋 لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ</div>
        <h1>UMRAH MANDIRI</h1>
        <p style="font-size: 1.2rem; opacity: 0.9; color: #ccc;">Panduan Terlengkap Perjalanan Spiritual</p>
    </div>
    """, unsafe_allow_html=True)


def render_gamification_bar():
    """Render XP bar - BLACK GOLD theme."""
    curr = get_current_level()
    nxt = get_next_level()
    
    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
    
    with col1:
        st.markdown(f"<div style='text-align:center;'><span style='font-size:2.5rem;'>{curr['icon']}</span><br><b style='color:#d4af37;'>Lv {curr['level']}</b><br><small style='color:#888;'>{curr['name']}</small></div>", unsafe_allow_html=True)
    
    with col2:
        if nxt:
            prog = (st.session_state.um_xp - curr["min_xp"]) / (nxt["min_xp"] - curr["min_xp"])
            prog = min(max(prog, 0), 1)
            st.markdown(f"""
            <div class="xp-bar-container">
                <div class="xp-bar-fill" style="width: {prog * 100}%;"></div>
                <div class="xp-bar-text">{st.session_state.um_xp} / {nxt['min_xp']} XP</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="xp-bar-container">
                <div class="xp-bar-fill" style="width:100%;"></div>
                <div class="xp-bar-text">🏆 MAX - {st.session_state.um_xp} XP</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.metric("🏆 Badges", f"{len(st.session_state.um_achievements)}/{len(ACHIEVEMENTS)}")
    
    with col4:
        st.metric("🔥 Streak", f"{st.session_state.um_streak}d")


def render_quick_stats():
    """Render quick stats - BLACK GOLD theme."""
    total_tasks = sum(len(p["tasks"]) for p in PILLAR_DATA.values())
    done_tasks = sum(len(st.session_state.um_tasks[p]) for p in PILLAR_DATA)
    task_pct = done_tasks / total_tasks * 100 if total_tasks > 0 else 0
    manasik_pct = len(st.session_state.um_manasik_completed) / len(MANASIK_STEPS) * 100
    savings_pct = st.session_state.um_savings["current"] / st.session_state.um_savings["target"] * 100
    
    cols = st.columns(4)
    
    with cols[0]:
        with st.container(border=True):
            st.markdown("### 📋 Persiapan")
            st.progress(task_pct / 100)
            st.caption(f"{done_tasks}/{total_tasks} ({task_pct:.0f}%)")
    
    with cols[1]:
        with st.container(border=True):
            st.markdown("### 📿 Manasik")
            st.progress(manasik_pct / 100)
            st.caption(f"{len(st.session_state.um_manasik_completed)}/8 langkah")
    
    with cols[2]:
        with st.container(border=True):
            st.markdown("### 💰 Tabungan")
            st.progress(min(savings_pct / 100, 1.0))
            st.caption(f"Rp {st.session_state.um_savings['current']:,.0f}".replace(",", "."))
    
    with cols[3]:
        with st.container(border=True):
            st.markdown("### ⏰ Countdown")
            if st.session_state.um_departure_date:
                days = (st.session_state.um_departure_date - date.today()).days
                if days > 0:
                    st.markdown(f"<h2 style='color:#d4af37;text-align:center;'>{days}</h2>", unsafe_allow_html=True)
                    st.caption("hari lagi")
                else:
                    st.success("🕋 Berangkat!")
            else:
                st.caption("Set tanggal")


def render_countdown():
    """Render countdown widget."""
    st.markdown("## ⏰ Countdown to Baitullah")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        dep = st.date_input("Tanggal Keberangkatan", value=st.session_state.um_departure_date or date.today() + timedelta(days=90), min_value=date.today())
        st.session_state.um_departure_date = dep
        dur = st.slider("Durasi (hari)", 7, 21, st.session_state.um_duration)
        st.session_state.um_duration = dur
    
    with col2:
        if st.session_state.um_departure_date:
            days = (st.session_state.um_departure_date - date.today()).days
            if days > 0:
                months = days // 30
                weeks = (days % 30) // 7
                rem = days % 7
                st.markdown(f"""
                <div style="text-align:center;padding:1rem;">
                    <span class="countdown-digit">{months}</span>
                    <span class="countdown-digit">{weeks}</span>
                    <span class="countdown-digit">{rem}</span>
                    <div style="margin-top:0.5rem;">
                        <span class="countdown-label" style="display:inline-block;width:60px;">Bulan</span>
                        <span class="countdown-label" style="display:inline-block;width:60px;">Minggu</span>
                        <span class="countdown-label" style="display:inline-block;width:60px;">Hari</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)


def render_pillars():
    """Render 3 pillar dashboard."""
    st.markdown("## 🏛️ 3 Pilar Persiapan")
    
    tabs = st.tabs([f"{PILLAR_DATA[p]['icon']} {PILLAR_DATA[p]['title'].split(':')[1]}" for p in PILLAR_DATA])
    
    for tab, (pid, pillar) in zip(tabs, PILLAR_DATA.items()):
        with tab:
            done = len(st.session_state.um_tasks[pid])
            total = len(pillar["tasks"])
            pct = done / total * 100 if total > 0 else 0
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {pillar['icon']} {pillar['title']}")
                st.caption(pillar['subtitle'])
                st.progress(pct / 100)
            with col2:
                if done == total:
                    st.success("✅ COMPLETE!")
            
            st.divider()
            
            for task in pillar["tasks"]:
                is_done = task["id"] in st.session_state.um_tasks[pid]
                col1, col2, col3 = st.columns([0.5, 3, 1])
                
                with col1:
                    if st.checkbox("✓", value=is_done, key=f"{pid}_{task['id']}", label_visibility="collapsed"):
                        if task["id"] not in st.session_state.um_tasks[pid]:
                            st.session_state.um_tasks[pid].append(task["id"])
                            add_xp(task["xp"], task["name"])
                    else:
                        if task["id"] in st.session_state.um_tasks[pid]:
                            st.session_state.um_tasks[pid].remove(task["id"])
                
                with col2:
                    badge = {"wajib": "🔴", "recommended": "🟡"}.get(task["priority"], "🟢")
                    if is_done:
                        st.markdown(f"~~{task['icon']} {task['name']}~~ ✅")
                    else:
                        st.markdown(f"{task['icon']} {task['name']} {badge}")
                
                with col3:
                    st.caption(f"+{task['xp']} XP")


def render_manasik():
    """Render virtual manasik - BLACK GOLD theme."""
    st.markdown("## 📿 Virtual Manasik Simulator")
    
    cols = st.columns(len(MANASIK_STEPS))
    for i, col in enumerate(cols):
        with col:
            is_done = i in st.session_state.um_manasik_completed
            is_curr = i == st.session_state.um_manasik_step
            color = "#d4af37" if is_done else ("#f4d03f" if is_curr else "#333")
            st.markdown(f"""
            <div style="text-align:center;">
                <div style="width:35px;height:35px;border-radius:50%;background:{color};display:flex;align-items:center;justify-content:center;margin:auto;color:{'#1a1a1a' if is_done or is_curr else '#888'};font-weight:bold;font-size:0.8rem;border:1px solid #d4af37;">{i+1}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    curr = MANASIK_STEPS[st.session_state.um_manasik_step]
    is_curr_done = st.session_state.um_manasik_step in st.session_state.um_manasik_completed
    
    with st.container(border=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {curr['icon']} Langkah {curr['step']}: {curr['title']}")
            st.markdown(f"📍 **Lokasi:** {curr['location']}")
            st.write(curr['desc'])
            st.markdown("**💡 Tips:**")
            for tip in curr['tips']:
                st.markdown(f"• {tip}")
        
        with col2:
            st.markdown("**🤲 Doa:**")
            st.markdown(f"<div class='doa-arabic'>{curr['dua']}</div>", unsafe_allow_html=True)
            st.caption(curr['dua_latin'])
            st.caption(f"*{curr['dua_arti']}*")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.um_manasik_step > 0:
            if st.button("⬅️ Sebelumnya", use_container_width=True):
                st.session_state.um_manasik_step -= 1
                st.rerun()
    
    with col2:
        if not is_curr_done:
            if st.button("✅ Tandai Selesai", use_container_width=True, type="primary"):
                st.session_state.um_manasik_completed.append(st.session_state.um_manasik_step)
                add_xp(25, f"Manasik: {curr['title']}")
                if len(st.session_state.um_manasik_completed) == len(MANASIK_STEPS):
                    unlock_achievement("manasik_pro")
                st.rerun()
        else:
            st.success("✅ Sudah dipelajari!")
    
    with col3:
        if st.session_state.um_manasik_step < len(MANASIK_STEPS) - 1:
            if st.button("Selanjutnya ➡️", use_container_width=True):
                st.session_state.um_manasik_step += 1
                st.rerun()


def render_budget():
    """Render budget optimizer."""
    st.markdown("## 💰 AI Budget Optimizer")
    
    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input("Total Budget (Rp)", 10000000, 100000000, 25000000, 1000000)
    with col2:
        priority = st.selectbox("Prioritas", ["💰 Hemat", "⚖️ Seimbang", "✨ Kenyamanan"])
    
    duration = st.slider("Durasi (hari)", 7, 21, 9, key="budget_duration")
    is_ramadan = st.checkbox("🌙 Musim Ramadan (+30%)")
    
    st.divider()
    
    selections = {}
    
    for cid, comp in COST_COMPONENTS.items():
        st.markdown(f"### {comp['label']}")
        
        idx = st.selectbox(
            f"Pilih {comp['label']}",
            range(len(comp["options"])),
            format_func=lambda i, c=comp: f"{c['options'][i]['name']} - Rp {c['options'][i]['price']:,}".replace(",", "."),
            key=f"budget_{cid}"
        )
        
        opt = comp["options"][idx]
        
        if comp.get("per_night"):
            price = opt["price"] * (duration - 1)
            st.caption(f"💡 {opt['tips']} • Total: Rp {price:,}".replace(",", "."))
        elif comp.get("per_day"):
            price = opt["price"] * duration
            st.caption(f"💡 {opt['tips']} • Total: Rp {price:,}".replace(",", "."))
        else:
            price = opt["price"]
            st.caption(f"💡 {opt['tips']}")
        
        selections[cid] = price
    
    subtotal = sum(selections.values()) + 1500000
    total = int(subtotal * 1.3) if is_ramadan else subtotal
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 Ringkasan")
        for cid, price in selections.items():
            st.markdown(f"• {COST_COMPONENTS[cid]['label']}: **Rp {price:,}**".replace(",", "."))
    
    with col2:
        delta = budget - total
        if delta >= 0:
            st.success(f"### ✅ Total: Rp {total:,}".replace(",", "."))
            st.info(f"💰 Sisa: Rp {delta:,}".replace(",", "."))
        else:
            st.error(f"### ⚠️ Total: Rp {total:,}".replace(",", "."))
    
    if st.button("💾 Simpan Budget", type="primary"):
        add_xp(50, "Budget planned!")
        unlock_achievement("budget_set")
        st.success("✅ Tersimpan!")


def render_weather():
    """Render weather & crowd."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## 🌡️ Cuaca")
        city = st.radio("Kota", ["makkah", "madinah"], format_func=lambda x: "🕋 Makkah" if x == "makkah" else "🕌 Madinah", horizontal=True)
        w = WEATHER_DATA[city]
        st.markdown(f"""
        <div class="weather-card">
            <div style="font-size:4rem;">{w['icon']}</div>
            <div class="weather-temp">{w['temp']}°C</div>
            <div>{w['condition']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("## 👥 Prediksi Keramaian Thawaf")
        for p in CROWD_PREDICTION:
            bars = "█" * p["level"] + "░" * (5 - p["level"])
            st.markdown(f"<div style='display:flex;'><span style='width:100px;'>{p['time']}</span><span style='color:{p['color']};font-family:monospace;'>{bars}</span></div>", unsafe_allow_html=True)
        st.success("✅ Best: 00:00-03:00")


def render_doa():
    """Render doa collection - EXPANDED with 20+ doa."""
    st.markdown("## 🤲 Koleksi Doa Umrah Lengkap")
    st.caption(f"📖 {len(DOA_COLLECTION)} doa untuk ibadah umrah Anda")
    
    cats = {
        "wajib": "🔴 Wajib/Rukun", 
        "thawaf": "🕋 Thawaf", 
        "sai": "🏃 Sa'i", 
        "zamzam": "💧 Zamzam",
        "madinah": "🕌 Madinah",
        "umum": "📿 Doa Umum"
    }
    cat = st.radio("Kategori", list(cats.keys()), format_func=lambda x: cats[x], horizontal=True)
    
    filtered = [d for d in DOA_COLLECTION if d["category"] == cat]
    
    st.caption(f"📖 {len(filtered)} doa dalam kategori ini")
    
    for doa in filtered:
        with st.container(border=True):
            st.markdown(f"### {doa['name']}")
            st.markdown(f"<div class='doa-arabic'>{doa['arabic']}</div>", unsafe_allow_html=True)
            st.markdown(f"**Latin:** {doa['latin']}")
            st.markdown(f"**Arti:** *{doa['meaning']}*")
            st.caption(f"⏰ Waktu: {doa['when']}")


def render_map():
    """Render map explorer."""
    st.markdown("## 🗺️ Lokasi Penting")
    
    city = st.radio("Kota", ["makkah", "madinah"], format_func=lambda x: "🕋 Makkah" if x == "makkah" else "🕌 Madinah", horizontal=True, key="map_city")
    pois = MAKKAH_POIS if city == "makkah" else MADINAH_POIS
    
    cols = st.columns(3)
    for i, poi in enumerate(pois):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {poi['icon']} {poi['name']}")
                st.caption(poi['desc'])


def render_daily():
    """Render daily challenges."""
    st.markdown("## 🎯 Daily Challenges")
    
    today = date.today().isoformat()
    if "um_daily_date" not in st.session_state or st.session_state.um_daily_date != today:
        st.session_state.um_daily_date = today
        st.session_state.um_daily_completed = []
    
    cols = st.columns(3)
    for i, ch in enumerate(DAILY_CHALLENGES):
        with cols[i % 3]:
            done = ch["id"] in st.session_state.um_daily_completed
            with st.container(border=True):
                if done:
                    st.success(f"### ✅ {ch['icon']}")
                    st.markdown(f"~~{ch['name']}~~")
                else:
                    st.markdown(f"### {ch['icon']}")
                    st.markdown(ch['name'])
                    st.caption(f"+{ch['xp']} XP")
                    if st.button("Complete", key=f"daily_{ch['id']}", use_container_width=True):
                        st.session_state.um_daily_completed.append(ch["id"])
                        add_xp(ch["xp"], f"Daily: {ch['name']}")
                        if len(st.session_state.um_daily_completed) == len(DAILY_CHALLENGES):
                            st.session_state.um_streak += 1
                        st.rerun()


def render_achievements():
    """Render achievements."""
    st.markdown("## 🏆 Achievements")
    
    unlocked = len(st.session_state.um_achievements)
    total = len(ACHIEVEMENTS)
    st.progress(unlocked / total)
    st.caption(f"🔓 {unlocked}/{total} unlocked")
    
    cols = st.columns(4)
    for i, ach in enumerate(ACHIEVEMENTS):
        with cols[i % 4]:
            is_unlocked = ach["id"] in st.session_state.um_achievements
            if is_unlocked:
                st.markdown(f"""
                <div class="achievement-card">
                    <div style="font-size:2rem;">{ach['icon']}</div>
                    <div style="font-weight:bold;">{ach['name']}</div>
                    <div style="font-size:0.8rem;">{ach['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="achievement-card locked">
                    <div style="font-size:2rem;">🔒</div>
                    <div style="font-weight:bold;">{ach['name']}</div>
                </div>
                """, unsafe_allow_html=True)


def render_savings():
    """Render savings tracker."""
    st.markdown("## 🐷 Tabungan Umrah")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        target = st.number_input("Target (Rp)", 10000000, 100000000, st.session_state.um_savings["target"], 1000000)
        st.session_state.um_savings["target"] = target
        
        with st.form("add_savings"):
            amount = st.number_input("Tambah (Rp)", 0, step=100000)
            if st.form_submit_button("💰 Tambah", use_container_width=True):
                st.session_state.um_savings["current"] += amount
                add_xp(10, "Menabung!")
                st.rerun()
    
    with col2:
        curr = st.session_state.um_savings["current"]
        pct = min(curr / target, 1.0) if target > 0 else 0
        st.markdown(f"<div style='text-align:center;'><span style='font-size:3rem;'>🐷</span><h3>Rp {curr:,.0f}</h3></div>".replace(",", "."), unsafe_allow_html=True)
        st.progress(pct)
        if pct >= 1.0:
            st.balloons()
            unlock_achievement("saver")


def render_sos():
    """Render SOS contacts."""
    st.markdown("## 🆘 Emergency SOS")
    st.error("⚠️ Dalam keadaan darurat, hubungi nomor di bawah!")
    
    tabs = st.tabs(["🇸🇦 Saudi", "🇮🇩 Indonesia"])
    
    with tabs[0]:
        cols = st.columns(3)
        for i, c in enumerate(EMERGENCY_CONTACTS["saudi"]):
            with cols[i]:
                with st.container(border=True):
                    st.markdown(f"### {c['icon']} {c['name']}")
                    st.markdown(f"## 📞 {c['phone']}")
    
    with tabs[1]:
        for c in EMERGENCY_CONTACTS["indonesia"]:
            with st.container(border=True):
                st.markdown(f"### {c['icon']} {c['name']}")
                st.markdown(f"📞 {c['phone']}")


def render_dyor():
    """Render DYOR disclaimer."""
    st.warning("""
    ⚠️ **DYOR - Do Your Own Research**
    
    LABBAIK adalah platform edukasi. Selalu verifikasi di:
    🇸🇦 [nusuk.sa](https://nusuk.sa) | 🇮🇩 [kemenag.go.id](https://kemenag.go.id)
    📞 KBRI Riyadh: +966-11-488-2800
    
    **Anda bertanggung jawab penuh atas keputusan perjalanan.**
    """)


# =============================================================================
# 🚀 MAIN RENDERER
# =============================================================================

def render_umrah_mandiri_page():
    """Main page renderer."""
    
    init_super_state()
    
    render_hero()
    render_gamification_bar()
    
    st.divider()
    render_quick_stats()
    st.divider()
    
    tabs = st.tabs([
        "⏰ Countdown",
        "🏛️ 3 Pilar",
        "📿 Manasik",
        "💰 Budget",
        "🌡️ Weather",
        "🗺️ Peta",
        "🤲 Doa",
        "🎯 Daily",
        "🏆 Badges",
        "🐷 Tabungan",
        "🆘 SOS",
    ])
    
    with tabs[0]: render_countdown()
    with tabs[1]: render_pillars()
    with tabs[2]: render_manasik()
    with tabs[3]: render_budget()
    with tabs[4]: render_weather()
    with tabs[5]: render_map()
    with tabs[6]: render_doa()
    with tabs[7]: render_daily()
    with tabs[8]: render_achievements()
    with tabs[9]: render_savings()
    with tabs[10]: render_sos()
    
    st.divider()
    render_dyor()


__all__ = ["render_umrah_mandiri_page"]
