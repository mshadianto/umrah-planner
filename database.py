"""
🗄️ Supabase Database Integration
=================================
Database integration for Umrah Planner AI

Features:
- User authentication & management
- Subscription tracking
- Lead management
- Order tracking
- Analytics data

Developer: MS Hadianto
"""

import os
import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import hashlib
import json

# Try to import supabase
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("Warning: supabase-py not installed. Run: pip install supabase")

# ============================================
# SUPABASE CONFIGURATION
# ============================================

# Get credentials from environment or Streamlit secrets
def get_supabase_config() -> Dict[str, str]:
    """Get Supabase configuration from environment or secrets"""
    
    # Try Streamlit secrets first
    if hasattr(st, 'secrets'):
        try:
            return {
                "url": st.secrets.get("SUPABASE_URL", ""),
                "key": st.secrets.get("SUPABASE_KEY", ""),
                "service_key": st.secrets.get("SUPABASE_SERVICE_KEY", "")
            }
        except:
            pass
    
    # Fall back to environment variables
    return {
        "url": os.getenv("SUPABASE_URL", ""),
        "key": os.getenv("SUPABASE_KEY", ""),  # anon/public key
        "service_key": os.getenv("SUPABASE_SERVICE_KEY", "")  # service role key
    }


def get_supabase_client() -> Optional[Client]:
    """Get Supabase client instance"""
    if not SUPABASE_AVAILABLE:
        return None
    
    config = get_supabase_config()
    
    if not config["url"] or not config["key"]:
        return None
    
    try:
        client = create_client(config["url"], config["key"])
        return client
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        return None


def get_supabase_admin_client() -> Optional[Client]:
    """Get Supabase admin client (service role)"""
    if not SUPABASE_AVAILABLE:
        return None
    
    config = get_supabase_config()
    
    if not config["url"] or not config["service_key"]:
        return None
    
    try:
        client = create_client(config["url"], config["service_key"])
        return client
    except Exception as e:
        print(f"Error creating Supabase admin client: {e}")
        return None


# ============================================
# DATABASE SCHEMA (SQL for Supabase)
# ============================================

