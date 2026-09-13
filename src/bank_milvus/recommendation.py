"""使用向量相似度和业务条件共同推荐银行产品。"""

from pymilvus import MilvusClient

from .config import COLLECTION_NAME
from .embedding import build_query_vector


def build_business_filter(max_risk: int, available_amount: float) -> str:
    """生成 Milvus 标量过滤表达式。"""
    if max_risk < 1:
        raise ValueError("max_risk 必须大于或等于1")
    if available_amount < 0:
        raise ValueError("available_amount 不能为负数")
    return (
        f"risk_level <= {max_risk} and "
        f"min_investment <= {float(available_amount)}"
    )


def recommend_products(
    client: MilvusClient,
    query: str,
    max_risk: int,
    available_amount: float,
    top_k: int = 3,
) -> list[dict]:
    """先过滤风险和起投金额，再按向量相似度返回 Top-K 产品。"""
    query_vector = build_query_vector(query)
    filter_expression = build_business_filter(max_risk, available_amount)

    search_result = client.search(
        collection_name=COLLECTION_NAME,
        data=[query_vector],
        filter=filter_expression,
        limit=top_k,
        output_fields=[
            "name",
            "category",
            "risk_level",
            "min_investment",
        ],
    )

    recommendations = []
    for hit in search_result[0]:
        entity = hit["entity"]
        recommendations.append(
            {
                "id": hit["id"],
                "name": entity["name"],
                "risk_level": entity["risk_level"],
                "min_investment": entity["min_investment"],
                "similarity": round(float(hit["distance"]), 4),
            }
        )
    return recommendations
