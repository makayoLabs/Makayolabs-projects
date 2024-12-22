#!/bin/bash

# Set variables
PROJECT_NAME=$1
IMAGE_NAME="${PROJECT_NAME}-image"
CLOUD_RUN_NAME="${PROJECT_NAME}-service"

# Step 1: Build Docker Image
echo "🚀 Building Docker Image..."
docker build -t $IMAGE_NAME .

# Step 2: Submit to Google Cloud Run
echo "🚢 Deploying to Google Cloud Run..."
gcloud run deploy $CLOUD_RUN_NAME \
    --image gcr.io/$(gcloud config get-value project)/$IMAGE_NAME \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated

echo "✅ Deployment Complete! Access your app:"
gcloud run services describe $CLOUD_RUN_NAME --platform managed --region us-central1 --format 'value(status.url)'
