"""
📊 Analytics & Tracking Integration
====================================
Google Analytics, Facebook Pixel, dan tracking internal

Copyright (c) 2025 MS Hadianto. All Rights Reserved.
"""

import streamlit as st
from datetime import datetime
import hashlib
import json

# ============================================
# ANALYTICS CONFIGURATION
# ============================================

ANALYTICS_CONFIG = {
    # Google Analytics 4
    "google_analytics": {
        "measurement_id": "G-XXXXXXXXXX",  # Ganti dengan GA4 ID Anda
        "enabled": True
    },
    # Facebook Pixel
    "facebook_pixel": {
        "pixel_id": "XXXXXXXXXXXXXXX",  # Ganti dengan FB Pixel ID
        "enabled": False
    },
    # Google Tag Manager
    "gtm": {
        "container_id": "GTM-XXXXXXX",  # Ganti dengan GTM ID
        "enabled": False
    },
    # Internal Analytics
    "internal": {
        "enabled": True,
        "store_in_db": True
    }
}

# ============================================
# GOOGLE ANALYTICS 4 INTEGRATION
# ============================================

def get_ga4_script():
    """Generate Google Analytics 4 script"""
    
    ga_id = ANALYTICS_CONFIG["google_analytics"]["measurement_id"]
    
    if not ANALYTICS_CONFIG["google_analytics"]["enabled"]:
        return ""
    
    return f"""
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{ga_id}', {{
            'page_title': document.title,
            'page_location': window.location.href,
            'send_page_view': true
        }});
        
        // Custom event tracking function
        function trackEvent(eventName, eventParams) {{
            gtag('event', eventName, eventParams);
        }}
        
        // Track scroll depth
        var scrollDepths = [25, 50, 75, 100];
        var trackedDepths = [];
        window.addEventListener('scroll', function() {{
            var scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
            scrollDepths.forEach(function(depth) {{
                if (scrollPercent >= depth && !trackedDepths.includes(depth)) {{
                    trackedDepths.push(depth);
                    trackEvent('scroll_depth', {{'depth': depth}});
                }}
            }});
        }});
    </script>
    """

def get_facebook_pixel_script():
    """Generate Facebook Pixel script"""
    
    pixel_id = ANALYTICS_CONFIG["facebook_pixel"]["pixel_id"]
    
    if not ANALYTICS_CONFIG["facebook_pixel"]["enabled"]:
        return ""
    
    return f"""
    <!-- Facebook Pixel -->
    <script>
        !function(f,b,e,v,n,t,s)
        {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', '{pixel_id}');
        fbq('track', 'PageView');
        
        // Custom event tracking
        function fbTrackEvent(eventName, eventParams) {{
            fbq('track', eventName, eventParams);
        }}
    </script>
    <noscript>
        <img height="1" width="1" style="display:none"
             src="https://www.facebook.com/tr?id={pixel_id}&ev=PageView&noscript=1"/>
    </noscript>
    """

def get_gtm_script():
    """Generate Google Tag Manager script"""
    
    container_id = ANALYTICS_CONFIG["gtm"]["container_id"]
    
    if not ANALYTICS_CONFIG["gtm"]["enabled"]:
        return ""
    
    return f"""
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','{container_id}');</script>
    <!-- End Google Tag Manager -->
    """

def inject_analytics_scripts():
    """Inject all analytics scripts into Streamlit"""
    
    all_scripts = ""
    
    # Add GA4
    all_scripts += get_ga4_script()
    
    # Add Facebook Pixel
    all_scripts += get_facebook_pixel_script()
    
    # Add GTM
    all_scripts += get_gtm_script()
    
    if all_scripts:
        st.markdown(all_scripts, unsafe_allow_html=True)

# ============================================
# INTERNAL ANALYTICS TRACKING
# ============================================

def init_analytics():
    """Initialize analytics storage in session state"""
    
    if 'analytics' not in st.session_state:
        st.session_state.analytics = {
            'session_id': hashlib.md5(str(datetime.now()).encode()).hexdigest()[:12],
            'session_start': datetime.now().isoformat(),
            'page_views': [],
            'events': [],
            'user_data': {},
            'conversions': []
        }

def track_page_view(page_name: str, page_params: dict = None):
    """Track page view"""
    
    init_analytics()
    
    page_view = {
        'page': page_name,
        'timestamp': datetime.now().isoformat(),
        'params': page_params or {}
    }
    
    st.session_state.analytics['page_views'].append(page_view)
    
    # Log for debugging
    print(f"[Analytics] Page view: {page_name}")

