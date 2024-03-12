import subprocess,logging


def create_index(index_name):
    args = {"index_name" : index_name}

    curl_command = """
curl -XPUT -H "Content-Type: application/json" \
-u Administrator:password http://172.23.108.119:8094/api/index/{index_name} -d \
'{{ 
   "name": "{index_name}",
   "type": "fulltext-index",
   "params": {{
    "doc_config": {{
    "docid_prefix_delim": "",
    "docid_regexp": "",
    "mode": "scope.collection.type_field",
    "type_field": "type"
   }},
   "mapping": {{
    "default_analyzer": "standard",
    "default_datetime_parser": "dateTimeOptional",
    "default_field": "_all",
    "default_mapping": {{
     "dynamic": true,
     "enabled": false
    }},
    "default_type": "_default",
    "docvalues_dynamic": false,
    "index_dynamic": true,
    "store_dynamic": false,
    "type_field": "_type",
    "types": {{
     "s1.cn1": {{
      "dynamic": false,
      "enabled": true,
      "properties": {{
       "vector_data": {{
       "enabled": true,
       "dynamic": false,
       "fields": [
        {{
         "dims": 1024,
         "index": true,
         "name": "vector_data",
         "similarity": "l2_norm",
         "type": "vector",
         "vector_index_optimized_for": "recall"
        }}
       ]
      }}
     }}
    }}
   }}
  }},
  "store": {{
   "indexType": "scorch",
   "segmentVersion": 16
  }}
 }},
 "sourceType": "gocbcore",
 "sourceName": "b1",
 "sourceParams": {{}},
 "planParams": {{
 "maxPartitionsPerPIndex": 1024,
 "indexPartitions": 1,
 "numReplicas": 0
 }}
}}'
""".format(**args)

    print(curl_command)
    try:
        subprocess.run(curl_command, shell=True, check=True)
        print(f"Index {index_name} created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating the index {index_name}: {e}")


# create_index("time1")