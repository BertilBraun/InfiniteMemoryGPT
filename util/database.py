
from .settings import config

DATABASE_IN_USE = config['database_in_use']
if DATABASE_IN_USE == 'milvus':
    from .milvus import *
elif DATABASE_IN_USE == 'pinecone':
    from .pinecone import *
else:
    raise Exception(f"Invalid database in use: {DATABASE_IN_USE}")
