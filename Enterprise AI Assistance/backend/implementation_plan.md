# Enterprise AI Assistant - Backend Implementation Plan

## 1. Core Architecture
The backend will be modularized into Agents, each responsible for a specific domain.

### Directory Structure
```
backend/
├── agents/
│   ├── __init__.py
│   ├── router.py       # Intent classification (LLM-based)
│   ├── rag.py          # Document retrieval & generation
│   ├── analytics.py    # Structured data analysis (Pandas + LLM)
│   └── recommendation.py # Synthesis & action suggestions
├── services/
│   ├── speech.py       # (Optional) STT/TTS
│   └── vector_store.py # Vector DB management
├── data/
│   ├── documents/      # PDF/Docx storage
│   └── structured/     # CSV/Excel storage
├── main.py             # FastAPI entry point
└── requirements.txt
```

## 2. Capabilities Implementation

### 2.1 Intent-Aware Router (`agents/router.py`)
- **Input**: User query string.
- **Logic**: Uses a lightweight LLM prompt to classify intent into:
  - `DOCUMENT_QUERY`: Questions about policies, SOPs.
  - `ANALYTICS_QUERY`: Questions about data trends, stats.
  - `ACTION_QUERY`: Requests for recommendations or decisions.
  - `GENERAL`: Conversational filler.

### 2.2 RAG Agent (`agents/rag.py`)
- **Stack**: LangChain + FAISS/Chroma + OpenAI/Gemini Embeddings.
- **Flow**:
  1. Load PDFs from `data/documents/`.
  2. Chunk and embed.
  3. Retrieve top-k chunks.
  4. Generate answer with source attribution.

### 2.3 Analytics Agent (`agents/analytics.py`)
- **Stack**: Pandas + LLM Agent (PandasAI or custom).
- **Flow**:
  1. Load CSVs from `data/structured/`.
  2. Generate Python code or reasoning to extract insights.
  3. Return textual summary of trends.

### 2.4 Recommendation Engine (`agents/recommendation.py`)
- **Logic**: logical synthesis of RAG context + Analytics insights to propose actions.

## 3. Next Steps
1. Install dependencies (`langchain`, `openai`, `faiss-cpu`, `pandas`).
2. Implement `router.py` first.
3. specific implementations for RAG and Analytics.
