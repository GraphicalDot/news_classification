
from __future__ import with_statement
from fabric.api import local, settings, prefix, abort, run, cd, env, require, hide, execute
from fabric.contrib.console import confirm
from fabric.network import disconnect_all
from fabric.colors import green as _green, yellow as _yellow
import os


env.use_ssh_config = True
env.hosts = ["ec2-54-208-89-26.compute-1.amazonaws.com"]
env.user = "ubuntu"
env.key_filename = "/home/k/Programs/PemFiles/sanil_news.pem"


"""
This is the file which remotely makes an ec2 instance for the use of this repository
"""

def before_env():
	run("sudo apt-get upgrade")
	run("sudo apt-get update")
	run("sudo apt-get install -y python-pip")

def after_env():
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("sudo apt-get install -y libevent-dev")
		run("sudo apt-get install -y python-all-dev")
		run("sudo apt-get install -y ipython")
		run("sudo apt-get install -y python-setuptools python-dev build-essential")


def virtual_env():
	run("sudo pip install virtualenv")
	with cd("/home/ubuntu/"):
		run("virtualenv --no-site-packages VirtualEnvironment")
		with cd("/home/ubuntu/VirtualEnvironment"):
			run("sudo apt-get install -y git")
			with prefix("source bin/activate"):
				run("git clone https://github.com/kaali-python/news_classification.git")


def installing_requirements():
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("sudo pip install -r requirements.txt")

def updating_git():
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("git pull origin master")


def nginx():
	"""
	This function installs nginx on the remote server and replaces its conf file with the one available in the
	git repository.Finally restart the nginx server
	"""
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("sudo apt-get install -y nginx")
	execute(update_nginx_conf)



def update_nginx_conf():
	"""
	This method updates the nginx configuration which if updated in the git repository.
	Then restarts the nginx server
	"""
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification/configs"):
		run("sudo cp nginx.conf /etc/nginx/sites-enabled/default")
		run("sudo service nginx restart")




def mongo():
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10")
		run("echo -e 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list")
		run("sudo apt-get update")
		run("sudo apt-get install -y mongodb-10gen")
	execute(update_mongo_conf)

def update_mongo_conf():
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification/configs"):
		run("sudo cp mongodb.conf /etc/mongodb.conf")
		run("sudo service mongodb restart")
	

def supervisord():
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("echo_supervisord_conf > /etc/supervisord.conf")
	execute("update_supervisord_conf")

def update_supervisord_conf():
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification/configs"):
		run("sudo cp supervisord.conf /etc/supervisord.conf")
		run("supervisorctl restart")


def supervisorctl(process):
	"""
	This method restart the process
	"""
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("supervisorctl restart %s"%(process))

def supervisor_status():
	"""
	This method outputs the status of the process being run by supervisord
	"""
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("supervisorctl status")


def update():
	print(_green("Connecting to EC2 Instance..."))	
	with hide("warnings"):
		execute(updating_git)
		print(_yellow("...Disconnecting EC2 instance..."))
		disconnect_all()


def deploy():
	print(_green("Connecting to EC2 Instance..."))	
	with hide("warnings"):
		execute(before_env)
		execute(virtual_env)
		execute(after_env)
		execute(installing_requirements)
		execute(nginx)
		execute(mongo)
		execute(supervisord)
		print(_yellow("...Disconnecting EC2 instance..."))
		run("sudo reboot")
		disconnect_all()

