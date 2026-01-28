#!/bin/bash

# Code Craze Study Guide - Restart Script
# This script stops and starts the application

# Colors for output
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Code Craze Academy - Restart Script${NC}"
echo -e "${BLUE}=======================================${NC}\n"

# Stop the application
./stop.sh

# Small delay
sleep 1

# Start the application
./start.sh
