"""
LABBAIK AI v6.0 - Database Integration Tests
=============================================
Integration tests for database repositories.
"""

import pytest
from datetime import datetime, date, timedelta
from uuid import uuid4
from unittest.mock import Mock, patch, MagicMock

from services.database.repository import (
    DatabaseConnection,
    BaseRepository,
    UserRepository,
    ChatRepository,
    BookingRepository,
    get_db,
)
from data.models import (
    User,
    UserRole,
    SubscriptionTier,
    ChatConversation,
    MessageRole,
    Booking,
    BookingStatus,
    PackageType,
)


# =============================================================================
# DATABASE CONNECTION TESTS
# =============================================================================

class TestDatabaseConnection:
    """Tests for DatabaseConnection class."""
    
    def test_singleton_pattern(self):
        """Test that DatabaseConnection is a singleton."""
        db1 = get_db()
        db2 = get_db()
        
        assert db1 is db2
    
    def test_connection_not_initialized(self):
        """Test behavior when not initialized."""
        db = DatabaseConnection()
        db._pool = None
        
        # Should not raise, just return None
        with db.get_cursor() as cursor:
            assert cursor is None
    
    @pytest.mark.integration
    def test_initialize_with_valid_url(self, test_database_url):
        """Test initialization with valid database URL."""
        db = DatabaseConnection()
        
        result = db.initialize(test_database_url)
        
        assert result is True
        
        db.close()
    
    @pytest.mark.integration
    def test_execute_simple_query(self, test_database_url):
        """Test executing a simple query."""
        db = DatabaseConnection()
        db.initialize(test_database_url)
        
        try:
            result = db.fetch_one("SELECT 1 as value")
            assert result is not None
            assert result["value"] == 1
        finally:
            db.close()


# =============================================================================
# BASE REPOSITORY TESTS
# =============================================================================

class TestBaseRepository:
    """Tests for BaseRepository class."""
    
    @pytest.fixture
    def mock_db(self):
        """Create mock database connection."""
        db = Mock(spec=DatabaseConnection)
        db.execute = Mock(return_value=1)
        db.fetch_one = Mock(return_value={"id": "123", "name": "Test"})
        db.fetch_all = Mock(return_value=[
            {"id": "1", "name": "Test 1"},
            {"id": "2", "name": "Test 2"}
        ])
        return db
    
    @pytest.fixture
    def repository(self, mock_db):
        """Create repository with mock db."""
        repo = BaseRepository(mock_db, "test_table")
        return repo
    
    def test_find_by_id(self, repository, mock_db):
        """Test finding entity by ID."""
        result = repository.find_by_id("123")
        
        assert result is not None
        mock_db.fetch_one.assert_called_once()
    
    def test_find_all(self, repository, mock_db):
        """Test finding all entities."""
        results = repository.find_all()
        
        assert len(results) == 2
        mock_db.fetch_all.assert_called_once()
    
    def test_find_all_with_limit(self, repository, mock_db):
        """Test finding all with limit and offset."""
        repository.find_all(limit=10, offset=5)
        
        call_args = mock_db.fetch_all.call_args
        assert "LIMIT" in call_args[0][0]
        assert "OFFSET" in call_args[0][0]
    
    def test_find_by_conditions(self, repository, mock_db):
        """Test finding by conditions."""
        repository.find_by(status="active", role="admin")
        
        call_args = mock_db.fetch_all.call_args
        sql = call_args[0][0]
        
        assert "WHERE" in sql
        assert "status" in sql
        assert "role" in sql
    
    def test_create(self, repository, mock_db):
        """Test creating entity."""
        mock_db.fetch_one.return_value = {
            "id": "new_id",
            "name": "New Entity"
        }
        
        result = repository.create({"name": "New Entity"})
        
        assert result is not None
        mock_db.fetch_one.assert_called()
    
    def test_update(self, repository, mock_db):
        """Test updating entity."""
        mock_db.fetch_one.return_value = {
            "id": "123",
            "name": "Updated Entity"
        }
        
        result = repository.update("123", {"name": "Updated Entity"})
        
        assert result is not None
    
    def test_delete(self, repository, mock_db):
        """Test deleting entity."""
        result = repository.delete("123")
        
        assert result is True
        mock_db.execute.assert_called()
    
    def test_count(self, repository, mock_db):
        """Test counting entities."""
        mock_db.fetch_one.return_value = {"count": 42}
        
        result = repository.count()
        
        assert result == 42
    
    def test_exists(self, repository, mock_db):
        """Test checking existence."""
        mock_db.fetch_one.return_value = {"exists": True}
        
        result = repository.exists("123")
        
        assert result is True


# =============================================================================
# USER REPOSITORY TESTS
# =============================================================================

