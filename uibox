#!/usr/bin/python3

import sys
import os
import shutil

args = sys.argv

if "--uninstall" in args:
	path = "/opt/TheBossBaby-app"
	if os.path.exists(path):
		shutil.rmtree(path)
	else:
		print(" [!] TheBossBaby-app Directory is not exists.")