def track_event(event_name: str, event_category: str = "engagement", 
                event_params: dict = None):
    """Track custom event"""
    
    init_analytics()
    
    event = {
        'name': event_name,
        'category': event_category,
        'timestamp': datetime.now().isoformat(),
        'params': event_params or {}
    }
    
    st.session_state.analytics['events'].append(event)
    
    # Log for debugging
    print(f"[Analytics] Event: {event_name} ({event_category})")

def track_conversion(conversion_type: str, value: float = 0, 
                    currency: str = "IDR", details: dict = None):
    """Track conversion event"""
    
    init_analytics()
    
    conversion = {
        'type': conversion_type,
        'value': value,
        'currency': currency,
        'timestamp': datetime.now().isoformat(),
        'details': details or {}
    }
    
    st.session_state.analytics['conversions'].append(conversion)
    
    # Also track as event
    track_event(f"conversion_{conversion_type}", "conversion", {
        'value': value,
        'currency': currency
    })
    
    print(f"[Analytics] Conversion: {conversion_type} - {value} {currency}")

def track_user_property(property_name: str, property_value):
    """Set user property for segmentation"""
    
    init_analytics()
    
    st.session_state.analytics['user_data'][property_name] = property_value

# ============================================
# ECOMMERCE TRACKING
# ============================================

def track_view_item(item_id: str, item_name: str, item_category: str, 
                   price: float, currency: str = "IDR"):
    """Track product/item view"""
    
    track_event("view_item", "ecommerce", {
        'item_id': item_id,
        'item_name': item_name,
        'item_category': item_category,
        'price': price,
        'currency': currency
    })

def track_add_to_cart(item_id: str, item_name: str, price: float, 
                     quantity: int = 1, currency: str = "IDR"):
    """Track add to cart"""
    
    track_event("add_to_cart", "ecommerce", {
        'item_id': item_id,
        'item_name': item_name,
        'price': price,
        'quantity': quantity,
        'value': price * quantity,
        'currency': currency
    })

def track_begin_checkout(items: list, total_value: float, currency: str = "IDR"):
    """Track checkout initiation"""
    
    track_event("begin_checkout", "ecommerce", {
        'items': items,
        'value': total_value,
        'currency': currency
    })

def track_purchase(transaction_id: str, items: list, total_value: float,
                  currency: str = "IDR", payment_method: str = None):
    """Track purchase completion"""
    
    track_conversion("purchase", total_value, currency, {
        'transaction_id': transaction_id,
        'items': items,
        'payment_method': payment_method
    })

# ============================================
# LEAD TRACKING
# ============================================

def track_lead(lead_id: str, lead_source: str, lead_value: float = 0):
    """Track lead generation"""
    
    track_conversion("lead", lead_value, "IDR", {
        'lead_id': lead_id,
        'source': lead_source
    })

def track_form_submit(form_name: str, form_data: dict = None):
    """Track form submission"""
    
    track_event("form_submit", "lead_gen", {
        'form_name': form_name,
        'fields_count': len(form_data) if form_data else 0
    })

# ============================================
# AFFILIATE TRACKING
# ============================================

def track_affiliate_click(partner_id: str, partner_name: str, 
                         destination_url: str = None):
    """Track affiliate link click"""
    
    track_event("affiliate_click", "affiliate", {
        'partner_id': partner_id,
        'partner_name': partner_name,
        'destination_url': destination_url
    })

def track_affiliate_conversion(partner_id: str, order_value: float,
                              commission: float, currency: str = "IDR"):
    """Track affiliate conversion (if we get callback)"""
    
    track_conversion("affiliate_sale", commission, currency, {
        'partner_id': partner_id,
        'order_value': order_value
    })

# ============================================
# SUBSCRIPTION TRACKING
# ============================================

def track_subscription_view(plan_name: str, plan_price: float):
    """Track subscription plan view"""
    
    track_event("view_subscription", "subscription", {
        'plan_name': plan_name,
        'plan_price': plan_price
    })

def track_subscription_start(plan_name: str, plan_price: float, 
                            billing_period: str = "monthly"):
    """Track new subscription"""
    
    track_conversion("subscription", plan_price, "IDR", {
        'plan_name': plan_name,
        'billing_period': billing_period
    })

# ============================================
# ANALYTICS DASHBOARD
# ============================================

