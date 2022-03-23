#! /bin/bash

cd /app/mobile

npm install
cd ./android
chmod +x gradlew
rm -rf ./app/build/generated/res
./gradlew --scan assembleRelease