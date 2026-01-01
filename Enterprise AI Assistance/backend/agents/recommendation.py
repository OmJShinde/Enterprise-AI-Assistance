import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

class RecommendationAgent:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo") if api_key else None
        
        self.prompt = PromptTemplate.from_template(
            """
            You are a Strategic Business Advisor.
            
            User Context/Query: {query}
            
            Based on general business best practices (and any provided context), provide a clear, actionable recommendation.
            Format your response as:
            1. Observation
            2. Recommended Action
            3. Expected Outcome
            
            Recommendation:
            """
        )

    def recommend(self, query: str) -> str:
        if not self.llm:
            return "Recommendation Engine Unavailable (No API Key)."
            
        chain = self.prompt | self.llm
        res = chain.invoke({"query": query})
        return res.content
