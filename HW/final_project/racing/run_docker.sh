#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to display usage information
usage() {
    echo "Usage: $0 [--build | --run | --clean | --help]"
    echo ""
    echo "Options:"
    echo "  --build    Build the Docker image without running the container"
    echo "  --run      Run an existing Docker image without rebuilding"
    echo "  --clean    Remove the Docker image and container"
    echo "  --help     Display this help message"
    echo ""
    echo "If no option is provided, the script will build and run the container."
}

# Set default behavior
BUILD=true
RUN=true
CLEAN=false

# Parse command-line arguments
if [ $# -gt 0 ]; then
    case "$1" in
        --build)
            BUILD=true
            RUN=false
            ;;
        --run)
            BUILD=false
            RUN=true
            ;;
        --clean)
            CLEAN=true
            BUILD=false
            RUN=false
            ;;
        --help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
fi

# Define image and container names
IMAGE_NAME="racing-app"
CONTAINER_NAME="racing-app-container"

# Clean existing containers and images if requested
if [ "$CLEAN" = true ]; then
    echo "Cleaning up existing Docker resources..."
    docker rm -f $CONTAINER_NAME 2>/dev/null || true
    docker rmi -f $IMAGE_NAME 2>/dev/null || true
    echo "Cleanup complete."
    exit 0
fi

# Build the Docker image if requested
if [ "$BUILD" = true ]; then
    echo "Building Docker image..."
    docker build -t $IMAGE_NAME .
fi

# Run the container if requested
if [ "$RUN" = true ]; then
    echo "Running Docker container..."
    # Stop and remove existing container if it exists
    docker rm -f $CONTAINER_NAME 2>/dev/null || true
    # Run the container with port mapping
    docker run -d -p 5001:5001 --name $CONTAINER_NAME $IMAGE_NAME
    echo "Container is running at http://localhost:5001"
fi

exit 0 