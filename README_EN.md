# 🐺 AI Werewolf | AI狼人杀

> An intelligent Werewolf game based on AI Agents, where AI players engage in reasoning, deception, and competition

English | [简体中文](README.md)

## ✨ Introduction

AI Werewolf is an innovative Werewolf game project that uses AI Agent technology to enable multiple AI players to autonomously reason, speak, and vote. Each AI player has independent thinking ability, memory system, and behavioral strategy, capable of engaging in real game matches.

### 🎯 Key Features

- **🤖 Intelligent AI Players** - Smart agents based on large language models, capable of reasoning and deception
- **🎭 Characterized Roles** - Each AI has unique personality and speaking style (rational, aggressive, humorous)
- **🎬 High Entertainment Value** - The dialogue and reasoning between AIs are captivating content
- **🏗️ Modular Architecture** - Clear code organization, easy to extend and maintain
- **🌐 Web Interface** - Modern web interface for real-time observation of AI matches
- **🔊 Text-to-Speech** - Support for Qwen TTS to voice AI characters

## 🚀 Quick Start

### Requirements

- Python 3.8+
- Node.js 16+
- LLM API Key (OpenAI, Qwen, or other compatible services)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yyvk/ai-werewolf.git
cd ai-werewolf

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp env.example.txt .env
# Edit .env file and fill in your API keys

# 4. Install frontend dependencies
cd frontend
npm install
cd ..
```

### Configure API Keys

Configure LLM API in `.env` file:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o-mini

# Or use Qwen (Alibaba Cloud)
DASHSCOPE_API_KEY=your-api-key-here
DASHSCOPE_MODEL=qwen-turbo

# Or use ModelScope
OPENAI_API_KEY=your-modelscope-token
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1
OPENAI_MODEL=Qwen/Qwen2.5-7B-Instruct
```

### Start the Project

#### Method 1: Using Start Scripts (Recommended)

**Windows PowerShell:**
```powershell
# Start backend
.\start_backend.ps1

# Start frontend (new terminal)
cd frontend
.\start.ps1
```

**Linux/Mac:**
```bash
# Start backend
python main.py

# Start frontend (new terminal)
cd frontend
npm run dev
```

#### Method 2: Manual Start

**Start Backend API Service:**
```bash
python main.py
```

Backend service addresses:
- API Service: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

**Start Frontend Web Interface:**
```bash
cd frontend
npm run dev
```

Frontend service address: http://localhost:3000

### Start Playing

1. Open browser and visit http://localhost:3000
2. Click **"Create New Game"** button
3. Configure game parameters (number of players, role configuration, etc.)
4. Click **"Create Game"** and enter the game room
5. Click **"Start Game"** to let AI begin the match
6. Click **"Next Round"** to advance the game

## 📁 Project Structure

```
ai-werewolf/
├── src/                    # Source code
│   ├── core/              # Core game logic
│   │   ├── models.py      # Data models
│   │   ├── game_engine.py # Game engine
│   │   └── event_system.py# Event system
│   ├── agents/            # AI Agent implementation
│   │   ├── base_agent.py  # Agent base class
│   │   ├── langchain_agent.py # LangChain implementation
│   │   └── agent_factory.py # Agent factory
│   ├── database/          # Database interface layer
│   ├── web/              # Web API service
│   ├── video/            # Video generation module
│   └── utils/            # Utilities and configuration
├── frontend/             # Frontend web interface
│   ├── src/             # Source code
│   │   ├── components/  # Vue components
│   │   ├── views/       # Page views
│   │   ├── stores/      # State management
│   │   └── api/         # API interface
│   └── public/          # Static assets
├── data/                # Data directory
│   ├── games/          # Game records
│   ├── logs/           # Log files
│   └── cache/          # Cache data
├── assets/             # Resource files
├── config/             # Configuration files
└── docs/               # Documentation
```

## 🏗️ Technical Architecture

### Architecture Style

- **Modular Design** - 6 core modules with clear responsibilities
- **Event-Driven** - Support for real-time response and state updates
- **Agent Architecture** - Each AI player is an independent agent

### Tech Stack

| Layer | Technology |
|-------|-----------|
| AI/LLM | LangChain, OpenAI, Qwen, ModelScope |
| Web Framework | FastAPI, Uvicorn, WebSocket |
| Frontend | Vue 3, Vite, Pinia, Vue Router |
| Database | JSON file storage, ChromaDB (planned), Redis (planned) |
| Text-to-Speech | DashScope TTS (Qwen) |
| Video Processing | MoviePy (planned), OpenCV (planned) |

### Architecture Diagram

```
┌─────────────────────────────────────────────┐
│        Client Layer (Web Browser)           │
│         Vue 3 + Vite + Axios                │
└───────────────────┬─────────────────────────┘
                    │ HTTP/WebSocket
┌───────────────────┴─────────────────────────┐
│           API Layer (FastAPI)                │
│     REST API + WebSocket                    │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────┴─────────────────────────┐
│      Business Logic Layer                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │Game      │  │AI Agent  │  │Event     │  │
│  │Engine    │  │LangChain │  │System    │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────┴─────────────────────────┐
│         Data Access Layer                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │Game      │  │Cache DB  │  │Vector DB │  │
│  │Repo JSON │  │Memory    │  │(planned) │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────┴─────────────────────────┐
│      External Services Layer                 │
│     OpenAI / Qwen / ModelScope              │
└─────────────────────────────────────────────┘
```

