from pymongo import MongoClient
from utils.app_utils import create_qdrant_collection
from fastembed import TextEmbedding

collection_name: str = 'test'
embed_model_name: str = 'snowflake/snowflake-arctic-embed-s'

# Ste 0: create qdrant_collection
create_qdrant_collection(collection_name=collection_name, embed_model=embed_model_name)

# Step 1: Connect to MongoDB
client = MongoClient('mongodb://127.0.0.1:27017/?replicaSet=rs0&directConnection=true')

# Step 2: Select Database
db = client['qdrant_kafka']

# Step 3: Select Collection
collection = db['docs']

# Step 4: Create a Document to Insert
description = "qdrant is a high available vector search engine"
embedding_model = TextEmbedding(model_name=embed_model_name)
vector = next(embedding_model.embed(documents=description)).tolist()
document = {
    "collection_name": collection_name,
    "id": 1,
    "vector": vector,
    "payload": {
        "name": "qdrant",
        "description": description,
        "url": "https://qdrant.tech/documentation"
    }
}

# Step 5: Insert the Document into the Collection
result = collection.insert_one(document)

# Step 6: Print the Inserted Document's ID
print("Inserted document ID:", result.inserted_id)
