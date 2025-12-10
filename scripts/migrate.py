#!/usr/bin/env python3
"""
LABBAIK AI v6.0 - Database Migration Script
===========================================
Run database migrations and schema updates.
"""

import os
import sys
import logging
import argparse
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import get_settings
from services.database.repository import get_db, DatabaseConnection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# MIGRATION DEFINITIONS
# =============================================================================

MIGRATIONS = [
    {
        "version": "001",
        "name": "initial_schema",
        "description": "Create initial database schema",
        "sql": """
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            email VARCHAR(255) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20),
            password_hash VARCHAR(255),
            role VARCHAR(20) DEFAULT 'user',
            subscription_tier VARCHAR(20) DEFAULT 'free',
            avatar_url TEXT,
            is_verified BOOLEAN DEFAULT FALSE,
            is_active BOOLEAN DEFAULT TRUE,
            last_login TIMESTAMP WITH TIME ZONE,
            preferences JSONB DEFAULT '{}',
            points INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            badges JSONB DEFAULT '[]',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
        """
    },
    {
        "version": "002",
        "name": "conversations_table",
        "description": "Create conversations table",
        "sql": """
        CREATE TABLE IF NOT EXISTS conversations (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            title VARCHAR(255),
            messages JSONB DEFAULT '[]',
            metadata JSONB DEFAULT '{}',
            is_archived BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_id);
        CREATE INDEX IF NOT EXISTS idx_conversations_archived ON conversations(is_archived);
        """
    },
    {
        "version": "003",
        "name": "bookings_table",
        "description": "Create bookings table",
        "sql": """
        CREATE TABLE IF NOT EXISTS bookings (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            booking_number VARCHAR(20) UNIQUE NOT NULL,
            user_id UUID REFERENCES users(id) ON DELETE SET NULL,
            partner_id UUID,
            status VARCHAR(20) DEFAULT 'draft',
            package_type VARCHAR(20),
            departure_city VARCHAR(100),
            departure_date DATE,
            return_date DATE,
            travelers JSONB DEFAULT '[]',
            hotel_makkah JSONB,
            hotel_madinah JSONB,
            outbound_flight JSONB,
            return_flight JSONB,
            base_price DECIMAL(15, 2) DEFAULT 0,
            taxes DECIMAL(15, 2) DEFAULT 0,
            fees DECIMAL(15, 2) DEFAULT 0,
            discount DECIMAL(15, 2) DEFAULT 0,
            total_price DECIMAL(15, 2) DEFAULT 0,
            currency VARCHAR(3) DEFAULT 'IDR',
            paid_amount DECIMAL(15, 2) DEFAULT 0,
            payment_status VARCHAR(20) DEFAULT 'unpaid',
            notes TEXT,
            confirmed_at TIMESTAMP WITH TIME ZONE,
            cancelled_at TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_bookings_user ON bookings(user_id);
        CREATE INDEX IF NOT EXISTS idx_bookings_status ON bookings(status);
        CREATE INDEX IF NOT EXISTS idx_bookings_number ON bookings(booking_number);
        """
    },
    {
        "version": "004",
        "name": "partners_table",
        "description": "Create partners table",
        "sql": """
        CREATE TABLE IF NOT EXISTS partners (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name VARCHAR(100) NOT NULL,
            type VARCHAR(50) NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            email VARCHAR(255) UNIQUE NOT NULL,
            phone VARCHAR(20),
            website VARCHAR(255),
            company_name VARCHAR(200),
            license_number VARCHAR(100),
            address TEXT,
            city VARCHAR(100),
            commission_rate DECIMAL(5, 4) DEFAULT 0.1,
            total_bookings INTEGER DEFAULT 0,
            total_revenue DECIMAL(15, 2) DEFAULT 0,
            rating DECIMAL(3, 2) DEFAULT 0,
            review_count INTEGER DEFAULT 0,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_partners_type ON partners(type);
        CREATE INDEX IF NOT EXISTS idx_partners_status ON partners(status);
        """
    },
    {
        "version": "005",
        "name": "subscriptions_notifications",
        "description": "Create subscriptions and notifications tables",
        "sql": """
        CREATE TABLE IF NOT EXISTS subscriptions (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            plan_id VARCHAR(50) NOT NULL,
            tier VARCHAR(20) NOT NULL,
            status VARCHAR(20) DEFAULT 'active',
            billing_cycle VARCHAR(20) DEFAULT 'monthly',
            price DECIMAL(15, 2),
            currency VARCHAR(3) DEFAULT 'IDR',
            starts_at TIMESTAMP WITH TIME ZONE NOT NULL,
            expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
            auto_renew BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS notifications (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            type VARCHAR(50) NOT NULL,
            title VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            link VARCHAR(500),
            is_read BOOLEAN DEFAULT FALSE,
            read_at TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_subscriptions_user ON subscriptions(user_id);
        CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
        CREATE INDEX IF NOT EXISTS idx_notifications_read ON notifications(is_read);
        """
    },
    {
        "version": "006",
        "name": "sessions_audit",
        "description": "Create user sessions and audit log tables",
        "sql": """
        CREATE TABLE IF NOT EXISTS user_sessions (
            session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            access_token TEXT NOT NULL,
            refresh_token TEXT,
            expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
            ip_address VARCHAR(45),
            user_agent TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS audit_logs (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID REFERENCES users(id) ON DELETE SET NULL,
            action VARCHAR(100) NOT NULL,
            resource_type VARCHAR(100),
            resource_id UUID,
            old_value JSONB,
            new_value JSONB,
            ip_address VARCHAR(45),
            user_agent TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions(user_id);
        CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id);
        CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_logs(action);
        """
    },
    {
        "version": "007",
        "name": "triggers",
        "description": "Create update triggers",
        "sql": """
        -- Function to update updated_at timestamp
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        
        -- Apply triggers (drop if exists first)
        DROP TRIGGER IF EXISTS update_users_updated_at ON users;
        CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        
        DROP TRIGGER IF EXISTS update_conversations_updated_at ON conversations;
        CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON conversations
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        
        DROP TRIGGER IF EXISTS update_bookings_updated_at ON bookings;
        CREATE TRIGGER update_bookings_updated_at BEFORE UPDATE ON bookings
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        """
    },
]


