"""
Financial Agent Module
======================
Agent for cost calculation and financial planning
"""

from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent
from config import (
    SCENARIO_TEMPLATES,
    COST_COMPONENTS,
    SEASONS,
    currency_config
)


class FinancialAgent(BaseAgent):
    """Agent for financial calculations and cost optimization"""
    
    def __init__(self):
        super().__init__(
            name="Financial Agent",
            description="Agent untuk kalkulasi biaya dan optimasi keuangan umrah"
        )
        self.calculator = UmrahCostCalculator()
    
    def get_system_prompt(self) -> str:
        return """Anda adalah Financial Agent yang ahli dalam kalkulasi biaya perjalanan umrah.

PERAN ANDA:
- Menghitung estimasi biaya umrah secara detail
- Memberikan analisis komponen biaya
- Merekomendasikan cara menghemat biaya
- Membuat proyeksi berbagai skenario

KEAHLIAN:
- Pemahaman mendalam tentang struktur biaya umrah
- Pengetahuan tentang variasi harga musiman
- Kemampuan analisis cost-benefit
- Pengalaman dalam perencanaan keuangan

FORMAT OUTPUT:
Berikan kalkulasi dalam format yang jelas:
1. Ringkasan total biaya
2. Breakdown per komponen
3. Perbandingan opsi (jika ada)
4. Rekomendasi optimasi

Gunakan mata uang Rupiah (IDR).
Selalu berikan range harga (minimum-maksimum) untuk fleksibilitas."""
    
    def calculate_cost(
        self,
        scenario: str,
        num_people: int = 1,
        duration_days: int = 9,
        departure_month: int = 6,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculate total umrah cost
        
        Args:
            scenario: Trip scenario
            num_people: Number of pilgrims
            duration_days: Trip duration
            departure_month: Month of departure
            context: RAG context
            
        Returns:
            Detailed cost breakdown
        """
        # Get calculation from calculator
        calculation = self.calculator.calculate(
            scenario=scenario,
            num_people=num_people,
            duration_days=duration_days,
            departure_month=departure_month
        )
        
        # Build query for AI analysis
        query = f"""Analisis dan jelaskan estimasi biaya umrah berikut:

PARAMETER:
- Skenario: {scenario}
- Jumlah Jamaah: {num_people} orang
- Durasi: {duration_days} hari
- Bulan Keberangkatan: {departure_month}

KALKULASI SISTEM:
{self._format_calculation(calculation)}

Tolong berikan:
1. Penjelasan setiap komponen biaya
2. Analisis apakah biaya ini wajar
3. Tips untuk optimasi biaya
4. Hal-hal yang perlu diperhatikan"""
        
        result = self.process(query, context)
        result["calculation"] = calculation
        
        return result
    
    def compare_scenarios(
        self,
        num_people: int = 1,
        duration_days: int = 12,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compare costs across different scenarios
        
        Args:
            num_people: Number of pilgrims
            duration_days: Trip duration
            context: RAG context
            
        Returns:
            Comparison analysis
        """
        comparisons = {}
        for scenario in ["ekonomis", "standard", "premium", "vip"]:
            comparisons[scenario] = self.calculator.calculate(
                scenario=scenario,
                num_people=num_people,
                duration_days=duration_days
            )
        
        query = f"""Bandingkan biaya umrah untuk {num_people} jamaah, {duration_days} hari:

{self._format_comparisons(comparisons)}

Berikan:
1. Analisis value for money setiap skenario
2. Rekomendasi berdasarkan budget
3. Perbedaan fasilitas yang signifikan
4. Saran skenario terbaik"""
        
        result = self.process(query, context)
        result["comparisons"] = comparisons
        
        return result
    
    def optimize_budget(
        self,
        budget: float,
        num_people: int,
        must_have: Optional[List[str]] = None,
        nice_to_have: Optional[List[str]] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Optimize trip within a given budget
        
        Args:
            budget: Total budget in IDR
            num_people: Number of pilgrims
            must_have: Required features
            nice_to_have: Optional features
            context: RAG context
            
        Returns:
            Optimization recommendations
        """
        query = f"""Optimasi perjalanan umrah dengan budget:

BUDGET: Rp {budget:,.0f}
JUMLAH JAMAAH: {num_people} orang
BUDGET PER ORANG: Rp {budget/num_people:,.0f}

FASILITAS WAJIB: {', '.join(must_have) if must_have else 'Tidak ada syarat khusus'}
FASILITAS DIINGINKAN: {', '.join(nice_to_have) if nice_to_have else 'Tidak ada'}

Tolong berikan:
1. Skenario optimal untuk budget ini
2. Alokasi budget per komponen
3. Fasilitas yang bisa didapat
4. Trade-off yang harus dipertimbangkan
5. Tips memaksimalkan budget"""
        
        return self.process(query, context)
    
    def create_savings_plan(
        self,
        target_cost: float,
        timeline_months: int,
        current_savings: float = 0,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a savings plan for umrah
        
        Args:
            target_cost: Target total cost
            timeline_months: Months until departure
            current_savings: Current savings amount
            context: RAG context
            
        Returns:
            Savings plan details
        """
        remaining = target_cost - current_savings
        monthly_target = remaining / timeline_months if timeline_months > 0 else remaining
        
        query = f"""Buatkan rencana tabungan umrah:

TARGET BIAYA: Rp {target_cost:,.0f}
TABUNGAN SAAT INI: Rp {current_savings:,.0f}
SISA YANG PERLU DITABUNG: Rp {remaining:,.0f}
WAKTU TERSEDIA: {timeline_months} bulan
TARGET BULANAN: Rp {monthly_target:,.0f}

Berikan:
1. Rencana tabungan bulanan yang realistis
2. Strategi menabung efektif
3. Opsi tabungan syariah yang direkomendasikan
4. Tips mengumpulkan dana lebih cepat
5. Milestone dan target per tahap"""
        
        result = self.process(query, context)
        result["savings_plan"] = {
            "target": target_cost,
            "current": current_savings,
            "remaining": remaining,
            "monthly": monthly_target,
            "timeline_months": timeline_months
        }
        
        return result
    
    def _format_calculation(self, calc: Dict) -> str:
        """Format calculation dict as string"""
        lines = []
        lines.append(f"Total: Rp {calc['total_min']:,.0f} - Rp {calc['total_max']:,.0f}")
        lines.append(f"\nBreakdown:")
        for item in calc["breakdown"]:
            lines.append(f"- {item['name']}: Rp {item['min']:,.0f} - Rp {item['max']:,.0f}")
        return "\n".join(lines)
    
    def _format_comparisons(self, comparisons: Dict) -> str:
        """Format comparison dict as string"""
        lines = []
        for scenario, calc in comparisons.items():
            template = SCENARIO_TEMPLATES.get(scenario, {})
            lines.append(f"\n{template.get('name', scenario).upper()}:")
            lines.append(f"  Total: Rp {calc['total_min']:,.0f} - Rp {calc['total_max']:,.0f}")
            lines.append(f"  Hotel: Bintang {template.get('hotel_star_makkah', 'N/A')}")
            lines.append(f"  Jarak ke Haram: {template.get('hotel_distance_makkah', 'N/A')}")
        return "\n".join(lines)


class UmrahCostCalculator:
    """Calculator for umrah costs"""
    
    def calculate(
        self,
        scenario: str,
        num_people: int = 1,
        duration_days: int = 9,
        departure_month: int = 6
    ) -> Dict[str, Any]:
        """
        Calculate detailed cost breakdown
        
        Args:
            scenario: Trip scenario
            num_people: Number of pilgrims
            duration_days: Trip duration
            departure_month: Month of departure
            
        Returns:
            Cost breakdown dictionary
        """
        template = SCENARIO_TEMPLATES.get(scenario, SCENARIO_TEMPLATES["standard"])
        
        # Get season multiplier
        multiplier = self._get_season_multiplier(departure_month)
        
        # Calculate each component
        breakdown = []
        
        # 1. Visa
        visa = COST_COMPONENTS["visa"]
        breakdown.append({
            "name": "Visa Umrah",
            "min": visa["base_price"] * num_people,
            "max": visa["base_price"] * num_people,
        })
        
        # 2. Tiket Pesawat
        tiket = COST_COMPONENTS["tiket_pesawat"].get(
            scenario, 
            COST_COMPONENTS["tiket_pesawat"]["standard"]
        )
        breakdown.append({
            "name": "Tiket Pesawat PP",
            "min": tiket["min"] * num_people * multiplier,
            "max": tiket["max"] * num_people * multiplier,
        })
        
        # 3. Hotel Makkah
        hotel_star = f"bintang_{template['hotel_star_makkah']}"
        if template['hotel_star_makkah'] == 5 and scenario == "vip":
            hotel_star = "bintang_5_premium"
        
        hotel_makkah = COST_COMPONENTS["hotel_makkah_per_night"].get(
            hotel_star,
            COST_COMPONENTS["hotel_makkah_per_night"]["bintang_3"]
        )
        makkah_nights = int(duration_days * 0.6)  # ~60% time in Makkah
        breakdown.append({
            "name": f"Hotel Makkah ({makkah_nights} malam)",
            "min": hotel_makkah["min"] * makkah_nights * num_people * multiplier,
            "max": hotel_makkah["max"] * makkah_nights * num_people * multiplier,
        })
        
        # 4. Hotel Madinah
        hotel_madinah_star = f"bintang_{template['hotel_star_madinah']}"
        if template['hotel_star_madinah'] == 5 and scenario == "vip":
            hotel_madinah_star = "bintang_5_premium"
        
        hotel_madinah = COST_COMPONENTS["hotel_madinah_per_night"].get(
            hotel_madinah_star,
            COST_COMPONENTS["hotel_madinah_per_night"]["bintang_3"]
        )
        madinah_nights = duration_days - makkah_nights - 1  # Remaining minus travel day
        breakdown.append({
            "name": f"Hotel Madinah ({madinah_nights} malam)",
            "min": hotel_madinah["min"] * madinah_nights * num_people * multiplier,
            "max": hotel_madinah["max"] * madinah_nights * num_people * multiplier,
        })
        
        # 5. Transportasi
        transport_type = template["transport_type"]
        transport = COST_COMPONENTS["transportasi"].get(
            transport_type,
            COST_COMPONENTS["transportasi"]["bus"]
        )
        breakdown.append({
            "name": "Transportasi Lokal",
            "min": transport["per_day"] * duration_days * num_people,
            "max": transport["per_day"] * duration_days * num_people * 1.2,
        })
        
        # 6. Makan
        meal_type = template["meal_type"]
        meals = COST_COMPONENTS["makan_per_day"].get(
            meal_type,
            COST_COMPONENTS["makan_per_day"]["prasmanan"]
        )
        breakdown.append({
            "name": f"Makan ({duration_days} hari)",
            "min": meals["min"] * duration_days * num_people,
            "max": meals["max"] * duration_days * num_people,
        })
        
        # 7. Muthawwif
        muthawwif_key = "premium_per_group" if scenario in ["premium", "vip"] else "base_per_group"
        muthawwif_cost = COST_COMPONENTS["muthawwif"][muthawwif_key]
        breakdown.append({
            "name": "Muthawwif/Guide",
            "min": muthawwif_cost,
            "max": muthawwif_cost * 1.5,
        })
        
        # 8. Perlengkapan
        perlengkapan_level = "premium" if scenario in ["premium", "vip"] else (
            "standard" if scenario == "standard" else "basic"
        )
        perlengkapan = COST_COMPONENTS["perlengkapan"][perlengkapan_level]
        breakdown.append({
            "name": "Perlengkapan",
            "min": perlengkapan["min"] * num_people,
            "max": perlengkapan["max"] * num_people,
        })
        
        # 9. Asuransi
        asuransi_level = "premium" if scenario in ["premium", "vip"] else (
            "standard" if scenario == "standard" else "basic"
        )
        asuransi = COST_COMPONENTS["asuransi"][asuransi_level]
        breakdown.append({
            "name": "Asuransi Perjalanan",
            "min": asuransi * num_people,
            "max": asuransi * num_people,
        })
        
        # 10. Handling Bandara
        handling_type = "vip" if scenario in ["premium", "vip"] else "standard"
        handling = COST_COMPONENTS["handling_bandara"][handling_type]
        breakdown.append({
            "name": "Handling Bandara",
            "min": handling * num_people,
            "max": handling * num_people,
        })
        
        # Calculate totals
        total_min = sum(item["min"] for item in breakdown)
        total_max = sum(item["max"] for item in breakdown)
        
        return {
            "scenario": scenario,
            "scenario_name": template["name"],
            "num_people": num_people,
            "duration_days": duration_days,
            "departure_month": departure_month,
            "season_multiplier": multiplier,
            "breakdown": breakdown,
            "total_min": total_min,
            "total_max": total_max,
            "per_person_min": total_min / num_people,
            "per_person_max": total_max / num_people,
        }
    
    def _get_season_multiplier(self, month: int) -> float:
        """Get price multiplier based on departure month"""
        for season_data in SEASONS.values():
            if month in season_data["months"]:
                return season_data["multiplier"]
        return 1.0
