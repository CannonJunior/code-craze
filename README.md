# Code Craze Academy

Interactive study guide for the Science Olympiad Code Craze event.

## Overview

Code Craze Academy is a gamified learning platform that helps students prepare for the Science Olympiad Code Craze competition. It features adaptive learning, competency tracking, and multiple practice modes.

## Topics Covered

### Division B (Middle School)
- **Principles of Coding** - Karel programming basics
- **AI & Machine Learning** - AI concepts, LLMs, ML types
- **Cryptography** - Ciphers, encryption, hash functions
- **Python Fundamentals** - Variables, loops, functions, data structures

### Division C (High School)
All Division B topics plus:
- **Quantum Computing** - Qubits, superposition, entanglement

## Quick Start

### Prerequisites
- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. Clone the repository:
```bash
cd code-craze
```

2. Install dependencies:
```bash
uv sync
```

3. Start the application:
```bash
./start.sh
```

4. Open your browser to: http://localhost:8989

### Test User
- Username: `student`
- Password: `password123`

## Features

### Adaptive Learning
- Intelligent question selection based on your performance
- Focus on weak areas or review mastered topics
- Competition simulation mode

### Practice Modes
- **Balanced Practice** - Mix of new content, review, and weak areas
- **Weak Area Focus** - Target struggling topics
- **Review Mode** - Reinforce learned material
- **Competition Simulation** - Realistic test conditions

### Progress Tracking
- Competency tracking across all topics
- Mastery levels: Novice → Developing → Proficient → Expert → Master
- Competition readiness score

### Gamification
- Points for correct answers
- Achievement badges
- Streak tracking

## Project Structure

```
code-craze/
├── backend/           # FastAPI Python backend
├── frontend/          # Vanilla JavaScript frontend
├── content/           # Educational content (topics, questions)
├── data/              # SQLite database
├── start.sh           # Start server
├── stop.sh            # Stop server
└── restart.sh         # Restart server
```

## Development

### Commands

```bash
# Start server
./start.sh

# Stop server
./stop.sh

# Restart server
./restart.sh

# Run manually
uv run backend/server.py

# Seed database with fresh data
uv run python backend/database/seed_data.py
```

### API Documentation

Once the server is running, visit: http://localhost:8989/docs

## Technology Stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Frontend**: Vanilla JavaScript, CSS
- **Database**: SQLite
- **Package Manager**: uv

## Resources

- [Science Olympiad Code Craze (HS)](https://codehs.com/course/ScienceOlympiadHS/overview)
- [Science Olympiad Code Craze (MS)](https://codehs.com/course/ScienceOlympiadMS/overview)
- [Science Olympiad Trial Events](https://www.soinc.org/learn/trial-events)

## License

This project is for educational purposes for Science Olympiad preparation.

---

*Code Craze Academy v0.1.0*
