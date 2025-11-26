#!/bin/bash
# ==============================================
# Umrah Planner AI - Run Script
# ==============================================

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}"
echo "🕋 Starting Umrah Planner AI..."
echo -e "${NC}"

# Activate virtual environment
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    # Windows Git Bash
    if [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    else
        echo -e "${YELLOW}Warning: Virtual environment not found. Run setup.sh first.${NC}"
    fi
else
    # Linux/MacOS
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    else
        echo -e "${YELLOW}Warning: Virtual environment not found. Run setup.sh first.${NC}"
    fi
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found. Creating from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}Please edit .env and add your API keys, then run again.${NC}"
    exit 1
fi

# Run Streamlit
echo -e "${GREEN}Starting Streamlit server...${NC}"
echo -e "${BLUE}Open http://localhost:8501 in your browser${NC}"
echo ""

streamlit run app.py --server.port 8501 --server.headless true
