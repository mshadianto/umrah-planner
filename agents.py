"""
LABBAIK Agent Orchestrator - Lightweight Version
=================================================
Uses Groq/OpenAI APIs directly without heavy ML dependencies.
No torch, transformers, sentence-transformers, or chromadb required.
"""

import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

# Try to import Groq
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    Groq = None

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None


@dataclass
class AgentResponse:
    """Response from an agent"""
    content: str
    agent_name: str
    success: bool
    metadata: Optional[Dict] = None


class BaseAgent:
    """Base agent using LLM APIs"""
    
    def __init__(self, name: str, system_prompt: str, provider: str = "groq"):
        self.name = name
        self.system_prompt = system_prompt
        self.provider = provider
        self.client = self._init_client()
    
    def _init_client(self):
        """Initialize LLM client based on provider"""
        if self.provider == "groq" and GROQ_AVAILABLE:
            api_key = os.getenv("GROQ_API_KEY", "")
            if api_key:
                return Groq(api_key=api_key)
        elif self.provider == "openai" and OPENAI_AVAILABLE:
            api_key = os.getenv("OPENAI_API_KEY", "")
            if api_key:
                return OpenAI(api_key=api_key)
        return None
    
    def run(self, query: str, context: Optional[str] = None) -> AgentResponse:
        """Run the agent with a query"""
        if not self.client:
            return AgentResponse(
                content="⚠️ API tidak tersedia. Pastikan API key sudah dikonfigurasi.",
                agent_name=self.name,
                success=False
            )
        
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            
            if context:
                messages.append({"role": "user", "content": f"Konteks: {context}\n\nPertanyaan: {query}"})
            else:
                messages.append({"role": "user", "content": query})
            
            # Select model based on provider
            if self.provider == "groq":
                model = "llama-3.3-70b-versatile"
            else:
                model = "gpt-4o-mini"
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=2000,
                temperature=0.7
            )
            
            return AgentResponse(
                content=response.choices[0].message.content,
                agent_name=self.name,
                success=True
            )
            
        except Exception as e:
            return AgentResponse(
                content=f"Error: {str(e)}",
                agent_name=self.name,
                success=False
            )


class UmrahPlannerAgent(BaseAgent):
    """Agent for Umrah planning assistance"""
    
    def __init__(self, provider: str = "groq"):
        system_prompt = """Anda adalah asisten perencana umrah yang ahli dan berpengalaman.
        
Tugas Anda:
- Membantu merencanakan perjalanan umrah
- Memberikan informasi tentang manasik, doa, dan tata cara ibadah
- Menyarankan hotel, transportasi, dan tips hemat
- Menjawab pertanyaan seputar visa dan regulasi
- Memberikan estimasi biaya yang realistis

Gaya komunikasi:
- Ramah dan informatif
- Gunakan bahasa Indonesia yang baik
- Sertakan emoji yang relevan
- Berikan jawaban yang terstruktur dan mudah dipahami

Selalu mulai dengan bismillah untuk pertanyaan tentang ibadah."""
        
        super().__init__("Umrah Planner", system_prompt, provider)


class BudgetAgent(BaseAgent):
    """Agent for budget planning and cost estimation"""
    
    def __init__(self, provider: str = "groq"):
        system_prompt = """Anda adalah ahli perencanaan keuangan untuk perjalanan umrah.

Keahlian Anda:
- Estimasi biaya umrah (tiket, hotel, visa, transportasi, makan)
- Tips menghemat biaya tanpa mengurangi kenyamanan
- Perbandingan harga berdasarkan musim
- Perencanaan tabungan untuk umrah

Format jawaban:
- Gunakan tabel atau list untuk breakdown biaya
- Sertakan range harga (minimum - maximum)
- Berikan tips hemat yang praktis
- Sebutkan mata uang dalam Rupiah (Rp)

Selalu berikan estimasi yang realistis berdasarkan kondisi terkini."""
        
        super().__init__("Budget Planner", system_prompt, provider)


class ManasikAgent(BaseAgent):
    """Agent for manasik and ibadah guidance"""
    
    def __init__(self, provider: str = "groq"):
        system_prompt = """Anda adalah ustadz/ustadzah yang ahli dalam manasik umrah dan haji.

Keahlian Anda:
- Tata cara umrah lengkap (ihram, tawaf, sa'i, tahallul)
- Doa-doa yang dibaca saat umrah
- Sunnah dan adab selama di tanah suci
- Ziarah ke tempat-tempat bersejarah
- Larangan dan hal yang membatalkan umrah

Gaya komunikasi:
- Penuh hikmah dan kelembutan
- Sertakan dalil jika relevan
- Gunakan transliterasi Arab yang mudah dibaca
- Berikan contoh praktis

Mulai setiap jawaban dengan Bismillah."""
        
        super().__init__("Manasik Guide", system_prompt, provider)


