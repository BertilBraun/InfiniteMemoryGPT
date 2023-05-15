import pinecone
from uuid import uuid4
from util.gpt import create_embedding
from util.types import DatabaseEntry, Message, Messages, Role
from .settings import config

pinecone.init(
    api_key=config['pinecone_api_key'],
    environment=config['pinecone_environment']
)

index_name = 'gpt4-pinecone-chatbot'

# only create index if it doesn't exist
if index_name not in pinecone.list_indexes():
    print("Creating index...")
    pinecone.create_index(
        name=index_name,
        dimension=1536,
        metric='cosine'
    )
    print("Index created.")

# now connect to the index
index = pinecone.Index(index_name)

def insert_data(question: str, answer: str, embedding: list[float]) -> None:
    entry = DatabaseEntry(
        id=str(uuid4()),
        question=question,
        answer=answer
    )
    # create IDs
    ids = [entry.id]
    # create metadata
    metadatas = [{'question': entry.question, 'answer': entry.answer}]
    # create records list for upsert
    records = zip(ids, [embedding], metadatas)
    # upsert to Pinecone
    index.upsert(vectors=records)

def search_top_k(question: str, k=5, hottest_last=True) -> Messages:
    print(Message(role=Role.SYSTEM, content="Searching for similar questions..."))
    embeddings = create_embedding(question)

    # now query
    xc = index.query([embeddings], top_k=k, include_metadata=True, include_values=False)

    responses = []
    for result in (xc['matches'] if not hottest_last else reversed(xc['matches'])):
        responses.append(Message(role=Role.USER, content=result['metadata']['question']))
        responses.append(Message(role=Role.ASSISTANT, content=result['metadata']['answer']))

    return responses