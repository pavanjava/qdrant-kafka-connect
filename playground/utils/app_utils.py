from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333", api_key="th3s3cr3tk3y")
dimension_dict = {"snowflake/snowflake-arctic-embed-s": 384}


def create_qdrant_collection(collection_name: str, embed_model: str):

    if not client.collection_exists(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=dimension_dict.get(embed_model), distance=models.Distance.COSINE)
        )
