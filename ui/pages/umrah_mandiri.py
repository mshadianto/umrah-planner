"""
================================================================================
🕋 LABBAIK AI v7.0 - UMRAH MANDIRI SUPER COMPLETE EDITION
================================================================================
MERGED: Gamification + Virtual Manasik + Budget AI + Weather + Daily Challenges
      + Visa Checker + Document Checker + PPIU Verification + Miqat Locator
================================================================================
"""

import streamlit as st
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# =============================================================================
# 🎨 SUPER STYLING - BLACK GOLD THEME
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

.visa-result-card {
    background: linear-gradient(135deg, #1a472a 0%, #0d2818 100%);
    border-radius: 15px;
    padding: 1.5rem;
    border: 2px solid #28a745;
    color: white;
    margin: 1rem 0;
}

.doc-status-ok { color: #28a745; }
.doc-status-warning { color: #ffc107; }
.doc-status-error { color: #dc3545; }

.miqat-card {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    border-radius: 15px;
    padding: 1.5rem;
    border: 1px solid #d4af37;
    margin: 1rem 0;
}

.ppiu-verified {
    background: linear-gradient(135deg, #1a472a 0%, #0d2818 100%);
    border: 2px solid #28a745;
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
}

.ppiu-unverified {
    background: linear-gradient(135deg, #4a1a1a 0%, #2d0d0d 100%);
    border: 2px solid #dc3545;
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
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
    # NEW ACHIEVEMENTS
    {"id": "visa_checked", "name": "Visa Expert", "icon": "🛂", "desc": "Cek kelayakan visa", "xp": 75, "cat": "preparation"},
    {"id": "docs_ready", "name": "Dokumen Lengkap", "icon": "📄", "desc": "Semua dokumen OK", "xp": 100, "cat": "preparation"},
    {"id": "miqat_master", "name": "Miqat Master", "icon": "📍", "desc": "Pahami miqat", "xp": 50, "cat": "knowledge"},
    {"id": "safe_travel", "name": "Safe Traveler", "icon": "🛡️", "desc": "Verifikasi PPIU", "xp": 75, "cat": "preparation"},
]

DAILY_CHALLENGES = [
    {"id": "read_dua", "name": "Baca 1 Doa Umrah", "xp": 10, "icon": "📖"},
    {"id": "arabic", "name": "Pelajari 3 Frasa Arab", "xp": 15, "icon": "🗣️"},
    {"id": "checklist", "name": "Centang 3 Checklist", "xp": 20, "icon": "✅"},
    {"id": "save", "name": "Tabung Hari Ini", "xp": 25, "icon": "💰"},
    {"id": "talbiyah", "name": "Latihan Talbiyah", "xp": 20, "icon": "🎵"},
]

# =============================================================================
# 🛂 VISA ELIGIBILITY DATA (NEW!)
# =============================================================================

class VisaType(Enum):
    E_TOURIST = "E-Tourist Visa"
    VISA_ON_ARRIVAL = "Visa on Arrival"
    UMRAH_VISA = "Umrah Visa (via PPIU)"
    FAMILY_VISIT = "Family Visit Visa"
    PERSONAL_VISIT = "Personal Visit Visa"

E_TOURIST_ELIGIBLE_DIRECT = [
    "United States", "United Kingdom", "Canada", "Australia", "New Zealand",
    "Germany", "France", "Italy", "Spain", "Netherlands", "Belgium", 
    "Switzerland", "Austria", "Sweden", "Norway", "Denmark", "Finland",
    "Japan", "South Korea", "Singapore", "Malaysia", "Brunei", 
    "China", "Hong Kong", "Macau", "Kazakhstan"
]

@dataclass
class VisaResult:
    eligible_types: List[VisaType]
    recommended: VisaType
    process_time: str
    estimated_cost_idr: int
    apply_url: str
    steps: List[str]
    notes: List[str]

def check_visa_eligibility(
    nationality: str,
    has_us_visa: bool = False,
    has_uk_visa: bool = False,
    has_schengen_visa: bool = False,
    has_saudi_relative: bool = False
) -> VisaResult:
    """Check visa eligibility based on nationality and existing visas."""
    
    eligible = []
    notes = []
    
    if nationality in E_TOURIST_ELIGIBLE_DIRECT:
        eligible.extend([VisaType.E_TOURIST, VisaType.VISA_ON_ARRIVAL])
    elif has_us_visa or has_uk_visa or has_schengen_visa:
        eligible.extend([VisaType.E_TOURIST, VisaType.VISA_ON_ARRIVAL])
        qualifying = []
        if has_us_visa: qualifying.append("US")
        if has_uk_visa: qualifying.append("UK")
        if has_schengen_visa: qualifying.append("Schengen")
        notes.append(f"✅ Eligible karena punya visa {', '.join(qualifying)} valid")
    
    if has_saudi_relative:
        eligible.append(VisaType.FAMILY_VISIT)
        notes.append("👨‍👩‍👧 Family Visit bisa diajukan oleh kerabat di Saudi")
    
    eligible.append(VisaType.UMRAH_VISA)
    
    if VisaType.E_TOURIST in eligible:
        return VisaResult(
            eligible_types=eligible,
            recommended=VisaType.E_TOURIST,
            process_time="Instant (online)",
            estimated_cost_idr=3_200_000,
            apply_url="https://www.nusuk.sa",
            steps=[
                "1️⃣ Kunjungi nusuk.sa atau download app NUSUK",
                "2️⃣ Pilih 'Get Visa' atau 'Apply for E-Visa'",
                "3️⃣ Isi data paspor dan informasi pribadi",
                "4️⃣ Upload foto dan scan paspor",
                "5️⃣ Bayar dengan kartu kredit/debit (SAR 480)",
                "6️⃣ Visa terbit dalam beberapa menit!",
                "7️⃣ Download dan simpan di HP"
            ],
            notes=notes
        )
    else:
        notes.append("⚠️ Pastikan PPIU terdaftar di KEMENAG!")
        notes.append("🔗 Verifikasi di: simpu.kemenag.go.id")
        return VisaResult(
            eligible_types=eligible,
            recommended=VisaType.UMRAH_VISA,
            process_time="1-3 hari kerja",
            estimated_cost_idr=2_500_000,
            apply_url="https://simpu.kemenag.go.id",
            steps=[
                "1️⃣ Pilih PPIU (Travel Agent) terdaftar KEMENAG",
                "2️⃣ Verifikasi di simpu.kemenag.go.id",
                "3️⃣ Serahkan paspor & dokumen ke travel agent",
                "4️⃣ Travel agent mengajukan via platform Maqam",
                "5️⃣ Visa terbit dalam 1-3 hari kerja",
                "6️⃣ Ambil paspor dengan visa di travel agent"
            ],
            notes=notes
        )

# =============================================================================
# 📋 DOCUMENT CHECKER DATA (NEW!)
# =============================================================================

@dataclass
class DocCheck:
    name: str
    status: str  # "ok", "warning", "error"
    message: str
    action: Optional[str] = None

@dataclass
class ReadinessReport:
    overall_status: str
    score: int
    checks: List[DocCheck]
    days_until_departure: int
    critical_actions: List[str]

def check_documents(
    departure_date: date,
    passport_expiry: date,
    passport_blank_pages: int,
    has_meningitis: bool,
    meningitis_date: Optional[date],
    has_insurance: bool,
    insurance_coverage: int,
    has_ticket: bool,
    has_hotel: bool
) -> ReadinessReport:
    """Check document readiness for Umrah."""
    
    checks = []
    critical = []
    today = date.today()
    days_until = (departure_date - today).days
    
    # Passport validity
    min_valid = departure_date + timedelta(days=180)
    if passport_expiry >= min_valid:
        checks.append(DocCheck("Paspor", "ok", f"Valid hingga {passport_expiry.strftime('%d/%m/%Y')} ✅"))
    elif passport_expiry >= departure_date:
        checks.append(DocCheck("Paspor", "warning", "Kurang dari 6 bulan validity!", "Perpanjang paspor segera"))
        critical.append("⚠️ Perpanjang paspor (butuh 6 bulan validity)")
    else:
        checks.append(DocCheck("Paspor", "error", "PASPOR EXPIRED!", "Harus perpanjang sebelum apply visa"))
        critical.append("🚨 URGENT: Paspor expired!")
    
    # Blank pages
    if passport_blank_pages >= 2:
        checks.append(DocCheck("Halaman Kosong", "ok", f"{passport_blank_pages} halaman ✅"))
    else:
        checks.append(DocCheck("Halaman Kosong", "error", f"Hanya {passport_blank_pages} (butuh min. 2)", "Tambah halaman paspor"))
        critical.append("Tambah halaman paspor")
    
    # Meningitis vaccine
    if has_meningitis and meningitis_date:
        valid_until = meningitis_date + timedelta(days=3*365)
        if valid_until >= departure_date:
            checks.append(DocCheck("Vaksin Meningitis", "ok", f"Valid hingga {valid_until.strftime('%d/%m/%Y')} ✅"))
        else:
            checks.append(DocCheck("Vaksin Meningitis", "warning", "Mungkin perlu booster", "Konsultasi dokter"))
    else:
        checks.append(DocCheck("Vaksin Meningitis", "error", "WAJIB - Belum vaksin!", "Vaksin di KKP Bandara"))
        critical.append("🚨 WAJIB: Vaksin Meningitis ACWY")
    
    # Insurance
    if has_insurance:
        if insurance_coverage >= 50000:
            checks.append(DocCheck("Asuransi", "ok", f"Coverage USD {insurance_coverage:,} ✅"))
        else:
            checks.append(DocCheck("Asuransi", "warning", f"Coverage kurang (USD {insurance_coverage:,})", "Upgrade ke min USD 50,000"))
    else:
        checks.append(DocCheck("Asuransi", "error", "Belum punya asuransi!", "Beli asuransi perjalanan"))
        critical.append("Beli asuransi perjalanan")
    
    # Ticket & Hotel
    if has_ticket:
        checks.append(DocCheck("Tiket PP", "ok", "Sudah ada ✅"))
    else:
        checks.append(DocCheck("Tiket PP", "warning", "Belum booking", "Booking tiket PP"))
    
    if has_hotel:
        checks.append(DocCheck("Hotel", "ok", "Sudah booking ✅"))
    else:
        checks.append(DocCheck("Hotel", "warning", "Belum booking", "Booking hotel"))
    
    # Calculate score
    scores = {"ok": 100, "warning": 50, "error": 0}
    avg = sum(scores[c.status] for c in checks) // len(checks)
    
    if avg >= 80:
        overall = "ready"
    elif avg >= 50:
        overall = "warning"
    else:
        overall = "not_ready"
    
    return ReadinessReport(
        overall_status=overall,
        score=avg,
        checks=checks,
        days_until_departure=days_until,
        critical_actions=critical
    )

# =============================================================================
# 📍 MIQAT DATA (NEW!)
# =============================================================================

MIQAT_DATA = {
    "jeddah_direct": {
        "name": "Yalamlam",
        "name_ar": "يلملم",
        "location": "Selatan Makkah",
        "timing": "Di pesawat, ~1 jam sebelum landing Jeddah",
        "tips": [
            "✅ Pakai ihram sebelum boarding lebih aman",
            "✅ Pilot biasanya mengumumkan saat mendekati miqat",
            "✅ Siapkan pakaian ihram di tas kabin"
        ]
    },
    "madinah_first": {
        "name": "Dzulhulaifah (Bir Ali)",
        "name_ar": "ذو الحليفة",
        "location": "10 km dari Masjid Nabawi",
        "timing": "Di Madinah, sebelum berangkat ke Makkah",
        "tips": [
            "✅ Miqat terjauh, paling mudah untuk pemula",
            "✅ Bisa mandi & ihram santai di hotel",
            "✅ Ada masjid di Bir Ali untuk sholat"
        ]
    },
    "transit_gulf": {
        "name": "Qarn al-Manazil",
        "name_ar": "قرن المنازل",
        "location": "Timur Makkah (arah Riyadh/Taif)",
        "timing": "Sebelum memasuki wilayah miqat di pesawat",
        "tips": [
            "✅ Perhatikan pengumuman pilot",
            "✅ Jika transit lama, bisa ihram di airport",
            "✅ Konsultasi travel agent untuk kepastian"
        ]
    }
}

TALBIYAH = {
    "arabic": "لَبَّيْكَ اللّٰهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيْكَ لَكَ لَبَّيْكَ، إِنَّ الْحَمْدَ وَالنِّعْمَةَ لَكَ وَالْمُلْكَ، لَا شَرِيْكَ لَكَ",
    "latin": "Labbaik Allahumma labbaik, labbaik laa syariika laka labbaik, innal hamda wan ni'mata laka wal mulk, laa syariika lak",
    "arti": "Aku penuhi panggilan-Mu ya Allah, tiada sekutu bagi-Mu. Segala puji, nikmat dan kerajaan milik-Mu."
}

# =============================================================================
# 🔍 PPIU DATA (NEW!)
# =============================================================================

# Sample verified PPIU (in production: from KEMENAG API)
SAMPLE_PPIU = [
    {"name": "PT. Arminareka Perdana", "id": "D/123/2020", "verified": True, "rating": 4.5, "city": "Jakarta"},
    {"name": "PT. Azra Tours", "id": "D/456/2021", "verified": True, "rating": 4.2, "city": "Surabaya"},
    {"name": "PT. Patuna Mekar Jaya", "id": "D/789/2019", "verified": True, "rating": 4.7, "city": "Jakarta"},
    {"name": "PT. Cheria Holiday", "id": "D/321/2022", "verified": True, "rating": 4.3, "city": "Bandung"},
    {"name": "PT. Al Hijaz Indowisata", "id": "D/654/2020", "verified": True, "rating": 4.6, "city": "Jakarta"},
    {"name": "PT. Ebad Wisata", "id": "D/987/2021", "verified": True, "rating": 4.4, "city": "Semarang"},
]

# =============================================================================
# 📿 VIRTUAL MANASIK DATA (EXISTING)
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
# 🏛️ 3 PILAR DATA (EXISTING)
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
# 💰 BUDGET DATA (EXISTING)
# =============================================================================

COST_COMPONENTS = {
    "flight": {
        "label": "✈️ Tiket Pesawat",
        "options": [
            {"name": "LCC Promo", "price": 5500000, "tips": "Book 2-3 bulan sebelumnya"},
            {"name": "LCC Regular", "price": 7000000, "tips": "Bagasi 20kg, no meal"},
            {"name": "Full Service", "price": 10000000, "tips": "Bagasi 30kg, meal included"},
            {"name": "Premium", "price": 15000000, "tips": "Turkish, Emirates, Saudi"},
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

# =============================================================================
# 🌡️ WEATHER & OTHER DATA (EXISTING)
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

# DOA COLLECTION (20+ doa - keeping existing)
DOA_COLLECTION = [
    {"name": "Talbiyah", "arabic": "لَبَّيْكَ اللّٰهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيْكَ لَكَ لَبَّيْكَ، إِنَّ الْحَمْدَ وَالنِّعْمَةَ لَكَ وَالْمُلْكَ، لَا شَرِيْكَ لَكَ", "latin": "Labbaik Allahumma labbaik...", "meaning": "Aku penuhi panggilan-Mu ya Allah...", "when": "Sejak miqat hingga thawaf", "category": "wajib"},
    {"name": "Niat Umrah", "arabic": "اَللّٰهُمَّ إِنِّيْ أُرِيْدُ الْعُمْرَةَ فَيَسِّرْهَا لِيْ وَتَقَبَّلْهَا مِنِّيْ", "latin": "Allahumma innii uridul 'umrah...", "meaning": "Ya Allah, aku ingin umrah...", "when": "Saat niat ihram di miqat", "category": "wajib"},
    {"name": "Doa Mulai Thawaf", "arabic": "بِسْمِ اللهِ وَاللهُ أَكْبَرُ", "latin": "Bismillahi wallahu akbar", "meaning": "Dengan nama Allah, Allah Maha Besar", "when": "Saat melewati Hajar Aswad", "category": "thawaf"},
    {"name": "Doa Rukun Yamani", "arabic": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ", "latin": "Rabbana aatina fid dunya hasanah...", "meaning": "Ya Tuhan, berilah kami kebaikan...", "when": "Antara Rukun Yamani dan Hajar Aswad", "category": "thawaf"},
    {"name": "Doa Naik Shafa", "arabic": "إِنَّ الصَّفَا وَالْمَرْوَةَ مِنْ شَعَائِرِ اللهِ", "latin": "Innash shafa wal marwata...", "meaning": "Shafa dan Marwah adalah syiar Allah", "when": "Saat naik ke Bukit Shafa", "category": "sai"},
    {"name": "Doa Minum Zamzam", "arabic": "اَللّٰهُمَّ إِنِّيْ أَسْأَلُكَ عِلْمًا نَافِعًا", "latin": "Allahumma inni as'aluka 'ilman nafi'an...", "meaning": "Ya Allah, aku mohon ilmu bermanfaat...", "when": "Saat minum air zamzam", "category": "zamzam"},
    {"name": "Salam Rasulullah", "arabic": "اَلسَّلَامُ عَلَيْكَ يَا رَسُوْلَ اللهِ", "latin": "Assalamu 'alaika ya Rasulallah", "meaning": "Salam sejahtera atasmu wahai Rasulullah", "when": "Di depan makam Rasulullah", "category": "madinah"},
    {"name": "Doa Raudhah", "arabic": "اَللّٰهُمَّ اجْعَلْ فِيْ قَلْبِيْ نُوْرًا", "latin": "Allahummaj'al fii qalbii nuran...", "meaning": "Ya Allah, jadikanlah cahaya di hatiku...", "when": "Saat sholat di Raudhah", "category": "madinah"},
    {"name": "Doa Perjalanan", "arabic": "سُبْحَانَ الَّذِيْ سَخَّرَ لَنَا هٰذَا", "latin": "Subhanalladzi sakhkhara lana hadza...", "meaning": "Maha Suci yang menundukkan ini untuk kami...", "when": "Saat naik kendaraan", "category": "umum"},
    {"name": "Istighfar", "arabic": "أَسْتَغْفِرُ اللهَ الْعَظِيْمَ", "latin": "Astaghfirullahal 'azhim...", "meaning": "Aku mohon ampun kepada Allah...", "when": "Setiap saat", "category": "umum"},
]

# =============================================================================
# 🔧 SESSION STATE
# =============================================================================

def init_super_state():
    """Initialize all session state."""
    defaults = {
        "um_xp": 0,
        "um_level": 1,
        "um_achievements": ["first_step"],
        "um_daily_completed": [],
        "um_streak": 0,
        "um_tasks": {"administrasi": [], "logistik": [], "eksekusi": []},
        "um_departure_date": None,
        "um_duration": 9,
        "um_manasik_step": 0,
        "um_manasik_completed": [],
        "um_savings": {"target": 25000000, "current": 0},
        # NEW states
        "um_visa_checked": False,
        "um_docs_checked": False,
        "um_miqat_checked": False,
        "um_ppiu_checked": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


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


def get_current_level():
    for lv in reversed(LEVELS):
        if st.session_state.um_xp >= lv["min_xp"]:
            return lv
    return LEVELS[0]


def get_next_level():
    curr = get_current_level()
    for lv in LEVELS:
        if lv["level"] > curr["level"]:
            return lv
    return None


# =============================================================================
# 🎨 RENDER FUNCTIONS - HEADER & GAMIFICATION
# =============================================================================

def render_hero():
    """Render hero header."""
    st.markdown(SUPER_CSS, unsafe_allow_html=True)
    st.markdown("""
    <div class="hero-gradient">
        <div class="arabic">🕋 لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ</div>
        <h1>UMRAH MANDIRI v7.0</h1>
        <p style="font-size: 1.2rem; opacity: 0.9; color: #ccc;">Panduan Terlengkap + Visa Checker + Document Validator</p>
    </div>
    """, unsafe_allow_html=True)


def render_gamification_bar():
    """Render XP bar."""
    curr = get_current_level()
    nxt = get_next_level()
    
    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
    
    with col1:
        st.markdown(f"<div style='text-align:center;'><span style='font-size:2.5rem;'>{curr['icon']}</span><br><b style='color:#d4af37;'>Lv {curr['level']}</b><br><small style='color:#888;'>{curr['name']}</small></div>", unsafe_allow_html=True)
    
    with col2:
        if nxt:
            prog = (st.session_state.um_xp - curr["min_xp"]) / (nxt["min_xp"] - curr["min_xp"])
            st.markdown(f"""
            <div class="xp-bar-container">
                <div class="xp-bar-fill" style="width: {min(prog, 1) * 100}%;"></div>
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
    """Render quick stats."""
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
                st.markdown(f"<h2 style='color:#d4af37;text-align:center;'>{max(days, 0)}</h2>", unsafe_allow_html=True)
                st.caption("hari lagi")
            else:
                st.caption("Set tanggal →")


# =============================================================================
# 🛂 NEW: VISA ELIGIBILITY CHECKER
# =============================================================================

def render_visa_checker():
    """Render Visa Eligibility Checker."""
    st.markdown("## 🛂 Cek Kelayakan Visa Umrah")
    st.info("💡 Ketahui jenis visa yang cocok untuk Anda dalam 1 menit!")
    
    with st.form("visa_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nationality = st.selectbox(
                "🌍 Kewarganegaraan",
                ["Indonesia", "Malaysia", "Singapore"] + E_TOURIST_ELIGIBLE_DIRECT[:10],
                index=0
            )
        
        with col2:
            st.write("**Visa yang dimiliki (masih valid):**")
        
        col3, col4, col5 = st.columns(3)
        with col3:
            has_us = st.checkbox("🇺🇸 Visa USA")
        with col4:
            has_uk = st.checkbox("🇬🇧 Visa UK")
        with col5:
            has_schengen = st.checkbox("🇪🇺 Visa Schengen")
        
        has_relative = st.checkbox("👨‍👩‍👧 Punya kerabat (ortu/pasangan/anak) di Saudi Arabia?")
        
        submitted = st.form_submit_button("🔍 Cek Kelayakan Visa", use_container_width=True, type="primary")
    
    if submitted:
        result = check_visa_eligibility(
            nationality=nationality,
            has_us_visa=has_us,
            has_uk_visa=has_uk,
            has_schengen_visa=has_schengen,
            has_saudi_relative=has_relative
        )
        
        # Award XP
        if not st.session_state.um_visa_checked:
            st.session_state.um_visa_checked = True
            add_xp(50, "Cek visa eligibility")
            unlock_achievement("visa_checked")
        
        st.markdown(f"""
        <div class="visa-result-card">
            <h2>✅ Rekomendasi: {result.recommended.value}</h2>
            <p>⏱️ Waktu Proses: <b>{result.process_time}</b></p>
            <p>💰 Estimasi Biaya: <b>Rp {result.estimated_cost_idr:,}</b></p>
        </div>
        """.replace(",", "."), unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 📋 Langkah-langkah:")
            for step in result.steps:
                st.write(step)
        
        with col2:
            st.link_button("🔗 Apply Sekarang", result.apply_url, use_container_width=True)
        
        if result.notes:
            st.warning("### ⚠️ Catatan Penting:")
            for note in result.notes:
                st.write(f"• {note}")


# =============================================================================
# 📋 NEW: DOCUMENT READINESS CHECKER
# =============================================================================

def render_document_checker():
    """Render Document Readiness Checker."""
    st.markdown("## 📋 Cek Kesiapan Dokumen")
    st.info("💡 Pastikan semua dokumen lengkap sebelum berangkat!")
    
    with st.form("doc_form"):
        st.subheader("📅 Tanggal Keberangkatan")
        departure = st.date_input(
            "Rencana berangkat",
            value=st.session_state.um_departure_date or date.today() + timedelta(days=60),
            min_value=date.today()
        )
        
        st.subheader("🛂 Paspor")
        col1, col2 = st.columns(2)
        with col1:
            passport_exp = st.date_input("Tanggal expired paspor", value=date.today() + timedelta(days=365*3))
        with col2:
            blank_pages = st.number_input("Halaman kosong", min_value=0, max_value=20, value=4)
        
        st.subheader("💉 Vaksinasi")
        col3, col4 = st.columns(2)
        with col3:
            has_vaccine = st.checkbox("Sudah vaksin Meningitis ACWY?")
        with col4:
            vaccine_date = st.date_input("Tanggal vaksinasi", value=date.today() - timedelta(days=365)) if has_vaccine else None
        
        st.subheader("🛡️ Asuransi & Booking")
        col5, col6, col7 = st.columns(3)
        with col5:
            has_insurance = st.checkbox("Punya asuransi?")
            coverage = st.number_input("Coverage (USD)", value=50000) if has_insurance else 0
        with col6:
            has_ticket = st.checkbox("Sudah ada tiket PP?")
        with col7:
            has_hotel = st.checkbox("Sudah booking hotel?")
        
        submitted = st.form_submit_button("🔍 Cek Kesiapan", use_container_width=True, type="primary")
    
    if submitted:
        st.session_state.um_departure_date = departure
        
        result = check_documents(
            departure_date=departure,
            passport_expiry=passport_exp,
            passport_blank_pages=blank_pages,
            has_meningitis=has_vaccine,
            meningitis_date=vaccine_date,
            has_insurance=has_insurance,
            insurance_coverage=coverage,
            has_ticket=has_ticket,
            has_hotel=has_hotel
        )
        
        # Award XP
        if not st.session_state.um_docs_checked:
            st.session_state.um_docs_checked = True
            add_xp(50, "Cek kesiapan dokumen")
        
        if result.score >= 80:
            unlock_achievement("docs_ready")
        
        # Status display
        status_config = {
            "ready": ("✅ SIAP BERANGKAT!", "success"),
            "warning": ("⚠️ HAMPIR SIAP", "warning"),
            "not_ready": ("❌ BELUM SIAP", "error")
        }
        text, type_ = status_config[result.overall_status]
        getattr(st, type_)(f"## {text}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📊 Skor Kesiapan", f"{result.score}%")
        with col2:
            st.metric("📅 Hari hingga Berangkat", f"{result.days_until_departure} hari")
        
        if result.critical_actions:
            st.error("### 🚨 ACTION DIPERLUKAN:")
            for action in result.critical_actions:
                st.write(f"• {action}")
        
        st.markdown("### 📝 Detail Checklist:")
        for check in result.checks:
            icon = {"ok": "✅", "warning": "⚠️", "error": "❌"}[check.status]
            with st.expander(f"{icon} {check.name}"):
                st.write(check.message)
                if check.action:
                    st.info(f"**Action:** {check.action}")


# =============================================================================
# 📍 NEW: MIQAT LOCATOR
# =============================================================================

def render_miqat_locator():
    """Render Miqat & Ihram Locator."""
    st.markdown("## 📍 Panduan Miqat & Ihram")
    
    st.error("⚠️ **PENTING:** Melewati miqat tanpa ihram = umrah tidak sah!")
    
    route = st.selectbox(
        "🛫 Pilih rute perjalanan Anda:",
        [
            "Jakarta → Jeddah (Direct)",
            "Jakarta → Madinah (Direct)",
            "Jakarta → Madinah → Makkah",
            "Via Dubai/Doha/Riyadh (Transit)"
        ]
    )
    
    if st.button("🔍 Lihat Panduan Miqat", use_container_width=True, type="primary"):
        # Award XP
        if not st.session_state.um_miqat_checked:
            st.session_state.um_miqat_checked = True
            add_xp(30, "Pelajari miqat")
            unlock_achievement("miqat_master")
        
        # Determine miqat
        if "Madinah" in route and "Makkah" in route:
            miqat = MIQAT_DATA["madinah_first"]
        elif "Jeddah" in route:
            miqat = MIQAT_DATA["jeddah_direct"]
        else:
            miqat = MIQAT_DATA["transit_gulf"]
        
        st.markdown(f"""
        <div class="miqat-card">
            <h2 style="color:#d4af37;">📍 Miqat Anda: {miqat['name']} ({miqat['name_ar']})</h2>
            <p><b>📌 Lokasi:</b> {miqat['location']}</p>
            <p><b>⏰ Waktu Ihram:</b> {miqat['timing']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 Tips:")
        for tip in miqat['tips']:
            st.write(tip)
        
        st.divider()
        
        st.markdown("### 🤲 Niat Umrah:")
        st.markdown(f"""
        <div class="doa-arabic">لَبَّيْكَ اللّٰهُمَّ عُمْرَةً</div>
        """, unsafe_allow_html=True)
        st.caption("**Labbaik Allahumma 'umratan** - Aku penuhi panggilan-Mu untuk umrah")
        
        st.markdown("### 🎵 Talbiyah:")
        st.markdown(f"""
        <div class="doa-arabic">{TALBIYAH['arabic']}</div>
        """, unsafe_allow_html=True)
        st.caption(f"**{TALBIYAH['latin']}**")
        st.caption(f"*{TALBIYAH['arti']}*")
        
        # Ihram checklist
        st.markdown("### ✅ Checklist Persiapan Ihram:")
        checklist = [
            "Mandi sunnah ihram",
            "Potong kuku & bulu",
            "Pakai pakaian ihram (pria: 2 kain putih)",
            "Wanita: pakaian menutup aurat",
            "Pakai wangi sebelum ihram",
            "Niat umrah",
            "Baca talbiyah"
        ]
        for item in checklist:
            st.checkbox(item, key=f"ihram_{item[:10]}")


# =============================================================================
# 🔍 NEW: PPIU VERIFICATION
# =============================================================================

def render_ppiu_checker():
    """Render PPIU Verification Tool."""
    st.markdown("## 🔍 Verifikasi Travel Agent (PPIU)")
    
    st.error("""
    ⚠️ **WASPADA PENIPUAN!**
    
    Banyak travel agent ILEGAL yang menipu jamaah!
    Selalu verifikasi di **simpu.kemenag.go.id** sebelum bayar!
    """)
    
    search = st.text_input("🔎 Cari nama travel agent:", placeholder="Contoh: Patuna, Arminareka...")
    
    if search:
        # Award XP once
        if not st.session_state.um_ppiu_checked:
            st.session_state.um_ppiu_checked = True
            add_xp(40, "Verifikasi PPIU")
            unlock_achievement("safe_travel")
        
        results = [p for p in SAMPLE_PPIU if search.lower() in p["name"].lower()]
        
        if results:
            for ppiu in results:
                if ppiu["verified"]:
                    st.markdown(f"""
                    <div class="ppiu-verified">
                        <h3>✅ {ppiu['name']}</h3>
                        <p><b>Status:</b> TERDAFTAR RESMI KEMENAG</p>
                        <p><b>No. Izin:</b> {ppiu['id']}</p>
                        <p><b>Kota:</b> {ppiu['city']}</p>
                        <p><b>Rating:</b> {'⭐' * int(ppiu['rating'])} ({ppiu['rating']}/5)</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="ppiu-unverified">
                        <h3>❌ {ppiu['name']}</h3>
                        <p><b>Status:</b> TIDAK TERDAFTAR - HATI-HATI!</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error(f"❌ Tidak ditemukan: '{search}'")
            st.warning("""
            **Kemungkinan:**
            1. Travel agent tidak terdaftar (ILEGAL!)
            2. Nama berbeda dengan yang terdaftar
            
            **Langkah selanjutnya:**
            - Minta nomor izin KEMENAG dari travel agent
            - Verifikasi manual di simpu.kemenag.go.id
            - **Jika tidak bisa diverifikasi, JANGAN BAYAR!**
            """)
    
    st.divider()
    st.info("""
    **🔗 Link Verifikasi Resmi:**
    - SISKOPATUH KEMENAG: [simpu.kemenag.go.id](https://simpu.kemenag.go.id/)
    - Hotline KEMENAG: **1500-363**
    """)


# =============================================================================
# 🎨 EXISTING RENDER FUNCTIONS (Shortened for space)
# =============================================================================

def render_countdown():
    """Render countdown widget."""
    st.markdown("## ⏰ Countdown to Baitullah")
    
    col1, col2 = st.columns([2, 3])
    with col1:
        dep = st.date_input("Tanggal Keberangkatan", value=st.session_state.um_departure_date or date.today() + timedelta(days=90))
        st.session_state.um_departure_date = dep
        dur = st.slider("Durasi (hari)", 7, 21, st.session_state.um_duration)
        st.session_state.um_duration = dur
    
    with col2:
        if st.session_state.um_departure_date:
            days = (st.session_state.um_departure_date - date.today()).days
            if days > 0:
                months, rem = divmod(days, 30)
                weeks, d = divmod(rem, 7)
                st.markdown(f"""
                <div style="text-align:center;">
                    <span class="countdown-digit">{months}</span>
                    <span class="countdown-digit">{weeks}</span>
                    <span class="countdown-digit">{d}</span>
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
            st.progress(done / total if total > 0 else 0)
            st.caption(f"{done}/{total} selesai")
            
            for task in pillar["tasks"]:
                is_done = task["id"] in st.session_state.um_tasks[pid]
                col1, col2 = st.columns([0.1, 0.9])
                with col1:
                    if st.checkbox("", value=is_done, key=f"{pid}_{task['id']}", label_visibility="collapsed"):
                        if task["id"] not in st.session_state.um_tasks[pid]:
                            st.session_state.um_tasks[pid].append(task["id"])
                            add_xp(task["xp"], task["name"])
                    elif task["id"] in st.session_state.um_tasks[pid]:
                        st.session_state.um_tasks[pid].remove(task["id"])
                with col2:
                    badge = {"wajib": "🔴", "recommended": "🟡"}.get(task["priority"], "")
                    st.write(f"{task['icon']} {task['name']} {badge} (+{task['xp']} XP)")


def render_manasik():
    """Render virtual manasik."""
    st.markdown("## 📿 Virtual Manasik Simulator")
    
    # Step indicator
    cols = st.columns(len(MANASIK_STEPS))
    for i, col in enumerate(cols):
        with col:
            is_done = i in st.session_state.um_manasik_completed
            is_curr = i == st.session_state.um_manasik_step
            color = "#d4af37" if is_done else ("#f4d03f" if is_curr else "#333")
            st.markdown(f"<div style='text-align:center;'><div style='width:30px;height:30px;border-radius:50%;background:{color};margin:auto;line-height:30px;color:{'#1a1a1a' if is_done or is_curr else '#888'};font-size:0.8rem;border:1px solid #d4af37;'>{i+1}</div></div>", unsafe_allow_html=True)
    
    st.divider()
    
    curr = MANASIK_STEPS[st.session_state.um_manasik_step]
    
    with st.container(border=True):
        st.markdown(f"### {curr['icon']} Langkah {curr['step']}: {curr['title']}")
        st.markdown(f"📍 **Lokasi:** {curr['location']}")
        st.write(curr['desc'])
        
        for tip in curr['tips']:
            st.write(f"• {tip}")
        
        st.markdown(f"<div class='doa-arabic'>{curr['dua']}</div>", unsafe_allow_html=True)
        st.caption(f"{curr['dua_latin']} - *{curr['dua_arti']}*")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.um_manasik_step > 0:
            if st.button("⬅️ Sebelumnya", use_container_width=True):
                st.session_state.um_manasik_step -= 1
                st.rerun()
    with col2:
        is_curr_done = st.session_state.um_manasik_step in st.session_state.um_manasik_completed
        if not is_curr_done:
            if st.button("✅ Selesai", use_container_width=True, type="primary"):
                st.session_state.um_manasik_completed.append(st.session_state.um_manasik_step)
                add_xp(25, f"Manasik: {curr['title']}")
                if len(st.session_state.um_manasik_completed) == len(MANASIK_STEPS):
                    unlock_achievement("manasik_pro")
                st.rerun()
        else:
            st.success("✅ Dipelajari!")
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
        budget = st.number_input("Total Budget (Rp)", 10_000_000, 100_000_000, 25_000_000, 1_000_000)
    with col2:
        is_ramadan = st.checkbox("🌙 Musim Ramadan (+30%)")
    
    duration = st.slider("Durasi (hari)", 7, 21, 9)
    
    selections = {}
    for cid, comp in COST_COMPONENTS.items():
        idx = st.selectbox(
            comp['label'],
            range(len(comp["options"])),
            format_func=lambda i, c=comp: f"{c['options'][i]['name']} - Rp {c['options'][i]['price']:,}".replace(",", "."),
            key=f"budget_{cid}"
        )
        opt = comp["options"][idx]
        if comp.get("per_night"):
            selections[cid] = opt["price"] * (duration - 1)
        elif comp.get("per_day"):
            selections[cid] = opt["price"] * duration
        else:
            selections[cid] = opt["price"]
    
    subtotal = sum(selections.values()) + 1_500_000  # Extras
    total = int(subtotal * 1.3) if is_ramadan else subtotal
    
    st.divider()
    delta = budget - total
    if delta >= 0:
        st.success(f"### ✅ Total: Rp {total:,}".replace(",", "."))
        st.info(f"💰 Sisa: Rp {delta:,}".replace(",", "."))
    else:
        st.error(f"### ⚠️ Over budget: Rp {total:,}".replace(",", "."))
    
    if st.button("💾 Simpan", type="primary"):
        add_xp(50, "Budget planned!")
        unlock_achievement("budget_set")


def render_weather():
    """Render weather."""
    st.markdown("## 🌡️ Cuaca Tanah Suci")
    
    col1, col2 = st.columns(2)
    for city, data in WEATHER_DATA.items():
        with col1 if city == "makkah" else col2:
            st.markdown(f"""
            <div class="weather-card">
                <h3>{'🕋 Makkah' if city == 'makkah' else '🕌 Madinah'}</h3>
                <div style="font-size:3rem;">{data['icon']}</div>
                <div class="weather-temp">{data['temp']}°C</div>
            </div>
            """, unsafe_allow_html=True)


def render_doa():
    """Render doa collection."""
    st.markdown("## 🤲 Koleksi Doa Umrah")
    
    cats = {"wajib": "🔴 Wajib", "thawaf": "🕋 Thawaf", "sai": "🏃 Sa'i", "zamzam": "💧 Zamzam", "madinah": "🕌 Madinah", "umum": "📿 Umum"}
    cat = st.radio("Kategori", list(cats.keys()), format_func=lambda x: cats[x], horizontal=True)
    
    for doa in [d for d in DOA_COLLECTION if d["category"] == cat]:
        with st.container(border=True):
            st.markdown(f"### {doa['name']}")
            st.markdown(f"<div class='doa-arabic'>{doa['arabic']}</div>", unsafe_allow_html=True)
            st.caption(f"**{doa['latin']}** - *{doa['meaning']}*")


def render_daily():
    """Render daily challenges."""
    st.markdown("## 🎯 Daily Challenges")
    
    cols = st.columns(3)
    for i, ch in enumerate(DAILY_CHALLENGES):
        with cols[i % 3]:
            done = ch["id"] in st.session_state.um_daily_completed
            with st.container(border=True):
                if done:
                    st.success(f"✅ {ch['icon']} ~~{ch['name']}~~")
                else:
                    st.write(f"{ch['icon']} {ch['name']} (+{ch['xp']} XP)")
                    if st.button("Complete", key=f"daily_{ch['id']}", use_container_width=True):
                        st.session_state.um_daily_completed.append(ch["id"])
                        add_xp(ch["xp"], ch['name'])
                        st.rerun()


def render_achievements():
    """Render achievements."""
    st.markdown("## 🏆 Achievements")
    
    cols = st.columns(4)
    for i, ach in enumerate(ACHIEVEMENTS):
        with cols[i % 4]:
            unlocked = ach["id"] in st.session_state.um_achievements
            st.markdown(f"""
            <div class="achievement-card {'locked' if not unlocked else ''}">
                <div style="font-size:2rem;">{'🔒' if not unlocked else ach['icon']}</div>
                <div style="font-weight:bold;">{ach['name']}</div>
                <div style="font-size:0.8rem;color:#888;">{ach['desc']}</div>
            </div>
            """, unsafe_allow_html=True)


def render_savings():
    """Render savings tracker."""
    st.markdown("## 🐷 Tabungan Umrah")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        target = st.number_input("Target (Rp)", 10_000_000, 100_000_000, st.session_state.um_savings["target"])
        st.session_state.um_savings["target"] = target
        
        with st.form("savings_form"):
            amount = st.number_input("Tambah (Rp)", 0, step=100000)
            if st.form_submit_button("💰 Tambah"):
                st.session_state.um_savings["current"] += amount
                add_xp(10, "Menabung!")
                if st.session_state.um_savings["current"] >= target:
                    unlock_achievement("saver")
                st.rerun()
    
    with col2:
        curr = st.session_state.um_savings["current"]
        st.markdown(f"<div style='text-align:center;'><span style='font-size:3rem;'>🐷</span><h3>Rp {curr:,.0f}</h3></div>".replace(",", "."), unsafe_allow_html=True)
        st.progress(min(curr / target, 1.0))


def render_sos():
    """Render SOS contacts."""
    st.markdown("## 🆘 Emergency SOS")
    st.error("⚠️ Dalam keadaan darurat, hubungi nomor di bawah!")
    
    for cat, contacts in EMERGENCY_CONTACTS.items():
        st.subheader("🇸🇦 Saudi Arabia" if cat == "saudi" else "🇮🇩 Indonesia")
        cols = st.columns(len(contacts))
        for i, c in enumerate(contacts):
            with cols[i]:
                st.markdown(f"**{c['icon']} {c['name']}**")
                st.markdown(f"📞 {c['phone']}")


def render_dyor():
    """Render DYOR disclaimer."""
    st.warning("""
    ⚠️ **DYOR - Do Your Own Research**
    
    LABBAIK adalah platform edukasi. Selalu verifikasi di:
    🇸🇦 [nusuk.sa](https://nusuk.sa) | 🇮🇩 [simpu.kemenag.go.id](https://simpu.kemenag.go.id)
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
    
    # TABS - Now with NEW critical features first!
    tabs = st.tabs([
        "🛂 Cek Visa",          # NEW
        "📋 Cek Dokumen",       # NEW
        "📍 Panduan Miqat",     # NEW
        "🔍 Verifikasi PPIU",   # NEW
        "⏰ Countdown",
        "🏛️ 3 Pilar",
        "📿 Manasik",
        "💰 Budget",
        "🌡️ Weather",
        "🤲 Doa",
        "🎯 Daily",
        "🏆 Badges",
        "🐷 Tabungan",
        "🆘 SOS",
    ])
    
    with tabs[0]: render_visa_checker()
    with tabs[1]: render_document_checker()
    with tabs[2]: render_miqat_locator()
    with tabs[3]: render_ppiu_checker()
    with tabs[4]: render_countdown()
    with tabs[5]: render_pillars()
    with tabs[6]: render_manasik()
    with tabs[7]: render_budget()
    with tabs[8]: render_weather()
    with tabs[9]: render_doa()
    with tabs[10]: render_daily()
    with tabs[11]: render_achievements()
    with tabs[12]: render_savings()
    with tabs[13]: render_sos()
    
    st.divider()
    render_dyor()


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    st.set_page_config(
        page_title="LABBAIK.AI - Umrah Mandiri v7.0",
        page_icon="🕋",
        layout="wide"
    )
    render_umrah_mandiri_page()


__all__ = ["render_umrah_mandiri_page"]
