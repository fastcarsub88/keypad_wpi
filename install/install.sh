#!/bin/bash

sudo apt-get install build-essential python-pip python-dev python-smbus git nginx python-pigpio -y
cd /home/pi
sudo pip install uwsgi
git clone https://github.com/fastcarsub88/keypad_wpi.git
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /home/pi/keypad/install/nginx_conf /etc/nginx/sites-enabled/
sudo nginx -s reload
sudo systemctl link /home/pi/keypad/install/wiegand_web.service
sudo systemctl link /home/pi/keypad/install/wiegand_reader.service
sudo systemctl link /home/pi/keypad/install/wiegand_schedule.service
sudo systemctl enable pigpiod
sudo systemctl enable wiegand_web
sudo systemctl enable wiegand_reader
sudo systemctl enable wiegand_schedule
