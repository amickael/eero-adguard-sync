TAG="amickael/eero-adguard-sync:$(cat ../VERSION)"

echo "$DOCKER_HUB_TOKEN" | docker login -u "$DOCKER_HUB_USERNAME" --password-stdin
docker build -t "$TAG" .
docker push "$TAG"
