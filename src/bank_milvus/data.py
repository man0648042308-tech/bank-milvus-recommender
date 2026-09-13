"""可重复使用的银行产品测试数据。"""

PRODUCTS = [
    {
        "id": 1,
        "name": "安心储蓄",
        "category": "deposit",
        "risk_level": 1,
        "min_investment": 500.0,
        "vector": [0.95, 0.10, 0.90, 0.50],
    },
    {
        "id": 2,
        "name": "稳健债券基金",
        "category": "fund",
        "risk_level": 2,
        "min_investment": 1000.0,
        "vector": [0.80, 0.35, 0.60, 0.70],
    },
    {
        "id": 3,
        "name": "成长股票基金",
        "category": "fund",
        "risk_level": 4,
        "min_investment": 1000.0,
        "vector": [0.20, 0.95, 0.50, 0.80],
    },
    {
        "id": 4,
        "name": "黄金ETF联接",
        "category": "fund",
        "risk_level": 3,
        "min_investment": 5000.0,
        "vector": [0.50, 0.65, 0.60, 0.40],
    },
    {
        "id": 5,
        "name": "高风险私募",
        "category": "private_fund",
        "risk_level": 5,
        "min_investment": 1_000_000.0,
        "vector": [0.10, 1.00, 0.10, 1.00],
    },
]
