import os
import shutil

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

default_setting = """\
[General]
check_auto_complete=false
check_auto_launche=true
check_auto_update=true
check_frameless=true
check_history_storage=false
check_hor_pattern=false
check_round=true
check_shadow=false
check_show_left_icon=true
check_show_right_icon=true
key_clear_line_text=Ctrl+W
key_clear_split_line_text=Ctrl+B
key_extend_height="Ctrl+H, Ctrl+="
key_extend_width="Ctrl+W, Ctrl+="
key_focus_line_search=Ctrl+F
key_open_settings=F1
key_quit_app=Ctrl+Q
key_resize_to_larg="Ctrl+Alt+="
key_resize_to_small=Ctrl+Alt+-
key_select_split_line_text=Ctrl+L
key_toggle_window=Alt+Space
key_zoomout_height="Ctrl+H, Ctrl+-"
key_zoomout_width="Ctrl+W, Ctrl+-"
placeholder_text=The Boss Baby - Go...
start_up_text=
theme=
window_height=319
window_max_extend=670
window_min_extend=58
window_opacity=1
window_width=720
window_style=Breeze
"""

def set_settings_if_not_exists():
    from PyQt5.QtCore import QSettings
    setting = QSettings("Everyskills", "TheBossBaby")
    _file = setting.fileName()
    if not os.path.exists(_file):
        _path = os.path.split(_file)
        os.mkdir(_path[0])
        with open(_path[0] + "/" + _path[1], "x") as _fw:
            _fw.write(default_setting)

def main():
    ### Download python modules
    os.system(f"python3 -m pip install -r {base_dir + 'requirements.txt'} --user")

    ## set TheBossBaby settings file
    set_settings_if_not_exists()
    
    ### Copy UIBxo Module to python library
    from distutils.sysconfig import get_python_lib
    _path = get_python_lib()
    shutil.copytree(base_dir + "UIBox", _path + "/UIBox")
    print(" [+] Copied UIBox Module -> ", _path, "\tDone...")

if __name__ == "__main__":
    try:
        main()
    except PermissionError:
        print("You must be root or sudo to run this file on Linux")
    except FileExistsError:
        pass

