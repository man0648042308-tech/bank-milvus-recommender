> 本仓库为个人作品集公开版：AI 大模型应用开发课程实战项目，模拟数据，非生产系统。更多项目见作品集主页。

# Day32：银行产品 Milvus 向量推荐作业

## 一句话说明

本项目把银行产品写入虚拟机中的 Milvus，然后同时使用“向量相似度”和“风险/起投金额”两个业务条件生成推荐结果。

## 环境分工

- Windows：VS Code、Python代码、uv、PyMilvus客户端。
- VMware Ubuntu：Milvus 2.6.22服务端。
- 服务地址：`http://192.168.220.77:19530`。
- 虚拟机部署目录：`/opt/day32-milvus`。

Windows没有运行Milvus Lite。Windows代码通过VMnet8访问虚拟机中的Milvus Standalone。

## 黄金执行路径

```text
用户中文需求
  → build_query_vector：变成四维查询向量
  → build_business_filter：生成风险与金额过滤条件
  → MilvusClient.search：过滤后进行COSINE相似度搜索
  → recommend_products：整理推荐结果
  → main：打印给用户
```

## 第一次运行

在VS Code中打开本项目，然后打开终端：

```powershell
Set-Location "./BankMilvus_Day32"
uv sync
uv run pytest
uv run python -m bank_milvus.main
uv run python tests\verify_integration.py
```

预期看到：

```text
1. 已连接 Milvus：http://192.168.220.77:19530
2. 已向 day32_bank_products 插入 5 个产品
3. 推荐结果：
   1. 安心储蓄，风险等级 1……
```

## 每条命令逐词解释

`Set-Location` 是PowerShell的“切换当前目录”命令；后面的双引号包住完整路径。

`uv sync`：

- `uv`：Python项目与依赖管理工具。
- `sync`：让本机虚拟环境与`pyproject.toml`声明保持一致。

`uv run pytest`：

- `run`：在本项目环境中运行命令。
- `pytest`：执行`tests`目录下的自动测试。

`uv run python -m bank_milvus.main`：

- `python`：启动Python解释器。
- `-m`：按照“模块”运行，不是按文件路径运行。
- `bank_milvus.main`：运行`src/bank_milvus/main.py`。

## 文件阅读顺序

现在必须读：

1. `src/bank_milvus/data.py`：数据长什么样。
2. `src/bank_milvus/embedding.py`：文本怎样变成向量。
3. `src/bank_milvus/database.py`：数据怎样进入Milvus。
4. `src/bank_milvus/crud.py`：怎样读取、更新和删除数据。
5. `src/bank_milvus/recommendation.py`：怎样过滤和搜索。
6. `src/bank_milvus/main.py`：上面五部分怎样串起来。

稍后再读：测试文件、索引参数、真正的中文嵌入模型。

暂时跳过：分区、BM25、稀疏向量、RRF、完整RAG。这些属于下一阶段，不能阻塞今天的可运行链路。

## 安全边界

- 代码只允许删除以`day32_`开头的练习Collection。
- `.env`不提交。
- 不修改课程原目录。
- 不会删除虚拟机中的PostgreSQL或其他数据。
