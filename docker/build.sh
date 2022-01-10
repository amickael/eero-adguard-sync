VERSION=$(cat ../VERSION)
TAG="amickael/eero-adguard-sync:$VERSION"

echo "$DOCKER_HUB_TOKEN" | docker login -u "$DOCKER_HUB_USERNAME" --password-stdin
docker build -t "$TAG" --build-arg EAG_VERSION="$VERSION" .
docker push "$TAG"
