"""不连接 Milvus 的确定性单元测试。"""

import pytest

from bank_milvus.database import ensure_safe_collection_name
from bank_milvus.embedding import build_query_vector
from bank_milvus.recommendation import build_business_filter


def test_low_risk_query_prefers_safety() -> None:
    vector = build_query_vector("我想找低风险、保本的产品")
    assert vector[0] == 1.0
    assert vector[0] > vector[1]


def test_business_filter_contains_both_rules() -> None:
    expression = build_business_filter(max_risk=2, available_amount=5000)
    assert expression == "risk_level <= 2 and min_investment <= 5000.0"


def test_collection_safety_guard() -> None:
    ensure_safe_collection_name("day32_test")
    with pytest.raises(ValueError):
        ensure_safe_collection_name("production_products")
