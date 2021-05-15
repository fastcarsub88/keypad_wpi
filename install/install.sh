#!/bin/bash

sudo apt-get install build-essential python-pip python-dev python-smbus git nginx -y
cd /home/pi
git clone https://github.com/SequentMicrosystems/megaioind-rpi.git
cd megaioind-rpi/python/megaioind/
sudo python setup.py install
sudo pip install uwsgi
sudo pip install requests
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /home/pi/rcontrolpi/install/nginx_conf /etc/nginx/sites-enabled/
sudo nginx -s reload
sudo systemctl link /home/pi/rcontrolpi/install/rcontrol_web.service
sudo systemctl link /home/pi/rcontrolpi/install/rcontrol_sched.service
sudo systemctl enable rcontrol_web
sudo systemctl enable rcontrol_sched
