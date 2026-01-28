# CLAUDE.md - Code Craze Academy Guidelines

## Project Overview

Code Craze Academy is a gamified learning platform for the Science Olympiad Code Craze event. It helps students prepare for competition through adaptive learning, competency tracking, and multiple practice modes.

## Critical Configuration

**PORT: 8989** - Never change without explicit permission. All scripts, configs, and frontend references use this port.

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Vanilla JavaScript (no frameworks)
- **Package Manager**: uv

## Project Structure

```
code-craze/
├── backend/           # FastAPI backend
│   ├── api/          # Routes and Pydantic models
│   ├── config/       # Settings
│   ├── database/     # SQLAlchemy models, db.py
│   └── services/     # Business logic
├── frontend/          # Vanilla JS frontend
│   ├── components/   # UI components
│   ├── utils/        # API client
│   └── styles/       # CSS
├── content/           # Educational content
│   ├── config/       # topics.yaml
│   └── questions/    # Question bank (JSON)
└── data/              # SQLite database (runtime)
```

## Key Commands

```bash
# Start application
./start.sh

# Stop application
./stop.sh

# Restart
./restart.sh

# Manual start
uv run backend/server.py

# Seed database
uv run python backend/database/seed_data.py
```

## Code Craze Topics (2026)

### Division B (Middle School)
1. Principles of Coding (Karel)
2. AI & Machine Learning
3. Cryptography
4. Python Fundamentals

### Division C (High School)
All Division B topics plus:
5. Quantum Computing

## Development Guidelines

1. **Max file size**: 500 lines
2. **Type hints**: Required on all functions
3. **Docstrings**: Google-style on every function
4. **Database**: Delete `data/code_craze.db` to reset

## API Endpoints

- `GET /health` - Health check
- `GET /api/info` - App info
- `GET /api/competencies` - User competency dashboard
- `POST /api/practice/start` - Start practice session
- `GET /api/practice/next` - Get next question
- `POST /api/practice/submit` - Submit answer

## Test User

- Username: `student`
- Password: `password123`
