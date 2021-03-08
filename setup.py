import os
import shutil
import json
import sys

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

def set_settings():
    from PyQt5.QtCore import QSettings    
    setting = QSettings("Everyskills", "TheBossBaby")
    data = json.load(open(base_dir + "settings.json"))

    for k, v in data.items():
        setting.setValue(k, v)

def main():
    os.system(f"{sys.argv[0]} -m pip install -r {base_dir + 'requirements.txt'} --user")

    ## set TheBossBaby settings file
    set_settings()

    ### Copy UIBxo Module to python library
    from distutils.sysconfig import get_python_lib
    _path = get_python_lib()
    shutil.copytree(base_dir + "UIBox", _path + "/UIBox")
    print(" [+] Copied UIBox Module -> ", _path, "\tDone...")

    if sys.platform.startswith("linux"):
    	path = "/opt/TheBossBaby-app"
    	if not os.path.exists(path):
    		os.mkdir(path)
    	shutil.copytree(base_dir + "src", path + "/src")
    	print(" [+] Copied TheBossBaby App -> ", path, "\tDone...")
    	shutil.copy2(base_dir + "uibox", "/usr/bin/")
	    print(" [+] Copied uibox CLI tool -> ", "/usr/bin/", "\tDone...")

if __name__ == "__main__":
    try:
        main()
    except PermissionError:
        print("You must be root or sudo to run this file on Linux")
    except FileExistsError:
        pass