SCHEMA_SQL = """
-- =============================================
-- UMRAH PLANNER AI - DATABASE SCHEMA
-- =============================================

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(20) DEFAULT 'free',
    status VARCHAR(20) DEFAULT 'active',
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    email_verified BOOLEAN DEFAULT FALSE,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- 2. Subscriptions Table
CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    plan VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    start_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    end_date TIMESTAMP WITH TIME ZONE,
    auto_renew BOOLEAN DEFAULT FALSE,
    payment_method VARCHAR(50),
    amount DECIMAL(15, 2),
    currency VARCHAR(3) DEFAULT 'IDR',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. User Stats Table
CREATE TABLE IF NOT EXISTS user_stats (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    date DATE DEFAULT CURRENT_DATE,
    ai_chat_count INTEGER DEFAULT 0,
    scenarios_created INTEGER DEFAULT 0,
    plans_saved INTEGER DEFAULT 0,
    bookings_made INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, date)
);

-- 4. Leads Table
CREATE TABLE IF NOT EXISTS leads (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    lead_code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    city VARCHAR(100),
    package_type VARCHAR(50),
    num_people INTEGER DEFAULT 1,
    travel_month VARCHAR(20),
    budget VARCHAR(50),
    notes TEXT,
    source VARCHAR(50) DEFAULT 'website',
    status VARCHAR(20) DEFAULT 'new',
    assigned_to UUID REFERENCES users(id),
    referred_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    converted_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- 5. Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    order_code VARCHAR(30) UNIQUE NOT NULL,
    user_id UUID REFERENCES users(id),
    lead_id UUID REFERENCES leads(id),
    order_type VARCHAR(50) NOT NULL,
    items JSONB NOT NULL,
    subtotal DECIMAL(15, 2) NOT NULL,
    discount DECIMAL(15, 2) DEFAULT 0,
    total DECIMAL(15, 2) NOT NULL,
    commission DECIMAL(15, 2) DEFAULT 0,
    currency VARCHAR(3) DEFAULT 'IDR',
    status VARCHAR(20) DEFAULT 'pending',
    payment_method VARCHAR(50),
    payment_status VARCHAR(20) DEFAULT 'unpaid',
    paid_at TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- 6. Affiliate Clicks Table
CREATE TABLE IF NOT EXISTS affiliate_clicks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    ref_code VARCHAR(30) NOT NULL,
    partner_id VARCHAR(50) NOT NULL,
    user_id UUID REFERENCES users(id),
    ip_address VARCHAR(50),
    user_agent TEXT,
    converted BOOLEAN DEFAULT FALSE,
    conversion_value DECIMAL(15, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. Price Alerts Table
CREATE TABLE IF NOT EXISTS price_alerts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    alert_code VARCHAR(20) UNIQUE NOT NULL,
    package_type VARCHAR(50) NOT NULL,
    target_price DECIMAL(15, 2) NOT NULL,
    departure_month VARCHAR(20),
    notification_methods JSONB DEFAULT '["email"]'::jsonb,
    status VARCHAR(20) DEFAULT 'active',
    triggered_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 8. Saved Plans Table
CREATE TABLE IF NOT EXISTS saved_plans (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    plan_name VARCHAR(255) NOT NULL,
    plan_type VARCHAR(50),
    plan_data JSONB NOT NULL,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 9. Chat History Table
CREATE TABLE IF NOT EXISTS chat_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id VARCHAR(50),
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    tokens_used INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 10. Audit Logs Table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    target_type VARCHAR(50),
    target_id UUID,
    old_value JSONB,
    new_value JSONB,
    ip_address VARCHAR(50),
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 11. App Settings Table
CREATE TABLE IF NOT EXISTS app_settings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value JSONB NOT NULL,
    description TEXT,
    updated_by UUID REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================
-- INDEXES
-- =============================================

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);

CREATE INDEX IF NOT EXISTS idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status);

CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_created ON leads(created_at);

CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_created ON orders(created_at);

CREATE INDEX IF NOT EXISTS idx_affiliate_partner ON affiliate_clicks(partner_id);
CREATE INDEX IF NOT EXISTS idx_affiliate_created ON affiliate_clicks(created_at);

CREATE INDEX IF NOT EXISTS idx_chat_user ON chat_history(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_session ON chat_history(session_id);

CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_logs(created_at);

-- =============================================
-- ROW LEVEL SECURITY (RLS)
-- =============================================

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE saved_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE price_alerts ENABLE ROW LEVEL SECURITY;

-- Users can read their own data
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid() = id);

-- Subscriptions - users can view their own
CREATE POLICY "Users can view own subscriptions" ON subscriptions
    FOR SELECT USING (auth.uid() = user_id);

-- User stats - users can view their own
CREATE POLICY "Users can view own stats" ON user_stats
    FOR SELECT USING (auth.uid() = user_id);

-- Saved plans - users can CRUD their own
CREATE POLICY "Users can manage own plans" ON saved_plans
    FOR ALL USING (auth.uid() = user_id);

-- Chat history - users can view their own
CREATE POLICY "Users can view own chats" ON chat_history
    FOR ALL USING (auth.uid() = user_id);

-- Price alerts - users can manage their own
CREATE POLICY "Users can manage own alerts" ON price_alerts
    FOR ALL USING (auth.uid() = user_id);

-- =============================================
-- FUNCTIONS
-- =============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_subscriptions_updated_at
    BEFORE UPDATE ON subscriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_leads_updated_at
    BEFORE UPDATE ON leads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_orders_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_saved_plans_updated_at
    BEFORE UPDATE ON saved_plans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Function to increment user stats
CREATE OR REPLACE FUNCTION increment_user_stat(
    p_user_id UUID,
    p_stat_name TEXT,
    p_increment INTEGER DEFAULT 1
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO user_stats (user_id, date)
    VALUES (p_user_id, CURRENT_DATE)
    ON CONFLICT (user_id, date) DO NOTHING;
    
    EXECUTE format('
        UPDATE user_stats 
        SET %I = %I + $1 
        WHERE user_id = $2 AND date = CURRENT_DATE
    ', p_stat_name, p_stat_name)
    USING p_increment, p_user_id;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- DEFAULT DATA
-- =============================================

-- Insert default super admin (password: Admin@123)
INSERT INTO users (username, email, password_hash, name, phone, role, status)
VALUES (
    'superadmin',
    'sopian.hadianto@gmail.com',
    '240be518fabd2724ddb6f04eeb9d5b0c5e0d7e576d3f2a7d0dc6f1f9e8a7b6c5', -- SHA256 of Admin@123
    'MS Hadianto',
    '628159658833',
    'superadmin',
    'active'
) ON CONFLICT (username) DO NOTHING;

-- Insert default app settings
INSERT INTO app_settings (key, value, description)
VALUES 
    ('free_chat_limit', '5', 'Daily chat limit for free users'),
    ('basic_chat_limit', '50', 'Daily chat limit for basic users'),
    ('basic_price', '49000', 'Basic subscription price'),
    ('premium_price', '149000', 'Premium subscription price'),
    ('vip_price', '499000', 'VIP subscription price'),
    ('maintenance_mode', 'false', 'Enable maintenance mode')
ON CONFLICT (key) DO NOTHING;
"""


