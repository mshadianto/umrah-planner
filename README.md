# 🕋 Umrah Planner AI

## RAG Agentic AI untuk Simulasi & Optimasi Biaya Perjalanan Umrah

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Aplikasi cerdas berbasis **RAG (Retrieval-Augmented Generation)** dan **Agentic AI** untuk membantu perencanaan keuangan perjalanan umrah. Mendukung **Groq** (gratis) dan **OpenAI** API.

---

## 🌟 Fitur Utama

### 💰 Simulasi Biaya Lengkap
- Kalkulasi biaya untuk 4 skenario: Ekonomis, Standard, Premium, VIP
- Rincian komponen: tiket pesawat, hotel, visa, transportasi, makan, dll
- Penyesuaian otomatis berdasarkan musim dan lokasi keberangkatan

### 🎯 Scenario Planning AI
- Perbandingan multi-skenario dengan visualisasi
- Analisis sensitivitas biaya
- Rekomendasi optimal berdasarkan budget

### 🤖 RAG-Powered AI Assistant
- Knowledge base komprehensif tentang umrah
- Jawaban akurat berbasis konteks
- Multi-agent orchestration untuk tugas kompleks

### 📊 Analisis & Laporan
- Grafik interaktif dengan Plotly
- Export ke PDF dan Excel
- Rencana cicilan dan tabungan

---

## 🚀 Quick Start (Windows Git Bash)

### Prerequisites
- Python 3.10 atau lebih baru
- Git Bash (termasuk dalam Git for Windows)
- VS Code (recommended)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/umrah-planner.git
cd umrah-planner
```

### Step 2: Jalankan Setup
```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Konfigurasi API Key
Edit file `.env` dan masukkan API key:

```env
# Pilih salah satu provider

# GROQ (Recommended - GRATIS!)
# Daftar di: https://console.groq.com/
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx

# ATAU OpenAI
# LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 4: Jalankan Aplikasi
```bash
./run.sh
```

Buka browser: **http://localhost:8501**

---

## 📦 Manual Installation (Alternative)

Jika script setup tidak berfungsi:

```bash
# 1. Buat virtual environment
python -m venv venv

# 2. Aktivasi (Windows Git Bash)
source venv/Scripts/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
cp .env.example .env

# 5. Edit .env dan tambahkan API key

# 6. Jalankan
streamlit run app.py
```

---

## 📁 Struktur Proyek

```
umrah-planner/
├── 📄 app.py                 # Main Streamlit application
├── 📄 config.py              # Configuration management
├── 📄 requirements.txt       # Python dependencies
├── 📄 setup.sh              # Setup script
├── 📄 run.sh                # Run script
├── 📄 .env.example          # Environment template
│
├── 📁 agents/               # AI Agents
│   ├── __init__.py
│   ├── base_agent.py        # Base agent class
│   ├── planning_agent.py    # Itinerary planning
│   ├── financial_agent.py   # Cost calculation
│   ├── research_agent.py    # Knowledge retrieval
│   └── orchestrator.py      # Multi-agent coordinator
│
├── 📁 rag/                  # RAG Components
│   ├── __init__.py
│   ├── embeddings.py        # Text embeddings
│   ├── vectorstore.py       # ChromaDB vector store
│   └── retriever.py         # Context retrieval
│
├── 📁 scenarios/            # Scenario Planning
│   ├── __init__.py
│   └── planner.py           # Scenario generator
│
├── 📁 utils/                # Utilities
│   ├── __init__.py
│   └── formatters.py        # Currency & text formatters
│
└── 📁 data/                 # Data Files
    ├── knowledge_base.json  # Umrah knowledge base
    └── chroma_db/           # Vector database
```

---

## 🔧 Konfigurasi

### LLM Provider Options

| Provider | Model | Kecepatan | Biaya |
|----------|-------|-----------|-------|
| **Groq** | llama-3.3-70b-versatile | ⚡ Sangat Cepat | 🆓 Gratis |
| **Groq** | mixtral-8x7b-32768 | ⚡ Cepat | 🆓 Gratis |
| **OpenAI** | gpt-4o-mini | 🚀 Cepat | 💵 Berbayar |
| **OpenAI** | gpt-4o | 🏎️ Sedang | 💵💵 Premium |

### Environment Variables

```env
# LLM Provider
LLM_PROVIDER=groq              # atau "openai"

