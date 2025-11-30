"""
================================================================================
LABBAIK - Visitor Tracking Module
================================================================================

Real-time visitor tracking using SQLite database for persistence.
Tracks unique visitors and total page views.

Author: MS Hadianto
Date: November 30, 2025
================================================================================
"""

import sqlite3
import hashlib
import streamlit as st
from datetime import datetime
from pathlib import Path


class VisitorTracker:
    """Track visitors using SQLite database for persistence"""
    
    def __init__(self, db_path="data/visitors.db"):
        """Initialize visitor tracker with database"""
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database and create tables if not exist"""
        # Create data directory if not exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table for unique visitors
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS visitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                visitor_id TEXT UNIQUE NOT NULL,
                first_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                visit_count INTEGER DEFAULT 1
            )
        """)
        
        # Table for page views
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS page_views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                visitor_id TEXT NOT NULL,
                page_name TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table for daily statistics
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_stats (
                date DATE PRIMARY KEY,
                unique_visitors INTEGER DEFAULT 0,
                total_views INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _get_visitor_id(self):
        """Generate unique visitor ID based on session"""
        # Try to get from session state first
        if "visitor_id" in st.session_state:
            return st.session_state.visitor_id
        
        # Generate new visitor ID
        # Using session_id if available, otherwise create unique ID
        session_id = st.runtime.scriptrunner.get_script_run_ctx().session_id
        visitor_id = hashlib.md5(session_id.encode()).hexdigest()
        
        st.session_state.visitor_id = visitor_id
        return visitor_id
    
    def track_visit(self, page_name="Home"):
        """Track a visit to the application"""
        try:
            visitor_id = self._get_visitor_id()
            
            # Only track once per session
            if "visit_tracked" not in st.session_state:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Update or insert visitor
                cursor.execute("""
                    INSERT INTO visitors (visitor_id, visit_count)
                    VALUES (?, 1)
                    ON CONFLICT(visitor_id) DO UPDATE SET
                        last_visit = CURRENT_TIMESTAMP,
                        visit_count = visit_count + 1
                """, (visitor_id,))
                
                # Record page view
                cursor.execute("""
                    INSERT INTO page_views (visitor_id, page_name)
                    VALUES (?, ?)
                """, (visitor_id, page_name))
                
                # Update daily stats
                today = datetime.now().date()
                cursor.execute("""
                    INSERT INTO daily_stats (date, unique_visitors, total_views)
                    VALUES (?, 1, 1)
                    ON CONFLICT(date) DO UPDATE SET
                        total_views = total_views + 1,
                        updated_at = CURRENT_TIMESTAMP
                """, (today,))
                
                conn.commit()
                conn.close()
                
                st.session_state.visit_tracked = True
                
        except Exception as e:
            # Silently fail - don't break app if tracking fails
            print(f"Visitor tracking error: {e}")
    
    def get_total_visitors(self):
        """Get total unique visitors count"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(DISTINCT visitor_id) FROM visitors")
            count = cursor.fetchone()[0]
            
            conn.close()
            return count
        except:
            return 0
    
    def get_total_views(self):
        """Get total page views count"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM page_views")
            count = cursor.fetchone()[0]
            
            conn.close()
            return count
        except:
            return 0
    
    def get_today_visitors(self):
        """Get today's unique visitors"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = datetime.now().date()
            cursor.execute("""
                SELECT COUNT(DISTINCT visitor_id)
                FROM visitors
                WHERE DATE(last_visit) = ?
            """, (today,))
            count = cursor.fetchone()[0]
            
            conn.close()
            return count
        except:
            return 0
    
    def get_today_views(self):
        """Get today's total page views"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = datetime.now().date()
            cursor.execute("""
                SELECT COUNT(*)
                FROM page_views
                WHERE DATE(timestamp) = ?
            """, (today,))
            count = cursor.fetchone()[0]
            
            conn.close()
            return count
        except:
            return 0
    
    def get_stats(self):
        """Get comprehensive visitor statistics"""
        return {
            "total_visitors": self.get_total_visitors(),
            "total_views": self.get_total_views(),
            "today_visitors": self.get_today_visitors(),
            "today_views": self.get_today_views(),
        }
    
    def get_daily_stats(self, days=7):
        """Get daily statistics for last N days"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT date, unique_visitors, total_views
                FROM daily_stats
                ORDER BY date DESC
                LIMIT ?
            """, (days,))
            
            stats = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "date": row[0],
                    "visitors": row[1],
                    "views": row[2]
                }
                for row in stats
            ]
        except:
            return []
    
    def get_popular_pages(self, limit=10):
        """Get most popular pages"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT page_name, COUNT(*) as views
                FROM page_views
                GROUP BY page_name
                ORDER BY views DESC
                LIMIT ?
            """, (limit,))
            
            pages = cursor.fetchall()
            conn.close()
            
            return [
                {"page": row[0], "views": row[1]}
                for row in pages
            ]
        except:
            return []


