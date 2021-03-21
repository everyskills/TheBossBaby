from .src.functions import strip_list
from .src.items import no_input_item, no_results_item, generate_search_items
from .src.youtube_search import YoutubeSearch

def Results(parent):

    if len(parent.text) == 0:
        return no_input_item(parent)

    params = strip_list(parent.text.split(' '))            
    search = YoutubeSearch(params)

    # search.show_thumbnails = True

    if parent.preferences('show_thumbnails') and search.show_thumbnails is None:
        search.show_thumbnails = True

    # if not search.has_query():
    #     return show_used_args(parser)

    results = search.execute()

    if not results:
        return no_results_item(parent)

    return generate_search_items(results, parent.settings("description_template"))