# =============================================================================
# MIGRATION TRACKING
# =============================================================================

MIGRATION_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""


def ensure_migration_table(db: DatabaseConnection):
    """Ensure migration tracking table exists."""
    db.execute(MIGRATION_TABLE_SQL)
    logger.info("Migration tracking table ready")


def get_applied_migrations(db: DatabaseConnection) -> set:
    """Get set of applied migration versions."""
    try:
        rows = db.fetch_all("SELECT version FROM schema_migrations")
        return {row["version"] for row in rows}
    except Exception:
        return set()


def record_migration(db: DatabaseConnection, version: str, name: str):
    """Record a migration as applied."""
    db.execute(
        "INSERT INTO schema_migrations (version, name) VALUES (%s, %s)",
        (version, name)
    )


# =============================================================================
# MIGRATION RUNNER
# =============================================================================

def run_migrations(db: DatabaseConnection, target_version: str = None):
    """
    Run pending migrations.
    
    Args:
        db: Database connection
        target_version: Optional specific version to migrate to
    """
    # Enable UUID extension
    try:
        db.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    except Exception as e:
        logger.warning(f"Could not create uuid-ossp extension: {e}")
    
    ensure_migration_table(db)
    applied = get_applied_migrations(db)
    
    pending = [m for m in MIGRATIONS if m["version"] not in applied]
    
    if target_version:
        pending = [m for m in pending if m["version"] <= target_version]
    
    if not pending:
        logger.info("No pending migrations")
        return
    
    logger.info(f"Found {len(pending)} pending migrations")
    
    for migration in pending:
        version = migration["version"]
        name = migration["name"]
        description = migration["description"]
        
        logger.info(f"Running migration {version}: {name}")
        logger.info(f"  Description: {description}")
        
        try:
            db.execute(migration["sql"])
            record_migration(db, version, name)
            logger.info(f"  ✓ Migration {version} applied successfully")
        except Exception as e:
            logger.error(f"  ✗ Migration {version} failed: {e}")
            raise


def rollback_migration(db: DatabaseConnection, version: str):
    """
    Rollback a specific migration (if rollback SQL defined).
    
    Args:
        db: Database connection
        version: Version to rollback
    """
    migration = next((m for m in MIGRATIONS if m["version"] == version), None)
    
    if not migration:
        logger.error(f"Migration {version} not found")
        return
    
    if "rollback_sql" not in migration:
        logger.error(f"Migration {version} has no rollback defined")
        return
    
    logger.info(f"Rolling back migration {version}")
    
    try:
        db.execute(migration["rollback_sql"])
        db.execute(
            "DELETE FROM schema_migrations WHERE version = %s",
            (version,)
        )
        logger.info(f"  ✓ Rollback of {version} successful")
    except Exception as e:
        logger.error(f"  ✗ Rollback failed: {e}")
        raise


def show_status(db: DatabaseConnection):
    """Show migration status."""
    ensure_migration_table(db)
    applied = get_applied_migrations(db)
    
    print("\n=== Migration Status ===\n")
    
    for migration in MIGRATIONS:
        version = migration["version"]
        name = migration["name"]
        status = "✓ Applied" if version in applied else "○ Pending"
        print(f"  {version}: {name} [{status}]")
    
    print(f"\n  Total: {len(MIGRATIONS)} migrations")
    print(f"  Applied: {len(applied)}")
    print(f"  Pending: {len(MIGRATIONS) - len(applied)}\n")


# =============================================================================
# CLI
# =============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Database migration tool")
    parser.add_argument(
        "command",
        choices=["migrate", "rollback", "status", "init"],
        help="Command to run"
    )
    parser.add_argument(
        "--version", "-v",
        help="Target version for migrate/rollback"
    )
    parser.add_argument(
        "--database-url",
        help="Database URL (overrides settings)"
    )
    
    args = parser.parse_args()
    
    # Get database URL
    if args.database_url:
        db_url = args.database_url
    else:
        settings = get_settings()
        db_url = settings.database.url
    
    if not db_url:
        print("Error: No database URL configured")
        print("Set DATABASE_URL environment variable or use --database-url")
        sys.exit(1)
    
    # Connect to database
    db = get_db()
    if not db.initialize(db_url):
        print("Error: Failed to connect to database")
        sys.exit(1)
    
    try:
        if args.command == "migrate":
            run_migrations(db, args.version)
        elif args.command == "rollback":
            if not args.version:
                print("Error: --version required for rollback")
                sys.exit(1)
            rollback_migration(db, args.version)
        elif args.command == "status":
            show_status(db)
        elif args.command == "init":
            run_migrations(db)
            print("\nDatabase initialized successfully!")
    finally:
        db.close()


if __name__ == "__main__":
    main()
