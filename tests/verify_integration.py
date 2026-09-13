"""连接真实 Milvus 的独立验收脚本。"""

from bank_milvus.config import COLLECTION_NAME
from bank_milvus.crud import delete_product, get_product, update_product
from bank_milvus.data import PRODUCTS
from bank_milvus.database import connect_client, prepare_demo_data
from bank_milvus.recommendation import recommend_products


def main() -> None:
    client = connect_client()
    try:
        inserted_count = prepare_demo_data(client)
        assert inserted_count == 5, f"应插入5条，实际为{inserted_count}条"

        rows = client.query(
            collection_name=COLLECTION_NAME,
            filter="id >= 1",
            output_fields=["id", "name"],
            limit=10,
        )
        assert len(rows) == 5, f"应查询到5条，实际为{len(rows)}条"

        recommendations = recommend_products(
            client,
            query="低风险、稳定、流动性好",
            max_risk=2,
            available_amount=5000,
        )
        assert recommendations, "推荐结果不能为空"
        assert all(item["risk_level"] <= 2 for item in recommendations)
        assert all(item["min_investment"] <= 5000 for item in recommendations)
        assert recommendations[0]["name"] == "安心储蓄"

        updated_product = {**PRODUCTS[1], "name": "稳健债券基金（已更新）"}
        assert update_product(client, updated_product) == 1
        saved_product = get_product(client, product_id=2)
        assert saved_product is not None
        assert saved_product["name"] == "稳健债券基金（已更新）"

        assert delete_product(client, product_id=5) == 1
        assert get_product(client, product_id=5) is None

        print("PASS 连接真实Milvus")
        print("PASS 创建Collection并插入5条产品")
        print("PASS 查询5条产品")
        print("PASS 风险与金额过滤")
        print("PASS 向量Top-K推荐")
        print("PASS Upsert更新产品")
        print("PASS Delete删除产品")
        print("验收结果：7/7通过")
    finally:
        client.close()


if __name__ == "__main__":
    main()
