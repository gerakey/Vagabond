#Checkout to master branch and pull updates
git checkout master
git pull

# Update python depdencies
cd server
pip3 install -r requirements.txt
cd ..

#Update JS dependencies
cd client
npm install
cd ..

