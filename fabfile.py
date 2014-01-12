from __future__ import with_statement
from fabric.api import show, local, settings, prefix, abort, run, cd, env, require, hide, execute
from fabric.contrib.console import confirm
from fabric.network import disconnect_all
from fabric.colors import green as _green, yellow as _yellow, red as _red
from fabric.contrib.files import exists
from fabric.utils import error
import os
import time

env.use_ssh_config = True
env.hosts = ["ec2-54-236-232-96.compute-1.amazonaws.com"]
env.user = "ubuntu"
env.key_filename = "/home/k/Programs/PemFiles/sanil_news.pem"
env.warn_only = False

"""
This is the file which remotely makes an ec2 instance for the use of this repository
"""

def before_env():
	""""
	This method should be run before installing virtual environment as it will install python pip
	required to install virtual environment

	"""
	run("sudo apt-get upgrade")
	run("sudo apt-get update")
	run("sudo apt-get install -y python-pip")

def after_env():
	"""
	This method activates the virtual environment and in virtual environment installs the required dependicies
	and should be run after installing virtual environement
	"""
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("sudo apt-get install -y libevent-dev")
		run("sudo apt-get install -y python-all-dev")
		run("sudo apt-get install -y ipython")
		run("sudo apt-get install -y python-setuptools python-dev build-essential")
		run("sudo apt-get install -y libxml2-dev libxslt1-dev")


def virtual_env():
	"""
	This method installs the virual environment and after installing virtual environment installs the git.
	After installing the git installs the reuiqred repository
	"""

	run("sudo pip install virtualenv")
	with cd("/home/ubuntu/"):
		run("virtualenv --no-site-packages VirtualEnvironment")
		with cd("/home/ubuntu/VirtualEnvironment"):
			run("sudo apt-get install -y git")
			with prefix("source bin/activate"):
				if not exists("/applogs", use_sudo=True):
					run("sudo mkdir /applogs")
					run("sudo chown -R ubuntu:ubuntu /applogs")
				if not exists("/home/ubuntu/VirtualEnvironment/news_classification", use_sudo=True):	
					run("git clone https://github.com/kaali-python/news_classification.git")


def installing_requirements():
	"""
	This function installs all the requirements required to run the package with the help of requirements.txt
	"""
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate"):
		run("sudo pip install -r news_classification/requirements.txt")

def update_git():
	"""
	This method will be run everytime the git repository is updated on the main machine.This clones the pushed updated 
	repository on the git on the remote server
	"""
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("git pull origin master")


def nginx():
	"""
	This function installs nginx on the remote server and replaces its conf file with the one available in the
	git repository.Finally restart the nginx server
	"""
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("sudo apt-get install -y nginx")
	with prefix("cd /home/ubuntu/VirtualEnvironment/news_classification/configs"):
		run("sudo cp nginx.conf /etc/nginx/nginx.conf")
	execute(update_nginx_conf)



def update_nginx_conf():
	"""
	This method updates the nginx configuration which if updated in the git repository.
	Then restarts the nginx server
	"""
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification/configs"):
		run("sudo cp nginx_default.conf /etc/nginx/sites-enabled/default")
		run("sudo service nginx restart")


def nginx_status():
	    """
	    Check if nginx is installed.
	    """
	    with settings(hide("running", "stderr", "stdout")):
	    	result = run('if ps aux | grep -v grep | grep -i "nginx"; then echo 1; else echo ""; fi')
	    	if result:
			    print (_green("Nginx is running fine......................"))
	    	else:
			    print (_red("Nginx is not running ......................"))
			    confirmation = confirm("Do you want to trouble shoot here??", default=True)
			    if confirmation:
				    print (_green("Checking nginx configuration file"))
				    with show("debug", "stdout", "stderr"):
				    	run("sudo nginx -t")
				    	run("sudo service nginx restart")
				    	run("sudo tail -n 50 /applogs/nginx_error.logs")
		return 


