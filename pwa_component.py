# pwa_component.py - PWA Integration for LABBAIK
# Progressive Web App support for Streamlit
# Version: 1.0.0

import streamlit as st
import streamlit.components.v1 as components

# ============================================
# PWA CONFIGURATION
# ============================================

PWA_CONFIG = {
    "name": "LABBAIK",
    "short_name": "LABBAIK",
    "description": "Platform AI Perencanaan Umrah #1 Indonesia",
    "theme_color": "#D4AF37",
    "background_color": "#1A1A1A",
    "display": "standalone",
    "orientation": "portrait",
    "start_url": "/",
    "scope": "/"
}


def inject_pwa_head():
    """Inject PWA meta tags into page head"""
    
    pwa_head = f"""
    <!-- PWA Meta Tags - LABBAIK -->
    <meta name="application-name" content="{PWA_CONFIG['name']}">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="{PWA_CONFIG['name']}">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="theme-color" content="{PWA_CONFIG['theme_color']}">
    <meta name="msapplication-TileColor" content="{PWA_CONFIG['background_color']}">
    <meta name="msapplication-tap-highlight" content="no">
    <meta name="format-detection" content="telephone=no">
    
    <!-- Viewport for mobile -->
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5, viewport-fit=cover">
    
    <!-- PWA Manifest -->
    <link rel="manifest" href="app/static/manifest.json">
    
    <!-- Favicon & Icons -->
    <link rel="icon" type="image/png" sizes="32x32" href="app/static/icons/icon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="app/static/icons/icon-16x16.png">
    <link rel="apple-touch-icon" href="app/static/icons/icon-180x180.png">
    <link rel="apple-touch-icon" sizes="152x152" href="app/static/icons/icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="app/static/icons/icon-180x180.png">
    <link rel="apple-touch-icon" sizes="167x167" href="app/static/icons/icon-167x167.png">
    
    <!-- Splash Screens iOS -->
    <link rel="apple-touch-startup-image" href="app/static/splash/splash-640x1136.png" media="(device-width: 320px) and (device-height: 568px)">
    <link rel="apple-touch-startup-image" href="app/static/splash/splash-750x1334.png" media="(device-width: 375px) and (device-height: 667px)">
    <link rel="apple-touch-startup-image" href="app/static/splash/splash-1242x2208.png" media="(device-width: 414px) and (device-height: 736px)">
    
    <!-- MS Tile -->
    <meta name="msapplication-TileImage" content="app/static/icons/icon-144x144.png">
    
    <style>
        /* PWA Optimizations */
        html, body {{
            overscroll-behavior-y: contain;
            -webkit-overflow-scrolling: touch;
        }}
        
        /* Safe area for notched devices */
        .main .block-container {{
            padding-top: env(safe-area-inset-top);
            padding-bottom: env(safe-area-inset-bottom);
            padding-left: env(safe-area-inset-left);
            padding-right: env(safe-area-inset-right);
        }}
        
        /* Hide scrollbar on mobile for cleaner look */
        @media (max-width: 768px) {{
            ::-webkit-scrollbar {{
                width: 0px;
                background: transparent;
            }}
        }}
        
        /* PWA Install Banner */
        .pwa-install-banner {{
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%);
            border: 2px solid #D4AF37;
            border-radius: 15px;
            padding: 15px 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
            z-index: 999999;
            max-width: 90%;
            animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        
        @keyframes slideUp {{
            from {{
                transform: translateX(-50%) translateY(150%);
                opacity: 0;
            }}
            to {{
                transform: translateX(-50%) translateY(0);
                opacity: 1;
            }}
        }}
        
        .pwa-install-banner .icon {{
            font-size: 2rem;
        }}
        
        .pwa-install-banner .content {{
            flex: 1;
        }}
        
        .pwa-install-banner .title {{
            color: #D4AF37;
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: 2px;
        }}
        
        .pwa-install-banner .subtitle {{
            color: #888;
            font-size: 0.8rem;
        }}
        
        .pwa-install-btn {{
            background: linear-gradient(135deg, #D4AF37 0%, #C9A86C 100%);
            color: #1A1A1A;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: 700;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            font-size: 0.9rem;
        }}
        
        .pwa-install-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(212, 175, 55, 0.4);
        }}
        
        .pwa-dismiss {{
            background: transparent;
            border: none;
            color: #666;
            font-size: 1.2rem;
            cursor: pointer;
            padding: 5px;
            line-height: 1;
        }}
        
        .pwa-dismiss:hover {{
            color: #999;
        }}
        
        /* Installed indicator */
        .pwa-installed-badge {{
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }}
    </style>
    """
    
    st.markdown(pwa_head, unsafe_allow_html=True)


