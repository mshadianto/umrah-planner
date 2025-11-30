"""
EMERGENCY HOTFIX for LABBAIK Footer HTML Rendering
Apply this ONLY if main app.py update doesn't work.

This file patches the render_labbaik_footer() function.
"""

def render_labbaik_footer_FIXED():
    """
    FIXED VERSION - Render LABBAIK branded footer with REAL visitor count
    This replaces the broken render_labbaik_footer() function
    """
    import streamlit as st
    from visitor_tracker import get_visitor_stats
    
    # Get REAL visitor statistics
    stats = get_visitor_stats()
    total_visitors = stats['total_visitors']
    total_views = stats['total_views']
    
    # Format with thousand separators
    visitor_str = f"{total_visitors:,}"
    views_str = f"{total_views:,}"
    
    # Simple, working footer HTML
    st.markdown(f"""
<div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); padding: 40px; border-radius: 20px; text-align: center; margin-top: 50px;">
    <div style="font-family: 'Noto Naskh Arabic', serif; font-size: 1.8rem; color: #D4AF37;">لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ</div>
    <div style="font-size: 1.3rem; font-weight: 700; color: white; letter-spacing: 0.25em; margin: 12px 0;">LABBAIK</div>
    <div style="color: #C9A86C; font-size: 0.95rem; margin-bottom: 20px;">Panggilan-Nya, Langkahmu</div>
    <div style="display: flex; justify-content: center; gap: 30px; margin: 20px 0;">
        <div style="background: rgba(212, 175, 55, 0.15); padding: 12px 24px; border-radius: 20px;">
            <div style="color: #D4AF37; font-size: 0.75rem; opacity: 0.8;">Total Pengunjung</div>
            <div style="color: #D4AF37; font-size: 1.5rem; font-weight: 700;">{visitor_str}</div>
        </div>
        <div style="background: rgba(0, 107, 60, 0.15); padding: 12px 24px; border-radius: 20px;">
            <div style="color: #C9A86C; font-size: 0.75rem; opacity: 0.8;">Total Page Views</div>
            <div style="color: #C9A86C; font-size: 1.5rem; font-weight: 700;">{views_str}</div>
        </div>
    </div>
    <div style="color: #888; font-size: 0.85rem; margin: 20px 0 15px;">📧 sopian.hadianto@gmail.com | 📱 +62 815 9658 833 | 🌐 labbaik.ai</div>
    <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px 20px; margin: 20px auto; max-width: 600px;">
        <div style="color: #D4AF37; font-size: 0.8rem; font-weight: 600; margin-bottom: 8px;">⚠️ Disclaimer</div>
        <div style="color: #aaa; font-size: 0.75rem; line-height: 1.6;">Aplikasi ini dikembangkan oleh <strong>non-developer</strong> dengan memanfaatkan teknologi AI (Claude, Gemini, dll). Informasi yang disajikan bersifat simulasi dan estimasi. Untuk keputusan perjalanan umrah, selalu konsultasikan dengan travel agent resmi berizin.</div>
    </div>
    <div style="border-top: 1px solid #333; padding-top: 20px; margin-top: 20px; color: #666; font-size: 0.8rem;">© 2025 LABBAIK. Hak Cipta Dilindungi.<br><span style="color: #D4AF37;">Made with ❤️ & AI by MS Hadianto</span><br><span style="color: #555; font-size: 0.7rem;">v3.0.0 Beta • Powered by Streamlit & Groq AI</span></div>
</div>
""", unsafe_allow_html=True)  # ← PENTING! unsafe_allow_html=True


# INSTRUCTIONS:
# 1. Open your app.py file
# 2. Find the function: def render_labbaik_footer():
# 3. Replace entire function with render_labbaik_footer_FIXED() above
# 4. Or add this at the end of app.py and change the call in main()
