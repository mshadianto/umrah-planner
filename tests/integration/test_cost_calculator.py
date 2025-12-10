"""
LABBAIK AI v6.0 - Integration Tests
===================================
Integration tests for services.
"""

import pytest
from datetime import date, datetime
from unittest.mock import Mock, patch

from services.cost.calculator import (
    calculate_umrah_cost,
    compare_packages,
    compare_seasons,
    get_season_type,
    get_flight_cost,
    get_hotel_cost_per_night,
)
from data.models import (
    CostSimulationInput,
    HotelStarRating,
    PackageType,
)


# =============================================================================
# COST CALCULATOR INTEGRATION TESTS
# =============================================================================

class TestCostCalculatorIntegration:
    """Integration tests for cost calculator service."""
    
    @pytest.fixture
    def sample_input(self):
        """Sample cost simulation input."""
        return {
            "departure_city": "Jakarta",
            "departure_date": date(2025, 3, 1),
            "return_date": date(2025, 3, 15),
            "traveler_count": 2,
            "hotel_makkah_star": 3,
            "hotel_madinah_star": 3,
            "days_makkah": 6,
            "days_madinah": 5,
            "package_type": "reguler",
            "include_visa": True,
            "include_insurance": True,
            "include_mutawif": True,
        }
    
    def test_calculate_umrah_cost_full(self, sample_input):
        """Test full cost calculation."""
        result = calculate_umrah_cost(sample_input)
        
        assert "breakdown" in result
        assert "total_per_person" in result
        assert "total_all" in result
        assert "season_type" in result
        
        # Check breakdown has all components
        breakdown = result["breakdown"]
        assert "flight_cost" in breakdown
        assert "hotel_makkah_cost" in breakdown
        assert "hotel_madinah_cost" in breakdown
        assert "visa_cost" in breakdown
        assert "insurance_cost" in breakdown
        assert "mutawif_cost" in breakdown
        assert "handling_fee" in breakdown
        
        # Check totals make sense
        assert result["total_per_person"] > 0
        assert result["total_all"] == result["total_per_person"] * sample_input["traveler_count"]
    
    def test_calculate_without_optional_services(self, sample_input):
        """Test calculation without optional services."""
        sample_input["include_visa"] = False
        sample_input["include_insurance"] = False
        sample_input["include_mutawif"] = False
        
        result = calculate_umrah_cost(sample_input)
        
        assert result["breakdown"]["visa_cost"] == 0
        assert result["breakdown"]["insurance_cost"] == 0
        assert result["breakdown"]["mutawif_cost"] == 0
    
    def test_seasonal_pricing_peak(self, sample_input):
        """Test peak season pricing."""
        # Ramadan period (approximate)
        sample_input["departure_date"] = date(2025, 3, 15)
        sample_input["return_date"] = date(2025, 3, 29)
        
        result = calculate_umrah_cost(sample_input)
        
        # Peak season should have multiplier > 1
        assert result["seasonal_multiplier"] >= 1.0
    
    def test_seasonal_pricing_low(self, sample_input):
        """Test low season pricing."""
        # Low season (September)
        sample_input["departure_date"] = date(2025, 9, 1)
        sample_input["return_date"] = date(2025, 9, 15)
        
        result = calculate_umrah_cost(sample_input)
        
        # Low season should have multiplier < 1
        assert result["seasonal_multiplier"] <= 1.0
    
    def test_package_type_vip_more_expensive(self, sample_input):
        """Test VIP package costs more than reguler."""
        # Calculate reguler
        sample_input["package_type"] = "reguler"
        reguler_result = calculate_umrah_cost(sample_input)
        
        # Calculate VIP
        sample_input["package_type"] = "vip"
        vip_result = calculate_umrah_cost(sample_input)
        
        assert vip_result["total_per_person"] > reguler_result["total_per_person"]
    
    def test_package_type_backpacker_cheaper(self, sample_input):
        """Test backpacker package costs less than reguler."""
        # Calculate reguler
        sample_input["package_type"] = "reguler"
        reguler_result = calculate_umrah_cost(sample_input)
        
        # Calculate backpacker
        sample_input["package_type"] = "backpacker"
        backpacker_result = calculate_umrah_cost(sample_input)
        
        assert backpacker_result["total_per_person"] < reguler_result["total_per_person"]
    
    def test_hotel_star_rating_affects_cost(self, sample_input):
        """Test higher star rating costs more."""
        # 3 star
        sample_input["hotel_makkah_star"] = 3
        sample_input["hotel_madinah_star"] = 3
        result_3star = calculate_umrah_cost(sample_input)
        
        # 5 star
        sample_input["hotel_makkah_star"] = 5
        sample_input["hotel_madinah_star"] = 5
        result_5star = calculate_umrah_cost(sample_input)
        
        assert result_5star["breakdown"]["hotel_makkah_cost"] > result_3star["breakdown"]["hotel_makkah_cost"]
    
    def test_more_travelers_increases_total(self, sample_input):
        """Test more travelers increases total cost."""
        sample_input["traveler_count"] = 1
        result_1 = calculate_umrah_cost(sample_input)
        
        sample_input["traveler_count"] = 5
        result_5 = calculate_umrah_cost(sample_input)
        
        # Per person should be same
        assert abs(result_1["total_per_person"] - result_5["total_per_person"]) < 1000
        
        # Total should be 5x
        assert result_5["total_all"] == result_5["total_per_person"] * 5
    
    def test_result_includes_notes(self, sample_input):
        """Test result includes helpful notes."""
        # VIP package should have note
        sample_input["package_type"] = "vip"
        result = calculate_umrah_cost(sample_input)
        
        assert "notes" in result
        assert isinstance(result["notes"], list)
    
    def test_result_includes_disclaimer(self, sample_input):
        """Test result includes disclaimer."""
        result = calculate_umrah_cost(sample_input)
        
        assert "disclaimer" in result
        assert len(result["disclaimer"]) > 0


