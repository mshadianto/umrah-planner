"""
💳 Payment Gateway Integration
==============================
Midtrans, Xendit, dan payment processing

Copyright (c) 2025 MS Hadianto. All Rights Reserved.
"""

import streamlit as st
from datetime import datetime, timedelta
import hashlib
import json
import hmac
import base64
from typing import Dict, Optional, Any

# ============================================
# PAYMENT GATEWAY CONFIGURATION
# ============================================

def get_payment_config():
    """Get payment gateway configuration from secrets or env"""
    
    config = {
        # Midtrans Configuration
        "midtrans": {
            "merchant_id": st.secrets.get("MIDTRANS_MERCHANT_ID", "YOUR_MERCHANT_ID"),
            "client_key": st.secrets.get("MIDTRANS_CLIENT_KEY", "YOUR_CLIENT_KEY"),
            "server_key": st.secrets.get("MIDTRANS_SERVER_KEY", "YOUR_SERVER_KEY"),
            "is_production": st.secrets.get("MIDTRANS_IS_PRODUCTION", False),
            "enabled": True
        },
        # Xendit Configuration
        "xendit": {
            "api_key": st.secrets.get("XENDIT_API_KEY", "YOUR_API_KEY"),
            "callback_token": st.secrets.get("XENDIT_CALLBACK_TOKEN", "YOUR_CALLBACK_TOKEN"),
            "is_production": st.secrets.get("XENDIT_IS_PRODUCTION", False),
            "enabled": False
        }
    }
    
    return config

# ============================================
# SUBSCRIPTION PLANS
# ============================================

SUBSCRIPTION_PLANS = {
    "basic": {
        "id": "basic",
        "name": "Basic Member",
        "price": 49000,
        "price_display": "Rp 49.000",
        "billing_period": "monthly",
        "description": "Akses fitur dasar dengan lebih banyak kuota",
        "features": [
            "50 Chat AI / hari",
            "Simpan 5 rencana",
            "Bandingkan 5 skenario",
            "Diskon 5% booking",
            "Email support"
        ],
        "badge": "🥉"
    },
    "premium": {
        "id": "premium",
        "name": "Premium Member",
        "price": 149000,
        "price_display": "Rp 149.000",
        "billing_period": "monthly",
        "description": "Fitur lengkap untuk perencanaan optimal",
        "features": [
            "Unlimited Chat AI",
            "Simpan 20 rencana",
            "Bandingkan unlimited",
            "Export PDF",
            "Price alert",
            "Diskon 10% booking",
            "Priority support"
        ],
        "badge": "⭐",
        "popular": True
    },
    "vip": {
        "id": "vip",
        "name": "VIP Elite",
        "price": 499000,
        "price_display": "Rp 499.000",
        "billing_period": "monthly",
        "description": "Pengalaman premium dengan layanan eksklusif",
        "features": [
            "Semua fitur Premium",
            "Dedicated assistant 24/7",
            "Konsultasi via video call",
            "Cashback 5%",
            "Free airport transfer",
            "Diskon 15% booking",
            "Exclusive flash sale access"
        ],
        "badge": "👑"
    }
}

# ============================================
# MIDTRANS INTEGRATION
# ============================================

