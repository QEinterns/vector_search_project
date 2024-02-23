import subprocess
import json

def vector_search1(index_name, search_vector, k, cb_coll):
  

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
      a = str(result.stdout)
      b = json.loads(a[2:len(a)-3])
    #   print(b,"\n")
      c = b['hits']
    #   print(c,"\n")
      # print(type(c))
      for i in c:
        docid = i['id']
        try:
            result = cb_coll.get(docid)
            data = result.value['data']
            # print('\n\n')
            similar_chunks += data
        except Exception as e:
            print(e)
      
      # print(res)
  except subprocess.CalledProcessError as e:
      print(f"Error executing curl command: {e}")
    
#   print(similar_chunks)
  return similar_chunks