class TestUserRepository:
    """Tests for UserRepository class."""
    
    @pytest.fixture
    def mock_db(self):
        """Create mock database."""
        db = Mock(spec=DatabaseConnection)
        return db
    
    @pytest.fixture
    def user_repo(self, mock_db):
        """Create user repository."""
        return UserRepository(mock_db)
    
    def test_find_by_email(self, user_repo, mock_db):
        """Test finding user by email."""
        mock_db.fetch_one.return_value = {
            "id": "user_123",
            "email": "test@example.com",
            "name": "Test User",
            "role": "user"
        }
        
        result = user_repo.find_by_email("test@example.com")
        
        assert result is not None
        call_args = mock_db.fetch_one.call_args
        assert "email" in call_args[0][0].lower()
    
    def test_find_by_email_not_found(self, user_repo, mock_db):
        """Test finding non-existent email."""
        mock_db.fetch_one.return_value = None
        
        result = user_repo.find_by_email("notfound@example.com")
        
        assert result is None
    
    def test_create_with_password(self, user_repo, mock_db):
        """Test creating user with password."""
        mock_db.fetch_one.return_value = {
            "id": "new_user",
            "email": "new@example.com",
            "name": "New User",
            "role": "user"
        }
        
        user_data = {
            "email": "new@example.com",
            "name": "New User"
        }
        password_hash = "hashed_password"
        
        result = user_repo.create_with_password(user_data, password_hash)
        
        assert result is not None
        # Verify password_hash was included
        call_args = mock_db.fetch_one.call_args
        assert "password_hash" in call_args[0][0]
    
    def test_update_last_login(self, user_repo, mock_db):
        """Test updating last login."""
        user_repo.update_last_login("user_123")
        
        mock_db.execute.assert_called_once()
        call_args = mock_db.execute.call_args
        assert "last_login" in call_args[0][0]
    
    def test_update_points(self, user_repo, mock_db):
        """Test updating user points."""
        mock_db.fetch_one.return_value = {"points": 150}
        
        result = user_repo.update_points("user_123", 50)
        
        assert result == 150
    
    def test_find_by_role(self, user_repo, mock_db):
        """Test finding users by role."""
        mock_db.fetch_all.return_value = [
            {"id": "1", "role": "admin"},
            {"id": "2", "role": "admin"}
        ]
        
        results = user_repo.find_by_role(UserRole.ADMIN)
        
        assert len(results) == 2


# =============================================================================
# CHAT REPOSITORY TESTS
# =============================================================================

class TestChatRepository:
    """Tests for ChatRepository class."""
    
    @pytest.fixture
    def mock_db(self):
        """Create mock database."""
        db = Mock(spec=DatabaseConnection)
        return db
    
    @pytest.fixture
    def chat_repo(self, mock_db):
        """Create chat repository."""
        return ChatRepository(mock_db)
    
    def test_find_by_user(self, chat_repo, mock_db):
        """Test finding chats by user."""
        mock_db.fetch_all.return_value = [
            {"id": "chat_1", "user_id": "user_123", "messages": []},
            {"id": "chat_2", "user_id": "user_123", "messages": []}
        ]
        
        results = chat_repo.find_by_user("user_123")
        
        assert len(results) == 2
    
    def test_find_by_user_with_limit(self, chat_repo, mock_db):
        """Test finding chats with limit."""
        mock_db.fetch_all.return_value = []
        
        chat_repo.find_by_user("user_123", limit=5)
        
        call_args = mock_db.fetch_all.call_args
        assert "LIMIT" in call_args[0][0]
    
    def test_add_message(self, chat_repo, mock_db):
        """Test adding message to chat."""
        # Mock existing chat
        mock_db.fetch_one.return_value = {
            "id": "chat_123",
            "messages": [{"role": "user", "content": "Hi"}]
        }
        
        new_message = {
            "role": "assistant",
            "content": "Hello!"
        }
        
        chat_repo.add_message("chat_123", new_message)
        
        # Verify update was called
        mock_db.execute.assert_called()
    
    def test_archive_chat(self, chat_repo, mock_db):
        """Test archiving a chat."""
        result = chat_repo.archive("chat_123")
        
        call_args = mock_db.execute.call_args
        assert "is_archived" in call_args[0][0]


# =============================================================================
# BOOKING REPOSITORY TESTS
# =============================================================================