class MidtransPayment:
    """Midtrans payment gateway handler"""
    
    def __init__(self):
        config = get_payment_config()["midtrans"]
        self.merchant_id = config["merchant_id"]
        self.client_key = config["client_key"]
        self.server_key = config["server_key"]
        self.is_production = config["is_production"]
        
        # API URLs
        if self.is_production:
            self.snap_url = "https://app.midtrans.com/snap/snap.js"
            self.api_url = "https://api.midtrans.com"
        else:
            self.snap_url = "https://app.sandbox.midtrans.com/snap/snap.js"
            self.api_url = "https://api.sandbox.midtrans.com"
    
    def create_transaction(self, order_id: str, amount: int, 
                          customer: Dict, item_details: list) -> Dict:
        """Create Snap transaction token"""
        
        # In production, this would make API call to Midtrans
        # For demo, we'll simulate the response
        
        transaction_data = {
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": amount
            },
            "customer_details": {
                "first_name": customer.get("name", "Customer"),
                "email": customer.get("email", "customer@email.com"),
                "phone": customer.get("phone", "08123456789")
            },
            "item_details": item_details,
            "callbacks": {
                "finish": f"https://umrah-planner-by-mshadianto.streamlit.app/?order_id={order_id}"
            }
        }
        
        # Simulate API response
        # In production: response = requests.post(f"{self.api_url}/snap/v1/transactions", ...)
        
        token = hashlib.md5(f"{order_id}{datetime.now()}".encode()).hexdigest()
        redirect_url = f"{self.snap_url.replace('/snap/snap.js', '')}/snap/v2/vtweb/{token}"
        
        return {
            "success": True,
            "token": token,
            "redirect_url": redirect_url,
            "order_id": order_id
        }
    
    def get_snap_script(self) -> str:
        """Get Midtrans Snap.js script"""
        
        return f"""
        <script src="{self.snap_url}" data-client-key="{self.client_key}"></script>
        <script>
            function payWithMidtrans(token) {{
                snap.pay(token, {{
                    onSuccess: function(result) {{
                        window.location.href = '/?payment=success&order_id=' + result.order_id;
                    }},
                    onPending: function(result) {{
                        window.location.href = '/?payment=pending&order_id=' + result.order_id;
                    }},
                    onError: function(result) {{
                        window.location.href = '/?payment=error';
                    }},
                    onClose: function() {{
                        console.log('Payment popup closed');
                    }}
                }});
            }}
        </script>
        """
    
    def verify_signature(self, order_id: str, status_code: str, 
                        gross_amount: str, signature: str) -> bool:
        """Verify Midtrans notification signature"""
        
        raw_string = f"{order_id}{status_code}{gross_amount}{self.server_key}"
        expected_signature = hashlib.sha512(raw_string.encode()).hexdigest()
        
        return signature == expected_signature

# ============================================
# XENDIT INTEGRATION
# ============================================

class XenditPayment:
    """Xendit payment gateway handler"""
    
    def __init__(self):
        config = get_payment_config()["xendit"]
        self.api_key = config["api_key"]
        self.callback_token = config["callback_token"]
        self.is_production = config["is_production"]
        
        # API URLs
        if self.is_production:
            self.api_url = "https://api.xendit.co"
        else:
            self.api_url = "https://api.xendit.co"  # Xendit uses same URL, different API keys
    
    def create_invoice(self, external_id: str, amount: int,
                      payer_email: str, description: str,
                      success_url: str = None) -> Dict:
        """Create Xendit invoice"""
        
        # In production, this would make API call to Xendit
        # For demo, we'll simulate
        
        invoice_data = {
            "external_id": external_id,
            "amount": amount,
            "payer_email": payer_email,
            "description": description,
            "success_redirect_url": success_url or "https://umrah-planner-by-mshadianto.streamlit.app/?payment=success",
            "failure_redirect_url": "https://umrah-planner-by-mshadianto.streamlit.app/?payment=failed"
        }
        
        # Simulate API response
        invoice_id = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        invoice_url = f"https://checkout.xendit.co/web/{invoice_id}"
        
        return {
            "success": True,
            "invoice_id": invoice_id,
            "invoice_url": invoice_url,
            "external_id": external_id,
            "amount": amount,
            "expiry_date": (datetime.now() + timedelta(days=1)).isoformat()
        }
    
    def verify_callback(self, callback_token: str) -> bool:
        """Verify Xendit callback token"""
        return callback_token == self.callback_token

# ============================================
# PAYMENT PROCESSING
# ============================================

