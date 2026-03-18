# Railway Quick Deploy Script
#!/bin/bash

set -e

echo "🚀 Railway Deployment Helper"
echo ""

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Check if logged in
echo "Checking Railway login..."
railway whoami || railway login

echo ""
echo "📋 Deployment Steps:"
echo ""
echo "1. Create project at https://railway.app"
echo "   - New Project → Deploy from GitHub repo"
echo "   - Select your photo-app repository"
echo ""
echo "2. Add PostgreSQL Database"
echo "   - New → Database → PostgreSQL"
echo "   - Railway will auto-set DATABASE_URL"
echo ""
echo "3. Set Environment Variables:"
echo "   - Go to Variables tab"
echo "   - Copy values from .env.railway.example"
echo ""
echo "4. Deploy:"
echo "   - Click Deploy button"
echo "   - Or run: railway up"
echo ""
echo "5. Run migrations:"
echo "   - railway run alembic upgrade head"
echo ""
echo "🔗 Useful Commands:"
echo "   railway link       # Link to existing project"
echo "   railway up         # Deploy current code"
echo "   railway logs       # View logs"
echo "   railway open       # Open dashboard"
echo ""

read -p "Open Railway dashboard? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    open https://railway.app
fi
