"""
Agent Orchestrator Module
=========================
Coordinates multiple agents for complex tasks
"""

from typing import Dict, Any, Optional, List
from .planning_agent import PlanningAgent
from .financial_agent import FinancialAgent
from .research_agent import ResearchAgent
from .base_agent import BaseAgent
from rag import RAGRetriever


class AgentOrchestrator:
    """Orchestrates multiple agents for comprehensive umrah planning"""
    
    def __init__(self):
        """Initialize all agents and RAG retriever"""
        self.planning_agent = PlanningAgent()
        self.financial_agent = FinancialAgent()
        self.research_agent = ResearchAgent()
        self.rag_retriever = RAGRetriever()
        
        # Intent classification keywords
        self.intent_keywords = {
            "planning": [
                "jadwal", "itinerary", "rencana", "kapan", "berapa hari",
                "schedule", "plan", "aktivitas", "kegiatan"
            ],
            "financial": [
                "biaya", "harga", "budget", "tabung", "cicilan", "hemat",
                "murah", "mahal", "cost", "rupiah", "bayar", "dana"
            ],
            "research": [
                "apa", "bagaimana", "mengapa", "syarat", "dokumen",
                "prosedur", "cara", "tips", "hotel", "visa", "pesawat",
                "persiapan", "bawa", "perlengkapan"
            ],
        }
    
    def initialize(self) -> Dict[str, Any]:
        """
        Initialize the orchestrator and RAG system
        
        Returns:
            Initialization status
        """
        doc_count = self.rag_retriever.initialize()
        return {
            "status": "success",
            "documents_loaded": doc_count,
            "agents_ready": [
                self.planning_agent.name,
                self.financial_agent.name,
                self.research_agent.name,
            ]
        }
    
    def process_query(
        self,
        query: str,
        use_rag: bool = True
    ) -> Dict[str, Any]:
        """
        Process a user query by routing to appropriate agent
        
        Args:
            query: User query
            use_rag: Whether to use RAG for context
            
        Returns:
            Agent response
        """
        # Get RAG context if enabled
        context = None
        if use_rag:
            context = self.rag_retriever.build_context(query)
        
        # Classify intent and route to appropriate agent
        intent = self._classify_intent(query)
        
        if intent == "planning":
            agent = self.planning_agent
        elif intent == "financial":
            agent = self.financial_agent
        else:
            agent = self.research_agent
        
        # Process with selected agent
        result = agent.process(query, context)
        result["intent"] = intent
        result["rag_used"] = use_rag
        
        return result
    
    def create_complete_plan(
        self,
        scenario: str,
        num_people: int,
        duration_days: int,
        departure_month: int,
        special_requests: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a complete umrah plan using all agents
        
        Args:
            scenario: Trip scenario
            num_people: Number of pilgrims
            duration_days: Trip duration
            departure_month: Month of departure
            special_requests: Special requirements
            
        Returns:
            Complete plan with itinerary and costs
        """
        # Get general context
        context = self.rag_retriever.build_context(
            f"umrah {scenario} {duration_days} hari"
        )
        
        results = {}
        
        # 1. Financial calculation
        results["financial"] = self.financial_agent.calculate_cost(
            scenario=scenario,
            num_people=num_people,
            duration_days=duration_days,
            departure_month=departure_month,
            context=context
        )
        
        # 2. Itinerary planning
        results["itinerary"] = self.planning_agent.create_itinerary(
            duration_days=duration_days,
            scenario=scenario,
            special_requests=special_requests,
            context=context
        )
        
        # 3. Requirements research
        results["requirements"] = self.research_agent.get_travel_requirements(
            context=context
        )
        
        # 4. Tips
        results["tips"] = self.research_agent.get_tips(
            topic=f"perjalanan umrah {scenario}",
            context=context
        )
        
        return {
            "plan_type": "complete",
            "parameters": {
                "scenario": scenario,
                "num_people": num_people,
                "duration_days": duration_days,
                "departure_month": departure_month,
                "special_requests": special_requests
            },
            "results": results
        }
    
    def compare_scenarios(
        self,
        num_people: int,
        duration_days: int
    ) -> Dict[str, Any]:
        """
        Compare all scenarios for decision making
        
        Args:
            num_people: Number of pilgrims
            duration_days: Trip duration
            
        Returns:
            Scenario comparison
        """
        context = self.rag_retriever.build_context("paket umrah perbandingan")
        
        return self.financial_agent.compare_scenarios(
            num_people=num_people,
            duration_days=duration_days,
            context=context
        )
    
    def get_recommendations(
        self,
        budget: float,
        num_people: int,
        preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get personalized recommendations
        
        Args:
            budget: Total budget
            num_people: Number of pilgrims
            preferences: User preferences
            
        Returns:
            Personalized recommendations
        """
        # Build preference query
        pref_str = ""
        if preferences:
            pref_items = []
            if preferences.get("hotel_priority"):
                pref_items.append(f"prioritas hotel: {preferences['hotel_priority']}")
            if preferences.get("comfort_level"):
                pref_items.append(f"tingkat kenyamanan: {preferences['comfort_level']}")
            if preferences.get("special_needs"):
                pref_items.append(f"kebutuhan khusus: {preferences['special_needs']}")
            pref_str = ", ".join(pref_items)
        
        context = self.rag_retriever.build_context(
            f"rekomendasi umrah budget {budget} {pref_str}"
        )
        
        # Get financial optimization
        must_have = preferences.get("must_have", []) if preferences else None
        nice_to_have = preferences.get("nice_to_have", []) if preferences else None
        
        return self.financial_agent.optimize_budget(
            budget=budget,
            num_people=num_people,
            must_have=must_have,
            nice_to_have=nice_to_have,
            context=context
        )
    
    def chat(
        self,
        message: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Handle a chat message
        
        Args:
            message: User message
            conversation_id: Optional conversation identifier
            
        Returns:
            Chat response
        """
        return self.process_query(message)
    
    def reset_conversations(self):
        """Reset all agent conversation histories"""
        self.planning_agent.reset_history()
        self.financial_agent.reset_history()
        self.research_agent.reset_history()
    
    def _classify_intent(self, query: str) -> str:
        """
        Classify the intent of a query
        
        Args:
            query: User query
            
        Returns:
            Intent category
        """
        query_lower = query.lower()
        
        scores = {intent: 0 for intent in self.intent_keywords}
        
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    scores[intent] += 1
        
        # Return intent with highest score, default to research
        max_intent = max(scores, key=scores.get)
        return max_intent if scores[max_intent] > 0 else "research"
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            "planning_agent": {
                "name": self.planning_agent.name,
                "history_length": len(self.planning_agent.conversation_history)
            },
            "financial_agent": {
                "name": self.financial_agent.name,
                "history_length": len(self.financial_agent.conversation_history)
            },
            "research_agent": {
                "name": self.research_agent.name,
                "history_length": len(self.research_agent.conversation_history)
            },
            "rag_retriever": self.rag_retriever.get_statistics()
        }
