# build client
cd client
npm run build
cd ..

# Copy compiled client into static folder of server
cp -dr ./client/build/* ./server/static/

echo "Build process complete."
