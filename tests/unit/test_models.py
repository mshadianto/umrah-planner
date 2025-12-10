"""
LABBAIK AI v6.0 - Data Models Unit Tests
========================================
Tests for Pydantic data models.
"""

import pytest
from datetime import datetime, date, timedelta
from pydantic import ValidationError

from data.models import (
    User,
    UserRole,
    SubscriptionTier,
    UserCreate,
    UserUpdate,
    ChatMessage,
    ChatConversation,
    MessageRole,
    Booking,
    BookingStatus,
    TravelerInfo,
    CostSimulationInput,
    CostBreakdown,
    HotelStarRating,
    PackageType,
    Partner,
    PartnerType,
    Notification,
    NotificationType,
)


# =============================================================================
# USER MODEL TESTS
# =============================================================================

class TestUserModel:
    """Tests for User model."""
    
    def test_create_user(self, sample_user_data):
        """Test creating user with valid data."""
        user = User(**sample_user_data)
        
        assert user.email == sample_user_data["email"]
        assert user.name == sample_user_data["name"]
        assert user.role == UserRole.USER
        assert user.is_active is True
    
    def test_user_default_values(self):
        """Test user default values."""
        user = User(
            email="test@example.com",
            name="Test User"
        )
        
        assert user.role == UserRole.USER
        assert user.subscription_tier == SubscriptionTier.FREE
        assert user.is_verified is False
        assert user.is_active is True
        assert user.points == 0
        assert user.level == 1
        assert user.badges == []
    
    def test_user_has_permission(self):
        """Test user permission check."""
        admin = User(
            email="admin@test.com",
            name="Admin",
            role=UserRole.ADMIN
        )
        
        user = User(
            email="user@test.com",
            name="User",
            role=UserRole.USER
        )
        
        assert admin.has_permission(UserRole.USER) is True
        assert admin.has_permission(UserRole.ADMIN) is True
        assert user.has_permission(UserRole.USER) is True
        assert user.has_permission(UserRole.ADMIN) is False
    
    def test_user_email_validation(self):
        """Test email validation."""
        with pytest.raises(ValidationError):
            User(email="invalid-email", name="Test")
    
    def test_user_name_validation(self):
        """Test name validation."""
        with pytest.raises(ValidationError):
            User(email="test@example.com", name="A")  # Too short


class TestUserCreate:
    """Tests for UserCreate model."""
    
    def test_password_validation_uppercase(self):
        """Test password must have uppercase."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="test@example.com",
                name="Test User",
                password="password123"  # No uppercase
            )
        assert "uppercase" in str(exc_info.value).lower()
    
    def test_password_validation_digit(self):
        """Test password must have digit."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="test@example.com",
                name="Test User",
                password="PasswordOnly"  # No digit
            )
        assert "digit" in str(exc_info.value).lower()
    
    def test_valid_password(self):
        """Test valid password."""
        user = UserCreate(
            email="test@example.com",
            name="Test User",
            password="ValidPass123"
        )
        assert user.password == "ValidPass123"


# =============================================================================
# CHAT MESSAGE TESTS
# =============================================================================

class TestChatMessage:
    """Tests for ChatMessage model."""
    
    def test_create_message(self):
        """Test creating chat message."""
        msg = ChatMessage(
            role=MessageRole.USER,
            content="Hello, world!"
        )
        
        assert msg.role == MessageRole.USER
        assert msg.content == "Hello, world!"
        assert msg.timestamp is not None
    
    def test_to_api_format(self):
        """Test converting to API format."""
        msg = ChatMessage(
            role=MessageRole.ASSISTANT,
            content="Hi there!"
        )
        
        api_format = msg.to_api_format()
        
        assert api_format == {
            "role": "assistant",
            "content": "Hi there!"
        }


class TestChatConversation:
    """Tests for ChatConversation model."""
    
    def test_add_message(self):
        """Test adding message to conversation."""
        conv = ChatConversation(user_id="user_123")
        
        msg = conv.add_message(MessageRole.USER, "Hello")
        
        assert len(conv.messages) == 1
        assert msg.content == "Hello"
        assert conv.message_count == 1
    
    def test_get_context_messages(self):
        """Test getting context messages."""
        conv = ChatConversation(user_id="user_123")
        
        # Add 15 messages
        for i in range(15):
            conv.add_message(MessageRole.USER, f"Message {i}")
        
        context = conv.get_context_messages(max_messages=10)
        
        assert len(context) == 10
        assert context[0].content == "Message 5"  # Should start from 5


# =============================================================================
# BOOKING TESTS
# =============================================================================

class TestTravelerInfo:
    """Tests for TravelerInfo model."""
    
    def test_create_traveler(self, sample_traveler_data):
        """Test creating traveler info."""
        traveler = TravelerInfo(**sample_traveler_data)
        
        assert traveler.name == sample_traveler_data["name"]
        assert traveler.passport_number == sample_traveler_data["passport_number"]
    
    def test_passport_expiry_validation(self):
        """Test passport expiry validation."""
        with pytest.raises(ValidationError):
            TravelerInfo(
                name="Test Traveler",
                passport_number="A12345678",
                passport_expiry=date(2020, 1, 1)  # Expired
            )


