#!/bin/bash

# Build and push to GitHub Container Registry
# Usage: ./push-to-ghcr.sh [USERNAME]

set -e

USERNAME=${1:-$(gh api user -q .login)}
if [ -z "$USERNAME" ]; then
    echo "Error: Could not determine GitHub username"
    echo "Usage: $0 [GITHUB_USERNAME]"
    exit 1
fi

IMAGE_PREFIX="ghcr.io/$USERNAME/photo-app"

echo "Building and pushing images to $IMAGE_PREFIX..."
echo ""

# Build backend
echo "Building backend..."
docker build -t "$IMAGE_PREFIX/backend:latest" ./backend
docker push "$IMAGE_PREFIX/backend:latest"

# Build frontend
echo "Building frontend..."
docker build -t "$IMAGE_PREFIX/frontend:latest" ./frontend
docker push "$IMAGE_PREFIX/frontend:latest"

# Build nginx
echo "Building nginx..."
docker build -t "$IMAGE_PREFIX/nginx:latest" ./nginx
docker push "$IMAGE_PREFIX/nginx:latest"

echo ""
echo "Done! Images pushed to:"
echo "  - $IMAGE_PREFIX/backend:latest"
echo "  - $IMAGE_PREFIX/frontend:latest"
echo "  - $IMAGE_PREFIX/nginx:latest"