def render_analytics_dashboard():
    """Render analytics dashboard for admin"""
    
    st.markdown("## 📊 Analytics Dashboard")
    
    init_analytics()
    analytics = st.session_state.analytics
    
    # Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Page Views", len(analytics['page_views']))
    
    with col2:
        st.metric("Events", len(analytics['events']))
    
    with col3:
        st.metric("Conversions", len(analytics['conversions']))
    
    with col4:
        total_revenue = sum(c['value'] for c in analytics['conversions'])
        st.metric("Total Revenue", f"Rp {total_revenue:,.0f}")
    
    st.markdown("---")
    
    # Tabs for different analytics views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Page Views", "🎯 Events", "💰 Conversions", "⚙️ Setup"
    ])
    
    with tab1:
        st.markdown("### Recent Page Views")
        if analytics['page_views']:
            for pv in analytics['page_views'][-10:]:
                st.write(f"• **{pv['page']}** - {pv['timestamp'][:19]}")
        else:
            st.info("No page views recorded yet")
    
    with tab2:
        st.markdown("### Recent Events")
        if analytics['events']:
            for event in analytics['events'][-10:]:
                st.write(f"• **{event['name']}** ({event['category']}) - {event['timestamp'][:19]}")
        else:
            st.info("No events recorded yet")
    
    with tab3:
        st.markdown("### Conversions")
        if analytics['conversions']:
            for conv in analytics['conversions']:
                st.write(f"• **{conv['type']}** - Rp {conv['value']:,.0f} - {conv['timestamp'][:19]}")
        else:
            st.info("No conversions recorded yet")
    
    with tab4:
        render_analytics_setup()

def render_analytics_setup():
    """Setup instructions for analytics"""
    
    st.markdown("""
    ### 🔧 Setup Analytics
    
    #### 1. Google Analytics 4
    
    1. Buka [Google Analytics](https://analytics.google.com)
    2. Buat Property baru (GA4)
    3. Buat Web Data Stream
    4. Copy Measurement ID (format: G-XXXXXXXXXX)
    5. Update di file `analytics.py`:
    
    ```python
    ANALYTICS_CONFIG = {
        "google_analytics": {
            "measurement_id": "G-YOUR_ID_HERE",
            "enabled": True
        }
    }
    ```
    
    #### 2. Facebook Pixel (Optional)
    
    1. Buka [Facebook Business Manager](https://business.facebook.com)
    2. Buat Pixel baru di Events Manager
    3. Copy Pixel ID
    4. Update di `analytics.py`
    
    #### 3. Google Tag Manager (Advanced)
    
    1. Buka [Google Tag Manager](https://tagmanager.google.com)
    2. Buat Container baru
    3. Copy Container ID (format: GTM-XXXXXXX)
    4. Update di `analytics.py`
    
    #### 4. Streamlit Secrets
    
    Untuk production, simpan ID di Streamlit Secrets:
    
    ```toml
    # .streamlit/secrets.toml
    GA_MEASUREMENT_ID = "G-XXXXXXXXXX"
    FB_PIXEL_ID = "XXXXXXXXXXXXXXX"
    GTM_CONTAINER_ID = "GTM-XXXXXXX"
    ```
    
    #### 5. Events yang Di-track
    
    | Event | Kategori | Kapan |
    |-------|----------|-------|
    | page_view | pageview | Setiap halaman |
    | form_submit | lead_gen | Submit form |
    | affiliate_click | affiliate | Klik affiliate link |
    | view_item | ecommerce | Lihat paket |
    | add_to_cart | ecommerce | Tambah ke keranjang |
    | begin_checkout | ecommerce | Mulai checkout |
    | purchase | ecommerce | Selesai bayar |
    | subscription | subscription | Subscribe |
    """)

# ============================================
# UTM PARAMETER HANDLING
# ============================================

def parse_utm_params():
    """Parse UTM parameters from URL"""
    
    # In Streamlit, we can access query params
    query_params = st.query_params
    
    utm_params = {
        'utm_source': query_params.get('utm_source', ''),
        'utm_medium': query_params.get('utm_medium', ''),
        'utm_campaign': query_params.get('utm_campaign', ''),
        'utm_term': query_params.get('utm_term', ''),
        'utm_content': query_params.get('utm_content', ''),
        'ref': query_params.get('ref', '')
    }
    
    # Store in session
    if any(utm_params.values()):
        st.session_state.utm_params = utm_params
        track_event("utm_landing", "acquisition", utm_params)
    
    return utm_params

def get_attribution_source():
    """Get attribution source for conversions"""
    
    if hasattr(st.session_state, 'utm_params'):
        return st.session_state.utm_params
    return {'source': 'direct'}

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_session_analytics():
    """Get current session analytics data"""
    
    init_analytics()
    return st.session_state.analytics

def export_analytics_json():
    """Export analytics data as JSON"""
    
    init_analytics()
    return json.dumps(st.session_state.analytics, indent=2)

def clear_analytics():
    """Clear analytics data (for testing)"""
    
    if 'analytics' in st.session_state:
        del st.session_state.analytics
    init_analytics()

if __name__ == "__main__":
    render_analytics_dashboard()