class TestBooking:
    """Tests for Booking model."""
    
    def test_create_booking(self, sample_booking):
        """Test creating booking."""
        assert sample_booking.booking_number.startswith("LBK-")
        assert sample_booking.status == BookingStatus.DRAFT
    
    def test_booking_traveler_count(self, sample_booking):
        """Test traveler count property."""
        assert sample_booking.traveler_count == 1
    
    def test_booking_balance_due(self, sample_booking):
        """Test balance due calculation."""
        sample_booking.total_price = 50000000
        sample_booking.paid_amount = 20000000
        
        assert sample_booking.balance_due == 30000000
    
    def test_return_date_validation(self, sample_traveler_data):
        """Test return date must be after departure."""
        traveler = TravelerInfo(**sample_traveler_data)
        
        with pytest.raises(ValidationError):
            Booking(
                user_id="user_123",
                package_type=PackageType.REGULER,
                departure_city="Jakarta",
                departure_date=date(2025, 3, 15),
                return_date=date(2025, 3, 1),  # Before departure
                travelers=[traveler]
            )


# =============================================================================
# COST SIMULATION TESTS
# =============================================================================

class TestCostSimulationInput:
    """Tests for CostSimulationInput model."""
    
    def test_create_cost_input(self, sample_cost_input):
        """Test creating cost simulation input."""
        assert sample_cost_input.departure_city == "Jakarta"
        assert sample_cost_input.traveler_count == 2
    
    def test_total_days_property(self, sample_cost_input):
        """Test total days calculation."""
        expected_days = (
            sample_cost_input.return_date - 
            sample_cost_input.departure_date
        ).days
        
        assert sample_cost_input.total_days == expected_days
    
    def test_traveler_count_validation(self):
        """Test traveler count limits."""
        with pytest.raises(ValidationError):
            CostSimulationInput(
                departure_city="Jakarta",
                departure_date=date(2025, 3, 1),
                return_date=date(2025, 3, 15),
                traveler_count=100,  # Exceeds max
                hotel_makkah_star=HotelStarRating.STANDARD,
                hotel_madinah_star=HotelStarRating.STANDARD,
                days_makkah=5,
                days_madinah=4,
            )


class TestCostBreakdown:
    """Tests for CostBreakdown model."""
    
    def test_subtotal_calculation(self):
        """Test subtotal calculation."""
        breakdown = CostBreakdown(
            flight_cost=10000000,
            hotel_makkah_cost=5000000,
            hotel_madinah_cost=4000000,
            visa_cost=500000,
            insurance_cost=300000,
            mutawif_cost=1000000,
            handling_fee=200000,
            other_costs=0
        )
        
        expected = 21000000
        assert breakdown.subtotal == expected


# =============================================================================
# PARTNER TESTS
# =============================================================================

class TestPartner:
    """Tests for Partner model."""
    
    def test_create_partner(self):
        """Test creating partner."""
        partner = Partner(
            name="Travel Berkah",
            type=PartnerType.TRAVEL_AGENT,
            email="info@travelberkah.com",
            phone="+628123456789",
            company_name="PT Travel Berkah Indonesia",
            address="Jl. Sudirman No. 123",
            city="Jakarta"
        )
        
        assert partner.name == "Travel Berkah"
        assert partner.type == PartnerType.TRAVEL_AGENT
        assert partner.commission_rate == 0.1  # Default 10%


# =============================================================================
# NOTIFICATION TESTS
# =============================================================================

class TestNotification:
    """Tests for Notification model."""
    
    def test_create_notification(self):
        """Test creating notification."""
        notif = Notification(
            user_id="user_123",
            type=NotificationType.INFO,
            title="Test Notification",
            message="This is a test"
        )
        
        assert notif.is_read is False
        assert notif.read_at is None
    
    def test_mark_read(self):
        """Test marking notification as read."""
        notif = Notification(
            user_id="user_123",
            type=NotificationType.SUCCESS,
            title="Test",
            message="Test message"
        )
        
        notif.mark_read()
        
        assert notif.is_read is True
        assert notif.read_at is not None


# =============================================================================
# ENUM TESTS
# =============================================================================

class TestEnums:
    """Tests for enum values."""
    
    def test_user_role_values(self):
        """Test user role values."""
        assert UserRole.GUEST.value == "guest"
        assert UserRole.USER.value == "user"
        assert UserRole.ADMIN.value == "admin"
    
    def test_booking_status_values(self):
        """Test booking status values."""
        assert BookingStatus.DRAFT.value == "draft"
        assert BookingStatus.CONFIRMED.value == "confirmed"
        assert BookingStatus.CANCELLED.value == "cancelled"
    
    def test_hotel_star_rating_values(self):
        """Test hotel star rating values."""
        assert HotelStarRating.BUDGET.value == 2
        assert HotelStarRating.DELUXE.value == 5
    
    def test_package_type_values(self):
        """Test package type values."""
        assert PackageType.REGULER.value == "reguler"
        assert PackageType.VIP.value == "vip"
        assert PackageType.MANDIRI.value == "mandiri"
