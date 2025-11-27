"""
🗄️ Supabase Database Integration
=================================
Database integration for LABBAIK - Umrah Planner AI

Features:
- User authentication & management
- Subscription tracking
- Lead management
- Order tracking
- Analytics data

Developer: MS Hadianto
Version: 3.0.0
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
    Client = Any
    print("Warning: supabase-py not installed. Using fallback mode.")

# ============================================
# DEMO USER CREDENTIALS (for fallback mode)
# ============================================
# These are the demo accounts available when Supabase is not connected

DEMO_CREDENTIALS = {
    "superadmin": {
        "password": "SuperLabbaik25",
        "role": "superadmin",
        "name": "MS Hadianto",
        "email": "sopian.hadianto@gmail.com"
    },
    "admin": {
        "password": "AdminLabbaik25",
        "role": "admin", 
        "name": "Admin LABBAIK",
        "email": "admin@labbaik.ai"
    },
    "demo": {
        "password": "DemoLabbaik25",
        "role": "free",
        "name": "Demo User",
        "email": "demo@labbaik.ai"
    }
}

# ============================================
# SUPABASE CONFIGURATION
# ============================================

def get_supabase_config() -> Dict[str, str]:
    """Get Supabase configuration from environment or secrets"""
    if hasattr(st, 'secrets'):
        try:
            return {
                "url": st.secrets.get("SUPABASE_URL", ""),
                "key": st.secrets.get("SUPABASE_KEY", ""),
                "service_key": st.secrets.get("SUPABASE_SERVICE_KEY", "")
            }
        except:
            pass
    
    return {
        "url": os.getenv("SUPABASE_URL", ""),
        "key": os.getenv("SUPABASE_KEY", ""),
        "service_key": os.getenv("SUPABASE_SERVICE_KEY", "")
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


# ============================================
# DATABASE HELPER CLASS
# ============================================

class SupabaseDB:
    """Supabase Database Helper Class"""
    
    def __init__(self):
        self.client = get_supabase_client()
        self._fallback_mode = self.client is None
        
        # Always initialize demo users on startup
        if self._fallback_mode:
            self._init_demo_users()
    
    @property
    def is_connected(self) -> bool:
        return self.client is not None
    
    def _init_demo_users(self):
        """Initialize demo users in session state"""
        if "users_db" not in st.session_state:
            st.session_state.users_db = {}
        
        # Always ensure demo users exist with correct credentials
        for username, creds in DEMO_CREDENTIALS.items():
            st.session_state.users_db[username] = {
                "id": f"{username}-001",
                "username": username,
                "email": creds["email"],
                "password_hash": hashlib.sha256(creds["password"].encode()).hexdigest(),
                "name": creds["name"],
                "phone": "628159658833" if username == "superadmin" else "",
                "role": creds["role"],
                "status": "active",
                "created_at": "2025-11-27T00:00:00",
                "last_login": None
            }
    
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
    
    def verify_password(self, username: str, password: str) -> bool:
        """Verify user password"""
        user = self.get_user_by_username(username)
        if not user:
            return False
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return user.get("password_hash") == password_hash
    
    def update_last_login(self, user_id: str):
        """Update last login timestamp"""
        if self._fallback_mode:
            # Update in session state
            if "users_db" in st.session_state:
                for user in st.session_state.users_db.values():
                    if user.get("id") == user_id:
                        user["last_login"] = datetime.now().isoformat()
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
        except:
            return []
    
    def get_user_stats_summary(self) -> Dict:
        """Get user statistics summary"""
        if self._fallback_mode:
            return self._fallback_get_stats()
        
        try:
            all_users = self.get_all_users()
            stats = {
                "total": len(all_users),
                "by_role": {},
                "by_status": {"active": 0, "inactive": 0},
                "new_today": 0,
                "new_this_month": 0
            }
            
            for user in all_users:
                role = user.get("role", "free")
                stats["by_role"][role] = stats["by_role"].get(role, 0) + 1
                stats["by_status"][user.get("status", "active")] += 1
            
            return stats
        except:
            return {"total": 0, "by_role": {}, "by_status": {}}
    
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
    
    # ==========================================
    # FALLBACK METHODS (In-memory storage)
    # ==========================================
    
    def _fallback_create_user(self, username: str, email: str, password: str, 
                              name: str, phone: str, role: str) -> Dict:
        """Fallback user creation using session state"""
        self._init_demo_users()  # Ensure demo users exist
        
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
        self._init_demo_users()  # Ensure demo users exist
        return st.session_state.users_db.get(username)
    
    def _fallback_get_all_users(self) -> List[Dict]:
        """Fallback get all users"""
        self._init_demo_users()
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
    st.markdown("## 🗄️ Database Status")
    
    db = get_db()
    
    if db.is_connected:
        st.success("✅ Supabase Connected!")
    else:
        st.warning("⚠️ Menggunakan Demo Mode (in-memory)")
        
        st.markdown("### 🔑 Demo Accounts")
        st.markdown("""
        | Username | Password | Role |
        |----------|----------|------|
        | `demo` | `DemoLabbaik25` | Free User |
        | `admin` | `AdminLabbaik25` | Admin |
        | `superadmin` | `SuperLabbaik25` | Super Admin |
        """)
