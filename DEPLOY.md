# 🚀 Deployment Guide - Railway.com

## Langkah-langkah Deploy ke Railway

### 1. Persiapan GitHub Repository

```bash
# Clone atau download project
cd umrah-planner

# Initialize git (jika belum)
git init

# Add semua files
git add .

# Commit
git commit -m "Initial commit - Umrah Planner AI"

# Buat repository baru di GitHub, lalu:
git remote add origin https://github.com/USERNAME/umrah-planner.git
git branch -M main
git push -u origin main
```

### 2. Deploy ke Railway

#### Opsi A: Via Railway Dashboard (Recommended)

1. **Login ke Railway**
   - Buka https://railway.app/
   - Login dengan GitHub

2. **Create New Project**
   - Klik "New Project"
   - Pilih "Deploy from GitHub repo"
   - Authorize Railway untuk akses GitHub
   - Pilih repository `umrah-planner`

3. **Configure Environment Variables**
   - Klik project yang baru dibuat
   - Go to "Variables" tab
   - Add variables berikut:

   ```
   LLM_PROVIDER=groq
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx
   GROQ_MODEL=llama-3.3-70b-versatile
   EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
   DEFAULT_CURRENCY=IDR
   USD_TO_IDR_RATE=15500
   ```

4. **Deploy**
   - Railway akan auto-detect Procfile
   - Deployment akan berjalan otomatis
   - Tunggu hingga status "Success"

5. **Generate Domain**
   - Go to "Settings" tab
   - Scroll ke "Domains"
   - Klik "Generate Domain"
   - Atau add custom domain

#### Opsi B: Via Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link ke existing project atau create new
railway link

# Set environment variables
railway variables set LLM_PROVIDER=groq
railway variables set GROQ_API_KEY=gsk_xxxxx
railway variables set GROQ_MODEL=llama-3.3-70b-versatile

# Deploy
railway up
```

### 3. Environment Variables yang Diperlukan

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `LLM_PROVIDER` | Yes | Provider AI | `groq` atau `openai` |
| `GROQ_API_KEY` | Yes* | Groq API Key | `gsk_xxxx` |
| `OPENAI_API_KEY` | Yes* | OpenAI API Key | `sk-xxxx` |
| `GROQ_MODEL` | No | Model Groq | `llama-3.3-70b-versatile` |
| `OPENAI_MODEL` | No | Model OpenAI | `gpt-4o-mini` |
| `EMBEDDING_MODEL` | No | Embedding model | Default sudah di-set |

*Pilih salah satu sesuai provider

### 4. Troubleshooting

#### Build Failed - Memory Issue
Railway free tier memiliki limit 512MB RAM. Jika build gagal:

1. Upgrade ke paid plan ($5/month)
2. Atau gunakan Dockerfile untuk optimize:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies first (cached)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 8501

# Run
CMD streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

#### App Tidak Bisa Diakses
- Pastikan PORT environment variable digunakan (Railway set otomatis)
- Check logs di Railway dashboard
- Pastikan domain sudah di-generate

#### ChromaDB Error
- Pastikan folder `data/chroma_db` tidak di-gitignore untuk struktur
- Buat `.gitkeep` di folder tersebut jika perlu

### 5. Monitoring & Logs

- **Logs**: Railway Dashboard > Project > Deployments > View Logs
- **Metrics**: Railway Dashboard > Project > Metrics
- **Usage**: Railway Dashboard > Usage

### 6. Custom Domain

1. Go to Settings > Domains
2. Add custom domain
3. Configure DNS:
   ```
   Type: CNAME
   Name: app (atau subdomain lain)
   Value: <railway-generated-url>
   ```

### 7. Auto-Deploy

Railway otomatis deploy setiap push ke branch `main`:

```bash
# Setiap perubahan
git add .
git commit -m "Update feature"
git push origin main
# Railway akan auto-deploy!
```

### 8. Biaya Railway

| Plan | Harga | Resources |
|------|-------|-----------|
| Free | $0 | 512MB RAM, 500 hrs/month |
| Hobby | $5/month | 8GB RAM, unlimited |
| Pro | Usage-based | Custom |

**Rekomendasi**: Hobby plan untuk production

---

## Alternative: Deploy ke Platform Lain

### Streamlit Cloud (Gratis)
1. Push ke GitHub
2. Buka https://share.streamlit.io/
3. Connect GitHub repo
4. Add secrets di Settings

### Render.com
1. Create Web Service
2. Connect GitHub
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `streamlit run app.py --server.port $PORT`

### Heroku
1. Add `Procfile` (sudah ada)
2. `heroku create`
3. `git push heroku main`

---

## Support

Jika ada masalah deployment:
1. Check Railway logs
2. Buka issue di GitHub
3. Join Railway Discord community