class TestBookingRepository:
    """Tests for BookingRepository class."""
    
    @pytest.fixture
    def mock_db(self):
        """Create mock database."""
        db = Mock(spec=DatabaseConnection)
        return db
    
    @pytest.fixture
    def booking_repo(self, mock_db):
        """Create booking repository."""
        return BookingRepository(mock_db)
    
    def test_find_by_booking_number(self, booking_repo, mock_db):
        """Test finding booking by number."""
        mock_db.fetch_one.return_value = {
            "id": "booking_123",
            "booking_number": "LBK-ABC12345",
            "status": "confirmed"
        }
        
        result = booking_repo.find_by_booking_number("LBK-ABC12345")
        
        assert result is not None
        assert result["booking_number"] == "LBK-ABC12345"
    
    def test_update_status(self, booking_repo, mock_db):
        """Test updating booking status."""
        mock_db.fetch_one.return_value = {
            "id": "booking_123",
            "status": "confirmed"
        }
        
        result = booking_repo.update_status("booking_123", BookingStatus.CONFIRMED)
        
        mock_db.fetch_one.assert_called()
    
    def test_update_status_with_timestamp(self, booking_repo, mock_db):
        """Test that status update includes timestamp."""
        mock_db.fetch_one.return_value = {
            "id": "booking_123",
            "status": "confirmed",
            "confirmed_at": datetime.utcnow()
        }
        
        booking_repo.update_status("booking_123", BookingStatus.CONFIRMED)
        
        call_args = mock_db.fetch_one.call_args
        assert "confirmed_at" in call_args[0][0]
    
    def test_get_revenue_stats(self, booking_repo, mock_db):
        """Test getting revenue statistics."""
        mock_db.fetch_one.return_value = {
            "total_revenue": 500000000,
            "booking_count": 20,
            "avg_booking_value": 25000000
        }
        
        stats = booking_repo.get_revenue_stats()
        
        assert stats["total_revenue"] == 500000000
        assert stats["booking_count"] == 20
    
    def test_get_revenue_stats_with_date_range(self, booking_repo, mock_db):
        """Test revenue stats with date range."""
        mock_db.fetch_one.return_value = {
            "total_revenue": 100000000,
            "booking_count": 5
        }
        
        start = date(2025, 1, 1)
        end = date(2025, 1, 31)
        
        booking_repo.get_revenue_stats(start_date=start, end_date=end)
        
        call_args = mock_db.fetch_one.call_args
        sql = call_args[0][0]
        assert "created_at" in sql


# =============================================================================
# INTEGRATION TEST WITH REAL DATABASE
# =============================================================================

@pytest.mark.integration
class TestDatabaseIntegration:
    """
    Integration tests that require a real database.
    These tests are skipped if no database is available.
    """
    
    @pytest.fixture
    def db_connection(self, test_database_url):
        """Create database connection for tests."""
        db = DatabaseConnection()
        
        if not db.initialize(test_database_url):
            pytest.skip("Database not available")
        
        yield db
        
        db.close()
    
    def test_user_crud_operations(self, db_connection):
        """Test full CRUD cycle for users."""
        user_repo = UserRepository(db_connection)
        
        # Create
        user_data = {
            "email": f"test_{uuid4().hex[:8]}@example.com",
            "name": "Integration Test User",
            "role": "user"
        }
        
        created = user_repo.create(user_data)
        assert created is not None
        user_id = created["id"]
        
        # Read
        found = user_repo.find_by_id(user_id)
        assert found is not None
        assert found["email"] == user_data["email"]
        
        # Update
        updated = user_repo.update(user_id, {"name": "Updated Name"})
        assert updated["name"] == "Updated Name"
        
        # Delete
        deleted = user_repo.delete(user_id)
        assert deleted is True
        
        # Verify deletion
        found_after_delete = user_repo.find_by_id(user_id)
        assert found_after_delete is None
    
    def test_booking_workflow(self, db_connection):
        """Test booking creation and status updates."""
        booking_repo = BookingRepository(db_connection)
        
        # Create booking
        booking_data = {
            "booking_number": f"LBK-TEST{uuid4().hex[:6].upper()}",
            "status": "draft",
            "package_type": "reguler",
            "departure_city": "Jakarta",
            "departure_date": date.today() + timedelta(days=60),
            "return_date": date.today() + timedelta(days=74),
            "total_price": 30000000
        }
        
        created = booking_repo.create(booking_data)
        assert created is not None
        booking_id = created["id"]
        
        # Update status
        updated = booking_repo.update_status(booking_id, BookingStatus.PENDING)
        assert updated["status"] == "pending"
        
        # Cleanup
        booking_repo.delete(booking_id)


# =============================================================================
# FIXTURES FOR INTEGRATION TESTS
# =============================================================================

@pytest.fixture
def test_database_url():
    """
    Get test database URL from environment.
    Skip tests if not available.
    """
    import os
    
    url = os.environ.get("TEST_DATABASE_URL") or os.environ.get("DATABASE_URL")
    
    if not url:
        pytest.skip("No database URL configured for integration tests")
    
    return url
