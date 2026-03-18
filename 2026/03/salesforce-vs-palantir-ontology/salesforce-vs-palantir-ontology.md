---
title: 为什么 Palantir 的 Ontology 是 AI 时代更好的企业架构——以及 Salesforce 为什么难以追赶
author: Mazy
description: 从架构基因、客户画像、商业模式三重锁定，深度拆解 Palantir Ontology 与 Salesforce Custom Objects 的本质差异
cover: ./cover.png
created: 2026-03-17
published:
  wechat: 2026-03-18
wechat_media_id: Kp3yNKpaOwwGup4XjiOi2g9Pb0QuSE58sgrtwdkfTrN4JuhkRysBW_Pzz5Oot-KZ
---

## 结论前置

Salesforce 和 Palantir 都以"对象建模"（Objects + Properties + Relationships）为核心抽象，但走出了截然不同的路径。在 AI 时代，这两条路径的适配性差异正在显现：**在需要跨系统数据融合、高安全治理、操作语义建模的场景下**，Palantir 的 Ontology 架构在语义清晰度、AI 原生集成、跨系统数据治理三个维度上具有结构性优势；而在 CRM 主导、有界操作、快速上线的场景下，Salesforce 的平台仍然是更务实的选择。

核心差异一句话：Palantir 的 Ontology 是跨企业的操作语义层（数据 → 语义 → 行动），Salesforce 的 Custom Objects 是 CRM 领域的关系型数据库抽象（表 → 字段 → 记录）。前者是为跨系统决策设计的世界模型，后者是为业务记录管理设计的高效平台。

Salesforce 难以追赶的根因不是技术能力不够——Data Cloud 全新技术栈、Missionforce 独立业务单元证明了它有能力和意愿。但架构基因、客户画像、商业模式三重锁定效应意味着它只能从 CRM 核心向外渐进扩展，而非自顶向下构建企业级 Ontology。收敛方向是单向的：Salesforce 在向 Palantir 靠拢，Palantir 没有在向 CRM 平台靠拢。

这不意味着 Salesforce 作为一家公司会失败。它有 ~$38B 年收入（FY2025）、15 万家企业客户、20 万+ 认证开发者——这些商业规模优势不会因为架构差异而一夜消失。但本文的论点是：**在跨系统数据融合和高治理 AI 操作这个特定但日益重要的领域**，Ontology 路径与 AI 时代的需求有着更深的契合。

---

## 目录

