# Complete Guide to Qdrant-kafka connector

### Installation of Confluent Kafka Platform

- navigate to https://www.confluent.io/installation/
- Download the distribution files (tar, zip, etc.)
- Extract the downloaded file using:
  - `tar -xvf confluent-<version>.tar.gz` or
  - `unzip confluent-<version>.zip`
- Configure Environment Variables:
  - `export CONFLUENT_HOME=/path/to/confluent-<version>`
  - `export PATH=$CONFLUENT_HOME/bin:$PATH`
- Run Confluent Platform Locally:
  - `confluent local start`
  - `confluent local stop`

### Installation of Qdrant

- `docker pull qdrant/qdrant` 
- `docker run -p 6334:6334 qdrant/qdrant`

### Installation of Qdrant-Kafka Sink Connector

- `confluent-hub install qdrant/qdrant-kafka:1.1.0 `

### Installation of MongoDB (with single node replicaset)

- run below docker compose file
  - `docker-compose -f <your-file-name>.yml up`
```
version: "3.8"

services:
  mongo1:
    image: mongo:7.0
    command: ["--replSet", "rs0", "--bind_ip_all", "--port", "27017"]
    ports:
      - 27017:27017
    healthcheck:
      test: echo "try { rs.status() } catch (err) { rs.initiate({_id:'rs0',members:[{_id:0,host:'host.docker.internal:27017'}]}) }" | mongosh --port 27017 --quiet
      interval: 5s
      timeout: 30s
      start_period: 0s
      start_interval: 1s
      retries: 30
    volumes:
      - "mongo1_data:/data/db"
      - "mongo1_config:/data/configdb"

volumes:
  mongo1_data:
  mongo1_config:
```

### Installation of MongoDB connector

- `confluent-hub install mongodb/kafka-connect-mongodb:latest`

### Qdrant sink connector configuration

```
{
  "name": "QdrantSinkConnectorConnector_0",
  "config": {
    "value.converter.schemas.enable": "false",
    "name": "QdrantSinkConnectorConnector_0",
    "connector.class": "io.qdrant.kafka.QdrantSinkConnector",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "topics": "topic_62,qdrant_kafka.docs",
    "errors.deadletterqueue.topic.name": "dead_queue",
    "errors.deadletterqueue.topic.replication.factor": "1",
    "qdrant.grpc.url": "http://localhost:6334",
    "qdrant.api.key": "************"
  }
}
```

### MongoDB source connector configuration

```
{
  "name": "MongoSourceConnectorConnector_0",
  "config": {
    "connector.class": "com.mongodb.kafka.connect.MongoSourceConnector",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "org.apache.kafka.connect.storage.StringConverter",
    "connection.uri": "mongodb://127.0.0.1:27017/?replicaSet=rs0&directConnection=true",
    "database": "qdrant_kafka",
    "collection": "docs",
    "publish.full.document.only": "true",
    "topic.namespace.map": "{\"*\":\"qdrant_kafka.docs\"}",
    "copy.existing": "true"
  }
}
```

### Running the playground application
- `pip install -r requirememts.txt`
- `python main.py`