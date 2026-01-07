# Enterprise AI Assistance - Quick Start Guide

## 🚀 Running the Project

### Method 1: Using Batch Scripts (Easiest)

1. **Start Backend**: Double-click `start-backend.bat`
2. **Start Frontend**: Double-click `start-frontend.bat`

### Method 2: Manual Commands

Open **TWO separate PowerShell terminals**:

**Terminal 1 - Backend:**
```powershell
cd "D:\projects\Enterprise AI Assistance\backend"
.\venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend:**
```powershell
cd "D:\projects\Enterprise AI Assistance\frontend"
npm run dev
```

## 🌐 Access URLs

- **Frontend (Main App)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 First Time Setup

Only run these commands the FIRST time you set up the project:

### Backend Setup
```powershell
cd "D:\projects\Enterprise AI Assistance\backend"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup
```powershell
cd "D:\projects\Enterprise AI Assistance\frontend"
npm install
```

## 🛑 Stopping the Servers

- Press `CTRL+C` in each terminal window
- Or close the terminal windows

## ⚠️ Troubleshooting

### Port Already in Use

If you get "port already in use" error:

**Find processes using ports:**
```powershell
netstat -ano | findstr :3000
netstat -ano | findstr :8000
```

**Kill the process (replace PID with actual process ID):**
```powershell
taskkill /PID <PID> /F
```

### Module Not Found Errors

Reinstall dependencies:
```powershell
cd backend
.\venv\Scripts\activate
pip install --force-reinstall -r requirements.txt
```

### Pydantic/Import Errors

```powershell
cd backend
.\venv\Scripts\activate
pip uninstall -y pydantic pydantic-core
pip install pydantic
pip install --force-reinstall -r requirements.txt
```

## 📁 Project Structure

```
Enterprise AI Assistance/
├── backend/              # FastAPI backend
│   ├── agents/          # AI agents (RAG, Analytics, etc.)
│   ├── utils/           # Utilities
│   ├── main.py          # Backend entry point
│   └── requirements.txt # Python dependencies
├── frontend/            # Next.js frontend
│   ├── src/            # Source code
│   └── package.json    # Node dependencies
├── start-backend.bat   # Backend launcher
└── start-frontend.bat  # Frontend launcher
```

## 🔑 Environment Variables

Create a `.env` file in the `backend` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 📝 Features

- **RAG (Retrieval Augmented Generation)**: Answer questions from uploaded documents
- **Analytics Agent**: Analyze CSV/Excel data with natural language queries
- **Recommendation Agent**: Get intelligent recommendations
- **Intent Routing**: Automatically routes queries to the appropriate agent

## 💡 Usage Tips

1. Always start the backend BEFORE the frontend
2. Keep both terminals open while using the application
3. Check the API documentation at http://localhost:8000/docs for available endpoints
4. Upload documents via the frontend interface or API

## 🆘 Need Help?

Check the logs in the terminal windows for error messages. Most issues are related to:
- Missing dependencies (run pip install/npm install)
- Port conflicts (kill existing processes)
- Missing environment variables (check .env file)
