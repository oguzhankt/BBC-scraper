from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
import xmlrpc


def title(soup):
    title = str(soup.title)
    return title[7:-19]


def souppify(url):
    website = requests.get(url)
    data = website.text
    soup = BeautifulSoup(data, "html.parser")
    return soup


def sublinks(soup):
    links = []
    print("Getting links please wait...")
    for link in soup.find_all('a'):
        links.append(link.get('href'))
        time.sleep(0.05)
    return links


def sleep():
    time.sleep(999)


def remove_links(body):
    finding = 0
    while not(finding == -1):
        start = body.find("a class=") - 1
        end = body.find("</a>") + 1
        str_to_remove = body[start : end]
        body = body.replace(str_to_remove, "")
        finding = body.find("story-body__link")
    return body


def prettify_body(raw_body):

    introduction = "story-body__introduction"
    ending = "top-stories-promo-story__summary "
    start = raw_body.find(introduction) + len(introduction) + 2
    end = raw_body.find(ending) - 12
    body = raw_body[start:end]
    body = body.replace("</p>", "")
    body = body.replace("<p>", "")
    body = remove_links(body)
    body = body.replace("/a>", "")
    body = body.replace("., ", ".")
    body = body.replace(". , ", ".")
    body = body.replace("<i>", "")
    body = body.replace("</i>", "")
    body = body.replace(",,,", "")
    body = body.replace(",,", "")

    return body


def lineify(body):
    body = body.replace(".", ".\n")
    return body


def get_news_urls(links, category):
    news_urls = []
    url = "http://www.bbc.com"
    for i in range(len(links)):
        if "3" in links[i] and category in links[i]:
            news_urls.append(url + links[i])
            time.sleep(0.05)

    for i in range(len(news_urls)):
        print(news_urls[i])
        time.sleep(0.05)

    return list(set(news_urls))


def get_news(news_urls):
    news = []
    for i in range(len(news_urls)):
        soup = souppify(news_urls[i])
        raw_body = str(soup.find_all("p"))
        body = prettify_body(raw_body)
        body = lineify(body)
        data = title(soup) + "\n" + body
        filename = str(datetime.now())[11:19].replace(":", "") + ".txt"
        file = open(filename, "a")
        file.write(data)
        print(data)
        file.close()
        print("File :", i+1 , " has been created...")
        time.sleep(1)





print("Welcome to BBC scraper:")
category = input("Which category do you want?\n")
url = "http://www.bbc.com/news/" + category
soup = souppify(url)
links = sublinks(soup)
print("News links:")
news_urls = get_news_urls(links, category)
get_news(news_urls)

sleep()
