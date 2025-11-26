"""
Scenario Planner Module
=======================
Advanced scenario planning for umrah trips
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from config import SCENARIO_TEMPLATES, SEASONS, COST_COMPONENTS


@dataclass
class UmrahScenario:
    """Data class for umrah scenario"""
    name: str
    scenario_type: str
    duration_days: int
    num_people: int
    departure_month: int
    hotel_star_makkah: int
    hotel_star_madinah: int
    hotel_distance_makkah: str
    hotel_distance_madinah: str
    meal_type: str
    transport_type: str
    estimated_min: float = 0
    estimated_max: float = 0
    features: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


class ScenarioPlanner:
    """Plans and compares different umrah scenarios"""
    
    def __init__(self):
        """Initialize scenario planner"""
        self.scenarios: List[UmrahScenario] = []
    
    def create_scenario(
        self,
        scenario_type: str,
        num_people: int = 1,
        duration_days: Optional[int] = None,
        departure_month: int = 6,
        custom_name: Optional[str] = None
    ) -> UmrahScenario:
        """
        Create a new scenario based on template
        
        Args:
            scenario_type: Base scenario type
            num_people: Number of pilgrims
            duration_days: Custom duration (optional)
            departure_month: Month of departure
            custom_name: Custom scenario name
            
        Returns:
            Created scenario
        """
        template = SCENARIO_TEMPLATES.get(
            scenario_type, 
            SCENARIO_TEMPLATES["standard"]
        )
        
        duration = duration_days or template["duration_days"]
        
        scenario = UmrahScenario(
            name=custom_name or template["name"],
            scenario_type=scenario_type,
            duration_days=duration,
            num_people=num_people,
            departure_month=departure_month,
            hotel_star_makkah=template["hotel_star_makkah"],
            hotel_star_madinah=template["hotel_star_madinah"],
            hotel_distance_makkah=template["hotel_distance_makkah"],
            hotel_distance_madinah=template["hotel_distance_madinah"],
            meal_type=template["meal_type"],
            transport_type=template["transport_type"],
            features=self._get_scenario_features(scenario_type),
            notes=self._get_scenario_notes(scenario_type, departure_month)
        )
        
        # Calculate estimates
        estimates = self._calculate_estimates(scenario)
        scenario.estimated_min = estimates["min"]
        scenario.estimated_max = estimates["max"]
        
        self.scenarios.append(scenario)
        return scenario
    
    def create_custom_scenario(
        self,
        name: str,
        num_people: int,
        duration_days: int,
        departure_month: int,
        hotel_star_makkah: int,
        hotel_star_madinah: int,
        meal_type: str,
        transport_type: str
    ) -> UmrahScenario:
        """
        Create a fully custom scenario
        
        Args:
            Various scenario parameters
            
        Returns:
            Custom scenario
        """
        distance_map = {
            3: "800-1500m",
            4: "300-500m",
            5: "100-300m",
        }
        
        scenario = UmrahScenario(
            name=name,
            scenario_type="custom",
            duration_days=duration_days,
            num_people=num_people,
            departure_month=departure_month,
            hotel_star_makkah=hotel_star_makkah,
            hotel_star_madinah=hotel_star_madinah,
            hotel_distance_makkah=distance_map.get(hotel_star_makkah, "500-1000m"),
            hotel_distance_madinah=distance_map.get(hotel_star_madinah, "500-1000m"),
            meal_type=meal_type,
            transport_type=transport_type,
            features=["Custom configuration"],
            notes=["Skenario dibuat sesuai preferensi pengguna"]
        )
        
        estimates = self._calculate_estimates(scenario)
        scenario.estimated_min = estimates["min"]
        scenario.estimated_max = estimates["max"]
        
        self.scenarios.append(scenario)
        return scenario
    
    def compare_scenarios(
        self,
        scenario_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Compare multiple scenarios
        
        Args:
            scenario_types: List of scenario types to compare
            
        Returns:
            Comparison results
        """
        if scenario_types is None:
            scenario_types = ["ekonomis", "standard", "premium", "vip"]
        
        comparisons = []
        for stype in scenario_types:
            scenario = self.create_scenario(stype)
            comparisons.append({
                "type": stype,
                "name": scenario.name,
                "duration": scenario.duration_days,
                "hotel_makkah": f"⭐ {scenario.hotel_star_makkah}",
                "hotel_madinah": f"⭐ {scenario.hotel_star_madinah}",
                "distance_makkah": scenario.hotel_distance_makkah,
                "estimated_min": scenario.estimated_min,
                "estimated_max": scenario.estimated_max,
                "features": scenario.features,
            })
        
        return {
            "scenarios": comparisons,
            "recommendation": self._get_recommendation(comparisons),
            "factors": self._get_comparison_factors()
        }
    
    def analyze_best_time(
        self,
        priority: str = "balanced"
    ) -> Dict[str, Any]:
        """
        Analyze best time to perform umrah
        
        Args:
            priority: Priority factor (cost/weather/crowd/balanced)
            
        Returns:
            Time analysis
        """
        months_analysis = []
        
        for month in range(1, 13):
            season_info = self._get_season_info(month)
            
            analysis = {
                "month": month,
                "month_name": self._get_month_name(month),
                "season": season_info["name"],
                "price_multiplier": season_info["multiplier"],
                "crowd_level": season_info["demand"],
                "weather": self._get_weather_info(month),
                "recommendation_score": self._calculate_recommendation_score(
                    season_info, priority
                )
            }
            months_analysis.append(analysis)
        
        # Sort by recommendation score
        months_analysis.sort(key=lambda x: x["recommendation_score"], reverse=True)
        
        return {
            "priority": priority,
            "analysis": months_analysis,
            "best_months": months_analysis[:3],
            "avoid_months": months_analysis[-3:],
            "notes": self._get_timing_notes(priority)
        }
    
    def scenario_what_if(
        self,
        base_scenario: UmrahScenario,
        changes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        What-if analysis for scenario changes
        
        Args:
            base_scenario: Base scenario to modify
            changes: Changes to apply
            
        Returns:
            Impact analysis
        """
        # Create modified scenario
        modified_attrs = {
            "name": f"{base_scenario.name} (Modified)",
            "scenario_type": base_scenario.scenario_type,
            "duration_days": changes.get("duration_days", base_scenario.duration_days),
            "num_people": changes.get("num_people", base_scenario.num_people),
            "departure_month": changes.get("departure_month", base_scenario.departure_month),
            "hotel_star_makkah": changes.get("hotel_star_makkah", base_scenario.hotel_star_makkah),
            "hotel_star_madinah": changes.get("hotel_star_madinah", base_scenario.hotel_star_madinah),
            "hotel_distance_makkah": base_scenario.hotel_distance_makkah,
            "hotel_distance_madinah": base_scenario.hotel_distance_madinah,
            "meal_type": changes.get("meal_type", base_scenario.meal_type),
            "transport_type": changes.get("transport_type", base_scenario.transport_type),
        }
        
        modified = UmrahScenario(**modified_attrs)
        modified_estimates = self._calculate_estimates(modified)
        
        # Calculate differences
        cost_diff_min = modified_estimates["min"] - base_scenario.estimated_min
        cost_diff_max = modified_estimates["max"] - base_scenario.estimated_max
        cost_diff_pct = ((modified_estimates["min"] + modified_estimates["max"]) / 2) / \
                        ((base_scenario.estimated_min + base_scenario.estimated_max) / 2) * 100 - 100
        
        return {
            "base_scenario": {
                "name": base_scenario.name,
                "estimated_min": base_scenario.estimated_min,
                "estimated_max": base_scenario.estimated_max,
            },
            "modified_scenario": {
                "name": modified.name,
                "estimated_min": modified_estimates["min"],
                "estimated_max": modified_estimates["max"],
            },
            "changes_applied": changes,
            "impact": {
                "cost_difference_min": cost_diff_min,
                "cost_difference_max": cost_diff_max,
                "cost_change_percentage": round(cost_diff_pct, 1),
                "direction": "increase" if cost_diff_pct > 0 else "decrease"
            },
            "recommendation": self._get_what_if_recommendation(cost_diff_pct, changes)
        }
    
    def _calculate_estimates(self, scenario: UmrahScenario) -> Dict[str, float]:
        """Calculate cost estimates for a scenario"""
        multiplier = self._get_season_multiplier(scenario.departure_month)
        
        # Base costs
        visa = 2500000 * scenario.num_people
        
        # Tiket based on scenario
        tiket_map = {
            "ekonomis": (8000000, 12000000),
            "standard": (10000000, 15000000),
            "premium": (15000000, 25000000),
            "vip": (25000000, 50000000),
            "custom": (10000000, 15000000),
        }
        tiket = tiket_map.get(scenario.scenario_type, tiket_map["standard"])
        
        # Hotel Makkah
        hotel_makkah_map = {
            3: (400000, 800000),
            4: (800000, 1500000),
            5: (1500000, 4000000),
        }
        hotel_makkah = hotel_makkah_map.get(scenario.hotel_star_makkah, (800000, 1500000))
        makkah_nights = int(scenario.duration_days * 0.6)
        
        # Hotel Madinah
        hotel_madinah_map = {
            3: (300000, 600000),
            4: (600000, 1200000),
            5: (1200000, 3000000),
        }
        hotel_madinah = hotel_madinah_map.get(scenario.hotel_star_madinah, (600000, 1200000))
        madinah_nights = scenario.duration_days - makkah_nights - 1
        
        # Meals
        meal_map = {
            "prasmanan": (150000, 200000),
            "prasmanan_plus": (200000, 300000),
            "menu_pilihan": (300000, 500000),
            "fine_dining": (500000, 1000000),
        }
        meals = meal_map.get(scenario.meal_type, meal_map["prasmanan"])
        
        # Transport
        transport_map = {
            "bus": 100000,
            "bus_ac": 150000,
            "vip_bus": 250000,
            "private_car": 500000,
        }
        transport = transport_map.get(scenario.transport_type, 150000)
        
        # Other costs
        other_min = 3000000  # Muthawwif, perlengkapan, handling
        other_max = 7000000
        
        # Calculate totals
        total_min = (
            visa +
            tiket[0] * scenario.num_people * multiplier +
            hotel_makkah[0] * makkah_nights * scenario.num_people * multiplier +
            hotel_madinah[0] * madinah_nights * scenario.num_people * multiplier +
            meals[0] * scenario.duration_days * scenario.num_people +
            transport * scenario.duration_days * scenario.num_people +
            other_min
        )
        
        total_max = (
            visa +
            tiket[1] * scenario.num_people * multiplier +
            hotel_makkah[1] * makkah_nights * scenario.num_people * multiplier +
            hotel_madinah[1] * madinah_nights * scenario.num_people * multiplier +
            meals[1] * scenario.duration_days * scenario.num_people +
            transport * scenario.duration_days * scenario.num_people +
            other_max
        )
        
        return {"min": total_min, "max": total_max}
    
    def _get_season_multiplier(self, month: int) -> float:
        """Get price multiplier for a month"""
        for season in SEASONS.values():
            if month in season["months"]:
                return season["multiplier"]
        return 1.0
    
    def _get_season_info(self, month: int) -> Dict[str, Any]:
        """Get season info for a month"""
        for season in SEASONS.values():
            if month in season["months"]:
                return season
        return SEASONS["regular"]
    
    def _get_scenario_features(self, scenario_type: str) -> List[str]:
        """Get features for a scenario type"""
        features_map = {
            "ekonomis": [
                "Hotel bintang 3",
                "Jarak hotel 800-1500m dari Haram",
                "Makan prasmanan 3x sehari",
                "Bus reguler AC",
                "Durasi standar 9 hari",
            ],
            "standard": [
                "Hotel bintang 4",
                "Jarak hotel 300-500m dari Haram",
                "Makan prasmanan plus 3x sehari",
                "Bus AC premium",
                "Durasi 12 hari",
                "Guide berbahasa Indonesia",
            ],
            "premium": [
                "Hotel bintang 5",
                "Jarak hotel 100-300m dari Haram",
                "Makan menu pilihan",
                "VIP Bus",
                "Durasi 14 hari",
                "Guide pribadi",
                "Handling bandara VIP",
            ],
            "vip": [
                "Hotel bintang 5 terbaik",
                "View Masjidil Haram/Nabawi",
                "Fine dining",
                "Private car",
                "Durasi fleksibel",
                "Personal assistant",
                "Fast track immigration",
                "Lounge access",
            ],
        }
        return features_map.get(scenario_type, features_map["standard"])
    
    def _get_scenario_notes(self, scenario_type: str, month: int) -> List[str]:
        """Get notes for a scenario"""
        notes = []
        
        season = self._get_season_info(month)
        if season["multiplier"] > 1:
            notes.append(f"⚠️ Musim {season['name']}: harga naik {int((season['multiplier']-1)*100)}%")
        
        if scenario_type == "ekonomis":
            notes.append("💡 Cocok untuk jamaah dengan budget terbatas")
            notes.append("🚶 Siapkan fisik untuk berjalan kaki lebih jauh")
        elif scenario_type == "vip":
            notes.append("👑 Pengalaman premium dengan layanan terbaik")
            notes.append("⏰ Waktu ibadah lebih fleksibel")
        
        return notes
    
    def _get_recommendation(self, comparisons: List[Dict]) -> str:
        """Get recommendation based on comparisons"""
        # Simple recommendation logic
        return """
Rekomendasi berdasarkan profil:
• Budget terbatas (< Rp 35 juta): Pilih Ekonomis
• Keseimbangan harga-kenyamanan: Pilih Standard
• Prioritas kenyamanan: Pilih Premium
• Pengalaman terbaik tanpa batasan budget: Pilih VIP
"""
    
    def _get_comparison_factors(self) -> List[str]:
        """Get factors to consider in comparison"""
        return [
            "Jarak hotel ke Masjidil Haram sangat mempengaruhi kenyamanan",
            "Durasi perjalanan mempengaruhi kedalaman ibadah",
            "Musim keberangkatan mempengaruhi harga signifikan",
            "Fasilitas makan penting untuk stamina ibadah",
            "Transportasi nyaman penting untuk jamaah lansia",
        ]
    
    def _get_month_name(self, month: int) -> str:
        """Get Indonesian month name"""
        names = [
            "Januari", "Februari", "Maret", "April",
            "Mei", "Juni", "Juli", "Agustus",
            "September", "Oktober", "November", "Desember"
        ]
        return names[month - 1]
    
    def _get_weather_info(self, month: int) -> str:
        """Get weather info for a month"""
        hot_months = [5, 6, 7, 8, 9]
        mild_months = [11, 12, 1, 2, 3]
        
        if month in hot_months:
            return "Panas (35-45°C)"
        elif month in mild_months:
            return "Sejuk (15-25°C)"
        else:
            return "Sedang (25-35°C)"
    
    def _calculate_recommendation_score(
        self,
        season_info: Dict,
        priority: str
    ) -> float:
        """Calculate recommendation score for a month"""
        base_score = 50
        
        # Cost factor (lower multiplier = higher score)
        cost_factor = (2 - season_info["multiplier"]) * 25
        
        # Crowd factor
        crowd_map = {"Sangat Tinggi": -20, "Tinggi": -10, "Normal": 10}
        crowd_factor = crowd_map.get(season_info["demand"], 0)
        
        if priority == "cost":
            return base_score + cost_factor * 2 + crowd_factor * 0.5
        elif priority == "crowd":
            return base_score + cost_factor * 0.5 + crowd_factor * 2
        else:  # balanced
            return base_score + cost_factor + crowd_factor
    
    def _get_timing_notes(self, priority: str) -> List[str]:
        """Get timing notes based on priority"""
        notes = {
            "cost": [
                "Hindari Ramadhan dan liburan sekolah untuk harga termurah",
                "Februari-Mei dan September-November adalah waktu terbaik",
                "Booking 4-6 bulan sebelumnya untuk early bird discount",
            ],
            "crowd": [
                "Hindari Ramadhan untuk menghindari kerumunan",
                "Hari kerja biasa lebih sepi dari weekend",
                "Waktu shubuh dan dhuhur lebih sepi untuk thawaf",
            ],
            "balanced": [
                "September-November menawarkan keseimbangan terbaik",
                "Cuaca nyaman dan harga reasonable",
                "Booking 3-4 bulan sebelumnya sudah cukup",
            ],
        }
        return notes.get(priority, notes["balanced"])
    
    def _get_what_if_recommendation(
        self,
        cost_change_pct: float,
        changes: Dict
    ) -> str:
        """Get recommendation for what-if analysis"""
        if cost_change_pct > 20:
            return "⚠️ Perubahan signifikan pada biaya. Pertimbangkan kembali."
        elif cost_change_pct > 0:
            return "💰 Ada kenaikan biaya, tapi mungkin worth it untuk kenyamanan."
        elif cost_change_pct < -10:
            return "✅ Penghematan bagus! Pastikan tidak mengorbankan hal penting."
        else:
            return "✅ Perubahan minimal pada biaya. Keputusan berdasarkan preferensi."
