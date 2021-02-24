## UIBox for cross-platform v1.0.0

UIBox is a Search extendable app with plugins and fetchers

![Example](https://raw.github.com/nate-parrott/flashlight/master/Image.png)

>## Installation
- ### Python Requirements
    - [Python Language](https://www.python.org)
    - [PyQt5](https://pypi.org/project/PyQt5/)
    - [PyQtWebKit](https://pypi.org/project/PyQtWebKit)
    - [psutil](https://pypi.org/project/psutil/)
    - [jinja2](https://pypi.org/project/Jinja2/)
    
- ### Steps to complete install
```bash
git clone https://www.github.com/everyskills/UIBox.git

## Unzip UIBox Archive 
## after then do this command

python3 install.py
```

>## Removing
```bash
uibox --uninstall
```

## Main Widgets for style

| ID/ObjectName    | Widget |
| -------------    | ------------- |
| UIB_list_widget   | QListWidget  |
| input         | QLineEdit  |
| UIB_web          | QWebView |
| UIB_progress_bar  | QProgressBar|
| UIB_search_icon   | QToolButton
| UIB_plugin_icon   | QToolButton


### example how to style UIBox Widgets
```css
/* List Widget */
#UIB_list_widget {
    background: gray;
}

/* Items style */
#UIB_list_widget:item {
    color: white;
    background: gray;
} 

/* UIB_line */
#input {
    color: white;
    background: gray;
}

/* Web View */
#UIB_web {
    background: black;
    color: white;
}
```
------------------------------------------

## Writing Plugins
<!-- ### you can see the examples in creator plugins -->
### You can program any type of plugins like QWidget or Items and this simple example for WebView plugin:

This is a basic walkthrough for creating a plugin. We'll create a simple say plugin, 
which print user text input to page 

**What makes a plugin**

A plugin needs a couple of things, which we'll explain below:

- a `.ext` directory, containing:
- an `info.json`
- a `plugin.py`
- an `Icon.png` (optional)

## Create the .ext 
to install your plugin go to settings and go to the downloads page and select path to the plugin directory.

### info.json
The first thing we need is an `info.json` file. Here's what to put in it:
```javascript
{
	"name": "Python Functions",
	"version": "1.0.0",
	"description": "simple description",        // (optional)
	"icon": "icon.png",                         // (optional)
	"help": "README.md",                        // (optional)
	"script": "main.py",
	"key": "print",
	"creator_name": "Author name",              // (optional)
	"creator_email": "example@domain.com",      // (optional)
    "creator_url": "https://www.example.com"    // (optional)
	"creator_description": "Python Developer",  // (optional)
	"system": "all"
}
```

(Remember to remove the inline comments, or else the JSON won't validate and the plugin will show up blank.)

Once that's there, you should be able to open up the UIBox Installed list and see your plugin. It doesn't do anything yet.

## plugin.py / json("script")
```python
def Results(parent):
    """ param: parent for main window methods """
    return {
        "title": "Your text is '%s'" % parent.text
    }
```

Now, if we type "print Hello world" into UIBox, we'll see the title our plugin returned.

## Detour: debugging
Sometimes, your Python script might crash you'll see error messages in the "errors" panel. If you want to debug your Javascript or HTML, right-click your web content and _Inspect Element_.


## Running the plugin
Of course, the plugin doesn't actually _do_ anything yet — ideally, we want it to search in google when we hit Enter. That's easy. Just add a function `run` to `plugin.py`.

Now, we need some way of passing the message that we're supposed to speak to run. That's why we returned an parent parameter for window methods

```python
def Run(parent):
    import os
    os.system('firefox --search '{}''.format(message)) # TODO: proper escaping via pipes.quote
```

There. **Now our plugin should work**. Type "what is python" into UIBox, hit enter, watch it go.


## Showing HTML inline in Spotlight

Many plugins, like Emoji and Call, return HTML and JavaScript to show content inline in the UIBox window. You can do this by returning an HTML string from your `results` function:

```python
def Results(parent):
    message = parent.text
    html = "<h1>{0}</h1>".format(message)
    return {
        "title": "Search for '{0}'".format(message),
        "html": html
    }
```

If you'd like to load a web URL, you should return a `delayed Javascript redirect`, which looks like this:

```javascript
<script>
    setTimeout(function() {
      window.location = 'http://google.com'
    }, 500); // delay so we don't get rate-limited by doing a request after every keystroke
</script>
```


There are two more fields you can return in your `results` dictionary that may be relevant if you're using webviews:
- `open_links_in_browser`: _optional_ when the user clicks links in the webview, they'll close UIBox and open in a browser


## Screenshots
Online plugin pages like [this one](url) have screenshots of plugins. Take a screenshot of UIBox showing your plugin by pressing `Meta + Shift + Return`, then saving that screenshot inside your plugin


## License
Licensed under the GPL and MIT licenses (see LICENSE)
