# 🏗️ LABBAIK AI v6.0 - Enterprise Architecture

## Project Structure Overview

```
labbaik-v6/
│
├── 📁 app/                          # Main Application Entry
│   ├── __init__.py
│   └── main.py                      # Streamlit entry point
│
├── 📁 core/                         # Core Business Logic
│   ├── __init__.py
│   ├── config.py                    # Configuration management
│   ├── constants.py                 # Application constants
│   ├── exceptions.py                # Custom exceptions
│   └── logging_config.py            # Logging configuration
│
├── 📁 services/                     # Business Services Layer
│   ├── __init__.py
│   ├── ai/                          # AI Services
│   │   ├── __init__.py
│   │   ├── base.py                  # Base AI service interface
│   │   ├── chat_service.py          # Chat completion service
│   │   ├── rag_service.py           # RAG implementation
│   │   └── embedding_service.py     # Embedding service
│   │
│   ├── auth/                        # Authentication Services
│   │   ├── __init__.py
│   │   ├── base.py                  # Auth interface
│   │   ├── google_auth.py           # Google OAuth
│   │   ├── email_auth.py            # Email/Password auth
│   │   └── session_manager.py       # Session management
│   │
│   ├── database/                    # Database Services
│   │   ├── __init__.py
│   │   ├── connection.py            # Connection pool manager
│   │   ├── repositories/            # Data repositories
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # Base repository
│   │   │   ├── user_repo.py         # User repository
│   │   │   ├── chat_repo.py         # Chat history repository
│   │   │   ├── booking_repo.py      # Booking repository
│   │   │   └── partner_repo.py      # Partner repository
│   │   └── migrations/              # Database migrations
│   │       ├── __init__.py
│   │       └── migrate.py
│   │
│   ├── cost/                        # Cost Calculation Services
│   │   ├── __init__.py
│   │   ├── simulator.py             # Cost simulator
│   │   ├── calculator.py            # Price calculator
│   │   └── currency.py              # Currency conversion
│   │
│   └── notification/                # Notification Services
│       ├── __init__.py
│       ├── base.py                  # Notification interface
│       ├── email_service.py         # Email notifications
│       └── whatsapp_service.py      # WhatsApp notifications
│
├── 📁 ui/                           # UI Components Layer
│   ├── __init__.py
│   ├── components/                  # Reusable UI Components
│   │   ├── __init__.py
│   │   ├── header.py                # Header component
│   │   ├── footer.py                # Footer component
│   │   ├── sidebar.py               # Sidebar component
│   │   ├── chat_widget.py           # Chat widget
│   │   ├── cost_display.py          # Cost display widget
│   │   └── booking_form.py          # Booking form
│   │
│   ├── pages/                       # Page Definitions
│   │   ├── __init__.py
│   │   ├── home.py                  # Home page
│   │   ├── chat.py                  # AI Chat page
│   │   ├── simulator.py             # Cost simulator page
│   │   ├── booking.py               # Booking page
│   │   ├── umrah_bareng.py          # Umrah Bareng page
│   │   ├── umrah_mandiri.py         # Umrah Mandiri page
│   │   ├── profile.py               # User profile page
│   │   └── admin/                   # Admin pages
│   │       ├── __init__.py
│   │       ├── dashboard.py         # Admin dashboard
│   │       ├── users.py             # User management
│   │       ├── revenue.py           # Revenue tracking
│   │       └── partners.py          # Partner management
│   │
│   ├── layouts/                     # Page Layouts
│   │   ├── __init__.py
│   │   ├── base_layout.py           # Base layout
│   │   ├── auth_layout.py           # Auth pages layout
│   │   └── admin_layout.py          # Admin pages layout
│   │
│   └── themes/                      # UI Themes
│       ├── __init__.py
│       ├── default.py               # Default theme
│       └── dark.py                  # Dark theme
│
├── 📁 data/                         # Data Layer
│   ├── __init__.py
│   ├── models/                      # Data Models (Pydantic)
│   │   ├── __init__.py
│   │   ├── user.py                  # User model
│   │   ├── chat.py                  # Chat model
│   │   ├── booking.py               # Booking model
│   │   ├── partner.py               # Partner model
│   │   ├── cost.py                  # Cost model
│   │   └── subscription.py          # Subscription model
│   │
│   ├── schemas/                     # API Schemas
│   │   ├── __init__.py
│   │   ├── request.py               # Request schemas
│   │   └── response.py              # Response schemas
│   │
│   └── knowledge/                   # Knowledge Base
│       ├── __init__.py
│       ├── umrah_guide.py           # Umrah guide data
│       ├── arabic_phrases.py        # Arabic phrases
│       ├── prayer_times.py          # Prayer times data
│       └── faq.py                   # FAQ data
│
├── 📁 plugins/                      # Plugin System
│   ├── __init__.py
│   ├── base.py                      # Plugin base class
│   ├── loader.py                    # Plugin loader
│   ├── registry.py                  # Plugin registry
│   └── available/                   # Available plugins
│       ├── __init__.py
│       ├── analytics/               # Analytics plugin
│       │   ├── __init__.py
│       │   ├── plugin.py
│       │   └── config.py
│       ├── gamification/            # Gamification plugin
│       │   ├── __init__.py
│       │   ├── plugin.py
│       │   └── badges.py
│       ├── booking_partners/        # Booking partners plugin
│       │   ├── __init__.py
│       │   ├── plugin.py
│       │   └── providers/
│       │       ├── __init__.py
│       │       ├── traveloka.py
│       │       └── tiket.py
│       └── payment/                 # Payment plugin
│           ├── __init__.py
│           ├── plugin.py
│           └── providers/
│               ├── __init__.py
│               ├── midtrans.py
│               └── xendit.py
│
├── 📁 utils/                        # Utility Functions
│   ├── __init__.py
│   ├── helpers.py                   # General helpers
│   ├── validators.py                # Input validators
│   ├── formatters.py                # Data formatters
│   ├── decorators.py                # Custom decorators
│   └── cache.py                     # Caching utilities
│
├── 📁 tests/                        # Test Suite
│   ├── __init__.py
│   ├── conftest.py                  # Pytest configuration
│   ├── fixtures/                    # Test fixtures
│   │   ├── __init__.py
│   │   └── data.py
│   ├── unit/                        # Unit tests
│   │   ├── __init__.py
│   │   ├── test_services/
│   │   ├── test_data/
│   │   └── test_utils/
│   ├── integration/                 # Integration tests
│   │   ├── __init__.py
│   │   ├── test_database/
│   │   └── test_ai/
│   └── e2e/                         # End-to-end tests
│       ├── __init__.py
│       └── test_flows/
│
├── 📁 scripts/                      # Utility Scripts
│   ├── setup_db.py                  # Database setup
│   ├── seed_data.py                 # Seed initial data
│   ├── migrate.py                   # Run migrations
│   └── deploy.py                    # Deployment script
│
├── 📁 config/                       # Configuration Files
│   ├── settings.yaml                # Main settings
│   ├── logging.yaml                 # Logging config
│   └── plugins.yaml                 # Plugin config
│
├── 📁 docs/                         # Documentation
│   ├── README.md                    # Main documentation
│   ├── ARCHITECTURE.md              # Architecture docs
│   ├── API.md                       # API documentation
│   ├── PLUGINS.md                   # Plugin development guide
│   └── DEPLOYMENT.md                # Deployment guide
│
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore
├── .streamlit/                      # Streamlit config
│   └── config.toml
├── pyproject.toml                   # Project config (Poetry)
├── requirements.txt                 # Dependencies
├── Dockerfile                       # Docker config
├── docker-compose.yml               # Docker compose
└── README.md                        # Project README
```

## Architecture Principles

### 1. Separation of Concerns
- **Core**: Business logic dan konfigurasi
- **Services**: Implementasi layanan (AI, Auth, Database)
- **UI**: Komponen antarmuka pengguna
- **Data**: Model data dan skema
- **Plugins**: Fitur extensible

### 2. Dependency Injection
- Services di-inject melalui dependency container
- Mudah untuk testing dan mocking

### 3. Repository Pattern
- Data access diabstraksi melalui repositories
- Clean separation antara business logic dan data layer

### 4. Plugin Architecture
- Fitur baru bisa ditambahkan tanpa mengubah core
- Hot-reload plugins tanpa restart aplikasi

### 5. Configuration Management
- Environment-based configuration
- Secrets management yang aman
- YAML-based settings untuk flexibility
