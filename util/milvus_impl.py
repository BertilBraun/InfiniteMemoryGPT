from uuid import uuid4

from pymilvus import (Collection, CollectionSchema, DataType, FieldSchema,
                      connections, utility)
from util.gpt import create_embedding
from util.types import Message, Messages, Role

from .settings import config

# Connect to Milvus
connections.connect(
    "default", 
    uri=config['milvus_uri'], 
    user="db_admin", 
    password=config['milvus_password'], 
    secure=True
)

# Create collection
fields = [
    FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
    FieldSchema(name="question", dtype=DataType.VARCHAR, max_length=8096),
    FieldSchema(name="answer", dtype=DataType.VARCHAR, max_length=8096),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=1536),
]

schema = CollectionSchema(fields, "Infinite memory chatbot using GPT-4 and Milvus")
collection_name = "gpt4_milvus_chatbot"

# Check if the collection exists
has = utility.has_collection(collection_name, using="default")

if not has:
    chatbot_collection = Collection(collection_name, schema, using="default", consistency_level="Strong")

    # Create index
    index = {
        "index_type": "AUTOINDEX",
        "metric_type": "L2",
        "params": {"nlist": 1536},
    }

    chatbot_collection.create_index("embeddings", index)

else:
    # If the collection exists, load it
    chatbot_collection = Collection(collection_name, using="default")

def insert_data(question: str, answer: str, embedding: list[float]) -> None:
    entities = [
        [str(uuid4())],  # Primary key
        [question],
        [answer],
        [embedding],
    ]

    chatbot_collection.insert(entities)
    chatbot_collection.flush()

def search_top_k(question: str, k=5, hottest_last=True) -> Messages:
    print("Searching for similar questions...")
    embeddings = create_embedding(question)

    chatbot_collection.load()
    search_params = {
        "metric_type": "L2",
        "params": {"nprobe": 10},
    }

    results = chatbot_collection.search(
        [embeddings],
        "embeddings",
        search_params,
        limit=k,
        output_fields=["question", "answer"]
    )
    
    messages = []
    for result in (results[0] if not hottest_last else reversed(results[0])):
        messages.append(Message(role=Role.USER, content=result[0].entity.question))
        messages.append(Message(role=Role.ASSISTANT, content=result[0].entity.answer))

    return messages