#!/bin/bash

# Test Runner Script for Nextcloud Service Reminder Application
# This script sets up the virtual environment, installs dependencies, and runs tests

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Determine the project root (assume script is in tests folder)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${YELLOW}=== Nextcloud Service Reminder - Test Runner ===${NC}"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed or not in PATH${NC}"
    exit 1
fi

echo -e "Found Python: $(python3 --version)"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists.${NC}"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing virtual environment..."
        rm -rf venv
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip to latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}ERROR: requirements.txt not found in project root${NC}"
    exit 1
fi

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Check if src directory exists
if [ ! -d "src" ]; then
    echo -e "${RED}ERROR: src directory not found${NC}"
    exit 1
fi

# Check if tests directory exists
if [ ! -d "tests" ]; then
    echo -e "${RED}ERROR: tests directory not found${NC}"
    exit 1
fi

# Run tests with PYTHONPATH set to include src
echo -e "${YELLOW}Running test suite...${NC}"
cd tests

# Add src to PYTHONPATH so imports work
export PYTHONPATH="$PROJECT_ROOT/src:$PYTHONPATH"

# Run all test files that match test_*.py pattern
python -m unittest discover -s . -p "test_*.py" -v

TEST_RESULT=$?

cd "$PROJECT_ROOT"

if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}=== All tests passed! ===${NC}"
else
    echo -e "${RED}=== Some tests failed. ===${NC}"
fi

# Deactivate virtual environment
deactivate 2>/dev/null || true

exit $TEST_RESULT