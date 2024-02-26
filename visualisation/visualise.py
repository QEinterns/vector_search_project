from datetime import timedelta
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from couchbase.cluster import Cluster
from couchbase.auth import PasswordAuthenticator

#connect2couchbase
username = "Administrator"
password = "password"
bucket_name = "b1"
scope_name = "s1"
collection_name = "c1"
        
auth = PasswordAuthenticator(
    username,
    password,
)

cluster = Cluster('couchbase://172.23.108.107', ClusterOptions(auth))
cluster.wait_until_ready(timedelta(seconds=5))
cb = cluster.bucket(bucket_name)
cb_coll = cb.scope(scope_name).collection(collection_name)
    
# Define a function to extract embeddings from documents
def extract_embeddings_from_documents(documents):
    embeddings = []
    for doc in documents:
        embedding = doc.get('vector_data') 
        embeddings.append(embedding)
    return np.array(embeddings)

# Retrieve all relevant documents from Couchbase
query = "SELECT * FROM b1" 
result = cluster.query(query)

# Extract embeddings from documents
embeddings = extract_embeddings_from_documents(result)

# Perform PCA to reduce dimensionality
pca = PCA(n_components=2)
embeddings_pca = pca.fit_transform(embeddings)

# Plot the reduced-dimensional embeddings
plt.scatter(embeddings_pca[:, 0], embeddings_pca[:, 1])
plt.title('PCA Visualization of Embeddings')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()
