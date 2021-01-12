# build client
cd client
npm run build
cd ..

# Copy compiled client into static folder of server
cp -dr ./client/build/* ./server/static/

# Deploy app
sudo rm -dr /var/www/$USER/*
sudo cp -dr server/* /var/www/$USER/

echo "Build process complete. Application has been deployed. Please restart the apache web server if needed."
