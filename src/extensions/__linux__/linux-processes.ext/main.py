import psutil
from UIBox import pkg

def get_processes():
    '''
    Get list of running process sorted by Memory Usage
    '''
    listOfProcObjects = {}
    # Iterate over the list
    for proc in psutil.process_iter():
       try:
            # Fetch process details as dict
            svmem = psutil.virtual_memory()
            swap = psutil.swap_memory()

            pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'exe'])
            pinfo["vms"] = float(pkg.get_size(proc.memory_info().vms)[:-2]) / float(pkg.get_size(svmem.total)[:-2]) * 100
            pinfo["swap"] = float(pkg.get_size(proc.memory_info().shared)[:-2]) / float(pkg.get_size(swap.total)[:-2]) * 100
            pinfo["event"] = proc

            listOfProcObjects.update({pinfo.get("pid"): pinfo})
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass

    return listOfProcObjects

def create_item(name, icon, subtitle, pid, nicon):
    return {
        "title": name,
        "subtitle": subtitle,
        "icon": icon,
        "icon_theme": True,
        "key": pid,
        "keep_app_open": True,
        "null_icon": nicon
    }

def Run(parent, item):
    proc = get_processes()[int(item.key)]
    return [
        {
            "icon": parent.include_file('img/kill.png'),
            "title": "KILL",
            "subtitle": f"enter for kill '{item.title}' process",
            "key": item.key,
            "func": lambda p,i: proc.get('event').kill(),
            "filter": False
        },

        {
            "icon": item.title,
            "icon_theme": True,
            "null_icon": parent.include_file('img/executable.png'),
            "title": f"{item.title}",
            "subtitle": "name of processe",
            "filter": False
        },

        {
            "title": f"{item.key}",
            "subtitle": "process PID",
            "filter": False
        },

        {
            "icon": parent.include_file("img/user.png"),
            "title": f"{proc.get('username', '')}",
            "subtitle": "Owner of this processe",
            "filter": False
        },

        {
            "icon": parent.include_file("img/task.png"),
            "title": f"{proc.get('memory_percent', 0)}%",
            "subtitle": "Memory of Process",
            "filter": False
        },

        {
            "icon": parent.include_file("img/task.png"),
            "title": f"{proc.get('cpu_percent', 0)}%",
            "subtitle": "CPU of Process",
            "filter": False
        },
        
        {
            "icon": parent.include_file('img/cmd.png'),
            "title": f"{proc.get('exe', '')}",
            "subtitle": "executable command for process",
            "filter": False
        },
    ]

def Results(parent):
    results = []
    for _, v in get_processes().items():
        if parent.text in v.get("name", ""):
            results.append(
            create_item(
                v.get("name", ""), 
                v.get("name", ""), 
                f"PID: {v.get('pid')}   EXE: {v.get('exe')}",
                v.get("pid"),
                parent.include_file('img/executable.png')
            ))

    return results[0:12]