def mongo():
	"""
	This method installs the mongodb database on the remote server.It after installing the mongodb replaces the 
	mongodb configuration with the one available in the git repository.

	"""
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10")
		run("echo -e 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list")
		run("sudo apt-get update")
		run("sudo apt-get install -y mongodb-10gen")
#		run("sudo cp configs/mongodb.conf /etc/mongodb.conf")
	run("sudo rm -rf  /var/lib/mongodb/mongod.lock")
	run("sudo service mongodb restart")


def mongo_status():
	    """
	    Check if nginx is installed.
	    """
	    with settings(hide("running", "stderr", "stdout")):
	    	result = run('if ps aux | grep -v grep | grep -i "mongodb"; then echo 1; else echo ""; fi')
	    	if result:
			    print (_green("Mongodb is running fine......................"))
	    	else:
			    print (_red("Mongodb is not running ......................"))
			    confirmation = confirm("Do you want to trouble shoot here??it will delete mongo.lock file", default=True)
			    if confirmation:
					run("sudo rm -rf  /var/lib/mongodb/mongod.lock ")
				    	run("sudo service mongodb restart")
		return 



def supervisord():
	"""
	It updates the supervisord configuration file which has already been installed by the pip -r requirements.txt
	"""
	with settings(user="ubuntu"):
		with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
			#You need to create a config file as you dont have the access 
			run("sudo touch /etc/supervisord.conf")
			run("sudo cp configs/supervisord.conf /etc/supervisord.conf")
			run("supervisord")

def update_supervisord_conf():
	"""
	This method updates the supervisord configuration file available in the git repository.It then restarts the 
	supervisord to update the configuration file.

	"""
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification/configs"):
		with show("debug", "stdout", "stderr"):
			run("sudo cp supervisord.conf /etc/supervisord.conf")
			run("sudo supervisorctl reload")


def supervisorctl(process):
	"""
	This method restart the process
	"""
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("sudo supervisorctl restart %s"%(process))

def supervisord_status():
	"""
	This method outputs the status of the process being run by supervisord on the remote server.
	"""
	print(_green("Getting status of the process running through supervisord..."))	
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("sudo supervisorctl status")
		
	confirmation = confirm("Do you want to trouble shoot here??", default=True)
	if confirmation:
		print (_green("Ouputting supervisor logs"))
		run("sudo tail -n 50 /applogs/supervisord.log")


def gunicorn_status():
	"""
	Check if gunicorn is running or not
	"""
	with settings(hide("running", "stdout", "stderr"), warn_only=True):
		result = run('if ps aux | grep -v grep | grep -i "gunicorn"; then echo 1; else echo ""; fi')
		if result:
			print (_green("Gunicorn is running fine......................"))
		else:
			print (_red("Gunicorn is not running ......................"))
			confirmation = confirm("Do you want to trouble shoot here??", default=True)
			if confirmation:
				print (_green("Ouputting gunicorn error logs"))
				with show("debug", "stdout", "stderr"):
					run("sudo tail -n 50 /applogs/gunicorn_error.logs")


def reboot():
	run("sudo reboot")


def status():
	print(_green("Connecting to EC2 Instance..."))	
	run("free -m")
	execute(supervisord_status)
	execute(mongo_status)
	execute(nginx_status)
	execute(gunicorn_status)
	print(_yellow("...Disconnecting EC2 instance..."))
	disconnect_all()



def update():
	print(_green("Connecting to EC2 Instance..."))	
	execute(update_git)
	execute(update_nginx_conf)
	execute(update_supervisord_conf)
	execute(nginx_status)
	execute(gunicorn_status)
		
	print(_yellow("...Disconnecting EC2 instance..."))
	disconnect_all()




def deploy():
	print(_green("Connecting to EC2 Instance..."))	
	execute(before_env)
	execute(virtual_env)
	execute(after_env)
	execute(installing_requirements)
	execute(nginx)
	execute(mongo)
	execute(supervisord)
	execute(status)
	print(_yellow("...Disconnecting EC2 instance..."))
#	run("sudo reboot")
	disconnect_all()

