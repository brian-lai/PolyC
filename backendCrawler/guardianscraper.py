import urllib2
from bs4 import BeautifulSoup
from cookielib import CookieJar
import requests
import json
#from guardianapi import Client
# url="http://www.nytimes.com/2015/08/21/us/politics/bernie-sanders-evokes-obama-of-08-but-with-less-hope.html?hp&action=click&pgtype=Homepage&module=second-column-region&region=top-news&WT.nav=top-news"
#url="https://www.google.com/search?espv=2&q=the+guardian+"+sys.argv[0]+"&spell=1&sa=X&ved=0CBsQvwUoAGoVChMI7fj30Lu5xwIVgzuICh1MMQ9B&biw=1920&bih=935"
# def scrapepage(url):
# htmlPage = urllib2.urlopen(url).read()


guard_url ="http://content.guardianapis.com/search?q=politics"


def get_content():
    api_url = 'http://content.guardianapis.com/search?q=politics'
    payload = {
        'api-key':              'vv5q83rjfd8ya8uymmpnaza6',
        'page-size':            5,
        'show-editors-picks':   'true',
        # 'show-elements':        'image',
        # 'show-fields':          'all'
    }
    response = requests.get(api_url, params=payload)
    data = response.json() # convert json to python-readable format
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)
    urls = []
    for i in range(len(data["response"]["results"])):
        urls.append(data["response"]["results"][i]["webUrl"])
    paragraphs_for_all_articles = []
    for i in range(len(urls)):
        cj = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        p = opener.open(urls[i])
        htmlPage = p.read()
        soup=BeautifulSoup(htmlPage,"html.parser")
        paragraphs=(soup.find_all('p'))
        allparagraphs = ""
        for paragraph in paragraphs:
            paragraph = str(paragraph)
            allparagraphs += paragraph
        paragraphs_for_all_articles.append(allparagraphs)
    # print paragraphs_for_all_articles
    return data

if __name__ == "__main__":
    get_content()
