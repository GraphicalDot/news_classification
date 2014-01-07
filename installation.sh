#!/bin/bash


echo -e "\n\nMaking application logs directory which will have the related logs for all the applications running\n\n"
sudo mkdir /applogs

echo -e "\n\nInstalling supervisord  and its changing its configuration file for gunicorn\n\n"
pip install supervisor
echo_supervisord_conf > /etc/supervisord.conf
cp /home/ubuntu



