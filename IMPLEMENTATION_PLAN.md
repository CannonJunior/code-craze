# Code Craze Study Guide - Implementation Plan

## Project Overview

Build a gamified learning platform for the Science Olympiad **Code Craze** event, mirroring the architecture of the Circuit Lab Study Guide. The platform will help students prepare for the 2026 competition through adaptive learning, competency tracking, and multiple practice modes.

---

## Research Summary

### Code Craze Event Details (2026)

**Division B (Middle School) Topics:**
1. Principles of Coding (Karel programming)
2. AI & Machine Learning
3. Cryptography
4. Python Coding

**Division C (High School) Topics:**
1. Principles of Coding (Karel programming)
2. AI & Machine Learning
3. Cryptography
4. Python Programming
5. Quantum Computing

**Competition Format:**
- Interactive quiz and coding activities
- Uses CodeHS.com platform for competition
- Laptop required with Google Chrome
- No external resources allowed during competition
- Teams assessed on practice module knowledge

**Sources:**
- [CodeHS Science Olympiad Code Craze (HS)](https://codehs.com/course/ScienceOlympiadHS/overview)
- [CodeHS Science Olympiad Code Craze (MS)](https://codehs.com/course/ScienceOlympiadMS/overview)
- [Science Olympiad Trial Events](https://www.soinc.org/learn/trial-events)

---

## Architecture (Mirroring Circuit Lab)

### Technology Stack
| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | FastAPI 0.115+ | Python web framework |
| **Server** | Uvicorn 0.32+ | ASGI application server |
| **Database** | SQLite + SQLAlchemy 2.0+ | Local database with ORM |
| **Config** | Pydantic 2.10+ | Data validation & settings |
| **Frontend** | Vanilla JavaScript | Single-page application |
| **Styling** | Plain CSS | Responsive design |
| **Package Manager** | uv | Fast Python package management |

### Port Configuration
- **Port: 8989** (matching circuit-lab convention)

---

## Project Structure

```
code-craze/
├── backend/                    # FastAPI Python backend
│   ├── api/
│   │   ├── routes.py          # All API endpoints
│   │   └── models.py          # Pydantic request/response schemas
│   ├── database/
│   │   ├── db.py              # SQLAlchemy setup, session management
│   │   ├── models.py          # SQLAlchemy ORM models
│   │   └── seed_data.py       # Initial test data
│   ├── services/
│   │   ├── competency_service.py    # Competency tracking & mastery
│   │   └── adaptive_learning.py     # Question selection algorithm
│   ├── config/
│   │   └── settings.py        # Environment configuration
│   └── server.py              # FastAPI app entry point
├── frontend/
│   ├── components/
│   │   ├── dashboard.js       # Competency dashboard UI
│   │   ├── practice.js        # Practice mode interface
│   │   └── progress.js        # Progress tracking UI
│   ├── utils/
│   │   └── api.js             # API client wrapper
│   ├── styles/
│   │   └── main.css           # Application styling
│   └── index.html             # Main HTML page
├── content/
│   ├── config/
│   │   └── topics.yaml        # Topic taxonomy for Code Craze
│   ├── questions/
│   │   └── sample_questions.json  # Question bank
│   └── lessons/               # Markdown lesson content
├── data/
│   └── code_craze.db          # SQLite database (runtime)
├── tests/                     # Unit tests
├── docs/                      # Documentation
├── .env                       # Environment variables
├── .env.template              # Configuration template
├── pyproject.toml             # Python dependencies
├── start.sh                   # Launch script
├── stop.sh                    # Stop script
├── restart.sh                 # Restart script
├── main.py                    # Entry point
├── README.md                  # Main documentation
├── CLAUDE.md                  # Project guidelines
└── TASK.md                    # Development roadmap
```

---

## Content Organization: Topic Taxonomy

### Division B (Middle School) - 4 Main Topics

```yaml
topics:
  - id: "1"
    name: "Principles of Coding"
    description: "Foundational programming concepts using Karel"
    subtopics:
      - id: "1.1"
        name: "Karel Commands"
        description: "Basic Karel commands: move, turnLeft, putBall, takeBall"
      - id: "1.2"
        name: "Functions"
        description: "Defining and calling functions"
      - id: "1.3"
        name: "Control Structures"
        description: "If/else statements and while loops"
      - id: "1.4"
        name: "Problem Decomposition"
        description: "Breaking down problems into smaller steps"

  - id: "2"
    name: "AI & Machine Learning"
    description: "Understanding artificial intelligence concepts"
    subtopics:
      - id: "2.1"
        name: "What is AI"
        description: "Definition and types of AI systems"
      - id: "2.2"
        name: "Generative AI"
        description: "Text, image, music, and video generation"
      - id: "2.3"
        name: "Machine Learning Types"
        description: "Supervised, unsupervised, reinforcement learning"
      - id: "2.4"
        name: "AI Risks & Ethics"
        description: "Bias, hallucinations, deepfakes, misinformation"

  - id: "3"
    name: "Cryptography"
    description: "Encryption and security concepts"
    subtopics:
      - id: "3.1"
        name: "Historical Ciphers"
        description: "Caesar cipher, substitution ciphers"
      - id: "3.2"
        name: "Symmetric Encryption"
        description: "Same key for encryption and decryption"
      - id: "3.3"
        name: "Asymmetric Encryption"
        description: "Public and private key pairs"
      - id: "3.4"
        name: "Hash Functions"
        description: "One-way functions and digital signatures"

  - id: "4"
    name: "Python Fundamentals"
    description: "Core Python programming skills"
    subtopics:
      - id: "4.1"
        name: "Variables & Data Types"
        description: "Strings, integers, floats, booleans"
      - id: "4.2"
        name: "Conditionals"
        description: "If/elif/else statements"
      - id: "4.3"
        name: "Loops"
        description: "For and while loops"
      - id: "4.4"
        name: "Functions"
        description: "Defining and calling Python functions"
      - id: "4.5"
        name: "Data Structures"
        description: "Lists, tuples, dictionaries"
```

### Division C (High School) - 5 Main Topics
(Includes all Division B topics plus:)

```yaml
  - id: "5"
    name: "Quantum Computing"
    description: "Introduction to quantum computing concepts"
    subtopics:
      - id: "5.1"
        name: "Quantum Basics"
        description: "Qubits, superposition, entanglement"
      - id: "5.2"
        name: "Quantum Gates"
        description: "Basic quantum operations"
      - id: "5.3"
        name: "Quantum Algorithms"
        description: "Shor's algorithm, Grover's algorithm basics"
      - id: "5.4"
        name: "Quantum Applications"
        description: "Cryptography, optimization, simulation"
```

---

## Database Schema (8 Tables - Same as Circuit Lab)

### Core Models

1. **users** - User accounts with authentication
2. **user_preferences** - UI settings & practice mode preferences
3. **user_competencies** - Topic-level performance tracking
4. **question_attempts** - Detailed analytics of every answer
5. **progress** - Level completion and scores
6. **questions** - Question bank with explanations
7. **badges** - Badge definitions
8. **user_badges** - Badges earned by users

### Question Structure
```json
{
  "id": 1,
  "question_text": "What does the Karel command 'move()' do?",
  "question_type": "multiple_choice",
  "topic_id": "1.1",
  "difficulty": 1,
  "answers": [
    {
      "text": "Moves Karel forward one step",
      "correct": true,
      "explanation": "Karel moves one space in the direction it's facing",
      "teaching_point": "move() always moves exactly one step forward"
    },
    {
      "text": "Turns Karel to the left",
      "correct": false,
      "explanation": "That's what turnLeft() does"
    }
  ],
  "solution_steps": ["Step 1...", "Step 2..."],
  "code_snippet": "move()\nmove()\nturnLeft()"
}
```

---

## API Endpoints (12 Routes)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Server status |
| GET | `/api/info` | App metadata |
| GET | `/api/competencies` | Full dashboard data |
| GET | `/api/competencies/{topic_id}` | Detailed topic data |
| POST | `/api/practice/start` | Start practice session |
| GET | `/api/practice/next` | Get next question |
| POST | `/api/practice/submit` | Submit answer |
| GET | `/api/preferences` | Get user settings |
| PUT | `/api/preferences` | Update preferences |
| GET | `/api/recommendations` | Get focus areas |
| GET | `/api/progress` | Level completion |
| GET | `/api/badges` | Available badges |

---

## Key Features

### 1. Adaptive Learning (Same as Circuit Lab)
- **Balanced Mode**: 50% new content, 30% review, 20% weak areas
- **Weak Focus Mode**: 70% struggling topics, 30% others
- **Review Mode**: Based on time since last practice
- **Competition Mode**: Uniform distribution

### 2. Competency Tracking
- Mastery levels: novice → developing → proficient → expert → master
- Real-time accuracy tracking
- Trend analysis (improving/stable/declining)

### 3. Gamification
- Points system for correct answers
- 30 badges (topic mastery, milestones, special achievements)
- Progress visualization

### 4. Question Types
- Multiple choice
- Code tracing (what does this code output?)
- Code completion (fill in the blank)
- Matching (concepts to definitions)
- True/False

---

## Implementation Phases

### Phase 1: Core Infrastructure (Priority)
**Goal:** Get the application running with basic functionality

1. **Backend Setup**
   - [ ] Create FastAPI server.py with lifespan management
   - [ ] Set up SQLAlchemy database models
   - [ ] Implement database initialization and seeding
   - [ ] Create API routes structure
   - [ ] Add Pydantic models for request/response validation

2. **Frontend Foundation**
   - [ ] Create index.html with SPA structure
   - [ ] Implement dashboard.js component
   - [ ] Implement practice.js component
   - [ ] Implement progress.js component
   - [ ] Create api.js utility for backend communication
   - [ ] Style with main.css

3. **Configuration**
   - [ ] Create topics.yaml with Code Craze taxonomy
   - [ ] Set up .env and .env.template
   - [ ] Create pyproject.toml with dependencies
   - [ ] Create start.sh, stop.sh, restart.sh scripts

4. **Sample Content**
   - [ ] Create 10-15 sample questions per topic (50+ total)
   - [ ] Include detailed explanations and teaching points
   - [ ] Add code snippets where applicable

### Phase 2: Services Implementation
**Goal:** Intelligent learning system

1. **Competency Service**
   - [ ] Implement update_competency()
   - [ ] Implement get_user_competencies()
   - [ ] Implement calculate_competition_readiness()
   - [ ] Implement get_recommendations()

2. **Adaptive Learning Service**
   - [ ] Implement question selection algorithm
   - [ ] Add practice mode weighting
   - [ ] Implement difficulty adaptation
   - [ ] Add recent question avoidance

### Phase 3: Content Population
**Goal:** Comprehensive question bank

- [ ] 100+ questions for Principles of Coding
- [ ] 100+ questions for AI & Machine Learning
- [ ] 100+ questions for Cryptography
- [ ] 100+ questions for Python Fundamentals
- [ ] 50+ questions for Quantum Computing (Div C only)

### Phase 4: Polish & Testing
**Goal:** Production-ready application

- [ ] Unit tests for all services
- [ ] Integration tests for API endpoints
- [ ] UI/UX refinements
- [ ] Documentation completion

---

## Files to Copy/Adapt from Circuit Lab

### Direct Copy (with path updates)
- `backend/config/settings.py` - Environment configuration
- `backend/database/db.py` - Database setup
- `start.sh`, `stop.sh`, `restart.sh` - Scripts
- `.env.template` - Configuration template
- `pyproject.toml` - Dependencies (same stack)

### Adapt with Content Changes
- `backend/database/models.py` - Same schema, different app name
- `backend/api/routes.py` - Same routes, Code Craze naming
- `backend/api/models.py` - Same Pydantic models
- `backend/services/competency_service.py` - Same logic
- `backend/services/adaptive_learning.py` - Same algorithm
- `frontend/index.html` - New branding, same structure
- `frontend/components/*.js` - Same logic, new content
- `frontend/utils/api.js` - Same API client
- `frontend/styles/main.css` - New color scheme

### Create New
- `content/config/topics.yaml` - Code Craze topic taxonomy
- `content/questions/sample_questions.json` - Code Craze questions
- `README.md` - New documentation
- `CLAUDE.md` - Project guidelines
- `TASK.md` - Development roadmap

---

## Branding & Theming

### Application Name
- **Code Craze Academy** (following "Circuit Cadet Academy" pattern)

### Color Scheme Suggestion
- Primary: `#2563eb` (Blue - coding/tech theme)
- Secondary: `#7c3aed` (Purple - AI/quantum theme)
- Accent: `#10b981` (Green - success/progress)
- Background: `#f8fafc` (Light gray)

### Mascot/Theme
- Coding-themed mascot (robot, pixel character, etc.)
- Tech-inspired icons for each topic area

---

## Success Criteria

1. **Functional Parity**: All features from Circuit Lab working
2. **Content Coverage**: Questions for all Code Craze topics
3. **Adaptive Learning**: Intelligent question selection
4. **Competition Readiness**: Students can simulate competition conditions
5. **Zero Cloud Dependencies**: Fully local operation

---

## Next Steps

1. Start Phase 1 implementation
2. Copy and adapt core files from circuit-lab
3. Create Code Craze topic taxonomy
4. Build initial question bank
5. Test and iterate

---

*Implementation Plan Created: 2026-01-28*
*Reference Repository: /home/junior/src/circuit-lab*
