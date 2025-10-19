#!/bin/bash
# deploy_frontend.sh
# Make sure you have AWS CLI installed and configured

set -e  # Exit on any error

# ----- CONFIGURATION -----
FRONTEND_DIR="/Users/karandeepsingh/Desktop/Projects/twin/frontend"                       # Path to your frontend source
BUILD_DIR="$FRONTEND_DIR/build"                # Build output folder
S3_BUCKET="twin-dev-frontend-606780901104"    # Your S3 bucket
CLOUDFRONT_DIST_ID="E3GMKRVAQYEGMU"           # CloudFront distribution ID

# ----- STEP 1: Build frontend -----
echo "🔧 Building frontend..."
cd "$FRONTEND_DIR"
npm install
npm run build

# ----- STEP 2: Sync to S3 -----
echo "☁️  Syncing build to S3 bucket $S3_BUCKET..."
aws s3 sync "$BUILD_DIR" "s3://$S3_BUCKET" --delete

# ----- STEP 3: Invalidate CloudFront cache -----
echo "🚀 Invalidating CloudFront distribution $CLOUDFRONT_DIST_ID..."
aws cloudfront create-invalidation \
    --distribution-id "$CLOUDFRONT_DIST_ID" \
    --paths "/*"

echo "✅ Deployment complete!"
