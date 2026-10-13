"""Day32 作业的一键运行入口。"""

from .config import COLLECTION_NAME, MILVUS_URI
from .database import connect_client, prepare_demo_data
from .recommendation import recommend_products


def main() -> None:
    client = connect_client()
    try:
        print(f"1. 已连接 Milvus：{MILVUS_URI}")
        inserted_count = prepare_demo_data(client)
        print(f"2. 已向 {COLLECTION_NAME} 插入 {inserted_count} 个产品")

        recommendations = recommend_products(
            client=client,
            query="我想找低风险、收益稳定而且比较灵活的产品",
            max_risk=2,
            available_amount=600,
        )
        print("3. 推荐结果：")
        for number, item in enumerate(recommendations, start=1):
            print(
                f"   {number}. {item['name']}，风险等级 "
                f"{item['risk_level']}，起投 {item['min_investment']:.0f} 元，"
                f"相似度 {item['similarity']}"
            )
    finally:
        client.close()


if __name__ == "__main__":
    main()



