from UIBox import pkg

ICON_FILE = 'images/icon.png'

def no_input_item(p):
    return [
        {
            "title": 'No input'
        }
    ]


def no_results_item():
    return [
        {
            "title":'No results'
        }
    ]

def generate_description(template, search):
    for key in search.keys():
        template = template.replace('{' + key + '}', str(search[key] or '∅'), 1)
    return template

def generate_search_item(search, description_template):
    return {
        "icon": search['thumbnail'] or ICON_FILE,
        "title": search['title'],
        "subtitle": generate_description(description_template, search),
        "func": lambda p,i: pkg.open_url(search['url'])
    }


def generate_search_items(results, description_template):
    return [generate_search_item(search, description_template) for search in results]
