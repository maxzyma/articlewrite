---
title: "Anthropic Managed Agents 深度解读：从三层解耦架构看 AI Agent 平台战略"
author: Mazy
description: 基于 Anthropic 6 篇官方工程博客的系统分析，拆解 Managed Agents 的 Session/Harness/Sandbox 三层解耦架构，并大胆推测 Anthropic 的平台化战略意图。
created: 2026-04-09
published: {}
---

## 引言：一篇工程博客背后的战略野心

2026 年 2 月 4 日，Anthropic 发布了一篇看似纯技术的工程博客：[*Scaling Managed Agents: Decoupling the brain from the hands*](https://www.anthropic.com/engineering/managed-agents)。标题朴素，讲的是如何把 Agent 拆成三个独立组件。

但把这篇文章放进 Anthropic 过去 14 个月发布的 6 篇 Agent 工程文章的时间线里看，画面完全不同——**这不是一次架构重构的技术复盘，而是一份 Agent 平台化的施工蓝图。**

本文基于对 25 篇业界 Agent Harness 文献的系统调研（详见 `notes/02-调研/harness/analysis.md`），聚焦 Anthropic 的 6 篇官方文章，拆解其技术路径，并推测其战略意图。

> **信源说明**：文中 `[#N]` 编号对应调研索引 `notes/02-调研/harness/README.md` 中的文章编号。所有引文均来自原文，非转述。

---

## 一、Anthropic 的 Agent 叙事时间线

先看事实。Anthropic 在 14 个月内发布了 6 篇 Agent 相关的工程文章，每篇都在推进一个清晰的叙事：

| 日期 | 文章 | 核心推进 |
|------|------|---------|
| 2024-12-19 | Building Effective Agents [#6] | **奠基**：定义 workflow vs agent，给出 7 个 composable patterns，提出 ACI 概念 |
| 2026-01-09 | Demystifying Evals for AI Agents [#10] | **度量**：区分 evaluation harness 和 agent harness，将 harness 提升为一等测量对象 |
| 2026-01-21 | 2026 Agentic Coding Trends Report [#11] | **数据**：context files 让错误率降 40%、完成速度提升 55%——用数据证明 harness 的价值 |
| 2026-01-28 | Building agents with the Claude Agent SDK [#14] | **蓝图**：Claude Agent SDK 即 harness 实现方案——工具、子 agent、compact、MCP |
| 2026-02-04 | Scaling Managed Agents [#15] | **架构**：Session/Harness/Sandbox 三层解耦，OS 虚拟化类比，生产级接口设计 |
| 2026-02-05 | Quantifying infrastructure noise [#18] | **护城河**：证明基础设施配置对 benchmark 影响达 6pp，暗示"跑分看 harness 不只看模型" |

这 6 篇文章的叙事逻辑是：**先告诉你 agent 该怎么建 → 再告诉你怎么评估 → 然后证明环境比模型更重要 → 接着给你 SDK → 再给你生产架构 → 最后证明你的 benchmark 可能在测 harness 而非模型。**

这不是随意发布的技术博客。这是一条精心设计的说服链。

---

## 二、Managed Agents 架构拆解

### 核心问题：Harness 会过时

Anthropic 在 [#15] 中开篇就点出了一个被业界普遍忽视的问题：

> *"Harnesses encode assumptions about model limitations that go stale as models improve."*

他们给了一个具体例子：Claude Sonnet 4.5 存在"上下文焦虑"（context anxiety），团队在 harness 中加入了上下文重置机制。但当 Claude Opus 4.5 上线后，这些重置变成了"死重"——Opus 根本没有这个问题。

**Phil Schmid 的 Bitter Lesson [#8] 在这里被验证了**：手工编码的 agent 逻辑总会被下一代模型淘汰。但 Anthropic 的解法不是 Schmid 说的"build to delete"——他们选择了更深层的方案：**用接口隔离变化**。

### 三层解耦

```
┌──────────────────────────────────────────┐
│  Session（会话层）                         │
│  append-only 事件流，活在 context window 外  │
│  接口：getEvents() — 灵活切片/回溯/重读      │
└──────────────┬───────────────────────────┘
               │ 读/写事件
┌──────────────▼───────────────────────────┐
│  Harness（控制层）                         │
│  无状态控制循环：调用 Claude + 路由 tool calls │
│  崩溃后 wake(sessionId) 即可恢复            │
└──────────────┬───────────────────────────┘
               │ execute(name, input) → string
┌──────────────▼───────────────────────────┐
│  Sandbox（执行层）                         │
│  代码执行环境，通过统一接口调用               │
│  provision({resources}) 按需创建            │
└──────────────────────────────────────────┘
```

三个关键设计决策：

**1. Session 是独立的事件流，不是 context window 的附属品。**

传统做法：长任务超出 context window → 压缩/修剪（不可逆）。Anthropic 的做法：Session 保留完整事件流，Harness 通过 `getEvents()` 灵活选择传入 Claude 的切片。

> 这意味着 **context engineering 从一次性决策变成了可回溯的策略**。你不需要在压缩时预判未来需要哪些 token——Session 都记着，随时可以重读。

**2. Harness 无状态，可随时替换。**

初始设计是三组件在单容器内（"宠物模式"）。容器挂了，会话就丢了。解耦后，容器变成"牛群"——任何一头牛（Harness 实例）挂了，换一头新的 `wake(sessionId)` 就行。

性能收益：
- p50 TTFT 降低 ~60%
- p95 TTFT 降低 >90%

**3. Sandbox 凭证隔离。**

> 凭证存在外部 vault，MCP proxy 持有 OAuth token，Sandbox 永远接触不到密钥。

这不只是安全设计——这是 **prompt injection 的防线**。Claude 生成的代码在 Sandbox 里执行，即使被注入恶意指令也拿不到凭证。

### OS 虚拟化类比

Anthropic 在文中反复使用 OS 类比：

> *"We virtualized the components of an agent... We're opinionated about the shape of these interfaces, not about what runs behind them."*

这与 Schmid [#8] 的 "Model=CPU, Harness=OS" 一脉相承，但更进一步：Schmid 是比喻，Anthropic 是实现。就像 `read()` 系统调用不关心底层是 1970 年代的磁盘还是现代 SSD，Managed Agents 的接口不关心背后是哪个版本的 Claude、什么样的 Sandbox。

---

## 三、与 OpenAI 的路线对比

同一天（2026-02-04），OpenAI 发布了 Codex harness 系列第二篇 [#16]，讲 App Server 架构。两家在同一天发布 harness 架构文章，这本身就值得玩味。

| 维度 | Anthropic Managed Agents [#15] | OpenAI Codex App Server [#16] |
|------|-------------------------------|-------------------------------|
| 架构哲学 | 三层解耦，接口稳定，实现可换 | 单一 harness 驱动多表面（CLI/Web/IDE） |
| 核心抽象 | Session 作为独立 Context Object | Thread lifecycle & persistence |
| 扩展方式 | Sandbox 统一接口 `execute()` | JSON-RPC 自定义协议 |
| 安全模型 | 凭证与执行环境彻底隔离 | 未详述 |
| 多 agent | "Many Brains, Many Hands"——Brain 可传递 Hand | 未涉及 |
| 设计口号 | "opinionated about interfaces, not implementations" | "all powered by the same Codex harness" |

**关键差异**：Anthropic 把 Harness 做成了可插拔的中间层（"meta-harness"），OpenAI 把 Harness 做成了统一平台。前者赌的是 harness 会随模型进步而过时，后者赌的是一个足够好的 harness 可以长期使用。

谁对？**Anthropic 自己的数据支持 Anthropic**——Claude Sonnet 的 context anxiety 补丁在 Opus 上变成死重，这种事只会越来越频繁。

---

## 四、大胆推测：Anthropic 的平台战略

以下是基于公开信源的推测，**无信源，基于推断**。

### 推测 1：Managed Agents 是 Anthropic 的 "AWS for AI Agents"

把三层架构和 OS 类比放在一起看：

- Session = 持久存储层（S3/EBS）
- Harness = 计算编排层（ECS/Lambda）
- Sandbox = 执行运行时（EC2/Fargate）

Anthropic 不是在做一个 coding agent，**它在做 Agent 的基础设施层**。就像 AWS 不写你的应用代码但提供 compute/storage/networking，Anthropic 不写你的 agent 逻辑但提供 session/harness/sandbox。

文中的 "opinionated about interfaces, not implementations" 是 AWS 哲学的翻版——你用 S3 的 API，但 S3 内部实现换了多少次你根本不知道。

**战略意图**：如果每个企业客户都把自己的 agent 跑在 Anthropic 的 Session/Harness/Sandbox 上，那切换到 GPT-5 的成本就不只是换模型——你的整个执行环境、会话历史、工具链都在 Anthropic 的基础设施里。**这才是真正的 lock-in，不是模型能力，是运行环境。**

### 推测 2：Session 是数据飞轮的入口

Session 是 append-only 的完整事件流——每一次 tool call、每一次 Claude 的推理、每一次用户反馈，全部记录。

如果你是 Anthropic，这意味着什么？**你拥有全世界最大的 "agent 如何工作" 数据集。** 不是静态的训练数据，而是实时的、带结果反馈的、跨任务类型的 agent 执行轨迹（traces）。

Harrison Chase 在 [#13] 中说过：*"Traces 是新的 source of truth。"* 而 Anthropic 的 Session 设计恰好是一个完美的 trace 收集器——它记录一切，格式统一，且不受 context window 限制。

**战略意图**：用 Session 数据训练下一代模型的 agent 能力。这形成了一个飞轮——更好的模型 → 更多人用 Managed Agents → 更多 Session 数据 → 更好的模型。

### 推测 3："Many Brains, Many Hands" 指向多模型编排

文章描述了一个耐人寻味的能力：

> *"Brain 可以把 Hand 传给另一个 Brain。"*

表面上看，这是多 agent 协调。但如果 Brain 不限于 Claude 呢？

Anthropic 的 Managed Agents 接口是：
- Brain（Harness）通过 API 调用模型
- Hand（Sandbox）通过 `execute(name, input) → string` 执行

**这两个接口都不硬绑 Claude。** Harness 可以调用任何模型的 API，Sandbox 的统一接口对调用方透明。

**战略意图**：Anthropic 可能在为"模型路由"做准备。简单任务用 Haiku，复杂推理用 Opus，特定领域用微调模型——甚至在某些场景下调用竞品模型。就像 AWS 不阻止你在 EC2 上跑 Oracle 数据库，Anthropic 可能不阻止你在 Managed Agents 里调用 GPT。因为一旦你的执行环境、会话历史、工具链都在 Anthropic 的基础设施上，**模型可替换，平台不可替换**。

### 推测 4：Benchmark 文章 [#18] 是进攻性叙事

发布 Managed Agents 架构的第二天，Anthropic 发布了 [#18]——证明基础设施配置对 benchmark 影响达 6 个百分点。

> *"A few-point lead might signal a real capability gap -- or it might just be a bigger VM."*

表面是学术严谨。但放在战略语境下：

1. Anthropic 刚刚发布了业界最精细的 harness 基础设施
2. 然后证明 benchmark 分数受基础设施影响巨大
3. 暗示：**如果你用我们的基础设施跑 benchmark，分数会更好**

这是一个精心设计的两步走：先给你最好的 harness → 再告诉你 harness 决定分数。

### 推测 5：终局是 "Agent Operating System"

把所有线索串起来：

| 组件 | Anthropic 已有 | OS 类比 |
|------|---------------|---------|
| Session | append-only 事件流 | 文件系统 |
| Harness | 无状态控制循环 | 进程调度器 |
| Sandbox | 统一 execute() 接口 | 系统调用 |
| MCP | 工具标准协议 | 设备驱动标准 |
| Agent SDK | 开发者 API | POSIX API |
| Compact | context 管理 | 内存管理 |
| Eval harness [#10] | 评估基础设施 | 性能监控 |

**Anthropic 正在构建 Agent Operating System。**

不是比喻——是字面意义上的操作系统。它管理计算资源（Harness 实例）、持久存储（Session）、I/O（Sandbox/MCP）、安全（凭证隔离）、多进程（Many Brains）。

Claude 模型是这个 OS 的默认"CPU"，但 OS 的价值从来不在于绑死某个 CPU 厂商。Windows 先是跑在 Intel 上，后来也跑在 ARM 上。**当 Anthropic 的 Agent OS 足够成熟时，模型层变成可替换的硬件。**

---

## 五、风险与反论

公平起见，以上推测存在明显的反论：

**1. 过度解读工程博客。** Anthropic 可能只是在解决眼前的工程问题（容器不稳定、TTFT 太慢），没有宏大的平台野心。但 6 篇文章的叙事连贯性和发布节奏让"纯技术驱动"的解释不太令人信服。

**2. Böckeler [#20] 的批判仍然成立。** Managed Agents 的实践主要在 Anthropic 自己的产品上验证。企业客户的 brownfield 环境（存量代码库、内部工具链、合规要求）是否能平滑接入，**无信源，未知**。

**3. OpenAI 可能也在做同样的事。** Codex App Server [#16] 的 thread lifecycle + JSON-RPC 也是平台化的路径。两家的差异可能只是实现策略不同，而非战略方向不同。

**4. 飞轮假设依赖规模。** Session 数据飞轮只有在足够多的企业客户使用 Managed Agents 时才能转起来。目前 Anthropic 的企业市场份额相比 OpenAI/Microsoft 仍处劣势（无信源，基于公开市场认知推断）。

---

## 六、结论

Anthropic 的 Managed Agents 不只是一个技术架构——它是一个战略宣言。

从 2024 年底的 "Building Effective Agents" 到 2026 年初的 Managed Agents，Anthropic 用 14 个月完成了一次叙事升级：从"模型很重要"到"模型周围的一切更重要"，从"用简单模式"到"用我们的基础设施"。

LangChain 的 Terminal-Bench 数据 [#21] 证明只改 harness 可以从 Top 30 跃升 Top 5（+13.7pp）。Anthropic 自己的数据 [#18] 证明基础设施噪声达 6pp。当 harness 的影响可以超过模型之间的能力差距时，**控制 harness 层的人控制 agent 时代的定价权**。

这就是 Anthropic 的赌注：**模型是 CPU，我们要做 OS。**

---

## 信源索引

| 编号 | 来源 | 文章 | URL |
|------|------|------|-----|
| #1 | Sequoia Capital | Goldilocks Agents | https://sequoiacap.com/article/goldilocks-agents/ |
| #6 | Anthropic | Building Effective Agents | https://www.anthropic.com/research/building-effective-agents |
| #8 | Phil Schmid | The importance of Agent Harness | https://www.philschmid.de/agent-harness-2026 |
| #10 | Anthropic | Demystifying Evals for AI Agents | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents |
| #11 | Anthropic | 2026 Agentic Coding Trends Report | https://resources.anthropic.com/2026-agentic-coding-trends-report |
| #13 | Chase x Sequoia | Context Engineering Long-Horizon Agents | https://sequoiacap.com/podcast/context-engineering-our-way-to-long-horizon-agents-langchains-harrison-chase/ |
| #14 | Anthropic | Building agents with the Claude Agent SDK | https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk |
| #15 | Anthropic | Scaling Managed Agents | https://www.anthropic.com/engineering/managed-agents |
| #16 | OpenAI | Unlocking the Codex harness | https://openai.com/index/unlocking-the-codex-harness/ |
| #17 | Mitchell Hashimoto | My AI Adoption Journey | https://mitchellh.com/writing/my-ai-adoption-journey |
| #18 | Anthropic | Quantifying infrastructure noise | https://www.anthropic.com/engineering/infrastructure-noise |
| #19 | OpenAI | Harness engineering: leveraging Codex | https://openai.com/index/harness-engineering/ |
| #20 | Böckeler/Thoughtworks | Harness Engineering | https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html |
| #21 | LangChain | Improving Deep Agents with harness engineering | https://blog.langchain.com/improving-deep-agents-with-harness-engineering/ |
| #22 | Ethan Mollick | A Guide to Which AI to Use in the Agentic Era | https://www.oneusefulthing.org/p/a-guide-to-which-ai-to-use-in-the |
