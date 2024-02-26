from bs4 import BeautifulSoup

def get_data(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    title = str(soup).split('<title>')[1].split('</title>')[0]
    if " | Couchbase Docs" in title:
        title = title[:(title.index(" | Couchbase Docs"))].replace(" ", "_")
    else:
        title = title.replace(" ", "_")
    data = ""
    lines = soup.find_all('p')
    for line in lines:
        data = data + " " + line.text
        # print(data)
    print(title)
    print()
    return title, data




"""import urllib.request 
from inscriptis import get_text 

def get_data():
    url = "https://docs.couchbase.com/server/current/learn/buckets-memory-and-storage/buckets.html"
    html = urllib.request.urlopen(url).read().decode('utf-8') 
    title = str(html).split('<title>')[1].split('</title>')[0]
    title = title[:(title.index(" | Couchbase Docs"))].replace(" ", "_")
    
    text = get_text(html) 
    
    print(text) 
    return title, text



import requests
from bs4 import BeautifulSoup

def get_data():
    # GET request
    r = requests.get('https://docs.couchbase.com/server/current/learn/buckets-memory-and-storage/buckets.html')
    # Parse the HTML
    soup = BeautifulSoup(r.content, "html.parser")

    # print(soup)
    title = str(soup).split('<title>')[1].split('</title>')[0]
    title = title[:(title.index(" | Couchbase Docs"))].replace(" ", "_")
    
    print(title) 
    data = ""
    lines = soup.find_all('p')
    for line in lines:
        data = data + " " + line.text
    # print(data)
    return title, data

"""


