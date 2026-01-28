#!/bin/bash

# Code Craze Study Guide - Stop Script
# This script safely stops the application running on port 8989

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Application port (CRITICAL: Always 8989)
PORT=8989

echo -e "${BLUE}🛑 Code Craze Academy - Stop Script${NC}"
echo -e "${BLUE}====================================${NC}\n"

# Find process using port 8989
PID=$(lsof -ti:${PORT} 2>/dev/null || true)

if [ -z "$PID" ]; then
    echo -e "${GREEN}✅ No process found running on port ${PORT}${NC}"
    echo -e "${GREEN}   Application is already stopped${NC}\n"
    exit 0
fi

echo -e "${YELLOW}🔍 Found process running on port ${PORT} (PID: ${PID})${NC}"
echo -e "${YELLOW}🔪 Stopping application...${NC}"

# Try graceful kill first
kill $PID 2>/dev/null || true

# Wait for graceful shutdown
sleep 2

# Check if still running
if lsof -ti:${PORT} >/dev/null 2>&1; then
    echo -e "${RED}⚠️  Process didn't stop gracefully, forcing...${NC}"
    kill -9 $PID 2>/dev/null || true
    sleep 1
fi

# Verify it's stopped
if lsof -ti:${PORT} >/dev/null 2>&1; then
    echo -e "${RED}❌ Failed to stop application on port ${PORT}${NC}"
    echo -e "${RED}   Please manually kill the process${NC}\n"
    exit 1
else
    echo -e "${GREEN}✅ Application stopped successfully${NC}"
    echo -e "${GREEN}   Port ${PORT} is now free${NC}\n"
fi
