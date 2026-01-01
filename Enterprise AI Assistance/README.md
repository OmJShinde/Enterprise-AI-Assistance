# Enterprise AI Assistant

## Overview
This is an Enterprise-grade AI Assistant capable of:
1.  **RAG**: Answering questions from internal PDFs/Policies.
2.  **Analytics**: Analyzing structured data (CSV/Excel) for trends.
3.  **Recommendations**: Providing strategic advice based on context.
4.  **Agentic Routing**: Automatically determining user intent.

## Architecture
- **Frontend**: Next.js 14, TailwindCSS.
- **Backend**: FastAPI, LangChain, OpenAI, ChromaDB, Pandas.

## Setup & Running

### Prerequisites
- Python 3.9+
- Node.js 18+
- OpenAI API Key (Put in `.env` file in `backend/` as `OPENAI_API_KEY=sk-...`)

### 1. Backend
```bash
cd backend
# Create virtual env (optional but recommended)
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt

# Run Server
python main.py
```
*Server runs on http://localhost:8000*

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```
*App runs on http://localhost:3000*

## Usage
1. Open the Frontend.
2. Upload a PDF (e.g., HR Policy) using the sidebar.
3. Upload a CSV (e.g., Sales Data) using the sidebar.
4.  Ask questions like:
    - "What is the probation period?" (Triggers RAG)
    - "Analyze the sales trend." (Triggers Analytics)
    - "Recommend a plan to improve sales." (Triggers Recommendation)
