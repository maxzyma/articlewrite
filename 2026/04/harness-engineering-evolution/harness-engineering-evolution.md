---
title: "Harness Engineering 概念演化史——从 Cognitive Architecture 到百万行零手写代码"
author: Mazy
description: 追溯 harness engineering 的四次命名演变，交叉分析 30 篇信源中的共识与分歧，用三组生产实证三角验证，并补上被忽视的安全维度。
cover: ./cover.png
created: 2026-04-14
published: {}
---

## 引言：一个概念的 22 个月

2024 年 6 月，Harrison Chase 在红杉的播客里说，agent 需要 "custom cognitive architecture"。22 个月后的 2026 年 4 月，Microsoft 公布了一个处理 35,000+ 事件的 SRE Agent，平均修复时间从 40.5 小时压到 3 分钟。

这 22 个月里发生了什么？

一个概念经历了四次命名——cognitive architecture、agentic systems、agent harness、harness engineering——每次改名都不是文字游戏，而是工程实践推动的认知升级。但这段演化史没有人系统写过。业界现有的 harness engineering 文章要么是入门解释，要么是单一视角的实践复盘，缺少一件事：**把 30+ 篇分散在不同时间线上的信源拉到一张图里看**。

本文基于对 30 篇原始信源 + 4 篇前置信源的系统精读，做三件事：

1. **追溯概念谱系**——谁在什么时间点、基于什么实践，给了这个概念一个新名字
2. **三角验证生产实证**——OpenAI 绿地百万行、Microsoft brownfield 35K 事件、LangChain benchmark +13.7pp，三组独立数据讲同一个故事
3. **补上安全维度**——OWASP 十大 agentic 风险、NVIDIA 开源 sandbox、Anthropic 分层防御，这些在多数 harness engineering 讨论中缺席

> **信源说明**：文中 `[#N]` 对应文末信源索引编号。所有引文来自原文，非转述。

---

## 一、四次命名：概念谱系学

### 第一次：Cognitive Architecture（2024-06）

