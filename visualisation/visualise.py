import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from couchbase.cluster import Cluster
from couchbase.auth import PasswordAuthenticator

# Connect to the Couchbase cluster
cluster = Cluster('couchbase://your_host')
authenticator = PasswordAuthenticator('username', 'password')
cluster.authenticate(authenticator)
bucket = cluster.bucket('your_bucket')
collection = bucket.default_collection()

# Define a function to extract embeddings from documents
def extract_embeddings_from_documents(documents):
    embeddings = []
    for doc in documents:
        embedding = doc.get('embedding_field')  # Replace 'embedding_field' with the field name containing the embedding
        embeddings.append(embedding)
    return np.array(embeddings)

# Retrieve all relevant documents from Couchbase
query = "SELECT * FROM your_bucket WHERE condition"  # Define your query condition
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
