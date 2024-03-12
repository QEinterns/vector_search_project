import subprocess
import json


  
def vector_search_chat(index_name, search_vector, k, cb_coll):
  args = {"index_name":index_name, "search_vector":search_vector,"k":k}
  curl_command = """
          
  curl -XPOST -H "Content-Type: application/json" -u Administrator:password \
  http://172.23.108.107:8094/api/index/{index_name}/query \
  -d '{{
    "query": {{
      "match_none": {{}}
    }},
    "explain": true,
    "knn": [
      {{
        "field": "vector_data",
        "k": {k},
        "vector":{search_vector}
      }}
    ],
    "size": 10,
    "from": 0
  }}'
  """.format(**args)

  # Execute the curl command using subprocess
  try:
      similar_chunks = ""
      result = subprocess.run(curl_command, shell=True, check=True,stdout=subprocess.PIPE)
      print("Context chunks retrieved successfully")
      a = result.stdout
      string_data = a.decode('utf-8')
      json_data = json.loads(string_data)
      c = json_data['hits']
      for i in c:
        docid = i['id']
        try:
            result = cb_coll.get(docid)
            data = result.value['data']
            similar_chunks += data
        except Exception as e:
            print(e)
      
  except subprocess.CalledProcessError as e:
      print(f"Error executing curl command: {e}")
    
  return similar_chunks



# import requests

# def vector_search_chat(index_name, search_vector, k, cb_coll):
#   similar_chunks = ""
#   try:
#       args = {"index_name":index_name, "search_vector":search_vector,"k":k}
#       curl_command = """
              
#       curl -XPOST -H "Content-Type: application/json" -u Administrator:password \
#       http://172.23.108.107:8094/api/index/{index_name}/query \
#       -d '{{
#         "query": {{
#           "match_none": {{}}
#         }},
#         "explain": true,
#         "knn": [
#           {{
#             "field": "vector_data",
#             "k": {k},
#             "vector":{search_vector}
#           }}
#         ],
#         "size": 10,
#         "from": 0
#       }}'
#       """.format(**args)
#       result = requests.get(curl_command)  # Assuming curl_command is a valid URL
#       result.raise_for_status()  # Raise an exception for non-2xx responses
#       print("Context chunks retrieved successfully")
      
#       json_data = result.json()
#       for hit in json_data.get('hits', []):
#           docid = hit.get('id')
#           if docid:
#               try:
#                   result = cb_coll.get(docid)
#                   data = result.value.get('data')
#                   if data:
#                       similar_chunks += data
#               except Exception as e:
#                   print(f"Error retrieving document {docid}: {e}")
#   except requests.RequestException as e:
#       print(f"Error retrieving context chunks: {e}")

#   return similar_chunks