# ============================================
# DATABASE HELPER FUNCTIONS
# ============================================

class SupabaseDB:
    """Supabase Database Helper Class"""
    
    def __init__(self):
        self.client = get_supabase_client()
        self.admin_client = get_supabase_admin_client()
        self._fallback_mode = self.client is None
    
    @property
    def is_connected(self) -> bool:
        return self.client is not None
    
    # ==========================================
    # USER OPERATIONS
    # ==========================================
    
    def create_user(self, username: str, email: str, password: str, 
                    name: str, phone: str = "", role: str = "free") -> Dict:
        """Create new user"""
        if self._fallback_mode:
            return self._fallback_create_user(username, email, password, name, phone, role)
        
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            result = self.client.table("users").insert({
                "username": username,
                "email": email,
                "password_hash": password_hash,
                "name": name,
                "phone": phone,
                "role": role,
                "status": "active"
            }).execute()
            
            if result.data:
                return {"success": True, "user": result.data[0], "message": "Registrasi berhasil!"}
            return {"success": False, "error": "Gagal membuat user"}
            
        except Exception as e:
            error_msg = str(e)
            if "duplicate" in error_msg.lower():
                if "username" in error_msg:
                    return {"success": False, "error": "Username sudah digunakan"}
                if "email" in error_msg:
                    return {"success": False, "error": "Email sudah terdaftar"}
            return {"success": False, "error": str(e)}
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        if self._fallback_mode:
            return self._fallback_get_user(username)
        
        try:
            result = self.client.table("users").select("*").eq("username", username).single().execute()
            return result.data
        except:
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        if self._fallback_mode:
            return None
        
        try:
            result = self.client.table("users").select("*").eq("email", email).single().execute()
            return result.data
        except:
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        if self._fallback_mode:
            return None
        
        try:
            result = self.client.table("users").select("*").eq("id", user_id).single().execute()
            return result.data
        except:
            return None
    
    def verify_password(self, username: str, password: str) -> bool:
        """Verify user password"""
        user = self.get_user_by_username(username)
        if not user:
            return False
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return user.get("password_hash") == password_hash
    
    def update_user(self, user_id: str, data: Dict) -> Dict:
        """Update user data"""
        if self._fallback_mode:
            return {"success": False, "error": "Database tidak tersedia"}
        
        try:
            # Remove sensitive fields
            safe_data = {k: v for k, v in data.items() 
                        if k not in ["id", "password_hash", "created_at"]}
            
            result = self.client.table("users").update(safe_data).eq("id", user_id).execute()
            
            if result.data:
                return {"success": True, "user": result.data[0]}
            return {"success": False, "error": "User tidak ditemukan"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_password(self, user_id: str, new_password: str) -> Dict:
        """Update user password"""
        if self._fallback_mode:
            return {"success": False, "error": "Database tidak tersedia"}
        
        try:
            password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            
            result = self.client.table("users").update({
                "password_hash": password_hash
            }).eq("id", user_id).execute()
            
            if result.data:
                return {"success": True, "message": "Password berhasil diubah"}
            return {"success": False, "error": "User tidak ditemukan"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_last_login(self, user_id: str):
        """Update last login timestamp"""
        if self._fallback_mode:
            return
        
        try:
            self.client.table("users").update({
                "last_login": datetime.now().isoformat()
            }).eq("id", user_id).execute()
        except:
            pass
    
    def get_all_users(self, role: str = None, status: str = None) -> List[Dict]:
        """Get all users with optional filters"""
        if self._fallback_mode:
            return self._fallback_get_all_users()
        
        try:
            query = self.client.table("users").select("*")
            
            if role:
                query = query.eq("role", role)
            if status:
                query = query.eq("status", status)
            
            result = query.order("created_at", desc=True).execute()
            return result.data or []
            
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
    
    def delete_user(self, user_id: str) -> Dict:
        """Delete user"""
        if self._fallback_mode:
            return {"success": False, "error": "Database tidak tersedia"}
        
        try:
            # Check if superadmin
            user = self.get_user_by_id(user_id)
            if user and user.get("username") == "superadmin":
                return {"success": False, "error": "Tidak bisa menghapus Super Admin"}
            
            result = self.client.table("users").delete().eq("id", user_id).execute()
            return {"success": True, "message": "User berhasil dihapus"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_user_stats_summary(self) -> Dict:
        """Get user statistics summary"""
        if self._fallback_mode:
            return self._fallback_get_stats()
        
        try:
            # Total users
            all_users = self.get_all_users()
            
            stats = {
                "total": len(all_users),
                "by_role": {},
                "by_status": {"active": 0, "inactive": 0},
                "new_today": 0,
                "new_this_month": 0
            }
            
            today = datetime.now().strftime("%Y-%m-%d")
            this_month = datetime.now().strftime("%Y-%m")
            
            for user in all_users:
                role = user.get("role", "free")
                stats["by_role"][role] = stats["by_role"].get(role, 0) + 1
                
                status = user.get("status", "active")
                stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
                
                created = user.get("created_at", "")
                if created.startswith(today):
                    stats["new_today"] += 1
                if this_month in created:
                    stats["new_this_month"] += 1
            
            return stats
            
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {"total": 0, "by_role": {}, "by_status": {}}
    
    # ==========================================
    # SUBSCRIPTION OPERATIONS
    # ==========================================
    
    def create_subscription(self, user_id: str, plan: str, months: int = 1, 
                           amount: float = 0, payment_method: str = None) -> Dict:
        """Create new subscription"""
        if self._fallback_mode:
            return {"success": False, "error": "Database tidak tersedia"}
        
        try:
            end_date = datetime.now() + timedelta(days=30 * months)
            
            # Deactivate old subscriptions
            self.client.table("subscriptions").update({
                "status": "expired"
            }).eq("user_id", user_id).eq("status", "active").execute()
            
            # Create new subscription
            result = self.client.table("subscriptions").insert({
                "user_id": user_id,
                "plan": plan,
                "status": "active",
                "end_date": end_date.isoformat(),
                "amount": amount,
                "payment_method": payment_method
            }).execute()
            
            # Update user role
            self.client.table("users").update({
                "role": plan
            }).eq("id", user_id).execute()
            
            if result.data:
                return {"success": True, "subscription": result.data[0]}
            return {"success": False, "error": "Gagal membuat subscription"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_active_subscription(self, user_id: str) -> Optional[Dict]:
        """Get user's active subscription"""
        if self._fallback_mode:
            return None
        
        try:
            result = self.client.table("subscriptions").select("*").eq("user_id", user_id).eq("status", "active").single().execute()
            return result.data
        except:
            return None
    
    # ==========================================
    # LEAD OPERATIONS
    # ==========================================
    
    def create_lead(self, data: Dict) -> Dict:
        """Create new lead"""
        if self._fallback_mode:
            return {"success": False, "error": "Database tidak tersedia"}
        
        try:
            # Generate lead code
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            import random, string
            suffix = ''.join(random.choices(string.digits, k=4))
            lead_code = f"LEAD-{timestamp}-{suffix}"
            
            data["lead_code"] = lead_code
            
            result = self.client.table("leads").insert(data).execute()
            
            if result.data:
                return {"success": True, "lead": result.data[0], "lead_code": lead_code}
            return {"success": False, "error": "Gagal membuat lead"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_leads(self, status: str = None, limit: int = 100) -> List[Dict]:
        """Get leads"""
        if self._fallback_mode:
            return []
        
        try:
            query = self.client.table("leads").select("*")
            
            if status:
                query = query.eq("status", status)
            
            result = query.order("created_at", desc=True).limit(limit).execute()
            return result.data or []
            
        except:
            return []
    
    def update_lead_status(self, lead_id: str, status: str) -> Dict:
        """Update lead status"""
        if self._fallback_mode:
            return {"success": False, "error": "Database tidak tersedia"}
        
        try:
            data = {"status": status}
            if status == "converted":
                data["converted_at"] = datetime.now().isoformat()
            
            result = self.client.table("leads").update(data).eq("id", lead_id).execute()
            
            if result.data:
                return {"success": True, "lead": result.data[0]}
            return {"success": False, "error": "Lead tidak ditemukan"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==========================================
    # ORDER OPERATIONS
    # ==========================================
    
    def create_order(self, data: Dict) -> Dict:
        """Create new order"""
        if self._fallback_mode:
            return {"success": False, "error": "Database tidak tersedia"}
        
        try:
            # Generate order code
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            import random, string
            suffix = ''.join(random.choices(string.digits, k=4))
            order_code = f"ORD-{timestamp}-{suffix}"
            
            data["order_code"] = order_code
            
            result = self.client.table("orders").insert(data).execute()
            
            if result.data:
                return {"success": True, "order": result.data[0], "order_code": order_code}
            return {"success": False, "error": "Gagal membuat order"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_orders(self, user_id: str = None, status: str = None, limit: int = 100) -> List[Dict]:
        """Get orders"""
        if self._fallback_mode:
            return []
        
        try:
            query = self.client.table("orders").select("*")
            
            if user_id:
                query = query.eq("user_id", user_id)
            if status:
                query = query.eq("status", status)
            
            result = query.order("created_at", desc=True).limit(limit).execute()
            return result.data or []
            
        except:
            return []
    
    # ==========================================
    # USER STATS OPERATIONS
    # ==========================================
    
    def increment_user_stat(self, user_id: str, stat_name: str, increment: int = 1):
        """Increment user daily stat"""
        if self._fallback_mode:
            return
        
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Try to get existing stat
            result = self.client.table("user_stats").select("*").eq("user_id", user_id).eq("date", today).execute()
            
            if result.data:
                # Update existing
                current = result.data[0].get(stat_name, 0)
                self.client.table("user_stats").update({
                    stat_name: current + increment
                }).eq("id", result.data[0]["id"]).execute()
            else:
                # Create new
                self.client.table("user_stats").insert({
                    "user_id": user_id,
                    "date": today,
                    stat_name: increment
                }).execute()
                
        except Exception as e:
            print(f"Error incrementing stat: {e}")
    
    def get_user_daily_stats(self, user_id: str) -> Dict:
        """Get user's stats for today"""
        if self._fallback_mode:
            return {"ai_chat_count": 0}
        
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            result = self.client.table("user_stats").select("*").eq("user_id", user_id).eq("date", today).execute()
            
            if result.data:
                return result.data[0]
            return {"ai_chat_count": 0, "scenarios_created": 0, "plans_saved": 0}
            
        except:
            return {"ai_chat_count": 0}
    
    # ==========================================
    # AUDIT LOG
    # ==========================================
    
    def log_action(self, user_id: str, action: str, target_type: str = None, 
                   target_id: str = None, old_value: Dict = None, new_value: Dict = None):
        """Log audit action"""
        if self._fallback_mode:
            return
        
        try:
            self.client.table("audit_logs").insert({
                "user_id": user_id,
                "action": action,
                "target_type": target_type,
                "target_id": target_id,
                "old_value": old_value,
                "new_value": new_value
            }).execute()
        except:
            pass
    
    def get_audit_logs(self, user_id: str = None, action: str = None, limit: int = 100) -> List[Dict]:
        """Get audit logs"""
        if self._fallback_mode:
            return []
        
        try:
            query = self.client.table("audit_logs").select("*")
            
            if user_id:
                query = query.eq("user_id", user_id)
            if action:
                query = query.eq("action", action)
            
            result = query.order("created_at", desc=True).limit(limit).execute()
            return result.data or []
            
        except:
            return []
    
    # ==========================================
    # FALLBACK METHODS (In-memory storage)
    # ==========================================
    
    def _fallback_create_user(self, username: str, email: str, password: str, 
                              name: str, phone: str, role: str) -> Dict:
        """Fallback user creation using session state"""
        if "users_db" not in st.session_state:
            st.session_state.users_db = {}
        
        if username in st.session_state.users_db:
            return {"success": False, "error": "Username sudah digunakan"}
        
        for user in st.session_state.users_db.values():
            if user.get("email") == email:
                return {"success": False, "error": "Email sudah terdaftar"}
        
        import uuid
        user_id = str(uuid.uuid4())
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        user = {
            "id": user_id,
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "phone": phone,
            "role": role,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "last_login": None
        }
        
        st.session_state.users_db[username] = user
        return {"success": True, "user": user, "message": "Registrasi berhasil!"}
    
    def _fallback_get_user(self, username: str) -> Optional[Dict]:
        """Fallback get user"""
        if "users_db" not in st.session_state:
            # Add default superadmin
            st.session_state.users_db = {
                "superadmin": {
                    "id": "superadmin-001",
                    "username": "superadmin",
                    "email": "sopian.hadianto@gmail.com",
                    "password_hash": hashlib.sha256("Admin@123".encode()).hexdigest(),
                    "name": "MS Hadianto",
                    "phone": "628159658833",
                    "role": "superadmin",
                    "status": "active",
                    "created_at": "2025-11-26T00:00:00",
                    "last_login": None
                }
            }
        
        return st.session_state.users_db.get(username)
    
    def _fallback_get_all_users(self) -> List[Dict]:
        """Fallback get all users"""
        if "users_db" not in st.session_state:
            self._fallback_get_user("superadmin")
        return list(st.session_state.users_db.values())
    
    def _fallback_get_stats(self) -> Dict:
        """Fallback get stats"""
        users = self._fallback_get_all_users()
        stats = {
            "total": len(users),
            "by_role": {},
            "by_status": {"active": 0, "inactive": 0},
            "new_today": 0,
            "new_this_month": 0
        }
        
        for user in users:
            role = user.get("role", "free")
            stats["by_role"][role] = stats["by_role"].get(role, 0) + 1
            stats["by_status"][user.get("status", "active")] += 1
        
        return stats


# ============================================
# GLOBAL DATABASE INSTANCE
# ============================================

def get_db() -> SupabaseDB:
    """Get database instance"""
    if "db" not in st.session_state:
        st.session_state.db = SupabaseDB()
    return st.session_state.db


# ============================================
# SETUP INSTRUCTIONS
# ============================================

def render_supabase_setup():
    """Render Supabase setup instructions"""
    st.markdown("## 🗄️ Supabase Database Setup")
    
    db = get_db()
    
    if db.is_connected:
        st.success("✅ Supabase Connected!")
    else:
        st.warning("⚠️ Supabase tidak terhubung. Menggunakan fallback mode (in-memory).")
        
        st.markdown("""
        ### 📋 Setup Instructions
        
        1. **Buat akun Supabase** di https://supabase.com
        
        2. **Buat project baru**
        
        3. **Jalankan SQL schema** di SQL Editor:
        """)
        
        with st.expander("📄 Lihat SQL Schema"):
            st.code(SCHEMA_SQL, language="sql")
        
        st.markdown("""
        4. **Tambahkan credentials** ke Streamlit secrets atau environment:
        
        **Streamlit Cloud** (`.streamlit/secrets.toml`):
        ```toml
        SUPABASE_URL = "https://your-project.supabase.co"
        SUPABASE_KEY = "your-anon-key"
        SUPABASE_SERVICE_KEY = "your-service-role-key"
        ```
        
        **Environment Variables**:
        ```bash
        export SUPABASE_URL="https://your-project.supabase.co"
        export SUPABASE_KEY="your-anon-key"
        export SUPABASE_SERVICE_KEY="your-service-role-key"
        ```
        
        5. **Restart aplikasi**
        """)
        
        st.markdown("---")
        
        st.markdown("### 🔑 Get API Keys")
        st.markdown("""
        1. Buka Supabase Dashboard → Settings → API
        2. Copy **URL** (Project URL)
        3. Copy **anon public** key
        4. Copy **service_role** key (untuk admin operations)
        """)
