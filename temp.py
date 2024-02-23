args = ("top_gun","top_gun1")

text = """
curl -XPUT -H "Content-Type: application/json" \
-u Administrator:password http://172.23.108.119:8094/api/index/{0} -d \
'{{
"name":{1},
"type": "fulltext-index",
""".format(*args)

print(text)

