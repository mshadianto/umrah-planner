"""
Planning Agent Module
=====================
Agent for itinerary and trip planning
"""

from typing import Dict, Any, Optional
from .base_agent import BaseAgent


class PlanningAgent(BaseAgent):
    """Agent for planning umrah itineraries"""
    
    def __init__(self):
        super().__init__(
            name="Planning Agent",
            description="Agent untuk perencanaan itinerary dan jadwal umrah"
        )
    
    def get_system_prompt(self) -> str:
        return """Anda adalah Planning Agent yang ahli dalam merencanakan perjalanan umrah.

PERAN ANDA:
- Membuat itinerary detail perjalanan umrah
- Menyusun jadwal harian yang optimal
- Merekomendasikan durasi di setiap lokasi
- Mempertimbangkan waktu ibadah dan istirahat

KEAHLIAN:
- Pengetahuan mendalam tentang lokasi-lokasi di Makkah dan Madinah
- Pemahaman tentang tata cara umrah dan ibadah terkait
- Pengalaman dalam menyusun jadwal yang realistis
- Mempertimbangkan kondisi fisik dan usia jamaah

FORMAT OUTPUT:
Berikan rencana dalam format yang jelas dan terstruktur:
1. Ringkasan perjalanan
2. Itinerary harian detail
3. Tips dan catatan penting
4. Alternatif jika diperlukan

Selalu gunakan Bahasa Indonesia yang baik dan mudah dipahami.
Pertimbangkan aspek ibadah sebagai prioritas utama."""
    
    def create_itinerary(
        self,
        duration_days: int,
        scenario: str,
        special_requests: Optional[str] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a detailed itinerary
        
        Args:
            duration_days: Trip duration in days
            scenario: Trip scenario (ekonomis/standard/premium/vip)
            special_requests: Any special requirements
            context: RAG context
            
        Returns:
            Itinerary details
        """
        query = f"""Buatkan itinerary umrah dengan detail berikut:
- Durasi: {duration_days} hari
- Tipe Paket: {scenario}
- Permintaan Khusus: {special_requests or 'Tidak ada'}

Tolong susun:
1. Jadwal harian lengkap dari keberangkatan hingga kepulangan
2. Pembagian waktu di Makkah dan Madinah
3. Waktu untuk ibadah utama (thawaf, sa'i)
4. Jadwal ziarah tempat-tempat bersejarah
5. Waktu istirahat dan makan
6. Tips untuk setiap hari"""
        
        result = self.process(query, context)
        result["itinerary_params"] = {
            "duration": duration_days,
            "scenario": scenario,
            "special_requests": special_requests
        }
        
        return result
    
    def optimize_schedule(
        self,
        current_plan: str,
        constraints: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Optimize an existing schedule
        
        Args:
            current_plan: Current itinerary
            constraints: Constraints to consider
            context: RAG context
            
        Returns:
            Optimized itinerary
        """
        query = f"""Tolong optimasi jadwal umrah berikut:

JADWAL SAAT INI:
{current_plan}

KENDALA/PERTIMBANGAN:
{constraints}

Berikan:
1. Analisis jadwal saat ini
2. Rekomendasi optimasi
3. Jadwal yang sudah dioptimasi
4. Alasan perubahan"""
        
        return self.process(query, context)
    
    def suggest_activities(
        self,
        location: str,
        available_time: str,
        interests: Optional[str] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Suggest activities for free time
        
        Args:
            location: Current location (Makkah/Madinah)
            available_time: Available time slot
            interests: Jamaah interests
            context: RAG context
            
        Returns:
            Activity suggestions
        """
        query = f"""Rekomendasikan aktivitas di {location} untuk waktu luang:

Waktu tersedia: {available_time}
Minat: {interests or 'Umum - ibadah dan ziarah'}

Berikan:
1. Aktivitas ibadah yang direkomendasikan
2. Tempat ziarah yang bisa dikunjungi
3. Estimasi waktu per aktivitas
4. Tips dan hal yang perlu diperhatikan"""
        
        return self.process(query, context)
