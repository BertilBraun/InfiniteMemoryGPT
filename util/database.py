
from .settings import config

DATABASE_IN_USE = config['database_in_use']
if DATABASE_IN_USE == 'milvus':
    from .milvus_impl import *
elif DATABASE_IN_USE == 'pinecone':
    from .pinecone_impl import *
else:
    raise Exception(f"Invalid database in use: {DATABASE_IN_USE}")