class TravelAgent(BaseAgent):
    """Agent for travel logistics and tips"""
    
    def __init__(self, provider: str = "groq"):
        system_prompt = """Anda adalah agen perjalanan berpengalaman untuk umrah.

Keahlian Anda:
- Pemilihan maskapai dan rute terbaik
- Rekomendasi hotel di Makkah dan Madinah
- Tips packing dan persiapan
- Informasi bandara dan imigrasi
- Transportasi lokal di Arab Saudi

Berikan informasi yang:
- Praktis dan up-to-date
- Mencakup berbagai budget (ekonomi hingga VIP)
- Mempertimbangkan kebutuhan khusus (lansia, anak-anak)
- Termasuk tips keamanan dan kenyamanan"""
        
        super().__init__("Travel Expert", system_prompt, provider)


class AgentOrchestrator:
    """Orchestrates multiple agents for comprehensive Umrah planning"""
    
    def __init__(self, provider: str = "groq"):
        self.provider = provider
        self.agents = {
            "planner": UmrahPlannerAgent(provider),
            "budget": BudgetAgent(provider),
            "manasik": ManasikAgent(provider),
            "travel": TravelAgent(provider)
        }
        self.conversation_history: List[Dict] = []
        self.is_initialized = False
    
    def initialize(self) -> Dict:
        """Initialize the orchestrator and all agents"""
        self.is_initialized = True
        return {"status": "success", "message": "Orchestrator initialized", "agents": list(self.agents.keys())}
    
    def detect_intent(self, query: str) -> str:
        """Detect user intent to route to appropriate agent"""
        query_lower = query.lower()
        
        # Budget-related keywords
        if any(word in query_lower for word in ["biaya", "harga", "budget", "murah", "hemat", "tabung", "estimasi", "berapa"]):
            return "budget"
        
        # Manasik-related keywords
        if any(word in query_lower for word in ["doa", "tawaf", "sai", "ihram", "manasik", "rukun", "wajib", "sunnah", "hukum"]):
            return "manasik"
        
        # Travel-related keywords
        if any(word in query_lower for word in ["hotel", "tiket", "pesawat", "visa", "packing", "bandara", "transportasi"]):
            return "travel"
        
        # Default to general planner
        return "planner"
    
    def run(self, query: str, context: Optional[str] = None) -> AgentResponse:
        """Run the appropriate agent based on query intent"""
        intent = self.detect_intent(query)
        agent = self.agents.get(intent, self.agents["planner"])
        
        # Add conversation context
        if self.conversation_history:
            recent_context = "\n".join([
                f"User: {h['query']}\nAssistant: {h['response'][:200]}..."
                for h in self.conversation_history[-3:]
            ])
            if context:
                context = f"{context}\n\nPercakapan sebelumnya:\n{recent_context}"
            else:
                context = f"Percakapan sebelumnya:\n{recent_context}"
        
        response = agent.run(query, context)
        
        # Store in history
        self.conversation_history.append({
            "query": query,
            "response": response.content,
            "agent": response.agent_name
        })
        
        return response
    
    def get_agent(self, agent_type: str) -> BaseAgent:
        """Get a specific agent by type"""
        return self.agents.get(agent_type, self.agents["planner"])
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


# ============================================
# COMPATIBILITY FUNCTIONS
# ============================================

def create_orchestrator(provider: str = "groq") -> AgentOrchestrator:
    """Factory function to create orchestrator"""
    return AgentOrchestrator(provider)


# Test function
if __name__ == "__main__":
    print("Testing AgentOrchestrator...")
    orchestrator = AgentOrchestrator()
    
    # Test intent detection
    test_queries = [
        "Berapa biaya umrah?",
        "Bagaimana cara tawaf?",
        "Rekomendasi hotel di Makkah?",
        "Bagaimana persiapan umrah?"
    ]
    
    for query in test_queries:
        intent = orchestrator.detect_intent(query)
        print(f"Query: {query}")
        print(f"Intent: {intent}")
        print("---")
