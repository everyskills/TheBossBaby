#!/usr/bin/python3

import json
import os
import glob
import subprocess
from UIBox import pkg

def read_workspaces():
    """ Reads VS Code recent workspaces """
    ## path = self.preferences['config_path'] = ~/.config/Code/

    config_path = "~/.config/Code/"

    absPath = os.path.expanduser(config_path)
    dirList = []
    for workspacePath in glob.glob(absPath + "/User/workspaceStorage/*/workspace.json"):
        data = json.load(open(workspacePath, 'r'))
        if 'folder' not in data:
            continue

        pointer = data['folder'].find('file://')
        if (pointer >= 0):
            path = data['folder'][7:]
            # get workspace name
            namePointer = path.rfind('/')
            name = path[namePointer + 1:]
            currentData = {'name': name, 'path': path}
            dirList.append(currentData)

    return dirList

def get_projects():
    """ Returns projects """

    mappedProjects = []
    projects_index = []
    full_project_path = os.path.expanduser(
        # self.preferences['projects_file_path'])~/.config/Code/User/globalStorage/alefragnani.project-manager/
        "~/.config/Code/User/globalStorage/alefragnani.project-manager/")

    # if self.preferences['include_project_manager'] == 'true':
    if True and os.path.exists(full_project_path):
        projects = []
        if os.path.isfile(full_project_path):
            with open(full_project_path) as projects_file:
                projects = json.load(projects_file)
        else:
            project_files = os.listdir(full_project_path)

            for projects_file in project_files:
                projects_file = os.path.join(full_project_path,
                                                projects_file)
                with open(projects_file) as file:
                    projects += json.load(file)

        for project in projects:
            projects_index.append(project['name'])
            mappedProjects.append({
                'name':
                project['name'],
                'path':
                project.get('fullPath') or project.get('rootPath'),
                'type':
                'project',
            })

    # if self.preferences['include_recent_workspaces'] == 'true':
    if True:
        recent_workspaces = read_workspaces()
        for w in recent_workspaces:
            if w['name'] not in projects_index:
                mappedProjects.append({
                    'name': w['name'],
                    'path': w['path'],
                    'type': 'workspace'
                })

    return mappedProjects

def Results(parent):
    items = []
    projects = get_projects()
    icon = parent.include_file("folder.png")

    if parent.text:
        projects = [
            item for item in projects
            if parent.text.strip().lower() in item['name'].lower()
        ]

    if not projects:
        return [{
            "icon": icon,
            "highlightable": False,
            "keep_app_open": True,
            "title": 'No projects found matching your criteria'
        }]
    
    for project in projects:
        if project['type'] == 'workspace':
            icon = parent.include_file("Icon.png")

        items.append({
            "icon": icon,
            "title": project['name'],
            "subtitle": project['path'],
            "keep_app_open": False,
            "ctrl_enter": lambda p, i: pkg.open_url(project['path'])
        })
    return items

def Run(parent, item):
    code_executable = "code"

    parent.post_message(parent.icon, "VSCode Loading...", f"{item.subtitle}", 3000)
    if not item.subtitle.startswith('vscode-remote://'):
        subprocess.Popen([code_executable, item.subtitle])
        # pkg.get_cmd_output([code_executable, item.subtitle])
    else:
        # pkg.get_cmd_output([code_executable, '--folder-uri', item.subtitle])        
        subprocess.Popen([code_executable, '--folder-uri', item.subtitle])
    parent.post_message(parent.icon, "VSCode finish startup", f"{item.subtitle}", 3000)

def ItemClicked(parent, item):
    Run(parent, item)

def ItemSelected(parent, item):
    pass