# Groq Configuration
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# OpenAI Configuration (jika menggunakan OpenAI)
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini

# Embedding Model (lokal, tidak perlu API)
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

# Currency
DEFAULT_CURRENCY=IDR
USD_TO_IDR_RATE=15500
```

---

## 📖 Cara Penggunaan

### 1. Simulasi Biaya Cepat
1. Pilih **Skenario Paket** (Ekonomis/Standard/Premium/VIP)
2. Masukkan jumlah jamaah
3. Pilih durasi dan bulan keberangkatan
4. Klik **Lihat Estimasi**

### 2. Perbandingan Skenario
1. Navigasi ke **Perbandingan Skenario**
2. Atur parameter: jumlah jamaah, durasi, bulan
3. Klik **Bandingkan Semua Skenario**
4. Lihat grafik dan tabel perbandingan

### 3. Chat dengan AI Assistant
1. Navigasi ke **Chat AI**
2. Tanyakan apa saja tentang umrah:
   - "Berapa biaya umrah ekonomi 2024?"
   - "Apa saja dokumen yang diperlukan?"
   - "Kapan waktu terbaik untuk umrah?"

### 4. Buat Rencana Lengkap
1. Navigasi ke **Buat Rencana**
2. Isi semua detail perjalanan
3. AI akan menghasilkan:
   - Itinerary lengkap
   - Rincian biaya
   - Persyaratan dokumen
   - Tips perjalanan

---

## 🏗️ Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit UI (app.py)                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                  Agent Orchestrator                          │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │ Planning     │ Financial    │ Research                 │ │
│  │ Agent        │ Agent        │ Agent                    │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    RAG Engine                                │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │ Embeddings   │ Vector Store │ Retriever                │ │
│  │ (Sentence    │ (ChromaDB)   │                          │ │
│  │  Transformers│              │                          │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│               LLM Provider (Groq / OpenAI)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Komponen Biaya Umrah

| Komponen | Ekonomis | Standard | Premium | VIP |
|----------|----------|----------|---------|-----|
| **Tiket Pesawat** | 8-12 jt | 10-15 jt | 15-25 jt | 25-50 jt |
| **Hotel Makkah** | 400-800rb/mlm | 800rb-1.5jt/mlm | 1.5-4jt/mlm | 4-15jt/mlm |
| **Hotel Madinah** | 300-600rb/mlm | 600rb-1.2jt/mlm | 1.2-3jt/mlm | 3-10jt/mlm |
| **Visa** | 2.5 jt | 2.5 jt | 2.5 jt | 2.5 jt |
| **Makan/hari** | 150-200rb | 200-300rb | 300-500rb | 500rb-1jt |
| **Total Range** | **25-32 jt** | **35-45 jt** | **55-85 jt** | **100-200 jt** |

---

## 🔍 Knowledge Base

Knowledge base berisi informasi komprehensif tentang:

- **Overview**: Rukun umrah, perbedaan haji-umrah
- **Visa**: Persyaratan, proses, biaya visa
- **Transportasi**: Penerbangan, bus, kereta Haramain
- **Akomodasi**: Hotel Makkah & Madinah per bintang
- **Konsumsi**: Biaya makan, restoran, air zamzam
- **Waktu**: Musim terbaik, peak season
- **Perlengkapan**: Barang wajib, oleh-oleh
- **Paket Travel**: Perbandingan paket, travel legal
- **Kesehatan**: Vaksin, persiapan fisik
- **Ibadah**: Thawaf, sa'i, ziarah

---

## 🛠️ Troubleshooting

### Error: Module not found
```bash
pip install -r requirements.txt
```

### Error: ChromaDB initialization
```bash
rm -rf data/chroma_db
# Jalankan ulang aplikasi
```

### Error: API Key not found
Pastikan file `.env` sudah ada dan berisi API key yang valid.

### Slow embedding generation
Embedding pertama kali membutuhkan waktu untuk download model (~300MB). Setelah itu akan lebih cepat.

---

## 🤝 Contributing

1. Fork repository
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buka Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - UI Framework
- [LangChain](https://www.langchain.com/) - LLM Framework
- [Groq](https://groq.com/) - Fast LLM Inference
- [ChromaDB](https://www.trychroma.com/) - Vector Database
- [Sentence Transformers](https://www.sbert.net/) - Embeddings

---

**Made with ❤️ for Indonesian Pilgrims**
