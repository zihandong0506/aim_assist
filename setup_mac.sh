#!/bin/bash
# setup_mac.sh
# Automates environment creation for Machine Learning on macOS

# 1. Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}>>> Starting Mac Environment Setup...${NC}"

# 2. Check for Python 3
if ! command -v python3 &> /dev/null
then
    echo -e "${RED}!!! Python3 could not be found. Please install it (brew install python3).${NC}"
    exit 1
fi

# 3. Create Virtual Environment (.venv)
if [ -d ".venv" ]; then
    echo -e "${YELLOW}>>> .venv already exists. Skipping creation.${NC}"
else
    echo -e "${YELLOW}>>> Creating virtual environment (.venv)...${NC}"
    python3 -m venv .venv
fi

# 4. Activate and Install
echo -e "${YELLOW}>>> Activating .venv and installing dependencies...${NC}"
source .venv/bin/activate

# Upgrade pip first to avoid binary incompatibility issues
pip install --upgrade pip

# Install from the requirements file
# Note: This will skip 'dxcam' and windows-specific tools automatically
pip install -r requirements.txt

# 5. Verify Apple Silicon (MPS) Acceleration
echo -e "${YELLOW}>>> Verifying Apple Metal (MPS) Support...${NC}"
python3 -c "import torch; print(f'${GREEN}>>> PyTorch Version: {torch.__version__}${NC}'); print(f'${GREEN}>>> MPS Available: {torch.backends.mps.is_available()}${NC}')"

echo -e "${GREEN}>>> Setup Complete!${NC}"
echo -e "To start working, type: ${YELLOW}source .venv/bin/activate${NC}"