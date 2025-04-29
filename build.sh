#!/bin/bash
set -e

# Configuration
IMAGE_NAME="driesv/doc-processor"
VERSION=$(python3 -c "exec(open('_version.py').read()); print(__version__)")
PLATFORMS="linux/amd64,linux/arm64"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Building Doc Processor Docker image${NC}"
echo -e "Version: ${GREEN}$VERSION${NC}"
echo -e "Platforms: ${GREEN}$PLATFORMS${NC}"

# Build and push for multiple platforms
echo -e "${YELLOW}Building and pushing multi-architecture image...${NC}"
docker buildx build --platform $PLATFORMS \
  --tag $IMAGE_NAME:latest \
  --tag $IMAGE_NAME:$VERSION \
  --push \
  ./src

echo -e "${GREEN}Build and push completed successfully!${NC}"
echo -e "Image is available at:"
echo -e "  ${GREEN}$IMAGE_NAME:latest${NC}"
echo -e "  ${GREEN}$IMAGE_NAME:$VERSION${NC}" 