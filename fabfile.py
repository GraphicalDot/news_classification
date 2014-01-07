
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

def AD_virtuaEnv():
	run("sudo apt-get upgrade")
	run("sudo apt-get update")
	run("sudo apt-get install -y libevent-dev")
	run("sudo apt-get install -y python-all-dev")
	run("sudo apt-get install -y python-pip")
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

def installation_script():
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("sudo chmod 755 installation.sh")
		run("./installation.sh")



def nginx():
	"""
	This function installs nginx on the remote server and replaces its conf file with the one available in the
	git repository.Finally restart the nginx server
	"""
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("sudo apt-get install -y nginx")
	execute(update_nginx_conf)
	run("sudo service nginx restart")



def update_nginx_conf():
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification/configs"):
		run("sudo cp nginx.conf /etc/nginx/sites-enabled/default")




def mongo():
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification"):
		run("sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10")
		run("echo -e 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list")
		run("sudo apt-get update")
		run("sudo apt-get install -y mongodb-10gen")
	execute(update_mongo_conf)
	run("sudo service mongodb restart")

def update_mongo_conf():
	with prefix("cd /home/ubuntu/VirtualEnvironment &&source bin/activate && cd news_classification/configs"):
		run("sudo cp mongodb.conf /etc/mongodb.conf")



def supervisor():
	pass

def update():
	print(_green("Connecting to EC2 Instance..."))	
	with hide("warnings"):
		execute(updating_git)
		print(_yellow("...Disconnecting EC2 instance..."))
		disconnect_all()


def deploy():
	print(_green("Connecting to EC2 Instance..."))	
	with hide("warnings"):
	#	execute(AD_virtuaEnv)
	#	execute(installing_requirements)
		execute(mongo)
		print(_yellow("...Disconnecting EC2 instance..."))
		disconnect_all()

