"""Milvus 连接、Collection 建立和数据写入。"""

from pymilvus import DataType, MilvusClient

from .config import (
    COLLECTION_NAME,
    COLLECTION_PREFIX,
    MILVUS_TOKEN,
    MILVUS_URI,
    VECTOR_DIMENSION,
)
from .data import PRODUCTS


def connect_client() -> MilvusClient:
    """连接虚拟机里的 Milvus 服务。"""
    return MilvusClient(uri=MILVUS_URI, token=MILVUS_TOKEN)


def ensure_safe_collection_name(collection_name: str) -> None:
    """只允许练习代码操作 day32_ 前缀的 Collection。"""
    if not collection_name.startswith(COLLECTION_PREFIX):
        raise ValueError(f"拒绝操作非练习集合：{collection_name}")


def recreate_collection(
    client: MilvusClient,
    collection_name: str = COLLECTION_NAME,
) -> None:
    """重新创建银行产品 Collection，并建立余弦索引。"""
    ensure_safe_collection_name(collection_name)

    if client.has_collection(collection_name):
        client.drop_collection(collection_name)

    schema = MilvusClient.create_schema(
        auto_id=False,
        enable_dynamic_field=False,
    )
    schema.add_field("id", DataType.INT64, is_primary=True)
    schema.add_field("vector", DataType.FLOAT_VECTOR, dim=VECTOR_DIMENSION)
    schema.add_field("name", DataType.VARCHAR, max_length=100)
    schema.add_field("category", DataType.VARCHAR, max_length=50)
    schema.add_field("risk_level", DataType.INT64)
    schema.add_field("min_investment", DataType.FLOAT)

    index_params = client.prepare_index_params()
    index_params.add_index(
        field_name="vector",
        index_type="AUTOINDEX",
        metric_type="COSINE",
    )

    client.create_collection(
        collection_name=collection_name,
        schema=schema,
        index_params=index_params,
        consistency_level="Strong",
    )


def insert_products(
    client: MilvusClient,
    collection_name: str = COLLECTION_NAME,
) -> int:
    """插入五个银行产品，返回实际插入条数。"""
    result = client.insert(collection_name=collection_name, data=PRODUCTS)
    return int(result["insert_count"])


def prepare_demo_data(client: MilvusClient) -> int:
    """创建 Collection 并填充作业数据。"""
    recreate_collection(client)
    return insert_products(client)
