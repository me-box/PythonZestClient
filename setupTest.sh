
docker kill zest

ZEST_IMAGE_VERSION="jptmoore/zest:v0.1.1"


echo "start the store with the default key"
docker run -p 5555:5555 -p 5556:5556 -d --name zest -v /tmp/storekey.txt:/storekey.txt --rm ${ZEST_IMAGE_VERSION} /app/zest/server.exe --secret-key-file example-server-key --identity '127.0.0.1' --enable-logging