def inject_service_worker():
    """Inject service worker registration and install prompt scripts"""
    
    sw_script = """
    <script>
        // ============================================
        // LABBAIK PWA - Service Worker & Install
        // ============================================
        
        // Check if already installed
        const isInstalled = window.matchMedia('(display-mode: standalone)').matches || 
                           window.navigator.standalone === true;
        
        // Store install prompt
        let deferredPrompt = null;
        let installBannerShown = false;
        
        // Register Service Worker
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', async () => {
                try {
                    const registration = await navigator.serviceWorker.register('app/static/service-worker.js', {
                        scope: '/'
                    });
                    console.log('🕋 LABBAIK SW registered:', registration.scope);
                    
                    // Check for updates
                    registration.addEventListener('updatefound', () => {
                        console.log('🔄 LABBAIK SW update found');
                    });
                } catch (error) {
                    console.log('⚠️ SW registration failed:', error);
                }
            });
        }
        
        // Capture install prompt
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            console.log('📱 Install prompt captured');
            
            // Show install banner after 10 seconds if not dismissed before
            if (!localStorage.getItem('pwa-banner-dismissed') && !installBannerShown && !isInstalled) {
                setTimeout(() => {
                    if (deferredPrompt && !installBannerShown) {
                        showInstallBanner();
                    }
                }, 10000);
            }
        });
        
        // Show install banner
        function showInstallBanner() {
            if (installBannerShown || isInstalled) return;
            installBannerShown = true;
            
            const banner = document.createElement('div');
            banner.className = 'pwa-install-banner';
            banner.id = 'pwa-install-banner';
            banner.innerHTML = `
                <span class="icon">📱</span>
                <div class="content">
                    <div class="title">Install LABBAIK</div>
                    <div class="subtitle">Akses cepat dari home screen</div>
                </div>
                <button class="pwa-install-btn" onclick="installPWA()">Install</button>
                <button class="pwa-dismiss" onclick="dismissBanner()">&times;</button>
            `;
            document.body.appendChild(banner);
        }
        
        // Install PWA
        async function installPWA() {
            if (!deferredPrompt) {
                console.log('No install prompt available');
                return;
            }
            
            deferredPrompt.prompt();
            const { outcome } = await deferredPrompt.userChoice;
            
            console.log('Install outcome:', outcome);
            
            if (outcome === 'accepted') {
                console.log('✅ User installed LABBAIK PWA');
            }
            
            deferredPrompt = null;
            dismissBanner();
        }
        
        // Dismiss banner
        function dismissBanner() {
            const banner = document.getElementById('pwa-install-banner');
            if (banner) {
                banner.style.animation = 'slideUp 0.3s ease-in reverse';
                setTimeout(() => banner.remove(), 300);
            }
            localStorage.setItem('pwa-banner-dismissed', 'true');
        }
        
        // Track installation
        window.addEventListener('appinstalled', () => {
            console.log('🎉 LABBAIK PWA installed successfully');
            dismissBanner();
            deferredPrompt = null;
        });
        
        // Expose functions globally
        window.installPWA = installPWA;
        window.dismissBanner = dismissBanner;
        window.showInstallBanner = showInstallBanner;
        
        // Log PWA status
        if (isInstalled) {
            console.log('📱 Running as installed PWA');
        }
    </script>
    """
    
    components.html(sw_script, height=0)


