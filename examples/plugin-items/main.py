#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
simple description what plugin do
"""

## NOTE: Before create your plugin, please check if not was taken your keyword
## NOTE: Write all Information in package.json for best quality
## NOTE: try using .png file type when you icon choose if you can, size(100x100)

## Function for Import from UIBox
## don't edit this to another name
def Results(parent):
    return [{
    
        ## Main Icon for item: QIcon(str)
    	"icon": "/path/to/icon",

        ## Get Icon from Default System Theme: QIcon.fromTheme(str)
    	"icon_theme": False,
        
        ## if icon theme is Null set this icon: QIcon(str)
        "null_icon": "",

        ## Set Item title NOTE: You can write simple html code
    	"title": f"Hello World '{parent.text}'",
    	
        ## Set Item Description NOTE: You can write simple html code
    	"subtitle": "I,m simple TheBossBaby Mode for make plugins",
    	
        ## Enable Default Filter 
    	"filter": False,

        ## Enable Highlight Text when word process
    	"highlightable": True,

        ## Don't Hide Window when item clicked
    	"keep_app_open": False,
    	
        ## Function Callback when item Return
    	"func": lambda p, i: (),

        ## Function Callback when item Pressed (Ctrl+Return)
    	"ctrl_enter": lambda p, i: (),
    	
        ## Function Callback when item Selected
    	"item_selected": lambda p, i: (),

        ## Function Callback when item Clicked
    	"item_clicked": lambda p, i: ()
    }]

## will run this function when the line input was clicked
def Run(parent):
    """ 
    :param parent: main window events and simple methods
    :param item: return clicked item content
    """
    pass

## will run this function when the item was selected
def ItemSelected(parnet, item):
    pass

## will run this function when the item was clicked
def ItemClicked(parent, item):
    pass


## will run this function when the item was pressed Ctrl+Return
def ItemCtrlEnter(parent, item):
	pass