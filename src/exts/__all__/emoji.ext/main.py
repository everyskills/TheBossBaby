#!/usr/bin/python3

import os
import json

from PyQt5.QtCore import QObject, pyqtSlot

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class MyApp(QObject):
    def __init__(self, parent) -> None:
        super(MyApp, self).__init__()
        self.p = parent

    ################## simple function for call python in javascript
    @pyqtSlot(str) # type of arguments/options
    def copy_emoji(self, icon):
        self.p.text_copy(str(icon))

def score(query, field):
    if field == query:
        return 1
    s = 0
    for word in query.split(" "):
        if word == field:
            s += 0.1
        elif word in field:
            s += 0.01
    return s

def strip_accents(s):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', s)
               if unicodedata.category(c) != 'Mn')

def normalize(s):
    s = s.lower()
    if type(s) == str:
        return strip_accents(s)
    else:
        return s

def find_emojis(query, emoji_arr):
    normalized_query = normalize(query)
    scored_matches = []
    others = []
    field_weights = {"aliases": 2.5, "tags": 2, "description": 1.5}
    for item in emoji_arr:
        s = 0
        for field_name, field in item.items():
            weight = field_weights.get(field_name, 0)
            if weight == 0: continue
            if field_name == 'aliases': field = ' '.join(map(str,field))
            if field_name == 'tags': field = ' '.join(map(str,field))
            s += weight * score(query.lower(), field.lower()) * 0.1 # perfect word match
            s += weight * score(query, field) * 0.1 # perfect word match
            s += weight * score(normalized_query, normalize(field))
        if s:
            item.update({'score': s})
            scored_matches.append(item)
        else:
            others.append(item)

    scored_matches.sort(key=lambda k: k['score'], reverse = True)

    return {
        "matches": scored_matches,
        "others": others
    }


def build_html(appearance, content, color, bg):
    html = """
    <html>
    <head>
        <style>
            body{
                padding: 10px 12px;
                font: 15px/1.4 'Helvetica Neue';
                font-weight: 300;
                color: {{color}};
                background-color: {{bg}};
                /*-webkit-user-select: none;*/
            }

            h1 {
                font-size: 20px;
                font-weight: 300;
            }

            h1 small {
                margin-left: 5px;
                color: rgb(119,119,119);
            }

            .emojis {
                margin: 0 -5px 30px;
                font-size: 2.2em;
            }

            .emoji {
                display: inline-block;
                width: 40px;
                height: 60px;
                padding: 5px;
                margin-bottom: 10px;
                text-align: center;
            }

            .emoji i {
                -webkit-user-select: all;
                font-style: normal;
            }

            label, small {
                font-size: 12px;
                overflow: hidden;
                white-space: nowrap;
            }

            label {
                display: block;
                font-size: 11px;
                -webkit-user-select: all;
            }

            .dark {
                color: rgb(224,224,224);
            }

        </style>

    </head>

    <body class="{{appearance}}">
        <div class="message"></div>
        {{content}}

        <script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
        <script>
            var backend = null;
            new QWebChannel(qt.webChannelTransport, function(channel) {
                backend = channel.objects.emoji;
            });
        </script>

    </body>
    </html>
    """

    html = html.replace("{{color}}", color).replace("{{bg}}", bg).replace("{{appearance}}", appearance)
    return html.replace("{{content}}", content)

def build_emoji_html(emoji):
    html = """
        <div class="emoji">
            <i onclick="backend.copy_emoji('{{icon}}')">{{icon}}</i>
            <label onclick="backend.copy_emoji('{{gemoji}}')">{{alias}} </label>
        </div>
        """

    alias = emoji['aliases'][0]
    gemoji = ':'+emoji['aliases'][0]+':'
    icon = emoji.get('emoji') or '-'

    html = html.replace('{{alias}}', alias)
    html = html.replace('{{gemoji}}', gemoji)
    return html.replace('{{icon}}', icon)

def Results(parent):
    query = parent.text
    emoji_arr = json.loads(open(base_dir + 'emoji.json').read())
    emojis = find_emojis(query, emoji_arr)
    content = ''
    output = ''
    title = 'No matching emoji found'

    if len(emojis['matches']):
        output = emojis['matches'][0].get('emoji')

        title = 'Copy the emoji \'%s\' to the clipboard' % (output)
        content = '<h1>Emoji matching your search <small>%s results</small></h1><div class="emojis">' % (len(emojis['matches']))
        for emoji in emojis['matches']:
            content += build_emoji_html(emoji)
            
        content += '</div>'

    if len(emojis['others']):
        content += '<h1>Other emojis</h1><div class="emojis">'
        for emoji in emojis['others']:
            content += build_emoji_html(emoji)
        content += '</div>'

    parent.text_copy(output)
    color = 'black' if not parent.style == 'dark' else 'white'
    bg = parent.dark_color if parent.style == 'dark' else parent.light_color

    return {
        "html": build_html("gemoji", content, color, bg),
        "title": title,
        "open_url_in_browser": True,
        "object": {"emoji": MyApp(parent)}
    }