def generate_order_id(prefix: str = "SUB") -> str:
    """Generate unique order ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = hashlib.md5(str(datetime.now().microsecond).encode()).hexdigest()[:4].upper()
    return f"{prefix}-{timestamp}-{random_suffix}"

def process_subscription_payment(plan_id: str, user_data: Dict, 
                                 payment_method: str = "midtrans") -> Dict:
    """Process subscription payment"""
    
    if plan_id not in SUBSCRIPTION_PLANS:
        return {"success": False, "error": "Invalid plan"}
    
    plan = SUBSCRIPTION_PLANS[plan_id]
    order_id = generate_order_id("SUB")
    
    # Store pending order
    if 'pending_orders' not in st.session_state:
        st.session_state.pending_orders = {}
    
    st.session_state.pending_orders[order_id] = {
        "order_id": order_id,
        "plan_id": plan_id,
        "plan_name": plan["name"],
        "amount": plan["price"],
        "user_data": user_data,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    
    # Create payment
    if payment_method == "midtrans":
        midtrans = MidtransPayment()
        
        item_details = [{
            "id": plan_id,
            "name": f"Subscription - {plan['name']}",
            "price": plan["price"],
            "quantity": 1
        }]
        
        result = midtrans.create_transaction(
            order_id=order_id,
            amount=plan["price"],
            customer=user_data,
            item_details=item_details
        )
        
        return result
    
    elif payment_method == "xendit":
        xendit = XenditPayment()
        
        result = xendit.create_invoice(
            external_id=order_id,
            amount=plan["price"],
            payer_email=user_data.get("email", "customer@email.com"),
            description=f"Subscription - {plan['name']}"
        )
        
        return result
    
    return {"success": False, "error": "Invalid payment method"}

def confirm_payment(order_id: str, payment_data: Dict) -> Dict:
    """Confirm payment after callback"""
    
    if 'pending_orders' not in st.session_state:
        return {"success": False, "error": "Order not found"}
    
    if order_id not in st.session_state.pending_orders:
        return {"success": False, "error": "Order not found"}
    
    order = st.session_state.pending_orders[order_id]
    
    # Update order status
    order["status"] = "paid"
    order["paid_at"] = datetime.now().isoformat()
    order["payment_data"] = payment_data
    
    # Activate subscription
    activate_subscription(order["user_data"], order["plan_id"])
    
    # Move to completed orders
    if 'completed_orders' not in st.session_state:
        st.session_state.completed_orders = []
    st.session_state.completed_orders.append(order)
    
    # Remove from pending
    del st.session_state.pending_orders[order_id]
    
    return {"success": True, "order": order}

def activate_subscription(user_data: Dict, plan_id: str):
    """Activate user subscription after payment"""
    
    # In production, update database
    # For now, update session state
    
    if 'user' in st.session_state and st.session_state.user:
        plan = SUBSCRIPTION_PLANS[plan_id]
        
        # Map plan to role
        role_mapping = {
            "basic": "basic",
            "premium": "premium",
            "vip": "vip"
        }
        
        st.session_state.user['role'] = role_mapping.get(plan_id, "free")
        st.session_state.user['subscription'] = {
            "plan_id": plan_id,
            "plan_name": plan["name"],
            "started_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
            "auto_renew": True
        }

# ============================================
# PAYMENT UI COMPONENTS
# ============================================

def render_pricing_page():
    """Render subscription pricing page"""
    
    st.markdown("## 💎 Pilih Paket Langganan")
    st.markdown("Upgrade untuk akses fitur premium dan diskon eksklusif")
    
    cols = st.columns(3)
    
    for i, (plan_id, plan) in enumerate(SUBSCRIPTION_PLANS.items()):
        with cols[i]:
            # Card styling
            is_popular = plan.get("popular", False)
            border_style = "3px solid #FFD700" if is_popular else "1px solid #ddd"
            
            st.markdown(f"""
            <div style="
                background: white;
                border: {border_style};
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                height: 450px;
                position: relative;
            ">
                {f'<div style="position:absolute;top:-10px;right:20px;background:#FFD700;color:#000;padding:3px 15px;border-radius:20px;font-size:12px;font-weight:bold;">POPULER</div>' if is_popular else ''}
                
                <div style="font-size: 2em; margin-bottom: 10px;">{plan['badge']}</div>
                <h3 style="color: #1e3c72; margin: 0;">{plan['name']}</h3>
                <div style="font-size: 2em; font-weight: bold; color: #2a5298; margin: 15px 0;">
                    {plan['price_display']}
                </div>
                <div style="color: #666; font-size: 0.9em; margin-bottom: 15px;">/ bulan</div>
                <div style="text-align: left; font-size: 0.85em;">
                    {''.join([f'<div style="padding:5px 0;border-bottom:1px solid #eee;">✅ {f}</div>' for f in plan['features'][:5]])}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Pilih {plan['name']}", key=f"select_{plan_id}", 
                        use_container_width=True,
                        type="primary" if is_popular else "secondary"):
                st.session_state.selected_plan = plan_id
                st.session_state.page = "checkout"
                st.rerun()

