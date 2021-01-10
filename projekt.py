# zczytywanie z pliku

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


 #to jest tylko z pliczku, zeby dzialalo offline, lokalnie zaciaga   
def read_file(file_name):
    with open (file_name, 'r',encoding="utf-8") as file:
        data = file.read().replace('\n', '')
        return data


def request_page(url):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    if r.status_code !=  200: # sprawdzamy czy wgl znalazlo serwer. to sa kodziki ustalone przez ludzi np 404 to blad
        print("{0}: {1}".format(r.status_code, r.reason))
        return None

    return r.text



# def dupa(page):
#     soup = BeautifulSoup(page, "lxml")
#     title=soup.find("title")
#     return title.text

# def dupa2(page):    
#     soup=BeautifulSoup(page, "lxml")
#     style=soup.find("div",{"style":"width:685px;height:1px"})
#     return style.text
    
# def dupa3(page):
#     soup=BeautifulSoup(page, "lxml")
#     stock=soup.find("a",{"href":"q/?s=wig20"})
#     stock_value=soup.find("span",{"id":"aq_wig20_c2"})
#     return stock.text + " " + stock_value.text 

def extract_stocks(page):
    soup=BeautifulSoup(page, "lxml")
    tbody=soup.find("tbody",{"align":"right","id":"f13"})
    tds = tbody.find_all("td")
    tds.pop(30) #pozioma linia dzielaca indeksy od kursu walut
    out=[]
    for i in range(0, len(tds), 5):
        stock_details={
            "Name": " ".join(tds[i].text.split()),
            "Rate": " ".join(tds[i+1].text.split()),
            "Percent_Change": " ".join(tds[i+2].text.split()),
            "Date": " ".join(tds[i+4].text.split())
        }
        out.append(stock_details)
        # print(" ".join(tds[i].text.split()))
        # try:
        #     print(" ".join(tds[i+1].text.split()))
        #     print(" ".join(tds[i+2].text.split()))
        #   #  print(tds[i+3].text.strip())
        #     print(" ".join(tds[i+4].text.split()))
        # except:
        #     print("An exception occurred")
        # print("\n")
        
    return out
        
    #return tbody.text


# #data base connect
# klient=MongoClient('mongodb://localhost:27017')
# bazaDanych=klient['bazaN4211_LucjaCh']
# kolekcja=bazaDanych.rynek
# #data
# stockPage = read_file("stooq.html")
# stockDetails = extract_stocks(stockPage)
# #adding to data base
# status=kolekcja.insert_many(stockDetails)
# print(status)

article_page = request_page("https://stooq.pl/n/?f=1383525&c=0&p=a")

def extract_article(page):
    soup=BeautifulSoup(page, "lxml")
    # article_alldata=soup.find("table",{"width":"98%","border":"0", "align":"center"})
    article_title=soup.find("font",{"id":"f22"})
    article_text=article_title.next_sibling
    dupa = article_text.text 
    return {"Title": article_title.text, "Text": article_text.text}

def extract_articles(page):
    BASE_URL="https://stooq.pl/"
    soup=BeautifulSoup(page, "lxml")
    article_table=soup.find("div",{"style":"padding:0px 10px"})
    rows = article_table.find_all("tr")
    out = []
    for row_idx in range(0, len(rows)):
        columns = rows[row_idx].findChildren("td", recursive=False)
        # lol = tds[i+1]
        if (len(columns) >= 3):
            article_details = {
                "Date": columns[0].text,
                "Title": columns[1].text,
                "Link": BASE_URL+columns[1].find("a")["href"],
                "Source": columns[2].text,
            }
            out.append(article_details)

        
    return out


#print(extract_article(article_page))

for page in range(1, 45):
    url = "https://stooq.pl/n/?c=0&s=2&p=a&l=" + str(page)
    articles_listing_page = request_page(url)
    extracted_articles_details = extract_articles(articles_listing_page)
    print(extracted_articles_details)
    for article_details in extracted_articles_details:
        article_main_page = request_page(article_details["Link"])
        chuj = extract_article(article_main_page)
        print(chuj)
