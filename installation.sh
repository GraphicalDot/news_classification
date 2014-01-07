#!/bin/bash


echo -e "\n\nMaking application logs directory which will have the related logs for all the applications running\n\n"
sudo mkdir /applogs

echo -e "\n\nInstalling python easy_install tool\n\n"
sudo apt-get install -y python-setuptools python-dev build-essential


echo -e "\n\nInstalling python devlopers tools\n\n"
sudo easy_install greenlet
sudo easy_install gevent


echo -e "\n\nInstalling flask\n\n"
sudo pip install Flask


echo -e "\n\nInstalling mongodb\n\n"
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo -e 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
sudo apt-get update
sudo apt-get install -y mongodb-10gen

echo -e "Installing python application interface for using mongodb"
pip install pymongo


echo -e  "\n\nInstalling python reqeusts module to use http protocols\n\n"
pip install requests

echo -e "\n\nInstalling flask-restful for using http standard protocols to be used in python\n\n"
pip install flask-restful


echo -e "\n\nInstalling gunicorn and its dependicies\n\n"
pip install gunicorn

echo -e "\n\nInstalling supervisord  and its changing its configuration file for gunicorn\n\n"
pip install supervisor
echo_supervisord_conf > /etc/supervisord.conf
cp /home/ubuntu



