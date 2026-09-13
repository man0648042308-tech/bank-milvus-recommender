"""集中管理运行配置，避免把不同机器的地址散落在代码中。"""

import os


MILVUS_URI = os.getenv("MILVUS_URI", "http://192.168.220.77:19530")
MILVUS_TOKEN = os.getenv("MILVUS_TOKEN", "root:Milvus")
COLLECTION_PREFIX = "day32_"
COLLECTION_NAME = f"{COLLECTION_PREFIX}bank_products"
VECTOR_DIMENSION = 4
