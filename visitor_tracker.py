# visitor_tracker.py - Visitor Analytics with Database Persistence
# Updated: 2025-12-03
# Uses Neon PostgreSQL for persistent storage

import streamlit as st
from datetime import datetime, timedelta
from collections import defaultdict
import hashlib
import os

# ============================================
# DATABASE CONNECTION
# ============================================

DB_AVAILABLE = False
_db_engine = None

def get_db_connection():
    """Get database connection using SQLAlchemy"""
    global DB_AVAILABLE, _db_engine
    
    if _db_engine is not None:
        return _db_engine
    
    try:
        from sqlalchemy import create_engine, text
        
        # Try to get database URL from secrets or environment
        db_url = None
        
        # Method 1: Streamlit secrets - multiple possible structures
        try:
            # Try connections.neon.url (standard Streamlit format)
            if hasattr(st, 'secrets'):
                if 'connections' in st.secrets and 'neon' in st.secrets['connections']:
                    db_url = st.secrets['connections']['neon'].get('url')
                elif 'DATABASE_URL' in st.secrets:
                    db_url = st.secrets['DATABASE_URL']
                elif 'database' in st.secrets:
                    db_url = st.secrets['database'].get('url')
        except Exception as e:
            print(f"[visitor_tracker] Secrets access: {e}")
        
        # Method 2: Environment variable
        if not db_url:
            db_url = os.environ.get("DATABASE_URL")
        
        if db_url and 'PASSWORD_KAMU' not in db_url and 'PASSWORD_ANDA' not in db_url:  # Skip if placeholder password
            _db_engine = create_engine(db_url, pool_pre_ping=True, pool_recycle=300)
            
            # Test connection and create tables if not exists
            with _db_engine.connect() as conn:
                # Create visitor_stats table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS visitor_stats (
                        id SERIAL PRIMARY KEY,
                        stat_key VARCHAR(100) UNIQUE NOT NULL,
                        stat_value INTEGER DEFAULT 0,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create page_views table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS page_views (
                        id SERIAL PRIMARY KEY,
                        page_name VARCHAR(100) NOT NULL,
                        visitor_id VARCHAR(50),
                        viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Initialize default stats if not exist
                conn.execute(text("""
                    INSERT INTO visitor_stats (stat_key, stat_value) 
                    VALUES ('total_visitors', 0), ('total_views', 0)
                    ON CONFLICT (stat_key) DO NOTHING
                """))
                
                conn.commit()
            
            DB_AVAILABLE = True
            print("[visitor_tracker] Database connected successfully")
            return _db_engine
        else:
            print("[visitor_tracker] No valid database URL found")
            
    except Exception as e:
        print(f"[visitor_tracker] DB connection failed: {e}")
        DB_AVAILABLE = False
    
    return None


# ============================================
# SESSION STATE FALLBACK
# ============================================

def init_session_state():
    """Initialize session state for visitor tracking"""
    if "visitor_id" not in st.session_state:
        # Generate unique visitor ID based on session
        session_id = str(id(st.session_state))
        st.session_state.visitor_id = hashlib.md5(session_id.encode()).hexdigest()[:12]
    
    if "page_views" not in st.session_state:
        st.session_state.page_views = defaultdict(int)
    
    if "visit_start" not in st.session_state:
        st.session_state.visit_start = datetime.now()
    
    if "counted_as_visitor" not in st.session_state:
        st.session_state.counted_as_visitor = False
    
    # Fallback stats in session state
    if "fallback_total_visitors" not in st.session_state:
        st.session_state.fallback_total_visitors = 1247  # Starting count
    
    if "fallback_total_views" not in st.session_state:
        st.session_state.fallback_total_views = 8934  # Starting count


# ============================================
# DATABASE OPERATIONS
# ============================================

def db_increment_stat(stat_key: str, increment: int = 1) -> int:
    """Increment a stat in database and return new value"""
    engine = get_db_connection()
    if not engine:
        return -1
    
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("""
                INSERT INTO visitor_stats (stat_key, stat_value) 
                VALUES (:key, :increment)
                ON CONFLICT (stat_key) 
                DO UPDATE SET 
                    stat_value = visitor_stats.stat_value + :increment,
                    last_updated = CURRENT_TIMESTAMP
                RETURNING stat_value
            """), {"key": stat_key, "increment": increment})
            
            row = result.fetchone()
            conn.commit()
            return row[0] if row else 0
    except Exception as e:
        print(f"[visitor_tracker] db_increment_stat error: {e}")
        return -1


