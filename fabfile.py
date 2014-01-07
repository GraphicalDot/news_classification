
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

def virtual_env():
	run("sudo pip install virtualenv")
	with cd("/home/ubuntu/"):
		run("virtualenv --no-site-packages VirtualEnvironment")
		with cd("/home/ubuntu/VirtualEnvironment"):
			run("sudo apt-get install -y git")
			with prefix("source bin/activate"):
				run("git clone https://github.com/kaali-python/news_classification.git")
				run("ls")


def diploy():
	print(_green("Connecting to EC2 Instance..."))	
	with hide("warnings"):
	#	execute(AD_virtuaEnv)
		execute(virtual_env)
		print(_yellow("...Disconnecting EC2 instance..."))
		disconnect_all()


