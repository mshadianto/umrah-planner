"""
Base Agent Module
=================
Base class for all agents in the system
Using Groq API only
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import os

from groq import Groq

from config import llm_config


class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, name: str, description: str):
        """
        Initialize base agent
        
        Args:
            name: Agent name
            description: Agent description/role
        """
        self.name = name
        self.description = description
        self.conversation_history = []
        
        # Initialize Groq client
        self.client = Groq(api_key=llm_config.groq_api_key)
        self.model = llm_config.groq_model
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        pass
    
    def call_llm(
        self,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """
        Call the LLM with messages
        
        Args:
            messages: List of message dicts with role and content
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            LLM response text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
    
    def process(
        self,
        query: str,
        context: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process a query
        
        Args:
            query: User query
            context: Optional context from RAG
            **kwargs: Additional parameters
            
        Returns:
            Agent response dict
        """
        # Build messages
        messages = [
            {"role": "system", "content": self.get_system_prompt()}
        ]
        
        # Add context if provided
        if context:
            messages.append({
                "role": "system",
                "content": f"Konteks dari knowledge base:\n{context}"
            })
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        # Add current query
        messages.append({"role": "user", "content": query})
        
        # Get response
        response = self.call_llm(messages)
        
        # Update history
        self.conversation_history.append({"role": "user", "content": query})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Keep history manageable (last 10 exchanges)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        return {
            "agent": self.name,
            "response": response,
            "query": query,
            "has_context": context is not None
        }
    
    def reset_history(self):
        """Reset conversation history"""
        self.conversation_history = []