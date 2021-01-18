#Fully automated the deployement process. ONLY RUN THIS SCRIPT ON THE 
#REMOTE SERVER! If you run this on your local machine, you're gonna 
#have a bad time.


#Build client first...
bash build.sh

#cd into root directory
cd ..

# Deploy app
sudo rm -dr /var/www/$USER/*
sudo cp -dr server/* /var/www/$USER/

#cd back into scripts folder
cd scripts

echo "Application has been deployed. Please restart apache if needed." 
