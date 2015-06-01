__author__ = 'Jus'

import json
import search_refine
from operator import itemgetter, attrgetter, methodcaller
# json_object = {{{"title":""string"},{"body":""string""},{"date":"mm/dd/yyyy"}*otherstuff*},{{......}}....}


def output_list_urls(json_object, query=str):
    title_all = []
    body_all = []
    date_all = []
    url = []
    for item_json in json_object:
        url.append(item_json['url'])
        title = item_json['title']
        body = item_json['body']
        date_unparsed = item_json['date']
        title_all.append(title)
        body_all.append(body)
        date_all.append(date_unparsed)
    scores_final = search_refine.search_refine(query, body_all, title_all, date_all)
    # list_format -> scores_final = [(score_1, index_1)....(score_n, index_n)]
    scores_final.sort(key=itemgetter(0), reverse=True)
    # Now, construct the json in the format you got it, and return it so that "child_process" from node can call"
    data = "{ "
    for i in range(len(scores_final)):
        url_curr = url[scores_final[1]]
        if i != (len(scores_final) - 1):
            data += "{" + "'url'" + ":" + url_curr + "}" + ", "
        else:
            data += "{" + "'url'" + ":" + url_curr + "} "
    data += "}"
    json_data = json.dumps(data)
    return json_data




