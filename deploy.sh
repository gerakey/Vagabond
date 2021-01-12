#Build client first...
bash build.sh

# Deploy app
sudo rm -dr /var/www/$USER/*
sudo cp -dr server/* /var/www/$USER/

echo "Application has been deployed. Please restart apache if needed." 