- [1. 调研范围与限制](#1-调研范围与限制)
- [2. 表面相似性](#2-表面相似性)
- [3. 三个根因](#3-三个根因)
- [4. 技术深潜 A：本体与元数据驱动的关系](#4-技术深潜-a本体ontology与元数据驱动metadata-driven的关系)
- [5. 技术深潜 B：Palantir 为什么选择"数据留在客户端"](#5-技术深潜-bpalantir-为什么选择数据留在客户端的路线)
- [6. 根因的六个下游推论](#6-根因的六个下游推论)
- [7. 各自的代价：架构优势不等于商业胜利](#7-各自的代价架构优势不等于商业胜利)
- [8. Salesforce 的类 Ontology 尝试](#8-salesforce-的类-ontology-尝试及其成果与局限)
- [9. 竞争格局观察](#9-竞争格局观察)
- [10. 启示](#10-启示)
- [Sources](#sources)

---

## 1. 调研范围与限制

本文只对比 Salesforce 和 Palantir，因为它们是"对象建模"路径分叉的最极端案例——同一个起点概念（对象 + 属性 + 关系），完全不同的终点。

**重要限制**：Snowflake、Databricks、Microsoft Fabric 也在构建语义层 / 统一数据模型，它们代表了第三条路径（数据湖 + 计算层 + 后加语义）。特别是 Microsoft 的 Fabric + Copilot Studio + Azure OpenAI 组合正在快速覆盖"AI 原生 + 跨系统语义"场景，对于已深度使用 Microsoft 365 + Azure 的 Fortune 500 企业，它可能是比 Palantir 更现实的选择。此外，Neo4j、dbt Semantic Layer 等开源/商业工具可以在任意平台上以低得多的成本构建语义层能力。这些路径与本文的核心论点（"早期架构假设决定了产品进化方向"）并不矛盾，但它们的存在意味着"要么选 Palantir，要么就没有 Ontology"是一个错误的二元框架。展开分析需要另一篇文章。

---

## 2. 表面相似性

| 维度 | Salesforce | Palantir Ontology |
|------|-----------|-------------------|
| 核心抽象 | Custom Object | Object Type |
| 属性 | Field | Property |
| 关系 | Lookup / Master-Detail | Link Type |
| 动作 | Flow / Apex Trigger | Action Type |
| 多态 | Record Type（弱） | Interface（强，真正的多态） |

看起来几乎是同一套概念。但这些相似性掩盖了根本性的架构差异。

---

## 3. 三个根因

### 3.1 架构基因：CRM 数据库 vs. 数据融合层

Salesforce 的架构起点是多租户关系型数据库。Custom Objects 本质上是对底层存储的一层 metadata 抽象——上层穿了一件"对象"的外衣。它的设计目标是让非技术人员能通过点击创建"表"，而不是建模现实世界。

> **架构演进说明**：Salesforce 的底层存储已经从早期的单一 Oracle 实例演进为高度异构的混合系统。Hyperforce（2020 年后逐步推出）将工作负载迁移到公有云原生存储（包括 PostgreSQL/Aurora、Cassandra 等），不再是纯 Oracle 架构。但核心的元数据驱动多租户范式（UDD + 虚拟表结构）保持不变——这是本文分析的焦点。

Palantir 的架构起点是异构数据融合。Ontology 是一层跨数据源的语义映射——底层可以是 Hadoop、Spark pipeline、流数据、第三方 API，上层统一映射为"对象-属性-链接"。它的设计目标是把分散在几十个系统中的数据统一为一个"数字孪生"。

关键区别：
- Salesforce Object = 自己存数据的容器（数据在 Salesforce 里）
- Palantir Object = 对外部数据的语义投影（数据可以在原系统里，Ontology 做映射和索引）

> **重要澄清**：Palantir Foundry 在大多数部署中实际上会把原始数据摄入到自己的 Dataset 中，并在 Foundry 的文件系统中存储转换后的数据。"数据留原处"主要适用于通过 Direct Connection 或 Zero Copy 模式读取的场景，并非所有部署的默认状态。Ontology 的核心价值是作为语义映射层，但不应将其等同于"完全不存数据"。

这意味着 Salesforce 从第一天就选择了"我是数据的主人"的范式（这让它能提供开箱即用的体验），而 Palantir 从第一天就接受"数据可能在别人那里，我做语义层"的现实（这让它能处理最复杂的数据环境，但也意味着每次部署都需要大量定制）。

### 3.2 客户画像：销售团队 vs. 运营决策者

Salesforce 的早期客户以中小企业为主，核心用户是销售和市场团队。他们关心的是线索、机会、管道、预测。这些概念天然适合关系型建模——Contact 属于 Account，Opportunity 关联 Contact，Lead 转化为 Opportunity。

Palantir 的早期客户是美国情报界和国防部（Peter Thiel 提供初始资金，CIA 旗下的 In-Q-Tel 是最早的外部机构投资者之一），核心用户是情报分析师和军事指挥官。他们关心的是"这个嫌疑人和哪些人通过话、去过哪些地方、资金流向哪里"。这些问题天然需要跨系统的实体关系图谱。

客户画像决定了产品进化方向。Salesforce 加的每一个功能都在强化 CRM 用例（Einstein 做的是预测成单概率）；Palantir 加的每一个功能都在强化跨领域数据融合（AIP 做的是在 Ontology 上跑 LLM，让 AI 操作业务对象）。

但这也创造了各自的盲区：Salesforce 很难理解"数据不能出域"的场景；Palantir 很难理解"客户想在 30 分钟内上线"的需求。值得注意的是，这里存在幸存者偏差：Palantir 因为被情报界场景迫使做出了特定架构选择，而这些选择恰好契合了 20 年后的 AI 需求——但我们看不到那些被迫做了类似选择但失败了的公司。

### 3.3 商业模式：座位费 vs. 平台部署费

Salesforce 的商业模式是按用户按月收费（per-seat SaaS）。这个模式的优化方向是：
1. 让更多人用 → 产品要简单、自助
2. 快速上线 → 预置数据模型（Account / Contact / Opportunity 开箱即用）
3. 低摩擦试用 → 标准化、模板化

Palantir 的商业模式是平台部署 + 前线工程师驻场（Forward Deployed Engineers）。这个模式允许：
1. 深度定制 → 每个客户的 Ontology 都不一样
2. 长周期交付 → 花几个月建模客户的业务实体和关系
3. 极高粘性 → 一旦 Ontology 建好，迁移成本极高

如果 Salesforce 尝试做 Ontology 级别的深度建模，会破坏其 per-seat SaaS 的经济模型——Ontology 需要大量前期投入来理解客户的业务实体，而 Salesforce 的 CAC 回收模型假设客户能在几周内上线。

反过来，Palantir 的 FDE 驻场模式在 2016 年之前是公司的财务负担——当时 FDE 人数超过产品工程师，服务成本居高不下。直到 AIP Bootcamp 模式出现（2023 年后），才找到缩短销售周期的方法。

---

## 4. 技术深潜 A：本体（Ontology）与元数据驱动（Metadata-Driven）的关系

表面上看，Salesforce 和 Palantir 都是"元数据驱动"的——都用元数据描述业务实体，运行时根据元数据动态生成行为。但"元数据驱动什么"这个问题上，两者的回答截然不同。

### 4.1 Salesforce：元数据驱动的虚拟数据库

Salesforce 的元数据架构是工程上的壮举。它的核心是 Universal Data Dictionary (UDD)——一组内部元表，其经典设计如下（基于 2008 年 Force.com 多租户白皮书，现代架构已有显著演进，见 §3.1 说明）：

| 内部表 | 存什么 | 类比 |
|--------|--------|------|
| MT_Objects | 对象定义（OrgID + ObjID + ObjName） | DDL: CREATE TABLE |
| MT_Fields | 字段定义（映射到 MT_Data 的 flex 列） | DDL: ALTER TABLE ADD COLUMN |
| MT_Data | 所有租户的实际数据（通用 flex 列，现代系统针对数值/日期/长文本有专用存储路径） | 数据本身 |
| MT_Indexes | 强类型索引列（StringValue / NumValue / DateValue） | CREATE INDEX |

当用户"创建一个 Custom Object"时，Salesforce 不执行任何 DDL（不 CREATE TABLE，不 ALTER COLUMN）。它只在 MT_Objects / MT_Fields 里写入元数据行，运行时由引擎读取元数据动态生成虚拟表结构。这就是为什么 Salesforce 能做到零停机 schema 变更——以及为什么它能服务 15 万家企业共享底层基础设施。

Apex 代码同样存在 UDD 里，编译后以元数据形式缓存。本质上整个平台就是一个元数据驱动的虚拟关系型数据库 + 虚拟应用运行时。

但这个元数据层的核心语义深度止步于数据库层面：
- 它描述的是"这个对象有哪些字段、什么类型、什么校验规则"
- 它的元数据服务于存储和查询，不服务于跨系统的业务语义建模

需要补充的是：Salesforce 的元数据并非完全没有业务语义。Field Description、Help Text、Validation Rule、Related Objects 构成了一套隐含的业务语义注释系统——Agentforce 的 Atlas 引擎正是读取这些信息来理解 Org 结构。20 年存量客户已经不自觉地在维护这套隐含语义。但这些语义是**可选的、分散的、质量参差不齐的**，而非 Ontology 那样**强制的、结构化的、建模时保证的**。

换言之：Salesforce 的核心元数据回答的是"数据长什么样"（schema），对"数据意味着什么"（semantics）提供了可选但不强制的支持。

### 4.2 Palantir：元数据驱动的操作语义层

Palantir 的 Ontology 也是元数据驱动的，但它驱动的不是虚拟数据库，而是一个多层语义系统。以下分层框架是**分析者对 Palantir 能力的归纳**（源自第三方分析，非 Palantir 官方术语），用于帮助理解其元数据的语义深度：

| 层（分析框架） | 对应的 Palantir 官方概念 | 元数据描述什么 | 示例 |
|----|----|----|------|
| 语义层 | Object Type、Property、Link Type | 用现实世界术语定义业务实体和关系 | "这是一个'工厂'，它有'产能'属性，与'供应商'有'供货'关系" |
| 操作层 | Action Type、Function | 定义可以对对象做什么操作，内嵌权限和业务规则 | "只有物流经理能'调拨库存'，且不能超过安全库存线" |
| 安全与治理层 | Object Security Policy、Markings、ABAC 策略 | 横切关注点：细粒度访问控制和数据分类 | "机密级对象只对 TS/SCI 持有者可见" |

Palantir 官方明确说：Ontology "far beyond data cataloging or schema design solutions"（远超数据编目或 schema 设计方案）。它的 Ontology Metadata Service (OMS) 不仅存对象定义，还存 Action Type 的完整逻辑、Function 的执行规则、对象间链接的语义约束。

这套系统的代价是复杂度：每次部署都需要 FDE 或合作伙伴花数周到数月来构建客户特定的 Ontology，而 Salesforce 的 Custom Object 几分钟就能建好。

### 4.3 两种元数据驱动的本质差异

```
Salesforce 元数据驱动路径:
  元数据 → 虚拟表结构 → 数据存储/查询 → UI 渲染
  （驱动的是"数据怎么存、怎么查"）

Palantir 元数据驱动路径:
  元数据 → 语义对象图谱 → 操作/行动/AI → 写回源系统
  （驱动的是"数据意味什么、能做什么、谁能做"）
```

| 维度 | Salesforce UDD | Palantir OMS |
|------|---------------|--------------|
| 元数据的对象 | 虚拟表/字段/索引 | 业务实体/语义关系/操作协议 |
| 语言 | 数据库术语（Field, Data Type, Validation Rule） | 现实世界术语（"工厂"、"供货关系"、"调拨"） |
| 作用范围 | 单一平台内的数据结构 | 跨数据源的语义统一层 |
| 动作建模 | 元数据不包含动作语义（Flow 是独立体系） | Action Type 是元数据的一等公民 |
| AI 集成 | Atlas 引擎读取 Field Description 等隐含语义（可选） | ML 模型输出直接映射为对象属性（建模时强制） |
| 演化方式 | Admin 通过 UI 修改，编译后缓存 | 运行时动态演化，支持分支（类似 Git branching） |
| 上手成本 | 低——点击即可创建对象 | 高——需要领域专家建模 |

### 4.4 一个类比

如果把两者都比作"地图"：

- Salesforce 的元数据像 AutoCAD 工程图纸：精确描述了每个房间的尺寸、材料、管线位置，图纸上可以标注房间用途（Field Description），但标注是可选的。工程图纸的优势是标准化、可量产。
- Palantir 的 Ontology 像一套建筑信息模型（BIM）：不仅标注了每个空间是什么（手术室/会议室/仓库），还定义了使用规则（"手术室每次使用后必须消毒"）和准入策略（"只有授权医护人员可以进入"）。BIM 的代价是需要更多前期投入来建模。

需要注意类比的局限：Salesforce 通过 Flow 和 Agentforce 也能做自动化推荐和操作——它不是一个只能展示数据的静态图纸。但其自动化能力的数据范围受限于 Salesforce 平台内。

两者都是"元数据驱动"的，但驱动的目标完全不同。

---

## 5. 技术深潜 B：Palantir 为什么选择"数据留在客户端"的路线？

这不是一个事后的技术选择，而是被创始场景、客户需求、公司哲学三重约束推导出的结果。

### 5.1 创始场景：情报界的数据不可能出域

Palantir 于 2003 年成立，初始资金来自 In-Q-Tel（CIA 的风投机构）。第一个产品 Gotham（2008 年发布）服务的是美国情报界（IC）和国防部。

在这个场景下，数据出域是物理不可能的：
- 情报数据有 TS/SCI（绝密/敏感隔离信息）分级，不能离开 SCIF（敏感隔离设施）
- 军事数据运行在 air-gapped（物理隔离）网络上，没有互联网连接
- 法律上，ITAR/EAR 出口管制禁止将国防相关数据移到非授权设施

所以 Palantir 从第一天就必须设计成"软件去客户那里，而不是数据来我这里"。这不是选择，是生存前提。

### 5.2 Apollo：让软件部署到任何地方的技术基础

为了支持"软件去客户那里"，Palantir 开发了 Apollo——一套专有的持续交付系统，能把 Foundry/Gotham 部署到公有云（AWS/Azure/GCP）、私有云和本地数据中心、物理隔离的涉密网络、以及边缘设备。

Apollo 管理所有环境的版本升级、配置变更、安全补丁，甚至能在完全断网的环境下工作。这套部署能力是 Palantir 花了十几年积累的壁垒——也是 Salesforce 很难复制 Palantir 模式的原因（Salesforce 的整个架构假设是"所有人连到我的多租户云上"）。

但 Apollo 同时是争议点和护城河：
- **护城河**：深度运维权限 = 极高迁移成本。一旦 Apollo 管理了客户的 CI/CD 管道、版本管理、安全补丁流程，替换成本不仅是应用层的，是运维基础设施层的
- **争议**：Apollo 是闭源专有系统，客户无法独立审计更新内容。这在涉密场景下创造了一个信任假设。欧洲多国对美国公司深度嵌入公共基础设施持谨慎态度——德国等国的 Palantir 项目曾因数据主权争议被限制

### 5.3 公司哲学：数据处理者，不是数据控制者

Palantir 在官方博客中反复强调这一点（[Palantir is Not a Data Company](https://blog.palantir.com/palantir-is-not-a-data-company-palantir-explained-1-a6fcf8b3e4cb)，2025 年 9 月；[Palantir Is Still Not a Data Company](https://blog.palantir.com/palantir-is-still-not-a-data-company-palantir-explained-7-8322d5b38cef)，2025 年 12 月）：

> - Palantir 是数据 processor（处理者），不是数据 controller（控制者）
> - 不收集、不存储、不出售个人数据
> - 不用客户数据训练 AI 模型然后卖给其他客户
> - 每个客户部署是合同、运营、技术上完全隔离的（walled-off）

这不仅是道德姿态，更是商业必需：Palantir 的客户如果发现它在汇集或转售数据，合同会立刻终止。"不碰数据"是 Palantir 能进入最高安全级别场景的门票。

但这个选择也有代价：**客户数据完全隔离意味着 Palantir 无法做跨客户的联邦学习或通用模型训练。** Salesforce 和 ServiceNow 恰恰可以利用多租户环境中汇聚的大规模行为数据来优化 AI 模型——这是 Palantir 架构无法触及的能力路径（详见 §6.2）。

### 5.4 与 Salesforce 的根本对比

| 维度 | Salesforce | Palantir |
|------|-----------|---------|
| 数据存储 | 多租户共享基础设施（数据在 Salesforce 的云里） | 客户独立实例（数据在客户的环境里） |
| 隔离模型 | 逻辑隔离（OrgID 区分，物理共享） | 物理隔离（每个客户独立部署） |
| 部署模式 | 只能 SaaS（连 GovCloud 也是 Salesforce 运营） | SaaS / 私有云 / 本地 / 涉密网络 / 边缘 |
| 数据主权 | 数据在 Salesforce 的基础设施上 | 数据在客户的基础设施上 |
| 核心假设 | "你把数据给我，我帮你管" | "你的数据不动，我把软件送过去" |
| 运维成本 | Salesforce 承担（含在订阅费里） | 客户承担（需专业团队或 Palantir 服务） |
| AI 训练数据 | 多租户数据可用于优化平台 AI 模型 | 客户隔离，无法做跨客户模型训练 |

### 5.5 这个选择如何塑造了 Ontology

"数据留在客户端"这个前提直接推动了 Ontology 成为语义映射层（而非纯数据存储层）的设计方向：

1. 数据分散在客户的几十个系统里 → 需要一个统一的语义映射
2. 客户不允许数据出域 → Ontology 的核心是元数据 + 语义索引（尽管 Foundry 通常也会摄入数据副本到自己的 Dataset 中用于转换和分析）
3. 涉密环境要求细粒度访问控制 → 安全策略成为 Ontology 的横切关注点
4. 部署在隔离网络 → Ontology 必须自包含运行，不依赖外部服务

反观 Salesforce：因为数据在自己这里，它没有同等的动力去建跨系统语义投影层——直接查自己的数据就好了。数据自有 = 语义层的优先级低，数据在外 = 语义层是必需品。这是两条路分叉的技术原点。

---

## 6. 根因的六个下游推论

以下 6 个维度遵循同一模式：两家公司都有看起来类似的能力，但第 3 节的三个根因在每个维度上产生了不同的设计决策。

### 6.1 Low-Code 应用构建：都能拖拽建应用，但应用的"地基"不同

| | Salesforce Lightning | Palantir Workshop |
|---|---|---|
| 表面相似 | 可视化拖拽组件，快速构建业务应用 | 可视化拖拽 Widget，快速构建操作应用 |
| 关键差别 | 组件绑定的是 Salesforce 平台内的记录 | Widget 绑定的是 Ontology 对象（任意业务实体 + 语义链接 + Action） |
| Salesforce 的优势 | 开箱即用的 CRM 组件库 + Industry Cloud 领域模板 + 20 万+ 认证开发者生态 | — |
| Palantir 的优势 | — | 一个界面可同时操作来自 SAP、IoT 传感器、自建数据库的对象 |

**Industry Cloud 的领域本体价值需要重点说明**：Salesforce 的 Industry Cloud 并非"通用 CRM 加壳"，而是包含了深度的行业特定本体：

- **Health Cloud**：内置 ClinicalTrial、CarePlan、MedicalCondition、Patient 等医疗实体，符合 HL7 FHIR R4 标准，与 SNOMED CT / ICD-10 编码系统对齐
- **Financial Services Cloud**：内置 FinancialAccount、RegulatoryBody、AssetAndLiability 等金融实体，参考了 FIBO 等金融行业标准
- **Manufacturing Cloud**：内置 SalesAgreement、RunRate、ProductionProgram 等制造业实体，参考了 ISA-95 等制造业标准
- **Net Zero Cloud**：内置 EmissionSource、CarbonCredit、EnergyUsage 等 ESG 实体，与 GHG Protocol 对齐

这些是 Salesforce 花了数十亿美元收购（Vlocity $13.3 亿）并与行业标准组织合作构建的**已验证的领域本体**。Palantir 的 Ontology 需要每个客户的 FDE 从零建模；Salesforce 的 Industry Cloud 给你一个对齐行业标准的出发点。对于医疗、金融、制造等行业，这个出发点的价值可能远超从零建模的灵活性。

但 Industry Cloud 仍然建立在 UDD 架构之上，数据范围受限于 Salesforce 平台内——它是领域本体，不是跨系统的企业 Ontology。

Pro-Code 层的分叉同样显著：Salesforce 的 Apex + Lightning Web Components 是专有技术栈（技能不可迁移到其他平台）；Palantir 的 OSDK 支持 TypeScript / Python / Java + OpenAPI（标准技术栈，技能完全可迁移）。Palantir 把 OSDK 的 TypeScript 库[开源到了 GitHub](https://github.com/palantir/osdk-ts)。不过，Salesforce 的专有生态也创造了巨大价值——全球超过 20 万名认证 Salesforce 开发者形成了自我强化的人才市场。

### 6.2 AI 集成：都有 AI Agent，但 Agent 的"操作对象"不同

| | Salesforce Agentforce | Palantir AIP |
|---|---|---|
| 表面相似 | AI Agent 能自主执行业务操作 | AI Agent 能自主执行业务操作 |
| 关键差别 | Agent 操作的是 Salesforce 平台内的记录，依赖元数据质量（可选的隐含语义） | Agent 操作的是 Ontology 对象，语义在建模时已强制定义 |
| Salesforce 的优势 | 庞大的存量客户基础可直接升级；多租户数据用于 AI 模型优化；CRM 领域预训练微调带来的实质功能优势 | — |
| Palantir 的优势 | — | AI 提案通过版本控制审核后合并，每个决策有审计轨迹；跨系统数据融合为 AI 提供完整上下文 |

**Salesforce 的训练数据规模优势不应被忽视**：Einstein 系列模型在过去 8 年已经从数亿条 CRM 交互（邮件往来、成单记录、服务工单）中学习到了特定领域的行为模式。Agentforce 对 Salesforce Org 结构（Flow、Apex、Permission Set）的原生理解来自于大量真实 org 配置数据，这让它在处理常见 CRM 任务时的准确率显著高于通用 LLM。这是 Palantir 客户完全隔离部署模型无法获得的规模优势。

Salesforce 的 AI 演进路径更曲折。Einstein（2016）是预测式 ML bolt-on；Agentforce（2024）引入了 Atlas 推理引擎，是一次架构重写。Atlas 比 Einstein 更深地理解 Salesforce 的 Org 结构（自定义对象、Flow、权限），但受限于底层平台的元数据质量——多位分析师指出"Agentforce 的瓶颈不是 LLM 质量，而是元数据质量"。但这个瓶颈的性质值得讨论：**元数据质量是可以工程改善的**（Salesforce 已经在做元数据质量自动改善工具、Prompt Builder + Grounding 机制），而 **Palantir 的 Ontology 建模需要 FDE 驻场数月，这个瓶颈是结构性的**。两种质量保证模式各有取舍：Ontology 是建模时强制的（不建好就无法运行），Salesforce 的语义是可选的（不写描述系统仍可运行，只是 AI 效果差）。

Palantir 的 AIP 是原生长在 Ontology 上的：LLM 直接查询语义对象图谱。AI 提出的变更（如"重新路由 50 批发货"）以 branch 形式存在——人类审核后 merge。需要指出的是，这种 human-in-the-loop 版本控制模式并非 Palantir 独创——LangGraph 的 interrupt/resume、CrewAI 的 human approval step、基于 Temporal/Airflow 的 agentic workflow 都能实现类似模式。Palantir 的差异化在于这套机制与 Ontology 深度绑定，提供了跨企业级的治理保证。

但这种精细的治理模型也意味着更重的操作流程：审核人员需要理解 Ontology 上下文才能做有意义的 merge/reject 决策，当 AI 批量操作涉及数百个对象时面临认知过载。这不适合"让 AI 快速回复客户邮件"这类轻量场景——而这恰恰是 Agentforce 的甜蜜点，也是大多数企业 AI 的优先使用场景。

### 6.3 安全模型：都有细粒度权限，但控制逻辑侧重不同

| | Salesforce | Palantir |
|---|---|---|
| 表面相似 | 对象级、字段级、记录级权限控制 | 对象级、属性级、行级权限控制 |
| 关键差别 | 多层混合模型：RBAC（Profile/Permission Set）+ DAC（Record Ownership）+ 条件授权（Sharing Rules，基于属性的条件共享） | 基于用户属性 vs. 数据属性的动态策略（ABAC + CBAC + PBAC）：运行时比对 |
| 适用场景 | "谁拥有这条记录"——商业场景为主 | "谁有权看这个密级的数据"——情报/国防场景 |

细节差异：
- Salesforce 的权限模型比纯 RBAC 复杂得多：Profile/Permission Set（RBAC 基础）+ Record-Level Ownership（DAC）+ Sharing Rules（基于标准字段的条件授权，已是 ABAC 的子集）+ Dynamic Forms（属性驱动的字段可见性）+ Shield Platform Encryption + Field Audit Trail + Event Monitoring。将其笼统归类为"RBAC"是不准确的
- Salesforce 不支持真正的 cell 级安全（"同一字段在不同记录上对同一用户有不同可见性"），但支持字段级安全（按角色控制某个字段的全局可见性）。这两个精度级别的区别很重要
- Palantir 支持 cell 级安全——Object Security Policy + Property Security Policy 组合实现。还支持 ABAC + RBAC + CBAC（分类控制）+ PBAC（目的控制），且强制标记（Markings）会随数据血缘自动传播
- Salesforce 的 Sharing Rules 只能增加访问权限，不能减少——这是"默认私有、逐步开放"的商业场景设计假设。Palantir 的标记系统则是"密级向下传播"——适合不同密级数据混合存储的场景

两种模型没有绝对优劣。Salesforce 的模型对大多数商业场景够用，管理员学习成本低得多，且 Governor Limits 提供了平台级的硬性安全边界——AI Agent 不可能因为配置失误突破资源限制，这在 AI 时代是有价值的"可预测失败边界"。Palantir 的模型为高安全场景而生，但配置复杂度高出一个量级。

### 6.4 数据管道：都做数据集成，但"谁的活"不同

| | Salesforce | Palantir Foundry |
|---|---|---|
| 表面相似 | 支持连接外部数据源，做数据转换 | 支持连接外部数据源，做数据转换 |
| 关键差别 | 数据集成是外包给合作伙伴的（MuleSoft / 第三方 ETL）；自己做 OLTP，不做 OLAP | 数据集成是平台核心能力：从摄入到转换到 Ontology 映射，全在一个系统内 |
| Salesforce 的优势 | 与 MuleSoft + Data Cloud Zero Copy（基于 Apache Iceberg）组合，不搬数据也能查 | — |
| Palantir 的优势 | — | 全生命周期管道（batch / incremental / streaming），完整数据血缘，版本控制 |

Palantir 的哲学是"原始数据原样摄入，不做外部预处理"——所有转换都在 Foundry 的版本控制管道里发生。2025 年推出的 HyperAuto / SDDI（Software-Defined Data Integration）更进一步，用 AI 自动匹配不同源系统的实体。

Salesforce 的哲学是"尽量少搬数据"——Data Cloud 用 Zero Copy 做联邦查询。这对已有成熟数据仓库的企业更友好（不需要再搬一次数据），但也意味着 Salesforce 对数据质量和血缘的控制力弱于 Foundry。

### 6.5 生态构建：都有生态，但"生态的单元"不同

| | Salesforce | Palantir |
|---|---|---|
| 表面相似 | 有合作伙伴生态和应用市场 | 有合作伙伴生态和联合方案 |
| 关键差别 | 生态单元是 App（AppExchange 上 7000+ 应用，ISV 自助上架） | 生态单元是战略联盟（ISG 评估约 40 家，高接触度联合交付） |
| Salesforce 的优势 | 大多数用户会安装 AppExchange 应用（Salesforce 官方称超过 1000 万次安装）；覆盖 SMB 到大企业 | — |
| Palantir 的优势 | — | 富士通、LG CNS 等深度合资；生态与产品深度绑定 |

Salesforce 的生态飞轮靠数量驱动——据 IDC 估算，其合作伙伴经济规模达数百亿美元。Palantir 的生态飞轮靠深度驱动——每个合作关系都是行业级的深度绑定。两者都有效，但适用的市场完全不同。

Palantir 的生态劣势在于：缺乏自助上架的 marketplace 意味着长尾创新受限。Salesforce 的 AppExchange 上诞生了 Veeva（生命科学 CRM，已独立上市）等成功公司——这种"平台上长出新公司"的现象在 Palantir 生态中还没有出现。

### 6.6 销售动作：都做企业销售，但"证明价值"的方式相反

| | Salesforce | Palantir |
|---|---|---|
| 表面相似 | 面向企业的直销 + 渠道 | 面向企业的直销 + 驻场工程师 |
| 关键差别 | 自助试用 / 引导 Demo → 几周内上线 → 按座位收费 | 5 天 AIP Bootcamp → 用客户真实数据跑出可用工作流 → 按平台收费 |
| Salesforce 的优势 | 低摩擦，几乎任何规模的企业都能开始 | — |
| Palantir 的优势 | — | 用真实数据证明价值 |

Salesforce 的 free trial / guided demo 用的是沙盒数据——客户看到的是"假设你的数据在这里会怎样"。SaaS free trial 的转化率通常远低于此。

Palantir 的 AIP Bootcamp 用的是客户真实数据——第一天接入源系统、构建 Ontology、注入 LLM 上下文；第二天开始跑真实工作流。据公司披露，截至 2024 Q4 已完成超过 1,300 次 Bootcamp，自述转化率约 75%。但需要明确：这两个数字均来自 Palantir 投资者沟通和分析师报告，非第三方审计。RBC 分析师 Rishi Jaluria 对此持明确保留态度："他们说 boot camp 方法更容易上手，但我们的调查中没有看到这一点。"Bootcamp 完成次数不能用来回应"转化率是否真的 75%"的质疑——这是两个不同的指标。

两种销售动作的根本差异：Salesforce 卖的是标准化产品的想象空间，Palantir 卖的是定制化方案的已验证 ROI。前者覆盖面广、边际成本低；后者客单价高、但需要 Palantir 自己的工程资源投入。

---

## 7. 各自的代价：架构优势不等于商业胜利

Palantir 在跨系统融合和高治理 AI 场景拥有更好的架构，但架构优势需要转化为商业规模才有意义。这一节分析两家各自为自己的路径付出的代价。

### 7.1 Palantir 的代价

| 代价 | 具体表现 |
|------|---------|
| 极高的价格 | 业界普遍认为 Palantir 是最贵的企业软件之一。据行业报道和分析师估算，典型商业项目 $1M-$5M/年起（Palantir 不公开标准定价，误差范围可能超过 2-3 倍），中小企业根本无法负担 |
| 漫长的商业化之路 | 2003 年成立，2023 年才开始在商业市场有显著增长。整整 20 年主要依赖政府合同 |
| FDE 模式的规模瓶颈 | 2016 年前 FDE 人数超过产品工程师。每个客户都需要 Palantir 自己的精英工程师驻场，这本质上是一种不可无限复制的资源。AIP Bootcamp 正在缓解但尚未根本解决 |
| Ontology 锁定（比 Apex 锁定更深） | Apex 是代码，代码可以用 Java/Python 重写。但 Ontology 是组织的认知基础设施——整个数据管道、所有 Workshop 应用、所有 Action Type、所有 AI Agent 都建立在同一套 Ontology 命名空间上。迁移一个 Ontology 等于重建整个企业的数字孪生。而且 Ontology 建模知识几乎不可迁移到其他平台——没有"Palantir Ontology 认证考试"，没有活跃的开发者社区 |
| Apollo 的双刃剑 | Apollo 不仅是供应商依赖，更是运维基础设施层锁定。如果 Palantir 停止支持某个部署环境，客户的整个基础设施更新机制会瘫痪。且 Apollo 是闭源系统，客户无法独立审计更新内容 |
| 生态不成熟 | 缺乏自助上架的 marketplace。ISG 2026 年初才开始评估约 40 家生态伙伴，与 Salesforce 的 7000+ AppExchange 应用不可比 |
| 人才市场窄 | 会用 Palantir 的工程师远少于 Salesforce 生态的 20 万+ 认证开发者 |
| 无法利用跨客户数据 | 客户完全隔离的部署模式意味着无法做联邦学习或跨客户模型优化，在 AI 模型训练的规模维度上处于劣势 |
| Ontology 建模的错误成本 | Ontology 建模深度更高意味着建错的代价更高。如果 Ontology 建模不完善，AI 的安全边界可能是空的——不像 Salesforce 的 Governor Limits 提供平台级硬性约束 |

### 7.2 Salesforce 的代价

| 代价 | 具体表现 |
|------|---------|
| 核心元数据范式的局限 | 尽管底层存储已演进到 Hyperforce 混合架构，但核心的 UDD 元数据范式（虚拟表结构 + 可选语义注释）在 AI 时代面临挑战——LLM 需要理解"这个字段在业务上意味着什么"，而核心元数据只保证了 schema 级描述。元数据质量参差不齐是 Agentforce 的实际瓶颈 |
| 收购拼凑 | MuleSoft、Tableau、Slack、Data Cloud 等产品底层架构各不相同，集成仍在进行中。Data Cloud 使用了完全不同于核心平台的技术栈（S3 + DynamoDB）——这既是 Salesforce 能构建新层的证据，也是集成复杂度的来源 |
| 跨系统语义层缺失 | UDD 做 schema 级元数据，Data Cloud 做客户数据统一，Industry Cloud 做领域本体——但缺少一个统一的跨系统操作语义层。这在 AI 需要同时操作 CRM、ERP、IoT 数据时成为瓶颈 |
| CRM 引力 | 每次试图超越 CRM（Data Cloud、Missionforce）都受到华尔街和内部组织的拉力——CRM 座位费仍是收入主体，偏离核心的投入需要持续证明 ROI |
| Apex 锁定 | 专有语言创造了短期粘性但长期限制了开发者池。AI Agent 更容易操作标准 API（REST/OpenAPI）而非专有语言。但 Salesforce 的 Metadata API + Tooling API 是标准化的、文档完整的，且 LLM 预训练数据中包含大量 SOQL/Apex 代码，AI 对 Salesforce 的"理解"反而高于对 Palantir 闭源系统的理解 |
| 数据范围受限 | 核心平台是 OLTP 架构，大规模分析需要外部数据仓库。Data Cloud 的 Zero Copy 是缓解而非解决 |

### 7.3 成本维度对比

这是决策者最关心但技术文章最常忽略的维度：

| | Salesforce | Palantir |
|---|---|---|
| 起步成本 | Platform Starter $25/用户/月，Enterprise $165/用户/月 | 据行业报道，典型商业项目 $1M-$5M/年起（非官方定价） |
| 实施成本 | 合作伙伴生态竞争充分，实施服务费率适中 | FDE 驻场或 Palantir 合作伙伴，费率高 |
| 运维成本 | 含在订阅费内（Salesforce 运维基础设施） | 客户需自行运维（或付费让 Palantir 管理） |
| 规模经济 | 用户越多越便宜（多租户共享） | 用户数量对成本影响有限（独立部署） |
| 适合规模 | 从 5 人团队到 Fortune 500 | 主要服务于 Fortune 500 和政府机构 |

---

## 8. Salesforce 的类 Ontology 尝试及其成果与局限

Salesforce 并非没有意识到语义层的价值。以下四次尝试各有成果，但都未能达到 Palantir Ontology 的跨系统操作语义深度：

### Customer 360 Data Model（2019）

目标：统一跨 Cloud（Sales / Service / Marketing）的客户身份。

成果：确实解决了同一客户在不同 Cloud 中 ID 不一致的问题，建立了 Global Party ID 体系。对于纯 CRM 场景，这是有意义的进步。

局限：只统一了"客户"这一个维度。企业的供应链、财务、生产等实体不在模型范围内。这不是"企业 Ontology"，是"客户 ID 统一"。

### MuleSoft 集成（2018 年 $65 亿收购）

目标：连接任意外部系统和 API。

成果：MuleSoft Anypoint 是市场领先的 iPaaS（集成平台即服务），确实解决了"连接"问题。超过 1,000 个预建连接器，支持 Salesforce 与 SAP、Oracle、自建系统的集成。

局限：MuleSoft 做的是数据管道（移动数据），不是语义层（理解数据）。你可以把 SAP 的数据搬到 Salesforce，但搬完之后两边的"客户"仍然是不同的概念——MuleSoft 不做语义对齐。

### Data Cloud（2022+，前身为 CDP / Customer 360 Audiences）

目标：统一客户数据，支持 AI 和分析。

成果：这是 Salesforce 最接近"语义层"的尝试。Data Cloud 用了完全不同于核心 CRM 的技术栈（微服务架构、S3 存储、DynamoDB、Apache Iceberg），支持 Zero Copy 联邦查询——数据不搬也能用。2024-2025 年开始引入语义数据建模和知识图谱能力，允许在 Customer 360 之外建模 Product、Order、Asset、Location 等非客户实体，目标是构建统一的企业数据语义层。

局限：Data Cloud 正在扩张边界，但其核心仍围绕客户数据统一和激活。它做的是"从 Customer 360 向外扩展的语义层"，而非 Palantir 那样"从企业全域出发的操作语义层"。且 Data Cloud 的信用消耗制（usage-based credits）让成本控制成为新的复杂度来源。

### Agentforce + Data 360 + Missionforce（2025+）

目标：超越 CRM，成为企业级 AI Agent 平台和政府/国防市场玩家。

成果：Agentforce 的 Atlas 推理引擎比 Einstein 更深地理解 Org 结构。Missionforce 业务单元直接对标 Palantir 进军国防。Salesforce 工程博客明确说目标是"Beyond CRM"。

局限：仍处于早期。核心张力未解——要支撑政府/国防客户的数据主权要求，就需要从根本上改变多租户 SaaS 的部署模式。而这会动摇 Salesforce 最大的架构优势。但 Data Cloud 用全新技术栈构建这一事实本身说明：**Salesforce 有能力在核心平台之外构建新的技术层——"架构基因锁定"不是技术不可能，而是优先级和激励结构问题。**

每一次尝试都受限于同一个根本张力：Salesforce 的收入主体来自 CRM 座位费，大幅偏离 CRM 核心需要极大的战略决心和耐心——而华尔街每个季度都在看财报。但 SAP 从专有 ERP 转向 HANA 再转向 S/4HANA 云的历程表明，遗留架构并不必然是致命约束——只是贵，而 Salesforce 不缺资本。

---

## 9. 竞争格局观察

2025-2026 年两家开始正面碰撞：
- Salesforce 成立 Missionforce 进军国防领域，直接对标 Palantir
- Palantir 市值（~$420B）已超过 Salesforce（~$230B），尽管收入只有后者的约 1/10。但市值差异主要反映的是增长预期、AI 叙事溢价和投资者情绪（PLTR 市盈率超过 200 倍，散户持仓比例约 25-30%），不宜简单解读为"市场对架构优劣的技术投票"
- 两家都在 AI Agent 上押重注：Salesforce 的 Agentforce vs. Palantir 的 AIP

从架构角度看两家的演进方向：
- Salesforce 在核心 CRM 平台之外构建新层的能力已被证明（Data Cloud 全新技术栈、Industry Cloud 领域本体）。但要做到 enterprise-wide 的跨系统操作语义层，需要解决"如何统一 CRM 核心、Data Cloud、Industry Cloud、MuleSoft 各自独立的数据模型"这个整合问题——这是工程挑战，不是不可能
- Palantir 则在加速补短板：AIP Bootcamp 把销售周期从一年压缩到 5 天；OSDK 开源降低开发者门槛；与富士通、LG CNS 的合资扩大分发渠道

Salesforce 有一张 Palantir 短期内无法复制的牌：15 万家现成客户 + 多租户训练数据。如果 Agentforce 能在这些存量客户中快速铺开——即使技术架构不如 AIP 深——纯粹的规模效应和 CRM 领域预训练优势可能让它在有界 CRM 场景中成为更务实的选择。

**对大多数企业来说，AI 落地的最大障碍不是语义层深度，而是更基础的问题**：数据质量（重复记录、空字段、格式不一致等普遍存在的数据治理欠账）、用户采纳（用户已建立在 Salesforce UI 上的工作习惯和肌肉记忆）、合规与可审计性（监管机构需要标准化审计报告，不是分布式语义安全策略）。在这些维度上，Salesforce 的优势是实质性的。

**第三条路径值得更多关注**：Snowflake / Databricks / Microsoft Fabric 在数据湖上加语义层，配合开源知识图谱（Neo4j、Amazon Neptune）和语义层工具（dbt Semantic Layer、Cube），可以用远低于 Palantir 的成本构建跨系统语义能力。它们目前缺少 Palantir Ontology 的操作层（Action Type + 治理）和深度安全策略，更接近"加强版数据目录"。但 Microsoft 的 Fabric + Copilot Studio + Azure OpenAI 组合正在快速填补这些空缺，且其在 Fortune 500 的渗透率远高于 Palantir——这可能是对 Palantir 最大的竞争威胁。

---

## 10. 启示

### 对本文论点的总结

**在需要跨系统数据融合、高安全治理、操作语义建模的场景下**，Palantir 的 Ontology 是更好的企业架构。这个判断基于三个技术事实：（1）结构化的语义对象图谱为 AI 推理提供了确定性保证（在高安全、高治理场景下，这种确定性是 RAG + 知识图谱等替代方案难以达到的）；（2）受治理的 Action Type 让 AI 可以安全地执行跨系统操作；（3）跨系统数据融合为 AI 提供了完整上下文。

但在 CRM 主导、有界操作、快速上线的场景下——这覆盖了绝大多数企业的 AI 优先需求——Salesforce 的平台有独立的、实质性的优势：规模化的训练数据、Industry Cloud 领域本体、低实施摩擦、已验证的合规框架、以及 15 万家客户建立的工作习惯。

Salesforce 正在向 Ontology 方向追赶——Data Cloud 语义建模、Missionforce 进军国防、"Beyond CRM" 战略宣示都是证据。但三重锁定（架构范式、客户画像、商业模式）意味着它只能从 CRM 核心向外渐进扩展，而非像 Palantir 那样从企业全域自顶向下建模。收敛方向是单向的：Salesforce 在向 Palantir 靠拢，Palantir 没有在向 CRM 平台靠拢——这本身就是市场对两种架构路径的方向性验证。

### 对做企业软件的人的教训

1. **"谁拥有数据"是最重要的架构假设。** 这个隐含假设决定了整个架构的进化方向，且一旦选定很难改变。

2. **商业模式是最强的架构约束。** per-seat SaaS 和平台部署费产生了完全不同的产品优化函数，每一个下游技术选择都被商业模式的引力场拉向不同方向。

3. **前 10 个客户定义了产品 DNA。** Salesforce 的早期客户是中小企业销售团队 → 一切围绕"记录"；Palantir 的早期客户是情报机构 → 一切围绕"数据主权"。之后很难改变。

4. **AI 放大了架构差异的后果。** 20 年前"够用"的架构假设（可选的语义注释、单一平台数据、所有权 RBAC）在 AI 需要跨系统操作时暴露出局限。结构化的语义层在高治理场景下提供了 AI Agent 所需的确定性保证——但这不等于"没有 Ontology 就不能跑 AI"（GPT-4/Claude 每天在没有 Ontology 的系统上执行大量任务）。

5. **"元数据驱动"是一个谱系。** 同一个技术标签下可以是完全不同的产品——Salesforce 用元数据驱动虚拟数据库（schema 级），Palantir 用元数据驱动操作语义（业务知识级）。只看标签会被误导。

6. **架构优势 ≠ 商业胜利，但特定场景下时间站在更好架构一边。** Palantir 用了 20 年才开始在商业市场爆发，而 Salesforce 同期建成了全球最大的企业软件生态。在跨系统融合场景中，架构精度的重要性正在上升；在有界 CRM 场景中，生态规模和实施便利性仍然是决定性因素。"最好的架构"取决于你在哪个战场。

---

## Sources

### Palantir 官方文档
- [Palantir Ontology Overview](https://www.palantir.com/docs/foundry/ontology/overview)
- [Palantir Ontology Architecture](https://www.palantir.com/docs/foundry/architecture-center/ontology-system)
- [Palantir: Why Create an Ontology?](https://www.palantir.com/docs/foundry/ontology/why-ontology)
- [Palantir Ontology Core Concepts](https://www.palantir.com/docs/foundry/ontology/core-concepts)
- [Palantir Data Connection Architecture](https://www.palantir.com/docs/foundry/data-connection/architecture)
- [Palantir Platform Architecture Overview](https://www.palantir.com/docs/foundry/platform-overview/architecture)
- [Palantir Open Architecture](https://www.palantir.com/platforms/foundry/open-architecture/)
- [Palantir AIP Overview](https://www.palantir.com/docs/foundry/aip/overview)
- [Palantir AIP Architecture Overview](https://www.palantir.com/docs/foundry/architecture-center/aip-architecture)
- [Palantir AIP Agent Studio Overview](https://www.palantir.com/docs/foundry/agent-studio/overview)
- [Palantir AIP Security and Privacy](https://www.palantir.com/docs/foundry/aip/aip-security)
- [Palantir Privacy and Security Statement](https://www.palantir.com/privacy-and-security/)
- [Palantir Security Overview](https://www.palantir.com/docs/foundry/security/overview)
- [Palantir Object Security Policies](https://www.palantir.com/docs/foundry/object-permissioning/object-security-policies)
- [Palantir Granular Policies](https://www.palantir.com/docs/foundry/platform-security-management/manage-granular-policies)
- [Palantir Workshop Overview](https://www.palantir.com/docs/foundry/workshop/overview)
- [Palantir OSDK Overview](https://www.palantir.com/docs/foundry/ontology-sdk/overview)
- [Palantir Data Integration Overview](https://www.palantir.com/docs/foundry/data-integration/overview)
- [Palantir AIP Bootcamp](https://www.palantir.com/platforms/aip/bootcamp/)

### Palantir 官方博客
- [Palantir is Not a Data Company (Palantir Explained #1)](https://blog.palantir.com/palantir-is-not-a-data-company-palantir-explained-1-a6fcf8b3e4cb)
- [Palantir Is Still Not a Data Company (Palantir Explained #7)](https://blog.palantir.com/palantir-is-still-not-a-data-company-palantir-explained-7-8322d5b38cef)
- [Palantir: Frequently Asked Questions](https://blog.palantir.com/about-palantir-ddddb78aec29)
- [Ontology-Oriented Software Development](https://blog.palantir.com/ontology-oriented-software-development-68d7353fdb12)
- [Ontology: Finding Meaning in Data](https://blog.palantir.com/ontology-finding-meaning-in-data-palantir-rfx-blog-series-1-399bd1a5971b)
- [Deploying Full Spectrum AI in Days: How AIP Bootcamps Work](https://blog.palantir.com/deploying-full-spectrum-ai-in-days-how-aip-bootcamps-work-21829ec8d560)

### Salesforce 官方文档
- [Salesforce Platform Multitenant Architecture](https://architect.salesforce.com/fundamentals/platform-multitenant-architecture)
- [Salesforce Multi Tenant Architecture (Developer Wiki)](https://developer.salesforce.com/ja/wiki/multi_tenant_architecture)
- [The Force.com Multitenant Architecture Whitepaper (PDF)](https://www.developerforce.com/media/ForcedotcomBookLibrary/Force.com_Multitenancy_WP_101508.pdf)
- [Metadata-Driven Architectures (O'Reilly)](https://www.oreilly.com/library/view/the-forcecom-multitenant/30000LTI00089/30000LTI00089_ch05.html)
- [Salesforce Data Security Model Explained Visually](https://developer.salesforce.com/blogs/developer-relations/2017/04/salesforce-data-security-model-explained-visually)
- [Beyond CRM: Engineering an Enterprise Agent Platform](https://engineering.salesforce.com/beyond-crm-how-salesforce-engineered-an-enterprise-agent-platform-for-any-workload/)
- [Salesforce Data Cloud Model Explained](https://www.cloudkettle.com/blog/salesforce-data-cloud-model-explained/)
- [Salesforce Data Cloud: 10 Things You Should Know](https://www.salesforceben.com/salesforce-data-cloud-things-you-should-know-before-you-enable-it/)
- [Why Do Salesforce Data Cloud Implementations Fail?](https://www.salesforceben.com/why-do-salesforce-data-cloud-implementations-fail/)
- [Salesforce Data Cloud Zero Copy Connectivity](https://www.salesforce.com/data/connectivity/zero-copy/)
- [Salesforce Agentforce vs Einstein Architecture (Sweep)](https://www.sweep.io/blog/agentforce-vs-einstein-copilot/)
- [Atlas Reasoning Engine vs Einstein (Vectr Solutions)](https://vectrsolutions.com/thought-leadership/atlas-reasoning-engine-vs-einstein/)

### 分析与对比
- [Understanding Palantir's Ontology: Semantic, Kinetic, and Dynamic Layers](https://pythonebasta.medium.com/understanding-palantirs-ontology-semantic-kinetic-and-dynamic-layers-explained-c1c25b39ea3c) — 注：三层分析框架来自此第三方博文，非 Palantir 官方术语
- [Palantir's Ontology vs Kimball's Star Schema - Comparative View](https://medium.com/business-friendly-data-modeling/palantirs-ontology-kimball-s-star-schema-and-model-driven-data-engineering-a-comparative-view-8b175464c42a)
- [Beyond Palantir's Ontology: The Path to Open Semantics](https://medium.com/towards-data-engineering/beyond-palantirs-ontology-the-paradigm-the-platform-and-the-path-to-open-semantics-f8e8b3b5fe93)
- [Shifting the Enterprise Ontology Paradigm](https://blog.pebblous.ai/project/CURK/ontology/enterprise-ontology-paradigm/en/)
- [Palantir's Secret Weapon Isn't AI - It's Ontology (DEV Community)](https://dev.to/s3atoshi_leading_ai/palantirs-secret-weapon-isnt-ai-its-ontology-heres-why-engineers-should-care-kk8) — 注：Palantir 爱好者向内容，非中立来源
- [Forward Deployed Engineers (Pragmatic Engineer)](https://newsletter.pragmaticengineer.com/p/forward-deployed-engineers)
- [Palantir: Inside the Category of One - FDEs (Everest Group)](https://www.everestgrp.com/palantir-inside-the-category-of-one-forward-deployed-software-engineers-blog/)
- [The Palantirization of Everything - a16z](https://a16z.com/the-palantirization-of-everything/)
- [Palantir Explained Like It's Software](https://tim.kicker.dev/2025/09/28/palantir-what/)
- [Salesforce vs Palantir: The AI Government Battle](https://www.salesforceben.com/salesforce-vs-palantir-the-ai-government-battle/)
- [Palantir is Now Worth More Than Salesforce - SaaStr](https://www.saastr.com/palantir-is-now-worth-more-420b-than-salesforce-230b-with-1-10th-the-revenue-does-this-make-sense-it-might/)
- [Palantir's AI Strategy: Path to AI Dominance](https://www.klover.ai/palantir-ai-strategy-path-to-ai-dominance-from-defense-to-enterprise/)
- [Inside Palantir's AI Sales Secret Weapon (Bloomberg)](https://finance.yahoo.com/news/inside-palantir-ai-sales-secret-110015454.html)
- [ISG to Assess Palantir Ecosystem Partners](https://www.businesswire.com/news/home/20260220605851/en/ISG-to-Assess-Palantir-Ecosystem-Partners)
- [Salesforce Database Architecture: A Multi-Tenant Deep Dive](https://cirra.ai/articles/salesforce-database-architecture-explained)
- [OSDK TypeScript Libraries (GitHub)](https://github.com/palantir/osdk-ts)
- [Palantir Slate vs Workshop vs OSDK](https://chanonroy.medium.com/palantir-slate-vs-workshop-vs-osdk-2467028567a8)
