import os
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

class AnalyticsAgent:
    def __init__(self):
        self.active_df = None
        api_key = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(temperature=0, model="gpt-4") if api_key else None 
        # GPT-4 is recommended for coding agents, 3.5 is weak with pandas

    def load_data(self, file_path: str):
        try:
            if file_path.endswith(".csv"):
                self.active_df = pd.read_csv(file_path)
            elif file_path.endswith(".xlsx"):
                self.active_df = pd.read_excel(file_path)
            return f"Loaded data with {len(self.active_df)} rows and columns: {list(self.active_df.columns)}"
        except Exception as e:
            return f"Error loading data: {str(e)}"

    def analyze(self, query: str) -> str:
        if self.active_df is None:
            return "No data loaded. Please upload a dataset first."
            
        if not self.llm:
            # Fallback: Basic stats
            desc = self.active_df.describe().to_string()
            return f"LLM not available. Here are the basic statistics:\n{desc}"

        agent = create_pandas_dataframe_agent(
            self.llm, 
            self.active_df, 
            verbose=True,
            allow_dangerous_code=True, # Required for exec-based agents
            handle_parsing_errors=True
        )
        
        try:
            response = agent.invoke(query)
            return response['output']
        except Exception as e:
            return f"Analysis failed: {str(e)}"
