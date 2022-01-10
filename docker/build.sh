VERSION=$(cat ../VERSION)
TAG="$DOCKER_HUB_USERNAME/eero-adguard-sync:$VERSION"

echo "$DOCKER_HUB_TOKEN" | docker login -u "$DOCKER_HUB_USERNAME" --password-stdin
docker build --no-cache -t "$TAG" --build-arg EAG_VERSION="$VERSION" .
docker push "$TAG"
