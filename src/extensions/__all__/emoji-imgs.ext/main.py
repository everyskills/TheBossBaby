import os
import logging
import sqlite3
from pprint import pprint

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")
logger = logging.getLogger(__name__)
extension_icon = base_dir + 'images/icon.png'
db_path = base_dir + 'emoji.sqlite'
conn = sqlite3.connect(db_path, check_same_thread=False)
conn.row_factory = sqlite3.Row

def normalize_skin_tone(tone):
    """
    Converts from the more visual skin tone preferences string to a more
    machine-readable format.
    """
    if tone == "👌 default": return ''
    elif tone == "👌🏻 light": return 'light'
    elif tone == "👌🏼 medium-light": return 'medium-light'
    elif tone == "👌🏽 medium": return 'medium'
    elif tone == "👌🏾 medium-dark": return 'medium-dark'
    elif tone == "👌🏿 dark": return 'dark'
    else: return None

def Results(parent):
        allowed_skin_tones = ["", "dark", "light", "medium", "medium-dark", "medium-light"]

        icon_style = parent.preferences('emoji_style')
        fallback_icon_style = parent.preferences('fallback_emoji_style')
        search_term = parent.text.replace('%', '') if parent.text else None
        search_with_shortcodes = search_term and search_term.startswith(':')
        # Add %'s to search term (since LIKE %?% doesn't work)

        skin_tone = normalize_skin_tone(parent.preferences('skin_tone'))

        if skin_tone not in allowed_skin_tones:
            logger.warning('Unknown skin tone "%s"' % skin_tone)
            skin_tone = ''

        search_term_orig = search_term
        if search_term and search_with_shortcodes:
            search_term = ''.join([search_term, '%'])

        elif search_term:
            search_term = ''.join(['%', search_term, '%'])

        if search_with_shortcodes:
            query = '''
                SELECT em.name, em.code, em.keywords,
                       em.icon_apple, em.icon_twemoji, em.icon_noto, em.icon_blobmoji,
                       skt.icon_apple AS skt_icon_apple, skt.icon_twemoji AS skt_icon_twemoji,
                       skt.icon_noto AS skt_icon_noto, skt.icon_blobmoji AS skt_icon_blobmoji,
                       skt.code AS skt_code, sc.code as "shortcode"
                FROM emoji AS em
                  LEFT JOIN skin_tone AS skt
                    ON skt.name = em.name AND tone = ?
                  LEFT JOIN shortcode AS sc
                    ON sc.name = em.name
                WHERE sc.code LIKE ?
                GROUP BY em.name
                ORDER BY length(replace(sc.code, ?, ''))
                LIMIT 8
                '''
            sql_args = [skin_tone, search_term, search_term_orig]
        else:
            query = '''
                SELECT em.name, em.code, em.keywords,
                       em.icon_apple, em.icon_twemoji, em.icon_noto, em.icon_blobmoji,
                       skt.icon_apple AS skt_icon_apple, skt.icon_twemoji AS skt_icon_twemoji,
                       skt.icon_noto AS skt_icon_noto, skt.icon_blobmoji AS skt_icon_blobmoji,
                       skt.code AS skt_code
                FROM emoji AS em
                  LEFT JOIN skin_tone AS skt
                    ON skt.name = em.name AND tone = ?
                WHERE em.name LIKE ?
                LIMIT 8
                '''
            sql_args = [skin_tone, search_term]

        # Display blank prompt if user hasn't typed anything
        if not search_term:
            search_icon = base_dir + 'images/%s/icon.png' % icon_style
            return [{
                "icon": search_icon,
                "title": 'Type in emoji name...'
            }]

        # Get list of results from sqlite DB
        items = []
        display_char = parent.preferences('display_char') != 'no'

        for row in conn.execute(query, sql_args):
            if row['skt_code']:
                icon = row['skt_icon_%s' % icon_style]
                icon = row['skt_icon_%s' % fallback_icon_style] if not icon else icon
                code = row['skt_code']
            else:
                icon = row['icon_%s' % icon_style]
                icon = row['icon_%s' % fallback_icon_style] if not icon else icon
                code = row['code']

            name = row['shortcode'] if search_with_shortcodes else row['name'].capitalize()
            if display_char: name += ' | %s' % code

            print(icon, name)
            
            items.append({
                "icon": icon, 
                "title": name,
                "key": code,
                "filter": False,
                "func": lambda p, i: parent.text_copy(i.key)
            })

        return items
