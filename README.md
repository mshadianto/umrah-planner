# 🕋 LABBAIK AI v6.0 - Super Boom Edition

<div align="center">

![LABBAIK AI](https://img.shields.io/badge/LABBAIK-AI%20v6.0-gold?style=for-the-badge&logo=kaaba)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-Proprietary-gray?style=for-the-badge)

**Platform Perencanaan Umrah AI #1 Indonesia**

*Panggilan-Nya, Langkahmu*

[Demo](https://labbaik.streamlit.app) · [Dokumentasi](https://docs.labbaik.cloud) · [Feedback](https://labbaik.cloud/feedback)

</div>

---

## ✨ Fitur Utama

### 🧭 Umrah Mandiri
- **Virtual Manasik Simulator** - Latihan 8 rukun umrah interaktif
- **3 Pilar Framework** - Checklist persiapan komprehensif
- **AI Budget Optimizer** - Hitung estimasi biaya dengan tips hemat
- **Weather & Crowd Prediction** - Info cuaca dan prediksi keramaian
- **Koleksi 20+ Doa** - Arab, Latin, dan terjemahan
- **Emergency SOS** - Kontak darurat lengkap

### 👥 Umrah Bareng
- **Smart Matching System** - AI matching berdasarkan preferensi
- **Trip Leader Verified** - Profil leader dengan rating
- **Group Chat** - Diskusi dengan calon teman perjalanan
- **Trip Management** - Kelola trip end-to-end

### 🎮 Gamification
- **10 Level Progress** - Dari Pemula hingga Grand Master
- **Daily Challenges** - Tantangan harian dengan XP rewards
- **Achievement System** - 10+ achievements untuk di-unlock
- **Leaderboard** - Kompetisi dengan jamaah lain

### 💰 Tools
- **AI Chat Assistant** - Tanya apa saja 24/7
- **Cost Simulator** - Estimasi biaya real-time
- **Savings Tracker** - Track tabungan umrah
- **Countdown Timer** - Hitung mundur ke hari H

---

## 🚀 Quick Deploy ke Streamlit Cloud

### Langkah 1: Download & Extract
```bash
# Download labbaik-v6-deploy.zip dari link yang diberikan
unzip labbaik-v6-deploy.zip
cd umrah-planner-v6
```

### Langkah 2: Push ke GitHub
```bash
# Inisialisasi git
git init
git branch -M main
git remote add origin https://github.com/mshadianto/umrah-planner.git

# Commit & Push
git add -A
git commit -m "🚀 LABBAIK AI v6.0 - Super Boom Edition"
git push -u origin main --force
```

### Langkah 3: Deploy di Streamlit Cloud
1. Buka https://share.streamlit.io
2. Klik **New app**
3. Pilih repository: `mshadianto/umrah-planner`
4. Branch: `main`
5. Main file: `app.py`
6. Klik **Deploy**

### Langkah 4: Konfigurasi Secrets
Di Streamlit Cloud → App Settings → Secrets, tambahkan:

```toml
DATABASE_URL = "postgresql://neondb_owner:xxx@ep-xxx.neon.tech/neondb?sslmode=require"
GROQ_API_KEY = "gsk_xxx"
OPENAI_API_KEY = "sk-xxx"
```

---

## 📁 Struktur Project

```
umrah-planner-v6/
├── app.py                 # Main entry point
├── requirements.txt       # Dependencies
├── .streamlit/
│   └── config.toml       # Streamlit config
├── ui/
│   ├── pages/
│   │   ├── home.py       # Homepage (BLACK GOLD theme)
│   │   ├── chat.py       # AI Chat Assistant
│   │   ├── simulator.py  # Cost Simulator
│   │   ├── umrah_mandiri.py  # Umrah Mandiri (Gamification!)
│   │   ├── umrah_bareng.py   # Umrah Bareng (Smart Matching)
│   │   └── booking.py    # Booking System
│   └── components/       # Reusable components
├── services/
│   ├── ai/              # AI services (Groq/OpenAI)
│   ├── database/        # Neon PostgreSQL
│   └── cost/            # Cost calculator
├── core/                # Config, constants, exceptions
├── data/
│   ├── models/          # Data models
│   └── knowledge/       # FAQ, Arabic phrases, guides
└── config/              # YAML configurations
```

---

## 🗄️ Database (Neon PostgreSQL)

Tabel yang tersedia:
- `users` - Data pengguna
- `visitor_stats` - Statistik pengunjung
- `visitor_logs` - Log kunjungan
- `open_trips` - Trip yang dibuka
- `trip_members` - Member dalam trip
- `saved_trips` - Trip yang disimpan
- `forum_posts` - Post forum
- `forum_comments` - Komentar
- `post_likes` - Like pada post

---

## 🎨 Theme: BLACK GOLD

Warna premium yang digunakan:
- Background: `#0d0d0d`, `#1a1a1a`
- Gold Primary: `#d4af37`
- Gold Light: `#f4d03f`
- Text: `#fafafa`, `#888888`

---

## 📞 Kontak

- **Developer:** MS Hadianto
- **Website:** https://labbaik.cloud
- **Email:** info@mshadianto.id

---

## 📜 License

Proprietary - © 2025 MS Hadianto. All rights reserved.

---

<div align="center">

**🕋 LABBAIK - Panggilan-Nya, Langkahmu**

</div>
