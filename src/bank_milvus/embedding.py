"""把中文需求转换为教学用四维向量。

四个维度依次表示：安全性、成长性、流动性、收益偏好。
真实项目会换成 BGE 等嵌入模型；这里先用确定性规则保证作业可复现、可测试。
"""


def build_query_vector(query: str) -> list[float]:
    """根据查询关键词生成四维向量。"""
    vector = [0.50, 0.50, 0.50, 0.50]

    if any(word in query for word in ("低风险", "稳健", "保本", "安全")):
        vector[0] = 1.00
        vector[1] = 0.20
    if any(word in query for word in ("高收益", "成长", "进取")):
        vector[1] = 1.00
        vector[3] = 0.90
    if any(word in query for word in ("灵活", "随时", "流动")):
        vector[2] = 1.00

    return vector
