# 📱 LABBAIK PWA Setup Guide
# Progressive Web App untuk Streamlit

## 🗂️ Folder Structure

```
umrah-planner/
├── app.py
├── pwa_component.py          # PWA integration
├── .streamlit/
│   └── config.toml
└── static/                    # PWA assets
    ├── manifest.json
    ├── service-worker.js
    ├── offline.html
    └── icons/
        ├── icon-72x72.png
        ├── icon-96x96.png
        ├── icon-128x128.png
        ├── icon-144x144.png
        ├── icon-152x152.png
        ├── icon-192x192.png
        ├── icon-384x384.png
        └── icon-512x512.png
```

## 📋 Step-by-Step Setup

### Step 1: Buat folder `static`

```bash
mkdir -p static/icons
```

### Step 2: Copy PWA files ke folder `static`

- `manifest.json` → `static/manifest.json`
- `service-worker.js` → `static/service-worker.js`
- `offline.html` → `static/offline.html`

### Step 3: Buat/Update `.streamlit/config.toml`

```toml
[server]
enableStaticServing = true

[theme]
primaryColor = "#D4AF37"
backgroundColor = "#1A1A1A"
secondaryBackgroundColor = "#2D2D2D"
textColor = "#FFFFFF"
```

### Step 4: Generate App Icons

Gunakan tool online untuk generate icons:
- https://www.pwabuilder.com/imageGenerator
- https://realfavicongenerator.net/

Upload logo LABBAIK 512x512, download semua ukuran.

### Step 5: Update `app.py`

Tambahkan di bagian atas setelah imports:

```python
# PWA Support
from pwa_component import init_pwa, render_install_button
```

Tambahkan di fungsi `main()` sebelum render apapun:

```python
def main():
    # Initialize PWA
    init_pwa()
    
    # ... rest of your code
```

### Step 6: Tambahkan Install Button (Opsional)

Di halaman Tentang Aplikasi atau Settings:

```python
def render_about():
    # ... existing code ...
    
    # Add PWA install section
    st.markdown("---")
    st.markdown("### 📱 Install LABBAIK di HP Anda")
    render_install_button()
```

## 🎨 Generate Icons Mudah

### Option 1: Online Generator (Recommended)

1. Buka https://www.pwabuilder.com/imageGenerator
2. Upload logo LABBAIK (512x512 PNG dengan background transparan)
3. Generate & download
4. Extract ke folder `static/icons/`

### Option 2: Manual dengan Python

```python
from PIL import Image

# Load original icon
img = Image.open('labbaik-logo-512.png')

# Generate all sizes
sizes = [72, 96, 128, 144, 152, 192, 384, 512]
for size in sizes:
    resized = img.resize((size, size), Image.LANCZOS)
    resized.save(f'static/icons/icon-{size}x{size}.png')
```

## ✅ Testing PWA

### Desktop Chrome:
1. Buka app di Chrome
2. Lihat address bar - ada icon install (⊕)
3. Klik untuk install

### Mobile Android:
1. Buka app di Chrome
2. Akan muncul banner "Add to Home Screen"
3. Atau tap menu ⋮ → "Add to Home screen"

### Mobile iOS (Safari):
1. Buka app di Safari
2. Tap Share button 📤
3. Scroll down, tap "Add to Home Screen"

## 🔍 Verify PWA

### Chrome DevTools:
1. F12 → Application tab
2. Check "Manifest" section
3. Check "Service Workers" section

### Lighthouse Audit:
1. F12 → Lighthouse tab
2. Check "Progressive Web App"
3. Run audit

## ⚠️ Limitations di Streamlit Cloud

Streamlit Cloud memiliki beberapa keterbatasan untuk PWA:

1. **Service Worker**: Mungkin tidak bekerja sempurna karena Streamlit menggunakan WebSocket
2. **Caching**: Limited karena konten dinamis
3. **Offline**: Basic offline page bisa, tapi app perlu internet

### Solusi Alternatif:
- Gunakan PWA Builder untuk wrap app: https://www.pwabuilder.com
- Input URL Streamlit app, generate Android APK

## 📱 Quick Install Instructions untuk User

Tambahkan di app:

```
📱 Install LABBAIK di HP Anda:

Android (Chrome):
1. Tap ⋮ menu
2. "Add to Home screen"
3. Tap "Add"

iPhone (Safari):
1. Tap 📤 Share
2. "Add to Home Screen"
3. Tap "Add"
```

## 🚀 Deploy Checklist

- [ ] Folder `static/` sudah ada di repo
- [ ] `manifest.json` sudah ada di `static/`
- [ ] Icons sudah ada di `static/icons/`
- [ ] `config.toml` sudah ada `enableStaticServing = true`
- [ ] `pwa_component.py` sudah di-import di `app.py`
- [ ] `init_pwa()` dipanggil di `main()`
- [ ] Test di mobile device
