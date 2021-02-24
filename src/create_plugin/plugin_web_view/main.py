#!/usr/bin/python3

import os
from PyQt5.QtCore import QObject, pyqtSlot

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

## You can use Jinja2 template in html code
HTML = """
<!DOCTYPE html>
<html lang="">
  <head>
    <meta charset="utf-8">
    <title></title>
  </head>
  <body>

    <h1 id="app"> Your Text: </h1>
    <h3> {{ text }} </h3>
    <button onclick="javascript:return_text()">Click me</button> <!-- run js script on click -->

    <script>
      function return_text() {
        var text = document.getElementById("app").innerText; // get h1 context
        kng.get_name(text); // call Python method
      }
    </script>
    
  </body>
</html>
"""

## remove it if you do not need it
class MyApp(QObject):
    def __init__(self) -> None:
        super().__init__()

    ################## simple function for call python in javascript
    @pyqtSlot(str) # type of arguments/options
    def get_name(self, text: str):
        """ get name from <h1> and print it from python code"""
        print("You'r using: ", text.strip(), " App")

def Plugin(parent=None):
    """ main function for start plugin from UIBox """
    return {
        ## HTML code or File path: (base_dir + "index.html")
        "html": HTML,
        
        ## remove it if you do not need it
        "object": MyApp(),

        ## status code return
        "status": True,
        
        ## the name for call python functions from HTML
        "call_name": "kng",
        
        ## [("icon", "title", callback), ...]
        "items": [("", "Your text '%s'" % parent.get_text(), lambda i, t: print(i, t), lambda i, t: print(i, t, "selected") )],
        
        ## Jinja Template Directory
        # "template_dir": "",
        
        ## Enable Jinja Template in HTML code
        "jinja": True,
        
        ## Jinja Render Keywords
        "keyword": {"text": parent.text},

        ## Start HTML File
        # "base_file": "index.html",

        ## Open Extrnal Links in Default applicatins/brwoser
        "open_links_in_browser": True
        }
