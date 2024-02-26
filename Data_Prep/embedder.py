from dependencies import *

class NumpyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)
    
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def embed(chunks, name, cb_coll):

    docid_counter  = 1
    for sentence in chunks:
        emb = model.encode(str(sentence.page_content))
        embedding = np.array(emb)
        np.set_printoptions(suppress=True)

        json_dump =  json.dumps(embedding, cls=NumpyEncoder)
        document = { 
            "data":str(sentence.page_content),
            "vector_data":ast.literal_eval(json_dump)
        }
        
        docid = 'docid:' + str(name) + str(docid_counter)
        docid_counter+=1

        try:
            result = cb_coll.upsert(docid, document)
            print(result.cas)
        except Exception as e:
            print(e)
    
    return 1
        
         
        # return docid,document