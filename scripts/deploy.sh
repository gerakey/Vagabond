#Fully automated the deployement process. ONLY RUN THIS SCRIPT ON THE 
#REMOTE SERVER! If you run this on your local machine, you're gonna 
#have a bad time.


#Build client first...
bash build.sh

#cd into root directory
cd ..

# Deploy app
rm -dr /var/www/$USER/*
cp -dr server/* /var/www/$USER/

#cd back into scripts folder
cd scripts

#WSGI Config
echo "
#Auto-generated WSGI configuration
import sys
sys.path.insert(0, '/var/www/$USER/')
sys.path.insert(0, '/var/www/$USER/env/lib/python3.8/site-packages')
from vagabond import app as application
" > /var/www/$USER/wsgi.py 

sudo service apache2 restart
echo "Application has been deployed. Please restart apache if needed." 
