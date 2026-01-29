# Code Craze Academy - Deployment Plan

## Overview

This plan outlines how to deploy Code Craze Academy as a web application accessible to external users. We'll cover multiple hosting options with their trade-offs.

---

## Recommended Platform: Render (Free Tier)

Render offers the best balance of simplicity, features, and free tier for educational applications.

### Why Render?
- Free tier available (with limitations)
- Native Python/FastAPI support
- Automatic HTTPS certificates
- Git-based deployments
- Persistent disk storage option (paid)
- Managed PostgreSQL available

### Free Tier Limitations
- Services sleep after 15 minutes of inactivity
- First request after sleep takes ~50 seconds
- 750 hours/month of free usage
- SQLite data may not persist across deployments without persistent disk

---

## Pre-Deployment Tasks

### 1. Database Decision

**Option A: Keep SQLite (Simple, but limited)**
- Works for demo/educational purposes
- Data resets on each deployment (free tier)
- Requires persistent disk ($7/month) for data persistence

**Option B: Migrate to PostgreSQL (Recommended for production)**
- Data persists across deployments
- Free tier: 1GB storage, expires after 90 days
- Better for multiple concurrent users

### 2. Required Files to Create

#### `requirements.txt`
```
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
sqlalchemy>=2.0.36
pydantic>=2.10.0
pydantic-settings>=2.6.0
python-dotenv>=1.0.1
passlib[bcrypt]>=1.7.4
python-jose[cryptography]>=3.3.0
python-multipart>=0.0.12
pyyaml>=6.0.2
gunicorn>=21.0.0
psycopg2-binary>=2.9.9
```

#### `Procfile`
```
web: gunicorn backend.server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

#### `render.yaml`
```yaml
services:
  - type: web
    name: code-craze-academy
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn backend.server:app -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: "3.11"
      - key: DEBUG
        value: "false"
      - key: PORT
        value: "8989"
      - key: SECRET_KEY
        generateValue: true
```

#### `runtime.txt`
```
python-3.11.7
```

---

## Deployment Steps for Render

### Step 1: Prepare Repository

1. Push code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit for deployment"
git remote add origin https://github.com/YOUR_USERNAME/code-craze.git
git push -u origin main
```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Authorize Render to access your repositories

### Step 3: Deploy Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: code-craze-academy
   - **Region**: Choose closest to your users
   - **Branch**: main
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend.server:app -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
4. Add Environment Variables:
   - `DEBUG=false`
   - `SECRET_KEY` (generate a secure random string)
5. Click "Create Web Service"

### Step 4: Wait for Deployment

- Render will build and deploy automatically
- Access your app at: `https://code-craze-academy.onrender.com`

---

## Alternative Platforms

### Railway ($5/month credit)

**Pros:**
- Very simple deployment
- Great UI and developer experience
- $5 free credit monthly

**Cons:**
- Requires credit card
- App stops when credit exhausted

**Deploy Command:**
```bash
railway login
railway init
railway up
```

### Fly.io (Pay-as-you-go)

**Pros:**
- Global edge deployment
- Persistent volumes available
- More control over infrastructure

**Cons:**
- Steeper learning curve
- CLI-focused workflow

**Deploy Command:**
```bash
fly launch
fly deploy
```

### PythonAnywhere (Free tier available)

**Pros:**
- Specifically designed for Python
- Free tier with limitations
- Web-based IDE

**Cons:**
- More limited than other options
- Older interface

---

## Code Modifications Required

### 1. Update `backend/server.py`

Add production ASGI configuration:

```python
import os

# Get port from environment (required for cloud platforms)
port = int(os.environ.get("PORT", 8989))

# In main() function, update uvicorn.run:
uvicorn.run(
    "backend.server:app",
    host="0.0.0.0",
    port=port,
    reload=False,  # Disable in production
    log_level="info",
)
```

### 2. Update `backend/config/settings.py`

Make settings production-ready:

```python
# Add to Settings class
port: int = Field(default=8989, alias="PORT")

# Update in Config
@property
def is_production(self) -> bool:
    return not self.debug
```

### 3. Update CORS Settings

Allow your deployed domain:

```python
# In settings.py, update allowed_origins
allowed_origins: str = Field(
    default="http://localhost:8989,https://code-craze-academy.onrender.com",
    alias="ALLOWED_ORIGINS"
)
```

### 4. Database Path for Production

Update `backend/database/db.py` to handle cloud environments:

```python
import os

# Use environment variable for database URL in production
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DB_DIR}/code_craze.db"
)

# Handle PostgreSQL URL format from Render
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
```

---

## PostgreSQL Migration (Optional but Recommended)

If using Render's PostgreSQL:

### 1. Create PostgreSQL Database on Render

1. Click "New +" → "PostgreSQL"
2. Name: `code-craze-db`
3. Choose Free tier
4. Copy the Internal Database URL

### 2. Update Environment Variables

Add to your web service:
- `DATABASE_URL`: (paste the internal URL from PostgreSQL)

### 3. Update SQLAlchemy Connection

The `db.py` changes above will automatically handle PostgreSQL connections.

---

## Security Checklist

Before deploying:

- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Set `DEBUG=false` in production
- [ ] Update CORS origins to include only your domain
- [ ] Remove default test user password or disable test user
- [ ] Enable HTTPS (automatic on Render)
- [ ] Review environment variables for sensitive data

---

## Post-Deployment Tasks

1. **Test the deployed application**
   - Visit `https://your-app.onrender.com`
   - Test all functionality
   - Check API docs at `/docs`

2. **Set up monitoring**
   - Render provides basic metrics
   - Check logs for errors

3. **Share with users**
   - Distribute the URL to students
   - Consider custom domain ($7/month on Render)

---

## Cost Summary

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| **Render** | 750 hrs/month, sleeps after 15min | $7/month (always on) |
| **Railway** | $5 credit/month | Pay as you go |
| **Fly.io** | Limited free resources | Pay as you go |
| **PythonAnywhere** | Limited CPU, bandwidth | $5+/month |

---

## Quick Start Checklist

1. [ ] Create `requirements.txt`
2. [ ] Create `Procfile`
3. [ ] Create `render.yaml`
4. [ ] Update server.py for production port
5. [ ] Update CORS settings
6. [ ] Push to GitHub
7. [ ] Create Render account
8. [ ] Deploy web service
9. [ ] Test deployed application
10. [ ] Share URL with users

---

## Support Resources

- [Render FastAPI Deployment Guide](https://render.com/articles/fastapi-deployment-options)
- [FastAPI Official Deployment Docs](https://fastapi.tiangolo.com/deployment/)
- [Railway FastAPI Guide](https://docs.railway.com/guides/fastapi)

---

*Deployment Plan Created: 2026-01-28*
