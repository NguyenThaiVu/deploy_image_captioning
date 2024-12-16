#!/bin/bash

# Variables
ACR_NAME="thaivubackend.azurecr.io"                # Replace with your ACR name
IMAGE_NAME="backend"      # Replace with your Docker image name
TAG="v1"                        # Replace with the image tag

# Get the ACR login server
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer --output tsv)

# Login to ACR
echo "Logging in to Azure Container Registry: $ACR_NAME"
az acr login --name $ACR_NAME

# Tag the Docker image
echo "Tagging the Docker image..."
docker tag $IMAGE_NAME $ACR_LOGIN_SERVER/$IMAGE_NAME:$TAG

# Push the Docker image to ACR
echo "Pushing the Docker image to ACR..."
docker push $ACR_LOGIN_SERVER/$IMAGE_NAME:$TAG

# Confirmation message
echo "Docker image pushed successfully to $ACR_LOGIN_SERVER/$IMAGE_NAME:$TAG"