## 🎮 Features

### Implemented ✅

- ✅ Complete Werewolf game rule engine (6/9 players)
- ✅ AI Agent system based on LangChain
- ✅ Multiple roles: Werewolf, Villager, Seer, Witch, Hunter
- ✅ Three AI personalities: Rational, Aggressive, Humorous
- ✅ RESTful API interface
- ✅ WebSocket real-time communication (planned)
- ✅ Vue 3 frontend interface
- ✅ Game state persistence (JSON)
- ✅ Event system and game replay
- ✅ TTS voice synthesis (Qwen)

### In Development 🚧

- 🚧 WebSocket real-time game state push
- 🚧 Multi-room support
- 🚧 Game video generation
- 🚧 Automatic highlight clip extraction
- 🚧 Player participation in games (1 player + N AIs)

### Planned 📋

- 📋 Vector database integration (ChromaDB)
- 📋 Redis cache layer
- 📋 More game modes (White Werewolf King, Guard, etc.)
- 📋 AI learning and evolution
- 📋 Social features (sharing, comments)
- 📋 Mobile adaptation

## 🔧 Configuration

### Game Configuration

Edit `config/default.json` to customize game parameters:

```json
{
  "game": {
    "num_players": 9,
    "roles": {
      "werewolf": 3,
      "villager": 3,
      "seer": 1,
      "witch": 1,
      "hunter": 1
    }
  },
  "llm": {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "temperature": 0.7
  },
  "agent": {
    "personalities": ["rational", "aggressive", "humorous"],
    "memory_limit": 10
  },
  "tts": {
    "enabled": true,
    "model": "qwen3-tts-flash",
    "voice": "Cherry"
  }
}
```

### Supported LLM Providers

1. **OpenAI**
   ```bash
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-4o-mini
   ```

2. **Qwen (Alibaba Cloud DashScope)**
   ```bash
   DASHSCOPE_API_KEY=sk-...
   DASHSCOPE_MODEL=qwen-turbo
   ```

3. **ModelScope**
   ```bash
   OPENAI_API_KEY=your-token
   OPENAI_API_BASE=https://api-inference.modelscope.cn/v1
   OPENAI_MODEL=Qwen/Qwen2.5-7B-Instruct
   ```

### TTS Voice Configuration

Supports Qwen TTS service with optional voice characters:
- Cherry (Female, gentle and sweet)
- ZhiMiao (Female, intellectual and elegant)
- Zhitian (Male, mature and steady)
- ZhiYan (Female, clear and bright)

## 🛠️ Development Guide

### Adding New Roles

1. Add role enum in `src/core/models.py`
2. Configure role count in `config/default.json`
3. Implement special abilities (if needed)

### Customizing AI Personalities

Modify personality prompts in `src/agents/langchain_agent.py`:

```python
PERSONALITIES = {
    "rational": "You are a rational and calm player...",
    "aggressive": "You are an aggressive and bold player...",
    "humorous": "You are a humorous and witty player..."
}
```

### Adding API Endpoints

Add new routes in `src/web/api.py`:

```python
@app.post("/api/custom-endpoint")
async def custom_endpoint():
    # Implement logic
    return {"status": "ok"}
```

### Running Tests

```bash
# Test backend API
python -m pytest tests/

# Test complete flow (Windows)
.\test_complete_flow.ps1

# Test Web API (Windows)
.\test_web_api.ps1
```

## 🤝 Contributing

Contributions are welcome!

1. Fork the project
2. Create a Feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 Python code style
- Use type hints
- Write clear docstrings
- Keep functions short and focused
- Add necessary unit tests

## 📊 Product Vision

### Watching Mode (Current Stage)
- Users can watch exciting matches between AIs
- AIs have different personalities and speaking styles
- Automatic generation of highlight clips
- Support for pause, replay, and speed adjustment

### Interactive Mode (Planned)
- Users can participate as players (1 player + 8 AIs)
- Users can bet/predict who is the werewolf
- Users can customize AI personalities
- Social sharing and friend battles

### Competitive Advantages
- ✨ AI characterization (not cold logic machines)
- ✨ Celebrity/IP integration (e.g., "Musk vs Zhuge Liang")
- ✨ Short video priority (suitable for TikTok/Bilibili)
- ✨ Dual mode: watching + participating

## 🐛 Troubleshooting

### Backend Startup Failed
- Check Python version (requires 3.8+)
- Confirm dependencies installed: `pip install -r requirements.txt`
- Check if port 8000 is occupied
- Verify API key configuration is correct

### Frontend Startup Failed
- Confirm Node.js is installed (requires 16+)
- Install dependencies: `cd frontend && npm install`
- Check if port 3000 is occupied

### AI Not Speaking or Speaking Abnormally
- Check if API key in `.env` is correct
- View log files `data/logs/werewolf_*.log`
- Try lowering `temperature` value in `config/default.json`
- Confirm network can access LLM API service

### TTS Voice Unavailable
- Confirm `DASHSCOPE_API_KEY` is configured
- Check `tts.enabled` is `true` in `config/default.json`
- View logs for specific error information

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 📞 Contact

- **GitHub Issues**: [Submit Issue](https://github.com/yyvk/ai-werewolf/issues)
- **Project Homepage**: [https://github.com/yyvk/ai-werewolf](https://github.com/yyvk/ai-werewolf)

---

**Let AI play Werewolf and witness the exciting showdown of reasoning and deception!** 🎭🤖

