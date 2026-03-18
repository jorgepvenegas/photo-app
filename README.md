# Photo Sharing App

A full-stack photo sharing application built with FastAPI, Vue.js 3, PostgreSQL, and Cloudflare R2.

## Features

- **Authentication**: JWT-based auth with email verification (via Resend)
- **Photo Upload**: Direct upload to Cloudflare R2 via presigned URLs
- **Photo Gallery**: Responsive grid with lazy loading
- **Comments**: Flat comment system on photos
- **Thumbnails**: Automatic thumbnail generation (small/medium/large)
- **Responsive UI**: Built with Tailwind CSS

## Tech Stack

**Backend**
- FastAPI + Python 3.11
- SQLAlchemy 2.0 + asyncpg
- FastAPI-Users (authentication)
- Alembic (migrations)
- Pillow (image processing)
- Boto3 (R2/S3 storage)
- Resend (email)

**Frontend**
- Vue.js 3 + Vite
- Pinia (state management)
- Vue Router
- Tailwind CSS
- TypeScript

**Infrastructure**
- PostgreSQL 15
- Cloudflare R2 (image storage)
- Docker + Docker Compose
- Railway (deployment)

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Environment Setup

1. Clone the repository
2. Copy environment variables:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and fill in your credentials:
   - Database settings
   - R2 credentials (Cloudflare)
   - Resend API key
   - JWT secrets

### Docker Development

Start all services:
```bash
docker-compose up -d
```

This starts:
- PostgreSQL on port 5432
- FastAPI backend on port 8000 (with hot reload)
- Vue.js frontend on port 5173 (with HMR)
- Nginx reverse proxy on port 80

Access the application:
- App: http://localhost
- API Docs: http://localhost/docs
- Frontend Dev: http://localhost:5173

### Local Development (without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head  # Run migrations
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Database Migrations

Create a new migration:
```bash
cd backend
alembic revision --autogenerate -m "description"
```

Run migrations:
```bash
alembic upgrade head
```

## Deployment (GHCR - GitHub Container Registry)

### Option 1: Automatic (GitHub Actions)

1. Push to GitHub - workflows in `.github/workflows/` will auto-build and push images
2. Images will be published to `ghcr.io/YOUR_USERNAME/photo-app/*`
3. Ensure GitHub Actions has permissions to write packages (Settings → Actions → Workflow permissions)

### Option 2: Manual Build & Push

**Login to GHCR:**
```bash
# Using GitHub CLI
echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin

# Or manually
docker login ghcr.io -u YOUR_USERNAME
```

**Build and push all images:**
```bash
./scripts/push-to-ghcr.sh YOUR_USERNAME
```

**Or build individually:**
```bash
# Backend
docker build -t ghcr.io/YOUR_USERNAME/photo-app/backend:latest ./backend
docker push ghcr.io/YOUR_USERNAME/photo-app/backend:latest

# Frontend
docker build -t ghcr.io/YOUR_USERNAME/photo-app/frontend:latest ./frontend
docker push ghcr.io/YOUR_USERNAME/photo-app/frontend:latest

# Nginx
docker build -t ghcr.io/YOUR_USERNAME/photo-app/nginx:latest ./nginx
docker push ghcr.io/YOUR_USERNAME/photo-app/nginx:latest
```

### Deploy with GHCR Images

**Using production docker-compose:**
```bash
# Set your GitHub username
export GITHUB_USERNAME=yourusername

# Deploy
docker compose -f docker-compose.prod.yml up -d
```

## Deployment (Railway)

Railway is the easiest way to deploy this application with automatic scaling and managed PostgreSQL.

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### Step 2: Create Railway Project

1. Go to https://railway.app and login with GitHub
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `photo-app` repository
5. Railway will detect `railway.toml` and use the backend Dockerfile

### Step 3: Add PostgreSQL Database

1. In your Railway project dashboard, click "New"
2. Select "Database" → "Add PostgreSQL"
3. Railway will automatically provide `DATABASE_URL` env var

### Step 4: Configure Environment Variables

Add these variables in Railway dashboard (Variables tab):

```bash
# Auth (generate secure random strings, 32+ chars)
JWT_SECRET=your-super-secret-key-here-minimum-32-chars
SECRET_KEY=another-secret-key-here-minimum-32-chars

# R2 Storage (from your .env)
R2_ENDPOINT=https://<account>.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your-key
R2_SECRET_ACCESS_KEY=your-secret
R2_BUCKET_NAME=photo-app
R2_PUBLIC_URL=https://<bucket>.<account>.r2.dev

# Email (Resend)
RESEND_API_KEY=re_xxxx
RESEND_FROM_EMAIL=noreply@yourdomain.com

# App URLs (update with your Railway domain)
APP_URL=https://photoapp-production.up.railway.app
FRONTEND_URL=https://photoapp-production.up.railway.app
DEBUG=false
```

### Step 5: Deploy Backend

Railway will auto-deploy when you push to GitHub. 

**First deployment:**
1. Deploy the backend service
2. Once running, go to the service → "Deploy" tab
3. Click "Deploy" to trigger first build

**Run migrations:**
1. Go to service "Logs" tab
2. Click "Start Command" and run: `alembic upgrade head`
3. Or use Railway CLI: `railway run alembic upgrade head`

### Step 6: Deploy Frontend (Static Site)

Railway can host the frontend as a static site:

1. In Railway project, click "New" → "Empty Service"
2. Connect same GitHub repo
3. Set Root Directory: `frontend`
4. Build Command: `npm install && npm run build`
5. Start Command: `npx serve -s dist -l 3000`
6. Add env var: `VITE_API_URL=https://your-backend-url.railway.app/api/v1`

### Step 7: Custom Domain (Optional)

1. Go to backend service → Settings → Domains
2. Click "Generate Domain" or add custom domain
3. Update `APP_URL` and `FRONTEND_URL` env vars with new domain
4. Redeploy both services

### Railway CLI (Alternative)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# Deploy
railway up

# Run migrations
railway run alembic upgrade head
```

### Troubleshooting

**CORS errors:** Update `FRONTEND_URL` env var to match your actual domain

**Database connection:** Ensure `DATABASE_URL` is set by Railway automatically

**R2 uploads failing:** Check R2 CORS policy includes your Railway domain

**Emails not sending:** Verify Resend domain is verified for production

## Project Structure

```
photo-app/
├── docker-compose.yml      # Local development orchestration
├── railway.toml            # Railway deployment config
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── services/       # Business logic (R2, email, images)
│   │   ├── main.py         # FastAPI entry point
│   │   ├── models.py       # SQLAlchemy models
│   │   └── schemas.py      # Pydantic schemas
│   └── alembic/            # Database migrations
├── frontend/               # Vue.js application
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── views/          # Page views
│   │   ├── stores/         # Pinia stores
│   │   ├── api/            # API client
│   │   └── types/          # TypeScript types
│   └── package.json
└── nginx/                  # Nginx configuration
```

## API Documentation

When running locally, API documentation is available at:
- Swagger UI: http://localhost/docs
- ReDoc: http://localhost/redoc

## License

MIT
