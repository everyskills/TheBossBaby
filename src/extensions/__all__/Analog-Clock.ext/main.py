#!/usr/bin/python3

def Results(parent):
    return {
      "html": parent.include_file("index.html"),
      "jinja": True,
      "open_links_in_browser": True
    }