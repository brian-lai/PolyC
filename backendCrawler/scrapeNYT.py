import urllib2
from bs4 import BeautifulSoup
from cookielib import CookieJar


url = "http://www.nytimes.com/politics/first-draft/2015/08/17/as-scott-walker-struggles-in-iowa-his-campaign-reaches-out-to-a-strategist/?ref=politics"
# oFile = open("C:\Users\Lucas\Data\nytPolitics.txt", 'wb')

# content = urllib2.urlopen(url).read()
# print content.getCode()


cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
p = opener.open(url)
htmlPage = p.read()


soup = BeautifulSoup(htmlPage, "html.parser")

print soup
# returnCode = content.getCode()
#
# print returnCode
#
