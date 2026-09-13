"""闭卷复现文件：完整项目通过后再做，不影响今晚主线交付。"""

# TODO 1：导入 MilvusClient。
# TODO 2：连接虚拟机中的 Milvus。
# TODO 3：打印所有 Collection。
# TODO 4：关闭客户端。
 
from pymilvus import MilvusClient
from bank_milvus.config import MILVUS_URI, MILVUS_TOKEN
client = MilvusClient(uri=MILVUS_URI, token=MILVUS_TOKEN)
try:
    collections = client.list_collections()
    print("Milvus 中的 Collection：",collections)
finally:
    client.close()