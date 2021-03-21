import subprocess

def Results(parent):
    # search = parent.text.lower()
    items = []

    # Get list of all windows, and process into a dictionary that looks like this:
    # {<window_id>: {ws: <workspace_id>, name: <window_name>}}
    result = subprocess.run(['wmctrl -l | awk \'{ if( $2 != "-1") { $3="";  print $0} }\''], capture_output=True, shell=True, text=True).stdout
    w_list = [y for y in (x.strip() for x in result.splitlines()) if y]
    w_dict = {x[1].split(maxsplit=2)[0]: {'ws': int(x[1].split(maxsplit=2)[1]), 'name': x[1].split(maxsplit=2)[2]} for x in enumerate(w_list)}
    
    # Get list of all workspaces and process into a dictionary that looks like this:
    # {<workspace_id>: <workspace_name>}
    result = subprocess.run(['wmctrl -d | awk \'{$1=$2=$3=$4=$5=$6=$7=$8=$9=""; print $0}\''], capture_output=True, shell=True, text=True).stdout
    ws_list = [y for y in (x.strip() for x in result.splitlines()) if y]
    ws_dict = {i: x for i, x in enumerate(ws_list)}

    for w_idx, window in w_dict.items():
        if parent.text.lower() or parent.text.lower() in window['name'].lower():
            items.append({
                # Workaround for https://github.com/Ulauncher/Ulauncher/issues/587
                "title": window['name'].replace('&', '&amp;') if parent.text.lower() else window['name'],
                "subtitle": f'Workspace: {window["ws"]}: {ws_dict[window["ws"]]}, Window Id: {w_idx}',
                "key": str(w_idx)
                # "func": lambda p, i: subprocess.run(f'wmctrl -ai {i.key}')
            })

    return items

def Run(p, i):
    print(i.key)
    # subprocess.run("wmctrl -ai " + i.key, shell=True)
    # pkg.run_app("wmctrl -ai " + i.key)
