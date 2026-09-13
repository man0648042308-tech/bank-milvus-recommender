# Milvus面试题10道（含项目回答）

## 1. Milvus是什么？

Milvus是面向向量数据的开源数据库，支持向量存储、标量字段、索引、相似度检索、过滤、分区以及稠密/稀疏混合检索。本项目使用Milvus Standalone保存银行产品并执行推荐检索。

## 2. Milvus Standalone由哪些核心容器组成？

本次2.6部署包含：Milvus Standalone服务、etcd和MinIO。etcd保存元数据，MinIO保存对象数据，Milvus提供查询和写入能力。客户端通过19530端口连接。

## 3. Milvus中的Collection和Schema是什么？

Collection类似关系数据库的表；Schema规定字段名称、类型、主键和向量维度。项目的Schema包含`id`、`vector`、`name`、`category`、`risk_level`和`min_investment`。

## 4. Milvus支持哪些常见字段？

常见标量字段有INT64、FLOAT、BOOL和VARCHAR；向量字段包括FLOAT_VECTOR、BINARY_VECTOR和SPARSE_FLOAT_VECTOR等。字段类型必须与插入数据匹配。

## 5. 如何使用PyMilvus连接Milvus？

使用`MilvusClient(uri=..., token=...)`创建客户端。本项目Windows客户端连接`http://192.168.220.77:19530`，服务运行在VMware虚拟机。程序结束时调用`client.close()`释放连接。

## 6. Insert和Upsert有什么区别？

Insert用于新增实体；当主键冲突时通常不能视为更新。Upsert按主键决定更新已有实体或插入新实体。生产代码还要关注一致性、批量大小和失败重试。

## 7. Milvus中的标量查询和向量搜索有什么区别？

`query()`按普通字段表达式查数据，例如`risk_level <= 2`；`search()`使用查询向量执行相似度搜索，也可以附加标量`filter`。本项目在`search()`中同时使用向量和业务过滤。

## 8. FLAT、IVF_FLAT和HNSW如何选择？

- FLAT：精确搜索，适合较小数据或基准测试。
- IVF_FLAT：先聚类缩小候选范围，速度和召回率由`nlist/nprobe`影响。
- HNSW：基于多层近邻图，通常有较好延迟和召回，但占用更多内存。

选择要基于数据规模、延迟、内存和召回率实测，不能只背结论。

## 9. Partition有什么作用？

Partition是在一个Collection内部对数据进行物理分组。按租户、地区或时间分区后，可以只搜索目标分区，减少扫描范围。但分区过多会增加管理成本，不能把它当普通标签滥用。

## 10. 如何排查Milvus连接失败？

按层排查：虚拟机是否运行；VMnet网络是否可达；`docker compose ps`中三个服务是否健康；19530是否映射到`0.0.0.0`；Windows的`Test-NetConnection`是否成功；URI和客户端版本是否正确；最后再看Milvus日志。不要一开始就反复改Python代码。