# Global tracker instance
_tracker = None

def get_tracker():
    """Get global visitor tracker instance"""
    global _tracker
    if _tracker is None:
        _tracker = VisitorTracker()
    return _tracker


def track_page_view(page_name="Home"):
    """Convenience function to track page view"""
    tracker = get_tracker()
    tracker.track_visit(page_name)


def get_visitor_count():
    """Get total unique visitors - REAL COUNT"""
    tracker = get_tracker()
    return tracker.get_total_visitors()


def get_page_view_count():
    """Get total page views - REAL COUNT"""
    tracker = get_tracker()
    return tracker.get_total_views()


def get_visitor_stats():
    """Get comprehensive visitor statistics"""
    tracker = get_tracker()
    return tracker.get_stats()


def render_visitor_stats():
    """Render visitor statistics widget"""
    stats = get_visitor_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "👥 Total Pengunjung",
            f"{stats['total_visitors']:,}",
            help="Total unique visitors sejak peluncuran"
        )
    
    with col2:
        st.metric(
            "📊 Total Views",
            f"{stats['total_views']:,}",
            help="Total page views sejak peluncuran"
        )
    
    with col3:
        st.metric(
            "🌟 Hari Ini (Visitors)",
            f"{stats['today_visitors']:,}",
            help="Unique visitors hari ini"
        )
    
    with col4:
        st.metric(
            "📈 Hari Ini (Views)",
            f"{stats['today_views']:,}",
            help="Page views hari ini"
        )


def render_analytics_dashboard():
    """Render full analytics dashboard (admin only)"""
    st.subheader("📊 Analytics Dashboard")
    
    tracker = get_tracker()
    stats = tracker.get_stats()
    
    # Overview
    st.markdown("### 📈 Overview")
    render_visitor_stats()
    
    st.markdown("---")
    
    # Daily trend
    st.markdown("### 📅 Trend 7 Hari Terakhir")
    daily_stats = tracker.get_daily_stats(days=7)
    
    if daily_stats:
        import pandas as pd
        import plotly.graph_objects as go
        
        df = pd.DataFrame(daily_stats)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['visitors'],
            name='Unique Visitors',
            mode='lines+markers',
            line=dict(color='#D4AF37', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['views'],
            name='Page Views',
            mode='lines+markers',
            line=dict(color='#006B3C', width=2)
        ))
        
        fig.update_layout(
            title="Visitor Trend",
            xaxis_title="Date",
            yaxis_title="Count",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Belum ada data untuk ditampilkan")
    
    st.markdown("---")
    
    # Popular pages
    st.markdown("### 🔥 Halaman Populer")
    popular_pages = tracker.get_popular_pages(limit=10)
    
    if popular_pages:
        import pandas as pd
        
        df = pd.DataFrame(popular_pages)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Belum ada data halaman")


if __name__ == "__main__":
    # Test the tracker
    tracker = VisitorTracker()
    tracker.track_visit("Test Page")
    stats = tracker.get_stats()
    print(f"Stats: {stats}")