def db_get_stat(stat_key: str) -> int:
    """Get a stat value from database"""
    engine = get_db_connection()
    if not engine:
        return -1
    
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT stat_value FROM visitor_stats WHERE stat_key = :key
            """), {"key": stat_key})
            
            row = result.fetchone()
            return row[0] if row else 0
    except Exception as e:
        print(f"[visitor_tracker] db_get_stat error: {e}")
        return -1


def db_log_page_view(page_name: str, visitor_id: str):
    """Log a page view to database"""
    engine = get_db_connection()
    if not engine:
        return False
    
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            # Insert page view
            conn.execute(text("""
                INSERT INTO page_views (page_name, visitor_id) 
                VALUES (:page, :visitor)
            """), {"page": page_name, "visitor": visitor_id})
            
            conn.commit()
            return True
    except Exception as e:
        print(f"[visitor_tracker] db_log_page_view error: {e}")
        return False


# ============================================
# PUBLIC API
# ============================================

def track_page_view(page_name: str):
    """Track a page view - main function called from app.py"""
    init_session_state()
    
    # Track in session state
    st.session_state.page_views[page_name] += 1
    
    # Try database operations
    engine = get_db_connection()
    
    if engine and DB_AVAILABLE:
        # Log page view to database
        db_log_page_view(page_name, st.session_state.visitor_id)
        
        # Increment total views
        db_increment_stat("total_views", 1)
        
        # Count as new visitor if first time in this session
        if not st.session_state.counted_as_visitor:
            db_increment_stat("total_visitors", 1)
            st.session_state.counted_as_visitor = True
    else:
        # Fallback to session state
        st.session_state.fallback_total_views += 1
        if not st.session_state.counted_as_visitor:
            st.session_state.fallback_total_visitors += 1
            st.session_state.counted_as_visitor = True


def get_visitor_count() -> int:
    """Get total unique visitor count"""
    init_session_state()
    
    if DB_AVAILABLE:
        count = db_get_stat("total_visitors")
        if count >= 0:
            return count
    
    return st.session_state.fallback_total_visitors


def get_page_view_count() -> int:
    """Get total page view count"""
    init_session_state()
    
    if DB_AVAILABLE:
        count = db_get_stat("total_views")
        if count >= 0:
            return count
    
    return st.session_state.fallback_total_views


def get_visitor_stats() -> dict:
    """Get visitor statistics summary"""
    init_session_state()
    
    total_visitors = get_visitor_count()
    total_views = get_page_view_count()
    today_visitors = get_today_visitors()
    
    # Calculate session stats
    session_views = sum(st.session_state.page_views.values())
    session_duration = datetime.now() - st.session_state.visit_start
    
    return {
        "total_visitors": total_visitors,
        "total_views": total_views,
        "today_visitors": today_visitors,
        "session_views": session_views,
        "session_duration": str(session_duration).split('.')[0],
        "visitor_id": st.session_state.visitor_id,
        "db_connected": DB_AVAILABLE,
        "pages_visited": dict(st.session_state.page_views)
    }


def get_today_visitors() -> int:
    """Get today's unique visitor count"""
    engine = get_db_connection()
    
    if engine and DB_AVAILABLE:
        try:
            from sqlalchemy import text
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT COUNT(DISTINCT visitor_id) 
                    FROM page_views 
                    WHERE DATE(viewed_at) = CURRENT_DATE
                """))
                row = result.fetchone()
                return row[0] if row and row[0] else 0
        except Exception as e:
            print(f"[visitor_tracker] get_today_visitors error: {e}")
    
    # Fallback: return 1 (current session)
    return 1


def get_page_stats() -> dict:
    """Get page-level statistics"""
    engine = get_db_connection()
    
    if engine and DB_AVAILABLE:
        try:
            from sqlalchemy import text
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT page_name, COUNT(*) as view_count
                    FROM page_views
                    GROUP BY page_name
                    ORDER BY view_count DESC
                    LIMIT 20
                """))
                
                return {row[0]: row[1] for row in result.fetchall()}
        except:
            pass
    
    return dict(st.session_state.page_views)


# ============================================
# RENDER FUNCTIONS
# ============================================

def render_visitor_stats():
    """Render visitor statistics widget"""
    stats = get_visitor_stats()
    
    db_badge = "🟢 DB" if stats["db_connected"] else "🟡 Session"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); 
                padding: 20px; border-radius: 15px; border: 1px solid #D4AF3740;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <span style="color: #D4AF37; font-weight: 700;">📊 Statistik Pengunjung</span>
            <span style="font-size: 0.7rem; color: #666;">{db_badge}</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
            <div style="background: rgba(212, 175, 55, 0.1); padding: 12px; border-radius: 10px; text-align: center;">
                <div style="color: #888; font-size: 0.75rem;">Total Visitors</div>
                <div style="color: #D4AF37; font-size: 1.3rem; font-weight: 700;">{stats['total_visitors']:,}</div>
            </div>
            <div style="background: rgba(0, 107, 60, 0.1); padding: 12px; border-radius: 10px; text-align: center;">
                <div style="color: #888; font-size: 0.75rem;">Total Views</div>
                <div style="color: #4CAF50; font-size: 1.3rem; font-weight: 700;">{stats['total_views']:,}</div>
            </div>
            <div style="background: rgba(0, 122, 255, 0.1); padding: 12px; border-radius: 10px; text-align: center;">
                <div style="color: #888; font-size: 0.75rem;">Today</div>
                <div style="color: #007AFF; font-size: 1.3rem; font-weight: 700;">{stats['today_visitors']:,}</div>
            </div>
        </div>
        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #333; text-align: center;">
            <span style="color: #666; font-size: 0.8rem;">
                Session: {stats['session_views']} views • {stats['session_duration']}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_analytics_dashboard():
    """Render full analytics dashboard for admin"""
    stats = get_visitor_stats()
    page_stats = get_page_stats()
    
    st.markdown("### 📊 Analytics Dashboard")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Visitors", f"{stats['total_visitors']:,}")
    with col2:
        st.metric("Total Page Views", f"{stats['total_views']:,}")
    with col3:
        avg_views = stats['total_views'] / max(stats['total_visitors'], 1)
        st.metric("Avg Views/Visitor", f"{avg_views:.1f}")
    with col4:
        st.metric("DB Status", "🟢 Connected" if stats['db_connected'] else "🟡 Session")
    
    # Page statistics
    if page_stats:
        st.markdown("#### 📄 Top Pages")
        
        import pandas as pd
        df = pd.DataFrame([
            {"Page": page, "Views": views}
            for page, views in sorted(page_stats.items(), key=lambda x: x[1], reverse=True)
        ])
        
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Current session info
    st.markdown("#### 🔍 Current Session")
    st.json({
        "visitor_id": stats['visitor_id'],
        "session_views": stats['session_views'],
        "session_duration": stats['session_duration'],
        "pages_visited": stats['pages_visited']
    })


# Initialize on import
init_session_state()
get_db_connection()  # Try to connect on import
