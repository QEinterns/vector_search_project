from bs4 import BeautifulSoup

input_file = '/Users/spatra/Desktop/Movie/Architect_Chat/Dataset/raw/temp.txt'
with open(input_file, 'r') as f:
    html_content = f.read()
soup = BeautifulSoup(html_content, "html.parser")

data = ""
lines = soup.find_all('p')
for line in lines:
    data = data + " " + line.text
    # print(data)

print(data)

output_file = '/Users/spatra/Desktop/Movie/Architect_Chat/Dataset/raw/kv_engine.txt'

with open(output_file, 'a', encoding='utf-8') as output:
    output.write("\n")
    output.write(data)
    




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


