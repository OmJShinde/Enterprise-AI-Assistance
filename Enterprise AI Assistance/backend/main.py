import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

from agents.router import IntentRouter
from agents.rag import RAGAgent
from agents.analytics import AnalyticsAgent
from agents.recommendation import RecommendationAgent
from utils.logger import setup_logger

load_dotenv()

# Setup Logger
logger = setup_logger("api_main")

app = FastAPI(title="Enterprise AI Assistant API")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agents
router = IntentRouter()
rag_agent = RAGAgent()
analytics_agent = AnalyticsAgent()
rec_agent = RecommendationAgent()

# Directories
os.makedirs("data/documents", exist_ok=True)
os.makedirs("data/structured", exist_ok=True)

class QueryRequest(BaseModel):
    query: str
    context_id: Optional[str] = None

@app.get("/")
def health_check():
    return {
        "status": "active", 
        "system": "Enterprise AI Assistant V2 (Agentic)",
        "capabilities": ["RAG", "Analytics", "Recommendations"]
    }

@app.post("/api/upload/document")
async def upload_document(file: UploadFile = File(...)):
    """Upload PDF/Text for RAG"""
    path = f"data/documents/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Ingest immediately
    result = rag_agent.ingest_document(path)
    return {"filename": file.filename, "status": "uploaded", "ingestion": result}

@app.post("/api/upload/data")
async def upload_data(file: UploadFile = File(...)):
    """Upload CSV/Excel for Analytics"""
    path = f"data/structured/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Load into agent
    result = analytics_agent.load_data(path)
    return {"filename": file.filename, "status": "uploaded", "load_result": result}

@app.post("/api/chat")
def chat_endpoint(request: QueryRequest):
    """
    Intelligent Agent Router
    """
    user_query = request.query
    logger.info(f"Received query: {user_query}")
    
    # 1. Determine Intent
    intent = router.route(user_query)
    logger.info(f"Detected Intent: {intent}")
    
    response_text = ""
    
    try:
        # 2. Route
        if "DOCUMENT" in intent:
            response_text = rag_agent.answer_query(user_query)
            
        elif "ANALYTICS" in intent:
            response_text = analytics_agent.analyze(user_query)
            
        elif "ACTION" in intent:
            # For action, we might validly want to check data or docs first?
            # For simple version, just go to Rec Agent
            response_text = rec_agent.recommend(user_query)
            
        else: # GENERAL
            # Just use Rec agent as a fallback chatter or return a polite message
            # But maybe we want the RAG agent's LLM to handle chit-chat?
            # Using Rec agent for now for generic "Advisor" persona
            response_text = rec_agent.recommend(user_query)
            
        logger.info("Request processed successfully.")
            
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "intent": intent,
        "response": response_text
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
