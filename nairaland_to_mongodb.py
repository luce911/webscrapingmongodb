# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 22:16:47 2017

@author: oodiete
"""

from bs4 import BeautifulSoup
import requests
   
BASE_URL = "http://www.nairaland.com"
articles = []

def request_page(url):
    """Util function to request pages"""
    
    r = requests.get(url)
    if r.status_code !=  200:
        print("{0}: {1}".format(r.status_code, r.reason))
        return None

    return r.text
    
def parse_users():
    """Uses soup to extract content of the user's profile page."""

    pass


def parse_page():
    """"""
    pass
    

def parse_article(url):
    """Parse_article => uses request to retrieve first page 
    of article, and uses soup to extract content of the page.."""
    #print    
    #print url,
    comments = []
    offset = 0
    
    page = request_page(url)

    # parse
    soup = BeautifulSoup(page, "lxml")
    posts = soup.find("table", {"summary": "posts"})
    tds = posts.find_all("td")
    
    for i in range(0, len(tds), 2):
        comment = {}
        i -= offset
        #print i,
        # retrieve timestamp info
#        print tds[i]
        details = tds[i].find("span", {"class": "s"})
        if details:        
            details = details.find_all("b")
        else:
            #print "bug",
            offset += 1
            continue
        
        time = details[0].text
        if len(details) > 1:
            day = details[1].text
        else:
            day = "July 17"
        
        if len(details) > 2:
            year = details[2].text
        else:
            year = "2017"
        
        # retrieve poster info
        details = tds[i].find_all("a")
        _id = details[0].get("name")
        
        if len(details) <= 4:
            user = None
        else:
            user = details[-1].text
            
        # retrieve content info
        links = len(tds[i+1].find("div", {"class":"narrow"}).find_all("a"))
        likes = tds[i+1].find("p", {"class":"s"})
        if likes:
            likes = likes.find_all("b")[0].text.strip()
        
        if not likes:
            likes = 0
        else:
            likes = int(likes.split()[0])
        
        shares = tds[i+1].find("p", {"class":"s"})
        if shares:
            shares = shares.find_all("b")[1].text.strip()

        if not shares:
            shares = 0
        else:
            shares = int(shares.split()[0])
        
        images = len(tds[i+1].find_all("img", {"class": "attachmentimage"}))

        quoting = False
        quote = tds[i+1].find("div", {"class":"narrow"}).find("blockquote")
        if quote:
            quoting = True
            


        comment["user"] = user
        comment["_id"] = _id
        comment["links"] = links
        comment["images"] = images
        comment["quoting"] = quoting
        comment["likes"] = likes
        comment["shares"] = shares
        comment["timestamp"] = "{} {},{}".format(time, day, year)
                    
            
        comments.append(comment)
        
    return comments
    
def parse_article_pages(info):
    """Parse_article => uses request to retrieve first page 
    of article, call parse_page for each article page."""

    url = info['url']
    page = request_page(url)

    # parse
    soup = BeautifulSoup(page, "lxml")
    
    # number of pages of that articles, m
    ads = soup.find("div", {"class": "ijapanla"})
    navs = ads.next_sibling.find_all("a")
    
    if len(navs) <= 2:
        m = 0 
    else:
        m = int(navs[-3].text.strip("()"))

        
    info['posts'] = []
    for i in range(m+1):
        art_url = "{0}/{1}".format(url, i)
            
        posts = parse_article(art_url)
        info['posts'].extend(posts)
    
    return info
        
    
def parse_forum_pages(url):
    """Uses request to retrieve the articles from apage of the forum,
    call parse_article for each article in page"""
 
    forum_data = []
    page = request_page(url)

    # parse
    soup = BeautifulSoup(page, "lxml")
    core = soup.body.find_all("table")[2]
    tds = core.findAll("td")

    for td in tds:
        info = {}
        a_data = td.find_all("a")
        
        info['_id'] = a_data[0].get("name")
        info['title'] = a_data[1].text
        #info['creator'] = a_data[-2].text
        info['url'] = "{}{}".format(BASE_URL, a_data[1].get("href"))

        s_spans = td.find("span", {"class":"s"})
        s_spans_b = s_spans.find_all("b")

        users = s_spans.find_all("a")
        if len(users) == 2: # first and last user is valid
            info['creator'] = users[0].text
            info['comments'] = int(s_spans_b[1].text)
            info['views'] = int(s_spans_b[2].text)
        else:
            info['creator'] = None
            info['comments'] = int(s_spans_b[0].text)
            info['views'] = int(s_spans_b[1].text)        
        
        #info['pages'] = int(a_data[-3].text.strip("()"))
        #info['views'] = int(a_data[-2].parent.next_sibling.next.text)
        #info['posts'] = int(a_data[-2].parent.next_sibling.next.next_sibling.next.text)
    
        forum_data.append(parse_article_pages(info))

    return forum_data
    
def parse_forum(url):
    """Uses request to retrieve landing page of the forum, 
    call parse_forum_pages for each pages of artcile in the forum."""
    
    page = request_page(url)
    if not page:
        # write error log
        return
        
    # parse 
    soup = BeautifulSoup(page, "lxml")

    # number of pages
    n = int(soup.body.div.div.next_sibling.find_all("b")[1].text) + 1

    # parse articles
    forum_data = []
    for i in range(40,42):#range(n):
        forum_url = "{0}/{1}".format(url, i)
        data = parse_forum_pages(forum_url)
        forum_data.extend(data)

    return forum_data
    
def main():
    """Starts with the main nairaland page and calls 
    parse_forum with the landing page of every forum/group."""

    # extract data from the following forums and save as json file for
    # upload into mongodb

    # data structure
    # {
    #   "_id": the 
    #   "url": 
    #   "views":
    #   "posts": [{"user": "", "links": "", "replies":}]
    #   "..."
    # }    

    forums = ["politics"]
    for forum in forums:
        url = "{0}/{1}".format(BASE_URL, forum)
        forum_data = parse_forum(url)
        
    return forum_data
    
    
if __name__ == "__main__":
    forum_data = main()