故事从红杉资本开始。2024 年 6 月 18 日，Sonya Huang 和 Pat Grady 发布了一篇名为 *"Goldilocks" Agents* 的文章 [#1]，配合同日上线的 Harrison Chase 播客访谈 [#2]。核心观点是：AutoGPT 类完全自主 agent 失败了，因为它们 *"too general and unconstrained to match our expectations"*。可靠的 agent 处于"金发姑娘区间"——有状态、有护栏，但不完全自主。

两周后，Chase 在 LangChain 博客给出了正式定义 [#3]：**Cognitive Architecture = 代码、提示词和 LLM 调用的流程设计**，决定 AI 系统如何"思考"。他画了一个六级自主性分类——从 Hard-coded code（Level 1）到 Autonomous agent（Level 6）——本质上是一个 **harness 紧度光谱**：Level 1 是最紧的 harness，Level 6 是无 harness。

Chase 同月的第二篇文章 [#4] 更进一步，把 agent 系统拆成两层：

- **Agentic infrastructure**（可外包）：持久化、队列、后台执行——*"does not make your beer taste better"*
- **Cognitive architecture**（必须自建）：决策逻辑和控制流——*"absolutely makes your beer taste better"*

这个区分至关重要。它预示了后来 harness 内部的分层——runtime（执行环境）和 control（决策逻辑）。

> 此时的关键词：custom cognitive architecture, orchestration layer, Goldilocks zone

### 第二次：Agentic Systems（2024-12）

2024 年 12 月 19 日，Anthropic 发布了 *Building Effective Agents* [#6]。这篇文章**没有使用 "harness" 一词**——用的是 "orchestrated"、"framework"、"agentic systems"。但它做了一件后来被反复引用的事：把 agent 系统分为 workflow（预定义代码路径编排 LLM）和 agent（LLM 动态控制流程），并给出 7 个从简单到复杂的 composable patterns。

Anthropic 还在这篇文章中提出了 ACI（Agent-Computer Interface）概念——*"Think about how much effort goes into human-computer interfaces (HCI), and plan to invest just as much effort in creating good agent-computer interfaces."*

这是一个微妙但关键的转折。Chase 强调的是人类工程师如何设计 agent 的"思考方式"（cognitive architecture）。Anthropic 强调的是 agent 如何与计算机环境交互（ACI）。**视角从 agent 内部转向了 agent 与环境的接口。** 而 "harness" 这个词，本质上就是对这个接口的工程化。

> 此时的关键词：workflow vs agent, composable patterns, ACI

### 第三次：Agent Harness（2026-01）

2025 年 12 月 31 日，Phil Schmid 在年终预测中写下：*"Agent Harnesses become the new moat for AI Labs"* [#7]。一周后的 2026 年 1 月 5 日，他发布了 Agent Harness 的首篇系统性定义 [#8]，给出了一个被广泛引用的类比：

**Model = CPU，Context Window = RAM，Agent Harness = OS，Agent = App**

这不只是比喻。它暗示了一个架构命题：正如操作系统抽象了硬件细节让应用可移植，harness 应该抽象模型细节让 agent 逻辑可在不同模型间迁移。Schmid 同时引入了 **"build to delete"** 原则——引用 Bitter Lesson：手工编码的 agent 逻辑总会被下一代模型淘汰，所以 harness 必须轻量、模块化，随时可拆。

两天后，Aakash Gupta 用更直白的语言推广了这个概念 [#9]：*"Model as engine, harness as car. Best engine without steering and brakes goes nowhere useful."* 他还给出了 harness 的六组件分类：Human-in-the-loop 控制、文件系统访问、工具调用编排、子 agent 协调、Prompt 预设管理、生命周期 hooks。

2026 年 1 月是一个**多声部爆发期**。在 Schmid/Gupta 定义 harness 的同一个月：

- Anthropic 正式区分了 evaluation harness 和 agent harness [#10]，并用数据证明 context files 让 agent 错误率降 40%、完成速度提升 55% [#11]
- OpenAI 发布了 Codex agent loop 的详细拆解 [#12]——这是一个具体 harness 实现的解剖
- Chase 在红杉第二次播客中说出了关键转折 [#13]：*"at some point in 2025, the models got good enough, and that's when we moved from scaffolds to harnesses"*
- Anthropic 发布了 Claude Agent SDK [#14]——这是 harness 的实现蓝图

Chase 在 [#13] 中还给出了一个三层分类：Models = tokens in/out，Frameworks = 无观点的抽象，**Harnesses = "batteries included" 有观点的实现**。这个分类精确地解释了为什么从 "scaffold" 到 "harness" 不是换个词——scaffold 是支撑结构，可以拆掉；harness 是驾驭系统，是运行时的一部分。

> 此时的关键词：Model=CPU / Harness=OS, build to delete, scaffolds → harnesses, context engineering

### 第四次：Harness Engineering（2026-02）

2026 年 2 月 5 日，Mitchell Hashimoto（HashiCorp 联合创始人）在一篇记录自己 AI 采用旅程的文章中，**首次命名了 "Harness Engineering"** [#17]：

> *"Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again."*

Hashimoto 把自己的旅程分为六个阶段：Drop the Chatbot → Reproduce Your Own Work → End-of-Day Agents → Outsource the Slam Dunks → **Engineer the Harness** → Always Have an Agent Running。第五阶段就是 harness engineering：不再容忍 agent 重复犯错，而是系统性地把每次错误转化为工程化的预防措施。

他给出了两种具体实践：**AGENTS.md**（隐式 prompting——用文档约束 agent 行为）和 **Programmed Tools**（编程化工具——用代码消除 agent 的自主决策空间）。

六天后，OpenAI 发布了一篇让所有人侧目的实验报告 [#19]：**3 人团队，5 个月，~100 万行代码，0 行手写，~1,500 个 PR，人均 3.5 PR/天**。他们不只用了 harness engineering，而是提出了 10 个系统实践：

1. Zero manual code（所有代码由 Codex 生成）
2. Depth-first decomposition（纵向分解任务）
3. Agent-to-agent review（agent 互审代码）
4. Application legibility（让代码对 agent 可读）
5. Repo as system of record（仓库即真相源）
6. Progressive disclosure（渐进式披露信息）
7. Mechanical enforcement（机械式强制执行规则）
8. Golden principles + GC（黄金原则 + 代码垃圾回收）
9. Doc-gardening agent（文档维护 agent）
10. Promote rule into code（从文档规则升级为代码约束）

他们也坦诚了早期失败：环境规范不足、"One big AGENTS.md" 导致信息过载、Pattern drift 无法靠人工清理。正是这些失败推动了上述 10 个实践的产生。

> *"Humans steer. Agents execute."* [#19]

从 cognitive architecture 到 harness engineering，每次命名变迁都有一个推动力：

| 命名 | 时间 | 推动力 |
|------|------|--------|
| Cognitive Architecture | 2024-06 | AutoGPT 失败，需要描述"有约束的 agent 设计" |
| Agentic Systems | 2024-12 | 视角从 agent 内部逻辑转向 agent 与环境的接口 |
| Agent Harness | 2026-01 | 模型能力跨过阈值，"脚手架"变成"驾驭系统" |
| Harness Engineering | 2026-02 | 从概念进入工程实践，需要一个学科名称 |

---

## 二、三组生产实证

概念演化到最后必须落地。2026 年 2-4 月，三组独立团队各自提供了 harness engineering 的生产数据。它们的价值不在于任何单独一组，而在于三角验证——不同场景、不同度量、不同团队，讲同一个故事。

### 实证 A：OpenAI 百万行绿地实验

**场景**：纯绿地项目，从零开始用 Codex 构建一个完整应用

**数据** [#19]：

| 指标 | 数值 |
|------|------|
| 手写代码行数 | 0 |
| 总代码行数 | ~100 万 |
| 时间跨度 | 5 个月 |
| 团队规模 | 3→7 人 |
| PR 总数 | ~1,500 |
| 人均 PR/天 | 3.5 |

**工程师做什么**：设计 harness（AGENTS.md、自定义工具、架构约束、垃圾回收规则），而非写代码。OpenAI 的总结：*"Give Codex a map, not a 1,000-page instruction manual."*

**局限性**（来自 Böckeler 的批判 [#20]）：纯绿地、无存量代码、团队拥有 Codex 全量能力、5 个月投入并非"快速启动"、缺乏行为测试证据。

### 实证 B：Microsoft Azure SRE Brownfield 案例

**场景**：存量生产系统的 SRE 运维——brownfield，35,000+ 真实事件

**数据** [#30]：

| 指标 | 数值 |
|------|------|
| 自主处理事件数 | 35,000+ |
| 平均修复时间 | 40.5h → 3min |
| 节省开发者工时 | 50,000+ 小时 |
| Agent 部署数量 | 1,300+ |
| 事件覆盖 RCA 率 | >90% |
| 工程师正面反馈 | 89% |

**关键演进**：这个案例有三篇前置文章记录了概念演进链：

1. **Context Engineering 阶段**：团队最初构建了 100+ 专用工具（bespoke tools），结果失败。转向 2-3 个宽泛工具 + 文件系统后，Intent Met 从 45% 跳到 75%。原文：*"We thought we were building an SRE agent. In reality, we were building a context engineering system that happens to do Site Reliability Engineering."*
2. **Harness Engineering 阶段**：突破来自**移除** scaffolding——*"Every prewritten query was a place we told the model not to think."* 预写的查询反而限制了模型的推理能力。
3. **Building Agents with Agents**：Agent 嵌入 SDLC 每个阶段（Plan/Code/Verify/Deploy/Operate），并有专用实例来维护自身。

**为什么重要**：Böckeler [#20] 明确质疑过 harness engineering 在存量代码中的适用性。Azure SRE 案例直接提供了 brownfield 证据——虽然仅限 SRE 领域，但它证明 harness engineering 不只在"从零开始"时有效。

### 实证 C：LangChain Benchmark 实验

**场景**：Terminal-Bench 2.0 coding benchmark，固定模型，只改 harness

**数据** [#21]：

| 指标 | 数值 |
|------|------|
| 模型 | gpt-5.2-codex（固定不变） |
| 改前排名 | Top 30 |
| 改后排名 | Top 5 |
| 通过率提升 | 52.8% → 66.5%（+13.7pp） |

**方法**：
- **Self-verification**：agent 天然缺乏自发的 build-verify loop，harness 需显式注入验证步骤
- **Reasoning sandwich**：xhigh-high-xhigh 推理模式分配——规划阶段用最高推理、执行阶段降级、验证阶段再拉回最高
- **Trace Analyzer Skill**：自动抓取实验 traces → 并行 error analysis agents → 综合改进建议

LangChain 的定义最为精准 [#21]：*"The purpose of the harness engineer: prepare and deliver context so agents can autonomously complete work."*

### 三角验证

三组数据指向同一个结论，但各有侧重：

| 维度 | OpenAI [#19] | Microsoft [#30] | LangChain [#21] |
|------|-------------|-----------------|-----------------|
| 场景 | 绿地开发 | Brownfield 运维 | Benchmark 竞赛 |
| 度量 | 生产效率 | 修复时间 | 通过率 |
| 控制变量 | 0 手写 vs 传统开发 | 有/无 agent | 同模型，变 harness |
| 核心发现 | 人变成 harness 设计者 | 移除 scaffolding 才突破 | +13.7pp 纯 harness 收益 |
| Anthropic 补充 | — | — | infra noise 6pp [#18] |

Anthropic 的 infra noise 研究 [#18] 为 LangChain 的实验提供了重要补充：同一模型、同一 harness、同一任务集，仅改变基础设施配置（CPU、RAM、时间限制），benchmark 分数差异达 6 个百分点。这意味着 **benchmark 排行榜可能在混淆模型能力和基础设施行为**。正如 Anthropic 所说：*"A few-point lead might signal a real capability gap -- or it might just be a bigger VM."*

---

## 三、五项共识与四项分歧

30 篇信源来自不同组织、不同利益立场，但在某些点上高度一致，在另一些点上明确对立。两者同样重要——共识告诉你什么是可靠的，分歧告诉你什么还没定论。

### 五项共识

**共识 1：Model 不是瓶颈，环境是**

这是最强的共识。几乎每篇文章都在说同一件事，只是用词不同：

- Anthropic：*"simple patterns"* [#6] → harness 配置影响 6pp [#18]
- Schmid：*"OS not CPU"* [#8]
- Hashimoto：*"engineer the harness"* [#17]
- OpenAI：*"environment was underspecified"* [#19]
- LangChain：同模型 +13.7pp [#21]
- Microsoft：TTM 40.5h→3min [#30]
- LangChain Survey：质量（32%）超过安全（24.9%）成为 agent 投产第一障碍

**共识 2：约束产生速度**

反直觉但一致：给 agent 更多自由度不会让它更快，反而更慢。

- Sequoia：Goldilocks zone [#1]
- Chase：domain-specific > general-purpose [#5]
- OpenAI：rigid layered architecture [#19]
- Böckeler：*"constraining the solution space"* [#20]
- Red Hat：*"structure in, structure out"* [#28]

**共识 3：文档即代码**

Agent 世界里，文档不再是"给人看的注释"，而是"给 agent 看的指令"。

- Hashimoto：AGENTS.md = 隐式 prompting [#17]
- OpenAI：repo as system of record [#19]
- Anthropic：ACI [#6]
- Chase：file system as critical infrastructure [#13]

**共识 4：反馈循环 > 一次性正确**

没有人相信能一次写对 harness，分歧在于如何迭代。

- OpenAI：*"corrections are cheap"* [#19]
- Schmid：build to delete [#8]
- Böckeler：garbage collection [#20]
- LangChain：self-verification [#21]
- Microsoft SRE：self-improvement loop [#30]

**共识 5：Harness 是竞争壁垒**

- Chase：*"own your cognitive architecture"* [#4]
- Schmid：*"new moat"* [#7]
- Gupta：*"model is commodity, harness is moat"* [#9]
- Mollick：*"same model, different harness = different capability"* [#22]
- LangChain Survey：57.3% 已投产，行业进入壁垒阶段

### 四项分歧

**分歧 1：Harness 该多重？**

| 轻量派 | 重投入派 |
|--------|---------|
| Schmid：build to delete [#8] | OpenAI：5 个月构建 [#19] |
| Willison：几十行代码 [#25] | LangChain：trace analyzer 系统 [#21] |
| Microsoft SRE：*"removing scaffolding was the breakthrough"* | Anthropic：生产级三层解耦架构 [#15] |

两派并不矛盾——轻量派说的是单个 harness 组件，重投入派说的是 harness 工程体系。但这个区分在讨论中经常被混淆。

**分歧 2：人该站在哪里？**

| On the loop | Out of the loop |
|-------------|-----------------|
| Morris：人设计 Why Loop，agent 执行 How Loop [#23] | OpenAI：agent-to-agent review，人只在最终 merge [#19] |
| Böckeler：*"relocating rigor"* 到环境设计 [#20] | Microsoft SRE：agent 调查自己的 bug |

Morris 的 Why/How Loop 模型 [#23] 提供了最清晰的框架：人关心"为什么做"（想法 ↔ 可工作的软件），agent 处理"怎么做"（规格 → 代码 → 测试）。但 OpenAI 的实践显示，即使 "怎么做" 的审查环节也可以 agent-to-agent，人类只在最终关口介入。

**分歧 3：Brownfield 可行性**

| 已验证 | 存疑 |
|--------|------|
| Microsoft Azure SRE：35K 生产事件 [#30] | Böckeler：明确质疑存量代码适用性 [#20] |

Azure SRE 案例提供了 brownfield 证据，但仅限 SRE 领域。产品开发类 brownfield（比如在一个 10 年历史的 Rails 代码库上做 harness engineering）仍无实证。

**分歧 4：安全模型——嵌入还是外挂？**

| 嵌入 harness | 外挂治理 |
|-------------|---------|
| Anthropic：四组件模型，安全属性分布在 Model/Harness/Tools/Environment [#29] | Microsoft：独立 Agent Governance Toolkit [#27] |
| NVIDIA：out-of-process 策略执行 [#26] | OWASP：风险分类框架，不规定实现方式 |

Anthropic 主张安全是 harness 的固有属性，不可外分。Microsoft 主张安全层应该独立于框架，支持 20+ 框架即插即用。NVIDIA 的 OpenShell 取了一个中间位置——进程外执行但与 agent 紧耦合。

---

## 四、被低估的安全维度

多数 harness engineering 讨论聚焦效率和可靠性，安全是后补的章节。但三组信源表明，安全不是 harness 的可选插件，而是设计约束。

### OWASP：十大 Agentic 风险

OWASP 在 2025 年 12 月发布了 *Top 10 for Agentic Applications 2026*，由 100+ 安全研究者参与。十项风险中，至少六项直接涉及 harness 设计：

| ID | 风险 | 与 Harness 的关系 |
|----|------|------------------|
| ASI01 | Agent Goal Hijack | Harness 的 prompt 注入防御 |
| ASI02 | Tool Misuse & Exploitation | Harness 的工具权限管理 |
| ASI03 | Agent Identity & Privilege Abuse | Harness 的身份和委托模型 |
| ASI05 | Unexpected Code Execution | Harness 的 sandbox 设计 |
| ASI06 | Memory & Context Poisoning | Harness 的 context 管理策略 |
| ASI08 | Cascading Agent Failures | Harness 的多 agent 隔离和熔断 |

OWASP 提出的核心设计原则是 **"principle of least agency"**——不给 agent 超过业务问题所需的自主权。这与 Sequoia 的 Goldilocks zone [#1] 一脉相承，但从安全视角重新论证。

### NVIDIA OpenShell：独立安全执行层

NVIDIA 的 OpenShell [#26] 是目前唯一的 agent-agnostic 开源运行时安全方案。四个关键组件：

- **Sandbox**：K3s in Docker 内核级隔离
- **Policy Engine**：YAML 声明式策略，denial-by-default
- **Privacy Router**：敏感 context 路由到本地模型
- **Credential Management**：运行时 env var 注入，凭证不落盘

OpenShell 的设计哲学——*"Every prompt injection is a potential credential leak"*——与 Anthropic Managed Agents [#15] 的安全边界设计互补：Anthropic 在架构层把凭证从 sandbox 中分离出去，OpenShell 在运行时层确保凭证不落盘。

### Anthropic："Defenses at Every Level"

Anthropic 在 *Trustworthy agents in practice* [#29] 中给出了最完整的安全框架。核心论点是：**大多数监管关注点聚焦模型，但这是不完整的。** Agent 行为取决于四个组件协同工作——Model / Harness / Tools / Environment——任何单一组件的安全保证都不够。

> *"Prompt injection illustrates a more general truth about agentic security: it requires defenses at every level."* [#29]

Anthropic 还给出了权限三级模型：always allow / needs approval / block。并将 MCP 捐赠给 Linux Foundation——把安全属性嵌入基础设施标准而非私有实现。

Microsoft 的 Agent Governance Toolkit [#27] 从另一端切入：覆盖 OWASP 全部十项风险、<0.1ms p99 策略执行（比 LLM API 调用快约 10,000 倍）、支持 20+ 框架、MIT 开源。它的隐喻很刺耳：*"Most AI agent frameworks today are like running every process as root -- no access controls, no isolation, no audit trail."*

LangChain 的行业调查提供了现实数据：在 2,000+ 人企业中，安全顾虑达 24.9%，仅次于质量（32%）。89% 已实施 observability，但只有 52% 做了 offline eval，37% 做了 online eval。**行业在 harness 的"看"上成熟了，但"验"上还差一半。**

---

## 五、四个未回答的问题

30 篇信源覆盖了概念定义、架构设计、生产验证、安全框架，但有些问题仍然没有答案。

### Q1：产品开发类 Brownfield 怎么做？

Microsoft Azure SRE [#30] 证明了 brownfield 的可行性，但 SRE 是一个特殊领域——事件响应有清晰的输入输出、成功标准明确（TTM 下降）、容错空间相对大（诊断错误可以重试）。

一个更有代表性的场景——在一个 10 年历史、百万行规模的产品代码库上做 harness engineering——目前没有公开实证。OpenAI 的百万行实验是纯绿地 [#19]，Böckeler 的质疑 [#20] 仍然成立。

### Q2：行为正确性如何验证？

Böckeler [#20] 尖锐地指出：OpenAI 的百万行实验缺乏行为测试证据。代码能跑 ≠ 代码正确。

Anthropic 的 eval 方法论 [#10] 提供了理论框架，但没有给出 harness engineering 场景下的具体实践。LangChain Survey 显示仅 52% 做了 offline eval——这意味着近一半投产的 agent 系统没有系统性的行为验证。

### Q3：Harness 维护成本的长期模型是什么？

四个信源给出了四种不同的答案：

- Schmid [#8]：build to delete——接受 harness 是消耗品
- OpenAI [#19]：harness 是重资产——投 5 个月构建，持续 GC
- Anthropic [#15]：用 OS 虚拟化接口对抗 harness 过时——接口稳定，实现可换
- LangChain [#24]：部分 harness 会被模型吸收——*"As models get more capable, some of what lives in the harness today will get absorbed into the model."*

没有人给出过 harness 维护成本的量化模型。这对技术管理者来说是一个实际问题：harness engineering 团队该多大？ROI 怎么算？

### Q4：安全标准何时统一？

OWASP 有风险分类，NVIDIA 有开源运行时，Microsoft 有治理工具包，Anthropic 有原则框架——但没有行业统一的 harness 安全基线。Anthropic 在 [#29] 中呼吁 NIST 参与标准化，但截至 2026 年 4 月，这仍是愿景而非现实。

---

## 六、一张图看全貌

```
2024-06   Chase: "Cognitive Architecture"
          ─ agent 需要 rails + state [#1-5]
              │
2024-12   Anthropic: "Agentic Systems"
          ─ workflow vs agent; ACI [#6]
              │
2025-12   Schmid: 预言 harness 是 2026 护城河 [#7]
              │
2026-01   ┌─ Schmid: Model=CPU, Harness=OS [#8]
          ├─ Gupta: "model is commodity, harness is moat" [#9]
          ├─ Anthropic: eval harness + 趋势报告 [#10,#11]
          ├─ OpenAI: Codex agent loop [#12]
          ├─ Chase: "scaffolds → harnesses" [#13]
          └─ Anthropic: Agent SDK [#14]
              │
2026-02   ┌─ Anthropic: Session/Harness/Sandbox 三层解耦 [#15]
          ├─ OpenAI: Codex App Server [#16]
          ├─ Hashimoto: 命名 "Harness Engineering" [#17]
          ├─ Anthropic: infra noise 6pp [#18]
          ├─ OpenAI: 百万行零手写 [#19]
          ├─ Böckeler: 三组件分析 + 批判 [#20]
          ├─ LangChain: 只改 harness → +13.7pp [#21]
          └─ Mollick: 大众传播 [#22]
              │
2026-03   ┌─ Morris: Why/How Loop [#23]
          ├─ LangChain: Agent = Model + Harness [#24]
          ├─ Willison: 入门心智模型 [#25]
          └─ NVIDIA: OpenShell [#26]
              │
2026-04   ┌─ Microsoft: Agent Governance Toolkit [#27]
          ├─ Red Hat: 两阶段结构化工作流 [#28]
          ├─ Anthropic: Trustworthy Agents [#29]
          └─ Microsoft: Azure SRE 35K 事件 [#30]
```

---

## 信源索引

| # | 日期 | 来源 | 标题 |
|---|------|------|------|
| 1 | 2024-06-18 | Sequoia Capital | "Goldilocks" Agents and the Power of Custom Cognitive Architectures |
| 2 | 2024-06-18 | Harrison Chase x Sequoia | Training Data Podcast: Building the Orchestration Layer |
| 3 | 2024-07-05 | Harrison Chase / LangChain | What is a "cognitive architecture"? |
| 4 | 2024-07-13 | Harrison Chase / LangChain | Why you should outsource your agentic infrastructure, but own your cognitive architecture |
| 5 | 2024-07-20 | Harrison Chase / LangChain | Planning for Agents |
| 6 | 2024-12-19 | Anthropic | Building Effective Agents |
| 7 | 2025-12-31 | Phil Schmid | 8 Predictions for 2026 |
| 8 | 2026-01-05 | Phil Schmid | The importance of Agent Harness in 2026 |
| 9 | 2026-01-07 | Aakash Gupta | 2025 Was Agents. 2026 Is Agent Harnesses. |
| 10 | 2026-01-09 | Anthropic | Demystifying Evals for AI Agents |
| 11 | 2026-01-21 | Anthropic | 2026 Agentic Coding Trends Report |
| 12 | 2026-01-23 | OpenAI | Unrolling the Codex agent loop |
| 13 | 2026-01-25 | Harrison Chase x Sequoia | Context Engineering Long-Horizon Agents |
| 14 | 2026-01-28 | Anthropic | Building agents with the Claude Agent SDK |
| 15 | 2026-02-04 | Anthropic | Scaling Managed Agents: Decoupling the brain from the hands |
| 16 | 2026-02-04 | OpenAI | Unlocking the Codex harness: App Server |
| 17 | 2026-02-05 | Mitchell Hashimoto | My AI Adoption Journey |
| 18 | 2026-02-05 | Anthropic | Quantifying infrastructure noise in agentic coding evals |
| 19 | 2026-02-11 | OpenAI | Harness engineering: leveraging Codex in an agent-first world |
| 20 | 2026-02-17 | Birgitta Böckeler / Thoughtworks | Harness Engineering |
| 21 | 2026-02-17 | LangChain | Improving Deep Agents with harness engineering |
| 22 | 2026-02-18 | Ethan Mollick | A Guide to Which AI to Use in the Agentic Era |
| 23 | 2026-03-04 | Kief Morris / Thoughtworks | Humans and Agents in Software Engineering Loops |
| 24 | ~2026-03 | LangChain | The Anatomy of an Agent Harness |
| 25 | ~2026-03 | Simon Willison | How coding agents work -- Agentic Engineering Patterns |
| 26 | 2026-03-16 | NVIDIA | OpenShell |
| 27 | 2026-04-02 | Microsoft | Introducing the Agent Governance Toolkit |
| 28 | 2026-04-07 | Red Hat | Harness engineering: Structured workflows for AI-assisted development |
| 29 | 2026-04-09 | Anthropic | Trustworthy agents in practice |
| 30 | ~2026-04-10 | Microsoft | How we build and use Azure SRE Agent |
| — | 2025-12-10 | OWASP | Top 10 for Agentic Applications 2026 |
| — | ~2026-01 | Microsoft | Context Engineering for Reliable AI Agents |
| — | ~2026-03 | Microsoft | Harness Engineering for Azure SRE Agent |
| — | ~2026 | LangChain | State of Agent Engineering 2026 |
