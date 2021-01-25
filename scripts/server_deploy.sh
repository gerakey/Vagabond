#Fully automated the deployement process. ONLY RUN THIS SCRIPT ON THE 
#REMOTE SERVER! If you run this on your local machine, you're gonna 
#have a bad time.

#Auto generated vagabond config
echo "
config = {
    'mysql_server': '127.0.0.1',
    'mysql_user': '$USER',
    'mysql_password': 'password',
    'mysql_port': '3306',
    'mysql_database': '$USER',
    'domain': '$USER.teamvagabond.com',
    'api_url': 'https://$USER.teamvagabond.com/api/v1'
}
" > ../server/vagabond/config/config.py

#WSGI Config
echo "
#Auto-generated WSGI configuration
import sys
sys.path.insert(0, '/var/www/$USER/')
sys.path.insert(0, '/var/www/$USER/env/lib/python3.8/site-packages')
from vagabond import app as application
" > ../server/wsgi.py

#cd into root directory
cd ..

# Deploy app
rm -dr /var/www/$USER/*
cp -dr server/* /var/www/$USER/

#cd back into scripts folder
cd scripts

sudo service apache2 restart
echo "Application has been deployed. Please restart apache if needed." 
