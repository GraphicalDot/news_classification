
from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, env, require, hide
from fabric.contrib.console import confirm
from fabric.network import disconnect_all
from fabric.colors import green as _green, yellow as _yellow
import os


env.use_ssh_config = True
env.hosts = ["ec2-54-208-89-26.compute-1.amazonaws.com"]
env.user = "ubuntu"
env.key_filename = "/home/k/Programs/PemFiles/sanil_news.pem"

def diskspace():
	print(_green("Connecting..."))	
	with hide("warnings"):
		run('df -h')
		run("ps aux| grep mongo")
		disconnect_all()
