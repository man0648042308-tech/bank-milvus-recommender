"""银行产品的读取、更新和删除操作。"""

from pymilvus import MilvusClient

from .config import COLLECTION_NAME


def get_product(client: MilvusClient, product_id: int) -> dict | None:
    """按照主键读取一个产品；不存在时返回None。"""
    rows = client.get(
        collection_name=COLLECTION_NAME,
        ids=[product_id],
        output_fields=[
            "id",
            "vector",
            "name",
            "category",
            "risk_level",
            "min_investment",
        ],
    )
    return rows[0] if rows else None


def update_product(client: MilvusClient, product: dict) -> int:
    """使用主键Upsert更新已有产品，返回影响条数。"""
    result = client.upsert(
        collection_name=COLLECTION_NAME,
        data=[product],
    )
    return int(result["upsert_count"])


def delete_product(client: MilvusClient, product_id: int) -> int:
    """按照主键删除一个产品，返回删除条数。"""
    result = client.delete(
        collection_name=COLLECTION_NAME,
        ids=[product_id],
    )
    return int(result["delete_count"])