class TestSeasonDetermination:
    """Tests for season determination."""
    
    def test_ramadan_is_peak(self):
        """Test Ramadan months are peak season."""
        season, multiplier = get_season_type(date(2025, 3, 15))
        assert season == "peak"
        assert multiplier > 1.0
    
    def test_regular_months(self):
        """Test regular months."""
        season, multiplier = get_season_type(date(2025, 9, 15))
        assert season == "regular"
        assert multiplier == 1.0
    
    def test_school_holiday_is_high(self):
        """Test school holiday months are high season."""
        season, multiplier = get_season_type(date(2025, 7, 15))
        assert season == "high"
        assert multiplier > 1.0


class TestFlightCosts:
    """Tests for flight cost lookup."""
    
    def test_jakarta_flight_cost(self):
        """Test Jakarta flight cost."""
        cost = get_flight_cost("Jakarta")
        assert cost > 0
    
    def test_surabaya_flight_cost(self):
        """Test Surabaya flight cost."""
        cost = get_flight_cost("Surabaya")
        assert cost > 0
    
    def test_unknown_city_defaults_to_jakarta(self):
        """Test unknown city defaults to Jakarta."""
        jakarta_cost = get_flight_cost("Jakarta")
        unknown_cost = get_flight_cost("Unknown City")
        assert unknown_cost == jakarta_cost


class TestHotelCosts:
    """Tests for hotel cost lookup."""
    
    def test_makkah_3_star(self):
        """Test Makkah 3-star hotel cost."""
        cost = get_hotel_cost_per_night("makkah", 3)
        assert cost > 0
    
    def test_madinah_5_star(self):
        """Test Madinah 5-star hotel cost."""
        cost = get_hotel_cost_per_night("madinah", 5)
        assert cost > 0
    
    def test_makkah_more_expensive_than_madinah(self):
        """Test Makkah hotels generally more expensive."""
        makkah_cost = get_hotel_cost_per_night("makkah", 4)
        madinah_cost = get_hotel_cost_per_night("madinah", 4)
        
        # Makkah typically more expensive due to proximity to Haram
        assert makkah_cost >= madinah_cost


class TestPackageComparison:
    """Tests for package comparison."""
    
    def test_compare_packages_returns_sorted(self):
        """Test package comparison returns sorted results."""
        base_input = {
            "departure_city": "Jakarta",
            "departure_date": date(2025, 5, 1),
            "return_date": date(2025, 5, 15),
            "traveler_count": 1,
            "hotel_makkah_star": 3,
            "hotel_madinah_star": 3,
            "days_makkah": 6,
            "days_madinah": 5,
            "include_visa": True,
            "include_insurance": True,
            "include_mutawif": True,
        }
        
        results = compare_packages(base_input)
        
        # Should return 4 package types by default
        assert len(results) == 4
        
        # Should be sorted by price (cheapest first)
        prices = [r["total_per_person"] for r in results]
        assert prices == sorted(prices)


class TestSeasonComparison:
    """Tests for season comparison."""
    
    def test_compare_seasons_returns_multiple(self):
        """Test season comparison returns multiple months."""
        base_input = {
            "departure_city": "Jakarta",
            "departure_date": date(2025, 5, 1),
            "return_date": date(2025, 5, 15),
            "traveler_count": 1,
            "hotel_makkah_star": 3,
            "hotel_madinah_star": 3,
            "days_makkah": 6,
            "days_madinah": 5,
            "include_visa": True,
            "include_insurance": True,
            "include_mutawif": True,
        }
        
        results = compare_seasons(base_input, months=[1, 3, 6, 9])
        
        assert len(results) == 4
        
        # Each result should have month info
        for result in results:
            assert "month" in result
            assert "month_name" in result
