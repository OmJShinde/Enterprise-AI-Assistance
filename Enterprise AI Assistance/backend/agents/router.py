import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from typing import Literal

class IntentRouter:
    def __init__(self):
        # Initialize LLM only if API key is present
        api_key = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo") if api_key else None
        
        self.prompt = PromptTemplate.from_template(
            """
            You are an Enterprise AI Assistant Router. Analyze the user's query and classify it into one of the following intents:
            
            1. DOCUMENT_QUERY: Questions that can be answered by looking up internal policies, SOPs, manuals, or training docs.
               Examples: "What is the leave policy?", "How do I claim expenses?", "Show me the safety guidelines."
            
            2. ANALYTICS_QUERY: Requests to analyze structured data, look for trends, statistics, or patterns in data (CSVs/Tables).
               Examples: "Analyze employee attrition trends.", "Which department has the lowest sales?", "Summarize performance metrics."
            
            3. ACTION_QUERY: Requests for recommendations, next steps, or decision support based on analysis.
               Examples: "What action should HR take based on these numbers?", "Recommend a strategy for retention."
            
            4. GENERAL: General conversation, greetings, or questions unrelated to enterprise data.
            
            Return ONLY the intent label (DOCUMENT_QUERY, ANALYTICS_QUERY, ACTION_QUERY, GENERAL).
            
            User Query: {query}
            Intent:
            """
        )

    def route(self, query: str) -> str:
        if not self.llm:
            return self._heuristic_route(query)
            
        try:
            chain = self.prompt | self.llm
            response = chain.invoke({"query": query})
            intent = response.content.strip().upper()
            valid_intents = ["DOCUMENT_QUERY", "ANALYTICS_QUERY", "ACTION_QUERY", "GENERAL"]
            
            if intent not in valid_intents:
                return "GENERAL"
            return intent
        except Exception as e:
            print(f"Routing Error: {e}")
            return self._heuristic_route(query)

    def _heuristic_route(self, query: str) -> str:
        """Fallback rule-based routing if LLM fails or is not configured."""
        query_lower = query.lower()
        
        analytics_keywords = ["analyze", "trend", "statistics", "data", "chart", "graph", "metrics", "count", "average"]
        doc_keywords = ["policy", "manual", "sop", "guideline", "rule", "leave", "probation", "document", "how to"]
        action_keywords = ["recommend", "suggest", "what should", "action", "plan", "strategy"]
        
        if any(k in query_lower for k in action_keywords):
            return "ACTION_QUERY"
        elif any(k in query_lower for k in analytics_keywords):
            return "ANALYTICS_QUERY"
        elif any(k in query_lower for k in doc_keywords):
            return "DOCUMENT_QUERY"
        else:
            return "GENERAL"