def render_checkout_page():
    """Render checkout page"""
    
    plan_id = st.session_state.get("selected_plan", "premium")
    
    if plan_id not in SUBSCRIPTION_PLANS:
        st.error("Paket tidak valid")
        return
    
    plan = SUBSCRIPTION_PLANS[plan_id]
    
    st.markdown(f"## 💳 Checkout - {plan['name']}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Data Pembeli")
        
        with st.form("checkout_form"):
            name = st.text_input("Nama Lengkap *")
            email = st.text_input("Email *")
            phone = st.text_input("No. HP *", placeholder="08xxxxxxxxxx")
            
            st.markdown("### 💳 Metode Pembayaran")
            
            payment_method = st.radio(
                "Pilih metode pembayaran:",
                options=["midtrans", "xendit", "manual"],
                format_func=lambda x: {
                    "midtrans": "💳 Kartu Kredit/Debit, GoPay, OVO, Bank Transfer (Midtrans)",
                    "xendit": "🏦 Virtual Account, E-Wallet, Retail (Xendit)",
                    "manual": "📱 Transfer Manual (Konfirmasi via WhatsApp)"
                }[x]
            )
            
            agree = st.checkbox("Saya setuju dengan Syarat & Ketentuan")
            
            submitted = st.form_submit_button("🔒 Bayar Sekarang", use_container_width=True)
            
            if submitted:
                if not name or not email or not phone:
                    st.error("Mohon lengkapi semua data")
                elif not agree:
                    st.error("Mohon setujui Syarat & Ketentuan")
                else:
                    user_data = {
                        "name": name,
                        "email": email,
                        "phone": phone
                    }
                    
                    if payment_method == "manual":
                        # Show manual transfer info
                        show_manual_transfer_info(plan, user_data)
                    else:
                        # Process payment
                        with st.spinner("Memproses pembayaran..."):
                            result = process_subscription_payment(
                                plan_id=plan_id,
                                user_data=user_data,
                                payment_method=payment_method
                            )
                            
                            if result["success"]:
                                st.success("✅ Order dibuat! Redirecting ke halaman pembayaran...")
                                
                                # Show payment button/link
                                if payment_method == "midtrans":
                                    st.markdown(f"""
                                    <a href="{result['redirect_url']}" target="_blank">
                                        <button style="
                                            background: #00AA5B;
                                            color: white;
                                            padding: 15px 30px;
                                            border: none;
                                            border-radius: 8px;
                                            font-size: 16px;
                                            cursor: pointer;
                                            width: 100%;
                                        ">
                                            Lanjutkan ke Pembayaran Midtrans
                                        </button>
                                    </a>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.markdown(f"""
                                    <a href="{result['invoice_url']}" target="_blank">
                                        <button style="
                                            background: #0066FF;
                                            color: white;
                                            padding: 15px 30px;
                                            border: none;
                                            border-radius: 8px;
                                            font-size: 16px;
                                            cursor: pointer;
                                            width: 100%;
                                        ">
                                            Lanjutkan ke Pembayaran Xendit
                                        </button>
                                    </a>
                                    """, unsafe_allow_html=True)
                                
                                st.info(f"Order ID: {result['order_id']}")
                            else:
                                st.error(f"Gagal membuat order: {result.get('error', 'Unknown error')}")
    
    with col2:
        # Order Summary
        st.markdown("""
        <div style="
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #ddd;
        ">
            <h4 style="margin: 0 0 15px 0;">🛒 Ringkasan Order</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        **Paket:** {plan['badge']} {plan['name']}
        
        **Harga:** {plan['price_display']}/bulan
        
        **Fitur:**
        """)
        
        for feature in plan['features'][:5]:
            st.write(f"✅ {feature}")
        
        st.markdown("---")
        
        st.markdown(f"""
        **Subtotal:** {plan['price_display']}
        
        **Diskon:** Rp 0
        
        **Total:** **{plan['price_display']}**
        """)
        
        st.markdown("""
        ---
        
        🔒 **Pembayaran Aman**
        
        Data Anda dilindungi dengan enkripsi SSL
        """)

def show_manual_transfer_info(plan: Dict, user_data: Dict):
    """Show manual bank transfer information"""
    
    order_id = generate_order_id("SUB")
    
    st.success("✅ Order dibuat!")
    
    st.markdown(f"""
    ### 📱 Transfer Manual
    
    **Order ID:** `{order_id}`
    
    **Jumlah:** **{plan['price_display']}**
    
    ---
    
    **Transfer ke:**
    
    🏦 **Bank BCA**
    - No. Rekening: `1234567890`
    - Atas Nama: MS Hadianto
    
    🏦 **Bank Mandiri**
    - No. Rekening: `0987654321`
    - Atas Nama: MS Hadianto
    
    ---
    
    **Setelah transfer:**
    
    1. Screenshot bukti transfer
    2. Kirim ke WhatsApp: **+62 815 9658 833**
    3. Sertakan Order ID: `{order_id}`
    
    Aktivasi akan dilakukan dalam 1x24 jam setelah konfirmasi pembayaran.
    """)
    
    # WhatsApp confirmation link
    wa_message = f"Konfirmasi pembayaran Umrah Planner\n\nOrder ID: {order_id}\nNama: {user_data['name']}\nEmail: {user_data['email']}\nPaket: {plan['name']}\nJumlah: {plan['price_display']}"
    wa_link = f"https://wa.me/628159658833?text={wa_message}"
    
    st.markdown(f"""
    <a href="{wa_link}" target="_blank">
        <button style="
            background: #25D366;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
            margin-top: 15px;
        ">
            📱 Konfirmasi via WhatsApp
        </button>
    </a>
    """, unsafe_allow_html=True)

def render_payment_success():
    """Render payment success page"""
    
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <div style="font-size: 80px;">🎉</div>
        <h1 style="color: #00AA5B;">Pembayaran Berhasil!</h1>
        <p style="font-size: 1.2em;">Terima kasih telah berlangganan Umrah Planner AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("Subscription Anda telah aktif. Silakan refresh halaman untuk melihat fitur premium Anda.")
    
    if st.button("🏠 Ke Beranda", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

# ============================================
# PAYMENT GATEWAY SETUP GUIDE
# ============================================

def render_payment_setup_guide():
    """Setup guide for payment gateways"""
    
    st.markdown("""
    ## 🔧 Setup Payment Gateway
    
    ### 1. Midtrans (Recommended)
    
    **Langkah Setup:**
    
    1. **Daftar Akun**
       - Buka [Midtrans Dashboard](https://dashboard.midtrans.com)
       - Daftar akun baru (gratis)
       - Verifikasi email dan lengkapi data bisnis
    
    2. **Dapatkan API Keys**
       - Login ke dashboard
       - Pilih Environment: Sandbox (testing) atau Production
       - Settings → Access Keys
       - Copy: Merchant ID, Client Key, Server Key
    
    3. **Konfigurasi di Aplikasi**
       ```toml
       # .streamlit/secrets.toml
       MIDTRANS_MERCHANT_ID = "G123456789"
       MIDTRANS_CLIENT_KEY = "SB-Mid-client-xxx"
       MIDTRANS_SERVER_KEY = "SB-Mid-server-xxx"
       MIDTRANS_IS_PRODUCTION = false
       ```
    
    4. **Setup Notification URL**
       - Settings → Configuration → Notification URL
       - Set URL: `https://your-app.streamlit.app/api/midtrans-webhook`
    
    **Biaya Midtrans:**
    - Setup: Gratis
    - Per transaksi: 2.9% + Rp 2.000 (kartu kredit)
    - GoPay/OVO: 2%
    - Bank Transfer: Rp 4.000
    
    ---
    
    ### 2. Xendit
    
    **Langkah Setup:**
    
    1. **Daftar Akun**
       - Buka [Xendit Dashboard](https://dashboard.xendit.co)
       - Daftar dan verifikasi bisnis
    
    2. **Dapatkan API Keys**
       - Settings → API Keys
       - Generate new key
    
    3. **Konfigurasi**
       ```toml
       # .streamlit/secrets.toml
       XENDIT_API_KEY = "xnd_development_xxx"
       XENDIT_CALLBACK_TOKEN = "your_callback_token"
       XENDIT_IS_PRODUCTION = false
       ```
    
    **Biaya Xendit:**
    - Setup: Gratis
    - Virtual Account: Rp 4.500
    - E-Wallet: 1.5% - 3%
    - Kartu Kredit: 2.9% + Rp 2.000
    
    ---
    
    ### 3. Testing
    
    **Midtrans Sandbox Test Cards:**
    ```
    Card Number: 4811 1111 1111 1114
    CVV: 123
    Exp: Any future date
    OTP: 112233
    ```
    
    **Xendit Test Mode:**
    - Use API key starting with `xnd_development_`
    - Simulate success/failure via dashboard
    
    ---
    
    ### 4. Go Live Checklist
    
    ```
    □ Verifikasi bisnis di Midtrans/Xendit
    □ Ganti API keys dari Sandbox ke Production
    □ Test dengan transaksi kecil
    □ Setup notification/webhook URL
    □ Test refund flow
    □ Monitor di dashboard
    ```
    """)

if __name__ == "__main__":
    render_pricing_page()
