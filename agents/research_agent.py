"""
Research Agent Module
=====================
Agent for information research and retrieval
"""

from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    """Agent for researching umrah information"""
    
    def __init__(self):
        super().__init__(
            name="Research Agent",
            description="Agent untuk riset informasi dan pengetahuan umrah"
        )
    
    def get_system_prompt(self) -> str:
        return """Anda adalah Research Agent yang ahli dalam memberikan informasi tentang umrah.

PERAN ANDA:
- Menjawab pertanyaan seputar umrah dengan akurat
- Memberikan informasi berdasarkan sumber terpercaya
- Menjelaskan prosedur dan tata cara ibadah
- Memberikan tips dan saran praktis

KEAHLIAN:
- Pengetahuan tentang fiqih ibadah umrah
- Informasi tentang Arab Saudi dan fasilitas
- Pemahaman tentang peraturan dan persyaratan
- Pengetahuan praktis perjalanan

FORMAT OUTPUT:
1. Jawaban langsung dan jelas
2. Penjelasan detail jika diperlukan
3. Sumber atau referensi (jika dari knowledge base)
4. Tips praktis terkait

Gunakan Bahasa Indonesia yang baik dan mudah dipahami.
Jika tidak yakin, sampaikan dengan jujur dan sarankan untuk konfirmasi."""
    
    def answer_question(
        self,
        question: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Answer a question about umrah
        
        Args:
            question: User question
            context: RAG context
            
        Returns:
            Answer with sources
        """
        return self.process(question, context)
    
    def explain_procedure(
        self,
        procedure: str,
        detail_level: str = "standard",
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Explain an umrah procedure
        
        Args:
            procedure: Procedure name (e.g., "thawaf", "sa'i", "ihram")
            detail_level: Level of detail (basic/standard/detailed)
            context: RAG context
            
        Returns:
            Procedure explanation
        """
        detail_instructions = {
            "basic": "Jelaskan secara singkat dan sederhana",
            "standard": "Jelaskan dengan detail yang cukup",
            "detailed": "Jelaskan secara mendetail termasuk dalil dan variasi pendapat"
        }
        
        query = f"""Jelaskan prosedur {procedure} dalam umrah.

Tingkat Detail: {detail_instructions.get(detail_level, detail_instructions['standard'])}

Tolong jelaskan:
1. Pengertian dan hukumnya
2. Tata cara pelaksanaan step-by-step
3. Doa-doa yang dibaca
4. Hal-hal yang membatalkan (jika ada)
5. Tips praktis"""
        
        return self.process(query, context)
    
    def get_travel_requirements(
        self,
        traveler_type: str = "dewasa",
        special_conditions: Optional[List[str]] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get travel requirements
        
        Args:
            traveler_type: Type of traveler (dewasa/lansia/anak/wanita_tanpa_mahram)
            special_conditions: Special conditions (hamil/disabilitas/dll)
            context: RAG context
            
        Returns:
            Requirements list
        """
        conditions_str = ", ".join(special_conditions) if special_conditions else "Tidak ada"
        
        query = f"""Berikan persyaratan perjalanan umrah untuk:

Tipe Jamaah: {traveler_type}
Kondisi Khusus: {conditions_str}

Jelaskan:
1. Dokumen yang diperlukan
2. Persyaratan kesehatan
3. Persyaratan khusus (jika ada)
4. Hal yang perlu dipersiapkan
5. Tips khusus untuk kategori ini"""
        
        return self.process(query, context)
    
    def compare_options(
        self,
        option_type: str,
        options: List[str],
        criteria: Optional[List[str]] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compare different options
        
        Args:
            option_type: Type of comparison (hotel/maskapai/travel/dll)
            options: List of options to compare
            criteria: Comparison criteria
            context: RAG context
            
        Returns:
            Comparison analysis
        """
        criteria_str = ", ".join(criteria) if criteria else "harga, kualitas, lokasi"
        options_str = ", ".join(options)
        
        query = f"""Bandingkan opsi {option_type} berikut:

Opsi: {options_str}
Kriteria Perbandingan: {criteria_str}

Berikan:
1. Tabel perbandingan
2. Kelebihan masing-masing
3. Kekurangan masing-masing
4. Rekomendasi berdasarkan profil berbeda"""
        
        return self.process(query, context)
    
    def get_tips(
        self,
        topic: str,
        traveler_profile: Optional[str] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get tips on a specific topic
        
        Args:
            topic: Tips topic
            traveler_profile: Traveler profile for personalization
            context: RAG context
            
        Returns:
            Tips and recommendations
        """
        profile_str = f"Profil Jamaah: {traveler_profile}" if traveler_profile else ""
        
        query = f"""Berikan tips tentang {topic} untuk perjalanan umrah.

{profile_str}

Berikan:
1. Tips utama yang paling penting
2. Hal-hal yang harus dihindari
3. Rekomendasi praktis
4. Pengalaman umum jamaah"""
        
        return self.process(query, context)
    
    def validate_travel_agent(
        self,
        agent_info: Dict[str, Any],
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate travel agent legitimacy
        
        Args:
            agent_info: Travel agent information
            context: RAG context
            
        Returns:
            Validation analysis
        """
        info_str = "\n".join(f"- {k}: {v}" for k, v in agent_info.items())
        
        query = f"""Bantu evaluasi travel umrah berikut:

{info_str}

Analisis:
1. Red flags yang perlu diwaspadai
2. Checklist verifikasi legalitas
3. Pertanyaan yang harus ditanyakan ke travel
4. Rekomendasi langkah verifikasi
5. Tanda-tanda travel yang terpercaya vs bermasalah"""
        
        return self.process(query, context)