def render_install_card():
    """Render install instructions card for About page"""
    
    install_html = """
    <div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); 
                border: 2px solid #D4AF3740; border-radius: 20px; padding: 25px; margin: 20px 0;">
        
        <div style="text-align: center; margin-bottom: 20px;">
            <span style="font-size: 3rem;">📱</span>
            <h3 style="color: #D4AF37; margin: 10px 0 5px 0;">Install LABBAIK di HP Anda</h3>
            <p style="color: #888; font-size: 0.9rem; margin: 0;">
                Akses LABBAIK langsung dari home screen - seperti aplikasi native!
            </p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
            <!-- Android -->
            <div style="background: #1E1E1E; border-radius: 15px; padding: 20px; border: 1px solid #333;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                    <span style="font-size: 1.5rem;">🤖</span>
                    <span style="color: #4CAF50; font-weight: 700;">Android</span>
                </div>
                <ol style="color: #aaa; font-size: 0.85rem; line-height: 1.8; padding-left: 20px; margin: 0;">
                    <li>Buka di <strong>Chrome</strong></li>
                    <li>Tap menu <strong>⋮</strong> (kanan atas)</li>
                    <li>Pilih "<strong>Add to Home screen</strong>"</li>
                    <li>Tap "<strong>Add</strong>"</li>
                </ol>
                <div style="margin-top: 15px; padding: 10px; background: #4CAF5020; border-radius: 8px; text-align: center;">
                    <span style="color: #4CAF50; font-size: 0.8rem;">✓ Gratis & Instant</span>
                </div>
            </div>
            
            <!-- iPhone -->
            <div style="background: #1E1E1E; border-radius: 15px; padding: 20px; border: 1px solid #333;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                    <span style="font-size: 1.5rem;">🍎</span>
                    <span style="color: #007AFF; font-weight: 700;">iPhone / iPad</span>
                </div>
                <ol style="color: #aaa; font-size: 0.85rem; line-height: 1.8; padding-left: 20px; margin: 0;">
                    <li>Buka di <strong>Safari</strong></li>
                    <li>Tap tombol <strong>Share</strong> 📤</li>
                    <li>Scroll, pilih "<strong>Add to Home Screen</strong>"</li>
                    <li>Tap "<strong>Add</strong>"</li>
                </ol>
                <div style="margin-top: 15px; padding: 10px; background: #007AFF20; border-radius: 8px; text-align: center;">
                    <span style="color: #007AFF; font-size: 0.8rem;">✓ No App Store needed</span>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 20px; padding: 15px; background: #D4AF3715; border-radius: 10px; text-align: center;">
            <div style="color: #D4AF37; font-weight: 600; margin-bottom: 5px;">💡 Keuntungan Install:</div>
            <div style="color: #888; font-size: 0.85rem;">
                Akses cepat • Layar penuh • Notifikasi • Hemat data
            </div>
        </div>
    </div>
    """
    
    st.markdown(install_html, unsafe_allow_html=True)
    
    # Manual install button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📱 Install LABBAIK Sekarang", type="primary", use_container_width=True, key="pwa_install_btn"):
            components.html("""
                <script>
                    if (window.installPWA) {
                        window.installPWA();
                    } else {
                        alert('Untuk install:\\n\\n📱 Android: Tap menu ⋮ → Add to Home screen\\n🍎 iPhone: Tap Share 📤 → Add to Home Screen');
                    }
                </script>
            """, height=0)


def render_pwa_status():
    """Show PWA installation status badge"""
    
    status_html = """
    <script>
        const isInstalled = window.matchMedia('(display-mode: standalone)').matches || 
                           window.navigator.standalone === true;
        
        const statusDiv = document.getElementById('pwa-status');
        if (statusDiv) {
            if (isInstalled) {
                statusDiv.innerHTML = '<span class="pwa-installed-badge">✓ Terinstall sebagai App</span>';
            }
        }
    </script>
    <div id="pwa-status"></div>
    """
    
    components.html(status_html, height=30)


def init_pwa():
    """Initialize PWA support - call at start of main()"""
    inject_pwa_head()
    inject_service_worker()


# ============================================
# USAGE:
# ============================================
# 
# In app.py:
# 
# from pwa_component import init_pwa, render_install_card
# 
# def main():
#     init_pwa()  # Add this at the start
#     ...
# 
# def render_about():
#     ...
#     render_install_card()  # Add in About page
# ============================================
