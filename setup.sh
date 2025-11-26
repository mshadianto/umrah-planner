#!/bin/bash
# ==============================================
# Umrah Planner AI - Setup Script
# For Windows Git Bash / Linux / MacOS
# ==============================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║          🕋 Umrah Planner AI - Setup Script               ║"
echo "║      RAG Agentic AI untuk Simulasi Biaya Umrah            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python version
echo -e "${YELLOW}[1/6] Checking Python version...${NC}"
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo -e "${RED}Error: Python not found. Please install Python 3.10+${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "  Found Python $PYTHON_VERSION"

# Check if version is 3.10+
MIN_VERSION="3.10"
if [ "$(printf '%s\n' "$MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$MIN_VERSION" ]; then
    echo -e "${RED}Error: Python 3.10+ required. Found $PYTHON_VERSION${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ Python version OK${NC}"

# Create virtual environment
echo -e "\n${YELLOW}[2/6] Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "  Virtual environment already exists"
else
    $PYTHON_CMD -m venv venv
    echo -e "${GREEN}  ✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "\n${YELLOW}[3/6] Activating virtual environment...${NC}"
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    # Windows Git Bash
    source venv/Scripts/activate
else
    # Linux/MacOS
    source venv/bin/activate
fi
echo -e "${GREEN}  ✓ Virtual environment activated${NC}"

# Upgrade pip
echo -e "\n${YELLOW}[4/6] Upgrading pip...${NC}"
pip install --upgrade pip --quiet
echo -e "${GREEN}  ✓ pip upgraded${NC}"

# Install dependencies
echo -e "\n${YELLOW}[5/6] Installing dependencies...${NC}"
echo -e "  This may take a few minutes..."
pip install -r requirements.txt --quiet
echo -e "${GREEN}  ✓ Dependencies installed${NC}"

# Setup environment file
echo -e "\n${YELLOW}[6/6] Setting up environment...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}  ✓ Created .env file from .env.example${NC}"
    echo -e "${YELLOW}  ⚠ Please edit .env and add your API keys${NC}"
else
    echo -e "  .env file already exists"
fi

# Create necessary directories
mkdir -p data/chroma_db
mkdir -p logs
mkdir -p exports

echo -e "\n${GREEN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              ✓ Setup Complete!                            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BLUE}Next steps:${NC}"
echo -e "  1. Edit ${YELLOW}.env${NC} file and add your API key:"
echo -e "     ${YELLOW}GROQ_API_KEY=your_key_here${NC}"
echo -e ""
echo -e "  2. Get free Groq API key at:"
echo -e "     ${BLUE}https://console.groq.com/${NC}"
echo -e ""
echo -e "  3. Run the application:"
echo -e "     ${GREEN}./run.sh${NC} (Linux/Mac/Git Bash)"
echo -e "     or"
echo -e "     ${GREEN}streamlit run app.py${NC}"
echo -e ""
echo -e "  4. Open in browser:"
echo -e "     ${BLUE}http://localhost:8501${NC}"
echo -e ""
