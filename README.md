# 🕋 LABBAIK AI v6.0

**Asisten Perjalanan Umrah Cerdas** - AI-powered Umrah planning platform for Indonesian pilgrims.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.32+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-proprietary-green.svg)](LICENSE)

---

## 📋 Overview

LABBAIK AI is a comprehensive Umrah planning platform that combines AI-powered assistance with practical planning tools. Built with a modular, enterprise-grade architecture, it helps Indonesian pilgrims plan their spiritual journey with confidence.

### Key Features

- 💬 **AI Chat Assistant** - Intelligent Q&A about Umrah using Groq/OpenAI
- 🧮 **Cost Simulator** - Accurate cost estimation with seasonal adjustments
- 📖 **Umrah Mandiri** - Comprehensive independent pilgrimage guide
- 👥 **Umrah Bareng** - Peer-to-peer trip matching
- 📝 **Booking Integration** - Partner booking system
- 🏆 **Gamification** - Badges, points, and engagement features
- 🔌 **Plugin System** - Extensible architecture for custom features

---

## 🏗️ Architecture

```
labbaik-v6/
├── app/                    # Application Entry Point
├── core/                   # Core Business Logic
│   ├── config.py          # Configuration Management
│   ├── constants.py       # Application Constants
│   ├── exceptions.py      # Custom Exceptions
│   └── logging_config.py  # Logging Configuration
├── services/              # Business Services
│   ├── ai/               # AI Services (Chat, RAG, Embeddings)
│   ├── auth/             # Authentication Services
│   ├── database/         # Database & Repositories
│   ├── cost/             # Cost Calculation
│   └── notification/     # Notifications
├── data/                  # Data Layer
│   ├── models/           # Pydantic Models
│   └── schemas/          # API Schemas
├── ui/                    # UI Components
│   ├── components/       # Reusable Components
│   ├── pages/            # Page Definitions
│   └── layouts/          # Page Layouts
├── plugins/               # Plugin System
│   ├── base.py           # Plugin Base Classes
│   └── available/        # Available Plugins
├── tests/                 # Test Suite
├── config/                # Configuration Files
└── docs/                  # Documentation
```

### Design Principles

1. **Separation of Concerns** - Clear boundaries between layers
2. **Dependency Injection** - Loosely coupled components
3. **Repository Pattern** - Abstracted data access
4. **Plugin Architecture** - Extensible without core modifications
5. **Configuration First** - Environment-based settings

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 15+ (optional, for full features)
- Redis (optional, for caching)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mshadianto/labbaik-ai.git
   cd labbaik-ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application**
   ```bash
   streamlit run app/main.py
   ```

### Using Docker

```bash
# Development
docker-compose up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `LABBAIK_ENV` | Environment (development/production) | No |
| `DATABASE_URL` | PostgreSQL connection string | Yes* |
| `GROQ_API_KEY` | Groq API key for LLM | Yes |
| `OPENAI_API_KEY` | OpenAI API key (fallback) | No |
| `SESSION_SECRET_KEY` | Session encryption key | Yes |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | No |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret | No |

*Required for full functionality

### Configuration File

Edit `config/settings.yaml` for detailed configuration:

```yaml
environment: development
debug: true

ai:
  groq_model: "llama-3.3-70b-versatile"
  groq_temperature: 0.7

ui:
  app_name: "LABBAIK AI"
  features:
    chat: true
    simulator: true
    gamification: true
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov=core --cov=services

# Run specific test category
pytest -m unit
pytest -m integration

# Run specific test file
pytest tests/unit/test_ai_services.py -v
```

---

## 🔌 Plugin Development

Create custom plugins to extend LABBAIK AI:

```python
from plugins.base import BasePlugin, PluginMetadata, PluginHook, HookEvents

class MyPlugin(BasePlugin):
    def __init__(self):
        metadata = PluginMetadata(
            name="my-plugin",
            version="1.0.0",
            description="My custom plugin"
        )
        super().__init__(metadata)
    
    def initialize(self, context) -> bool:
        # Setup logic
        return True
    
    def activate(self) -> bool:
        self.status = PluginStatus.ACTIVE
        return True
    
    @PluginHook(HookEvents.CHAT_MESSAGE_SENT)
    def on_chat_message(self, user_id: str, message: str):
        # Handle chat messages
        pass
```

---

## 📦 Deployment

### Streamlit Cloud

1. Connect your GitHub repository
2. Set environment variables in Streamlit Cloud
3. Deploy!

### Docker Production

```bash
docker build -t labbaik-ai:latest --target production .
docker run -d -p 8501:8501 --env-file .env labbaik-ai:latest
```

### Kubernetes

Helm charts available in `deploy/helm/`.

---

## 📚 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md)
- [API Documentation](docs/API.md)
- [Plugin Development](docs/PLUGINS.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

Proprietary - © 2024 MS Hadianto. All rights reserved.

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- AI powered by [Groq](https://groq.com/) and [OpenAI](https://openai.com/)
- RAG with [ChromaDB](https://www.trychroma.com/) and [Sentence Transformers](https://www.sbert.net/)

---

<p align="center">
  <strong>🕋 LABBAIK AI - Membantu Perjalanan Spiritual Anda 🕋</strong>
  <br>
  <em>Do Your Own Research • Plan Your Journey • Trust Your Heart</em>
</p>
