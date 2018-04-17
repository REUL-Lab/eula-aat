#!/bin/bash

# Add repos and download using apt
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get update
sudo apt-get install -y uwsgi python-dev uwsgi-plugin-python python-pip default-jre nginx nodejs mongodb-org-server google-chrome-stable g++ make unzip

# Install boilerpipe
git clone https://github.com/misja/python-boilerpipe.git /tmp/python-boilerpipe
# Save directory so we an climb back
olddir=$(pwd)

pip install -r /tmp/python-boilerpipe/requirements.txt
cd /tmp/python-boilerpipe/ && python /tmp/python-boilerpipe/setup.py install

cd $olddir
rm -rf /tmp/python-boilerpipe

wget https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip -P /tmp
unzip /tmp/chromedriver_linux64.zip -d /bin
rm /tmp/chromedriver_linux64.zip

pip install -r requirements.txt

# Install punkt
python -c 'import nltk; nltk.download("punkt", download_dir="/usr/local/share/nltk_data")'