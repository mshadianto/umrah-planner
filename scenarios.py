"""
LABBAIK Scenario Planner Module
Budget simulation and scenario comparison
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class BudgetBreakdown:
    """Breakdown of umrah costs"""
    flight: float
    visa: float
    hotel_makkah: float
    hotel_madinah: float
    transport: float
    meals: float
    misc: float
    total: float


@dataclass
class ScenarioResult:
    """Result of a budget scenario"""
    name: str
    breakdown: BudgetBreakdown
    duration_days: int
    departure_city: str
    package_type: str
    description: str


class ScenarioPlanner:
    """Plans and compares different umrah budget scenarios"""
    
    # Base prices in IDR
    BASE_PRICES = {
        "flight": {
            "economy": 9_000_000,
            "business": 25_000_000
        },
        "visa": 1_200_000,
        "hotel_per_night": {
            3: 500_000,
            4: 1_000_000,
            5: 2_500_000
        },
        "transport_per_day": 150_000,
        "meals_per_day": 200_000,
        "misc_per_day": 100_000
    }
    
    # City multipliers
    CITY_MULTIPLIERS = {
        "Jakarta": 1.0,
        "Surabaya": 1.05,
        "Medan": 1.1,
        "Makassar": 1.15,
        "Bandung": 1.08,
        "Semarang": 1.07,
        "Yogyakarta": 1.06,
        "Denpasar": 1.12,
        "Palembang": 1.1,
        "Balikpapan": 1.15
    }
    
    # Season multipliers
    SEASON_MULTIPLIERS = {
        "low": 0.85,
        "regular": 1.0,
        "high": 1.4,
        "ramadan": 1.6
    }
    
    def __init__(self):
        self.scenarios: List[ScenarioResult] = []
    
    def calculate_budget(
        self,
        departure_city: str = "Jakarta",
        duration_days: int = 9,
        package_type: str = "standard",
        num_people: int = 1,
        season: str = "regular",
        nights_makkah: int = 5,
        nights_madinah: int = 4
    ) -> BudgetBreakdown:
        """Calculate budget breakdown for given parameters"""
        
        # Get multipliers
        city_mult = self.CITY_MULTIPLIERS.get(departure_city, 1.0)
        season_mult = self.SEASON_MULTIPLIERS.get(season, 1.0)
        
        # Package settings
        package_settings = {
            "ekonomis": {"flight": "economy", "hotel": 3, "meals": False, "mult": 1.0},
            "standard": {"flight": "economy", "hotel": 4, "meals": True, "mult": 1.3},
            "premium": {"flight": "business", "hotel": 5, "meals": True, "mult": 1.8},
            "vip": {"flight": "business", "hotel": 5, "meals": True, "mult": 2.5}
        }
        
        pkg = package_settings.get(package_type, package_settings["standard"])
        pkg_mult = pkg["mult"]
        
        # Calculate individual costs
        flight = self.BASE_PRICES["flight"][pkg["flight"]] * city_mult * season_mult
        visa = self.BASE_PRICES["visa"]
        
        hotel_rate = self.BASE_PRICES["hotel_per_night"][pkg["hotel"]]
        hotel_makkah = hotel_rate * nights_makkah * season_mult
        hotel_madinah = hotel_rate * nights_madinah * season_mult * 0.9  # Madinah slightly cheaper
        
        transport = self.BASE_PRICES["transport_per_day"] * duration_days
        
        if pkg["meals"]:
            meals = self.BASE_PRICES["meals_per_day"] * duration_days
        else:
            meals = self.BASE_PRICES["meals_per_day"] * duration_days * 0.5  # Self-catering
        
        misc = self.BASE_PRICES["misc_per_day"] * duration_days
        
        # Apply package multiplier
        total = (flight + visa + hotel_makkah + hotel_madinah + transport + meals + misc) * pkg_mult
        
        # Multiply by number of people
        per_person = BudgetBreakdown(
            flight=flight,
            visa=visa,
            hotel_makkah=hotel_makkah / num_people if num_people > 1 else hotel_makkah,
            hotel_madinah=hotel_madinah / num_people if num_people > 1 else hotel_madinah,
            transport=transport,
            meals=meals,
            misc=misc,
            total=total
        )
        
        return per_person
    
    def create_scenario(
        self,
        name: str,
        departure_city: str = "Jakarta",
        duration_days: int = 9,
        package_type: str = "standard",
        season: str = "regular"
    ) -> ScenarioResult:
        """Create a named scenario"""
        
        breakdown = self.calculate_budget(
            departure_city=departure_city,
            duration_days=duration_days,
            package_type=package_type,
            season=season
        )
        
        descriptions = {
            "ekonomis": "Paket hemat untuk budget terbatas",
            "standard": "Paket standar dengan kenyamanan baik",
            "premium": "Paket premium dengan layanan ekstra",
            "vip": "Paket VIP dengan pengalaman terbaik"
        }
        
        result = ScenarioResult(
            name=name,
            breakdown=breakdown,
            duration_days=duration_days,
            departure_city=departure_city,
            package_type=package_type,
            description=descriptions.get(package_type, "")
        )
        
        self.scenarios.append(result)
        return result
    
    def compare_scenarios(self, scenarios: List[ScenarioResult] = None) -> Dict:
        """Compare multiple scenarios"""
        
        if scenarios is None:
            scenarios = self.scenarios
        
        if not scenarios:
            return {"error": "No scenarios to compare"}
        
        comparison = {
            "scenarios": [],
            "cheapest": None,
            "most_expensive": None,
            "average": 0
        }
        
        totals = []
        for s in scenarios:
            comparison["scenarios"].append({
                "name": s.name,
                "total": s.breakdown.total,
                "package": s.package_type,
                "city": s.departure_city
            })
            totals.append(s.breakdown.total)
        
        if totals:
            comparison["cheapest"] = min(comparison["scenarios"], key=lambda x: x["total"])
            comparison["most_expensive"] = max(comparison["scenarios"], key=lambda x: x["total"])
            comparison["average"] = sum(totals) / len(totals)
        
        return comparison
    
    def get_recommendations(self, budget: float) -> List[Dict]:
        """Get package recommendations based on budget"""
        
        recommendations = []
        
        packages = ["ekonomis", "standard", "premium", "vip"]
        
        for pkg in packages:
            breakdown = self.calculate_budget(package_type=pkg)
            
            if breakdown.total <= budget:
                recommendations.append({
                    "package": pkg,
                    "total": breakdown.total,
                    "savings": budget - breakdown.total,
                    "fits_budget": True
                })
            else:
                recommendations.append({
                    "package": pkg,
                    "total": breakdown.total,
                    "over_budget": breakdown.total - budget,
                    "fits_budget": False
                })
        
        return recommendations


# Convenience function
def create_planner() -> ScenarioPlanner:
    """Factory function to create scenario planner"""
    return ScenarioPlanner()
