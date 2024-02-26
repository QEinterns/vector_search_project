from bs4 import BeautifulSoup
import os

path = "/Users/spatra/Desktop/Data_Prep/docs"

# list to store files
res = []

# Iterate directory
for file_path in os.listdir(path):
    # check if current file_path is a file
    if os.path.isfile(os.path.join(path, file_path)):
        # add filename to list
        res.append(file_path)

for file in res:
    print(file)
    file = os.path.join(path, file)
    with open(file, 'r') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    title = str(soup).split('<title>')[1].split('</title>')[0]
    if " | Couchbase Docs" in title:
        title = title[:(title.index(" | Couchbase Docs"))].replace(" ", "_")
    else:
        title = title.replace(" ", "_")
        
    print(title) 
    data = ""
    lines = soup.find_all('p')
    for line in lines:
        data = data + " " + line.text
        # print(data)
    print()
    print(title)
    print(data)
    print("\n\n")