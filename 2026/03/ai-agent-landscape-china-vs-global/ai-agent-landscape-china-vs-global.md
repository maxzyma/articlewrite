---
title: 中外 AI Agent 产品层对标全景图：从 Claude Code/Cowork 到国内大厂的追赶与分化
author: Mazy
description: 以腾讯 CodeBuddy/WorkBuddy 为引子，系统梳理 2026 年初中外 AI Agent 产品五大形态、主要玩家及关键差异
cover: ./images/cover.png
created: 2026-03-10
published: {}
---

# 中外 AI Agent 产品层对标全景图：从 Claude Code/Cowork 到国内大厂的追赶与分化

> **TL;DR** — 2026 年初，AI Agent 产品层已形成 CLI Agent、AI IDE、IDE 插件、桌面 Agent、通用 Agent 五大形态。海外以 Anthropic（Claude Code + Cowork）和 OpenClaw 为标杆，国内腾讯、阿里、字节各以 2-4 款产品完成全形态覆盖，价格普遍更低甚至免费开源。但产品"形似"之后，生态深度、安全架构和商业模式的差异正在成为下半场的分水岭。

---

## 一、背景：为什么现在谈 Agent 产品层？

2025 年被称为"Agent 应用元年"。进入 2026 年，战场从模型能力之争迅速转向产品层的全面角逐。

三个事件标志着这一转折：

**第一，Claude Code 跑出 $1B ARR。** Anthropic 的命令行 AI 编程工具在 2025 年 Q4 达到 10 亿美元年化收入，证明"AI Agent 即产品"的商业逻辑成立——不再只是模型 API 的套壳应用，而是有独立付费意愿的生产力工具。

**第二，OpenClaw 3 个月 20 万 Star。** 开源桌面 Agent 的爆发说明，开发者和知识工作者已经准备好让 AI 直接操作本地电脑，而不只是对话。ClawHub 上 5700+ Skills 的生态更证明了"Skill 自举"这一范式的威力。

**第三，国内大厂密集发布。** 腾讯 2026 年 3 月 9 日上线 WorkBuddy，完成 CodeBuddy + WorkBuddy 双产品矩阵；阿里以 Qoder + Qwen Code + 通义灵码 + QoderWork 四线齐发；字节 Trae 发布 Solo 模式。各家不再只做"一个产品"，而是覆盖完整的产品形态矩阵。

这不再是"谁的模型更强"的问题，而是"谁的产品矩阵更完整、生态更深"的系统性竞争。

---

## 二、海外标杆：五大产品形态

在进入国内对标之前，先厘清海外已经跑通的五大产品形态。

### 1. CLI Agent（命令行智能体）

**代表产品：Claude Code**

开发者在终端输入自然语言，Agent 自主读代码、改文件、跑测试、提交 Git。2025 年 2 月预览、5 月随 Claude 4 正式发布，到 Q4 已达 $1B ARR。核心价值不是"代码补全"，而是"代码执行"——从提示到提交，全链路自主完成。

配合 Claude 4.5 Opus 和后续的 Opus 4.6 模型，Claude Code 在多文件重构任务上的成功率比竞品高 20-40%。

### 2. AI IDE（AI 原生集成开发环境）

**代表产品：Cursor**

在 VS Code 基础上重建的 AI 原生 IDE，将代码补全、对话、Agent 任务融为一体。2025-2026 年推出 Background Agents，支持并行处理多个编码任务。形态优势是"所见即所得"——开发者不离开编辑器就能完成从提问到修改的闭环。

### 3. IDE 插件

**代表产品：GitHub Copilot**

最早起步、渗透率最高的形态。作为现有 IDE 的插件存在，学习成本最低。但受限于插件架构，难以实现跨文件的深度 Agent 行为。2025 年后逐渐被 AI IDE 和 CLI Agent 的体验超越。

### 4. 桌面 Agent（Desktop Agent）

**代表产品：Claude Cowork / OpenClaw**

两者定位有显著差异：

- **Cowork**（2026 年 1 月研究预览）：Anthropic 官方的桌面 AI 工具，面向非技术用户，处理文件整理、表格处理、邮件自动化等办公任务。所有操作需用户授权，运行在隔离沙箱中。安全优先。
- **OpenClaw**（原 Clawdbot）：开源社区驱动，用户通过 WhatsApp/Telegram/企微远程遥控本地电脑执行任务。核心创新是"Skill 自举"——Agent 遇到未知任务时自主编写 Skill，封装为 SKILL.md 复用。自由度优先。

### 5. 通用 Agent（General-Purpose Agent）

**代表产品：Devin / Manus**

- **Devin**（Cognition AI）：定位"首个 AI 软件工程师"，专注代码任务的端到端自主执行。
- **Manus**（Monica/蝴蝶效应）：中国团队打造的通用 Agent，覆盖研究、报告、数据分析等多领域。采用规划-执行-验证三代理架构。ARR 突破 $1 亿后被 Meta 以超 $20 亿收购。

---

## 三、国内全景对标

### 腾讯：双产品矩阵，从内部走向外部

腾讯是国内最早完成"开发者 + 知识工作者"双线布局的厂商。

| 产品 | 形态 | 对标 | 状态 |
|------|------|------|------|
| CodeBuddy Code 2.0 | CLI Agent | Claude Code | 已发布 |
| CodeBuddy IDE | AI IDE | Cursor | 已发布 |
| WorkBuddy | 桌面 Agent | Cowork / OpenClaw | 2026-03-09 正式上线 |

**CodeBuddy** 在腾讯内部渗透率超 90%，编码时间平均缩短 40%，AI 生成代码占比超 50%。2.0 版本开放 SDK 支持被集成，支持 Plugin 插件市场和隔离沙箱运行环境。模型层支持 GPT-5.2-Codex、Gemini 3 Pro 等海外顶级模型，国内版接入 DeepSeek-V3、GLM-4.7 等。

**WorkBuddy** 的差异化在于"腾讯全家桶连接"——打通企微、QQ、飞书、钉钉，支持手机远程遥控桌面 Agent。技术架构为"本地沙盒执行 + 多模型调度 + 安全网关防护"。完全兼容 OpenClaw Skills，但降低了部署门槛：从下载到连接企微，最快 1 分钟。内测期已覆盖 2000+ 名员工，涵盖 HR、行政、运营、销售等非技术岗位。

### 阿里：四线齐发，从模型到产品的全覆盖

阿里是产品线最完整的国内玩家，四款产品覆盖四大形态。

| 产品 | 形态 | 对标 | 特色 |
|------|------|------|------|
| Qoder | AI IDE | Cursor | Qwen3-Max 驱动，价格约 Cursor 一半 |
| Qwen Code | CLI Agent | Claude Code | Apache 2.0 开源，每日 2000 次免费 |
| 通义灵码（Lingma）| IDE 插件 | GitHub Copilot | 公安部 C3 认证，金融/政务场景 |
| QoderWork | 桌面 Agent | Cowork / OpenClaw | 桌面 Agent，随 Qoder 生态发布 |

关键差异化：**开源 + 免费策略**。Qwen Code 采用 Apache 2.0 完全开源，支持 Skills、SubAgents、Plan Mode 等高级功能，兼容 Anthropic/Google/OpenAI 协议。底层 Qwen3-Coder（480B 参数 MoE 架构）支持 119 种编程语言，原生 256K 上下文可扩展至 1M。

阿里的基础设施投入也是国内最大：2025-2027 三年 3800 亿元用于云和 AI 基础设施。

### 字节跳动：IDE 先行，Solo 模式突围

字节选择了不同的路径——先用 AI IDE 占领开发者心智，再向 Agent 平台扩展。

| 产品 | 形态 | 对标 | 特色 |
|------|------|------|------|
| Trae | AI IDE | Cursor | 支持 GPT-5.x / Gemini 3 等多模型切换 |
| Trae Solo | 自主 Agent 模式 | Devin | AI 主导全流程：需求→代码→测试→预览 |
| trae-agent | 开源 CLI Agent | Claude Code | GitHub 上万 Star |
| 扣子空间（Coze Space）| 通用 Agent 平台 | — | 面向 C 端，多模态交互 |

**Trae Solo** 是字节的关键创新：在"双模编程"中，Solo 模式让 AI 完全主导任务执行，从需求理解到代码预览全链路自主完成。这实质上是在 IDE 框架内实现了类 Devin 的体验。

字节 2026 年计划投入 1600 亿元用于 AI 研发，稳坐国内投入第一梯队。

### 百度：模型强、Agent 产品层相对薄弱

| 产品 | 形态 | 对标 | 特色 |
|------|------|------|------|
| 心响 APP | 通用 Agent | Manus（移动端） | 首个移动端通用超级智能体 |
| 文心智能体平台 | Agent 平台 | — | 数十万活跃 Agent，垂直领域强 |
| 文心 5.0 | 基础模型 | GPT-5 / Claude 4 | 2.4 万亿参数，40+ 基准超越竞品 |

百度在模型层依然强劲（文心 5.0 在 40+ 权威基准测试中表现优异），但在 AI 编程产品层缺少与 Claude Code 或 Cursor 直接对标的工具。其优势领域是垂直行业 Agent：法律咨询、医疗辅助、教育等，2025 年以 210 个中标项目、约 23.16 亿元蝉联大模型"标王"。

### 创业公司：模型+产品双轮驱动

| 公司 | 核心产品 | 定位 | 亮点数据 |
|------|---------|------|---------|
| 智谱 AI | CodeGeeX / AutoGLM / GLM-4.7 | 编程模型 + Agent | Coding Plan 4 个月 15 万付费用户；GLM-4.7 SWE-Bench 73.8% 创开源新高 |
| MiniMax | M2.1 编程模型 | 全栈编程模型 | VIBE 榜 88.6 分接近 Claude Opus 4.5；Starter 套餐 29 元/月 |
| 月之暗面 | Kimi K2 | 编程模型 | 256K 上下文，工具调用格式正确率 100%，兼容 Anthropic API |
| 网易有道 | LobsterAI | 桌面 Agent | 全场景个人助理，中国版 OpenClaw 定位 |

创业公司的策略分化明显：智谱和 MiniMax 走"模型+Coding Plan 订阅"路线，直接向开发者收费；月之暗面专注模型能力打磨，通过兼容 Anthropic API 降低迁移成本；网易有道则切入桌面 Agent 应用层。

---

## 四、对标全景表

![五大形态 × 中外产品矩阵](images/fig1-product-matrix.png)

| 产品形态 | 海外标杆 | 腾讯 | 阿里 | 字节 | 百度 | 创业公司 |
|---------|---------|------|------|------|------|---------|
| **CLI Agent** | Claude Code | CodeBuddy Code 2.0 | Qwen Code (开源) | trae-agent (开源) | — | — |
| **AI IDE** | Cursor | CodeBuddy IDE | Qoder | Trae / Trae Solo | — | — |
| **IDE 插件** | GitHub Copilot | CodeBuddy 插件 | 通义灵码 | — | — | CodeGeeX (智谱) |
| **桌面 Agent** | Cowork / OpenClaw | WorkBuddy | QoderWork | — | — | LobsterAI (网易有道) |
| **通用 Agent** | Devin / Manus | — | — | 扣子空间 | 心响 APP | AutoGLM (智谱) |

**关键发现：**

1. **阿里和腾讯** 的产品矩阵最完整，各覆盖 4 个形态。
2. **字节** 在 IDE 形态上最深入（Trae Solo 的全自主模式），但桌面 Agent 缺位。
3. **百度** 在开发者工具形态（CLI Agent / AI IDE / IDE 插件）上几乎空白。
4. **CLI Agent** 形态出现了开源趋势：Qwen Code（Apache 2.0）和 trae-agent 均开源。
5. **没有任何一家国内厂商在通用 Agent 上形成强势产品**——Manus 被 Meta 收购后，这个赛道在国内出现了真空。

---

## 五、四维差异分析

![中外 AI Agent 厂商四维差异雷达图](images/fig2-ecosystem-radar.png)

### 维度一：生态策略

| | Anthropic | 腾讯 | 阿里 | 字节 |
|---|---|---|---|---|
| 核心策略 | 模型领先 + 产品闭环 | 全家桶连接 | 开源+云服务 | 免费获客+模型多选 |
| Skill 生态 | Claude Code Skills | 兼容 OpenClaw Skills + MCP | Qwen Code Skills/SubAgents | Trae 插件市场 |
| 模型选择 | 仅 Claude 系列 | 多模型（混元/DeepSeek/GLM/Kimi/MiniMax） | Qwen 系列为主 | 自研+OpenRouter 多模型 |

腾讯的策略最独特：WorkBuddy 完全兼容 OpenClaw Skills，同时打通腾讯系办公产品（企微、腾讯文档、腾讯会议），形成"开源 Skill 生态 + 私有办公生态"的双层连接。

阿里则走了最激进的开源路线：Qwen Code 完全开源，兼容 Anthropic/Google/OpenAI 三大协议，既是自家 Qoder 的基座，也是开发者生态的入口。

### 维度二：模型策略

国内 AI Coding 模型已形成"国际三强领跑，国产快速追赶"的格局：

**第一梯队**（SWE-Bench > 75%）：Claude Opus 4.6、GPT-5.2-Codex、Gemini 3 Pro

**第二梯队**（SWE-Bench 70-75%）：Qwen3-Coder、Kimi K2、GLM-4.7

**第三梯队**（SWE-Bench 65-70%）：MiniMax M2.1、DeepSeek V3.2

关键趋势是**模型选择权的开放**。Claude Code 只能用 Claude 模型，而国内产品普遍支持多模型切换。CodeBuddy 支持混元、DeepSeek、GLM、Kimi、MiniMax 五家模型；Trae 接入 GPT-5.x、Gemini 3 等海外模型。这反映了国内厂商"不把鸡蛋放在一个篮子里"的务实策略，也说明单一国产模型尚未达到让厂商完全押注的信心水平。

### 维度三：安全架构

安全是桌面 Agent 形态的核心差异点。

| | Claude Cowork | OpenClaw | WorkBuddy |
|---|---|---|---|
| 执行环境 | 容器化沙箱 | 本地直接执行 | 本地沙盒 + 安全网关 |
| 权限模型 | 每步用户授权 | 用户自由授权 | 企业级权限管控 |
| Skill 来源 | 官方审核 | 社区上传（曾有 20% 恶意率）| 兼容 OpenClaw + 自有审核 |
| 数据处理 | 本地为主 | 完全本地 | 本地 + 腾讯云安全网关 |

OpenClaw 的安全问题不容忽视：Wiz 曾发现配置错误的数据库泄露 150 万个 API token，ClawHub 早期约 900 个恶意 Skill（占比约 20%），卡巴斯基将其评为"2026 年最大的潜在内部威胁"。腾讯 WorkBuddy 兼容 OpenClaw Skills 的同时引入安全网关审核，实际上是在"自由度"和"安全性"之间寻找平衡点。

### 维度四：商业模式

| 产品 | 定价策略 | 价格区间 |
|------|---------|---------|
| Claude Code | Pro $20/月，Max 更高 | $20-$200/月 |
| Cursor | Pro $20/月 | $20/月 |
| CodeBuddy | 免费额度 + 付费 | 免费起步 |
| Qwen Code | 开源免费（每日 2000 次） | 免费 |
| Trae | 免费 + 付费 | 免费起步 |
| 智谱 Coding Plan | 按模型/额度分层 | 约涨价 30% |
| MiniMax Starter | 月度订阅 | 29 元/月 |

国内产品的定价普遍低于海外竞品。Qwen Code 完全免费开源，MiniMax Starter 29 元/月（约 $4），智谱 Coding Plan 虽然涨价 30% 仍远低于 Claude Code 的 $20/月。这既是竞争策略（以价格换市场），也反映了国内开发者对 AI 编程工具的付费意愿仍在培育期。

---

## 六、OpenClaw 催化效应

OpenClaw 的爆发不仅是一个产品事件，而是对整个中国 AI 产业链产生了连锁反应。

### 云厂商抢滩部署入口

OpenClaw 爆火后，阿里云、腾讯云、京东云、火山引擎、百度智能云相继宣布上线 OpenClaw 云端极简部署及全套云服务。这说明云厂商已经把"Agent 部署"视为新的基础设施入口，类似于当年的"容器化部署"之争。

### Skill 生态驱动产品设计

OpenClaw 的 "Skill 自举"机制（Agent 遇到未知任务时自主编写 Skill 并封装复用）深刻影响了国内产品设计。腾讯 WorkBuddy 选择完全兼容 OpenClaw Skills；CodeBuddy 2.0 推出 Plugin 插件市场。Skill/Plugin 生态正在成为桌面 Agent 产品的核心竞争力。

### Coding Plan 订阅模式兴起

随着 OpenClaw 在国内开发者中的普及，以固定月费替代按 Token 计费的 Coding Plan 订阅模式成为行业标配。智谱、MiniMax、阿里云百炼、火山方舟纷纷推出 Coding Plan 套餐。这一模式本质上是把"模型能力"包装为"开发者工具服务"，提升了付费意愿和用户粘性。

### 地方政府入局

更值得关注的是，深圳龙岗区和无锡高新区等地方政府出台了支持 OpenClaw 发展的专项政策，单项支持最高达 500 万元。AI Agent 从技术热点进入政策视野，意味着其产业化进程正在加速。

---

## 七、趋势与判断

### 判断一：产品层"形似"已完成，"神似"才刚开始

国内大厂在产品形态上的追赶速度很快——从 Claude Code 发布到国内出现全面对标产品，只用了不到一年。但产品形态的复制只是第一步。

真正的差距在于**模型-产品的深度耦合**。Claude Code 之所以成功，不仅因为它是一个好的 CLI 工具，更因为 Claude 模型在多步推理、工具调用、代码理解上的原生优势。国内产品支持多模型切换看似是优势（灵活），实则暴露了底层模型的短板（没有一个够强到独占）。

**预测：2026 年下半年，至少有 1-2 家国内厂商会从"多模型支持"转向"自研模型深度绑定"策略。**

### 判断二：桌面 Agent 将是下一个主战场

CLI Agent 和 AI IDE 主要服务开发者（全球约 3000 万），而桌面 Agent 面向所有知识工作者（全球约 10 亿）。腾讯 WorkBuddy 瞄准的 HR、行政、运营、销售等非技术岗位，市场规模远大于 AI 编程。

但桌面 Agent 面临的挑战也更复杂：操作系统权限、数据安全、企业合规，每一个都是重度工程问题。OpenClaw 的安全事故（150 万 API token 泄露、20% 恶意 Skill）已经是前车之鉴。

**预测：2026 年 Q3-Q4，桌面 Agent 的竞争焦点将从"能做什么"转向"如何安全地做"。**

### 判断三：中国 AI Agent 的出海窗口正在关闭

Manus 被 Meta 收购、OpenClaw 创始人加入 OpenAI——顶级人才和项目正在向海外巨头集中。与此同时，国内市场的竞争已经白热化，价格战使得盈利困难。

但反过来看，这也意味着国内市场将进入"务实落地"阶段。不再追求"全球化"的宏大叙事，而是在国内企业场景中把 Agent 真正用起来。字节 1600 亿、阿里 3800 亿的巨额投入，最终需要通过企业客户的实际使用来验证。

---

## 参考资料

1. [WorkBuddy - AI Agent 办公新范式](https://www.codebuddy.cn/work/)
2. [Tencent launches OpenClaw-like workplace AI agent WorkBuddy - TechNode](https://technode.com/2026/03/09/tencent-launches-openclaw-like-workplace-ai-agent-workbuddy/)
3. [Claude封锁中国，腾讯带着国产AI编程工具CodeBuddy来了 - InfoQ](https://www.infoq.cn/article/soadsraioyt8ckqhijx5)
4. [「从夯到拉」2026年AI编程工具全景测评 - 知乎](https://zhuanlan.zhihu.com/p/1999804779141030200)
5. [AI 编程 2025 总结：国产模型"能力追平"，国产编程工具还在"情感陪伴" - Phodal](https://www.phodal.com/blog/ai-coding-2025-summary/)
6. [2026年，国内有哪些可替代Cursor、Windsurf、Devin的AI编程工具？ - 知乎](https://www.zhihu.com/question/8876692769)
7. [The AI Agent Landscape in 2026 - AI Makers](https://www.aimakers.co/blog/ai-agents-landscape-2026/)
8. [Claude Code迎来最强中国对手！ - 腾讯新闻](https://news.qq.com/rain/a/20260126A01RL400)
9. [OpenClaw、Cowork引爆AI代理革命 - 证券时报](https://www.stcn.com/article/detail/3634640.html)
10. [OpenClaw 深度解析 - 知乎](https://zhuanlan.zhihu.com/p/2012694232666760139)
11. [2026是Agent生死之年 - 思聪网](https://www.techgg.com/portal.php?mod=view&aid=237)
12. [国内 AI Coding Plan 横向测评报告（2026年3月）](https://blog.lightnote.com.cn/china-ai-coding-plan-benchmark/)
13. [Claude不让我们用，国产平替能顶上吗？ - 36氪](https://36kr.com/p/3456392450037382)
14. [OpenClaw 平替产品全景对比 - 53AI](https://www.53ai.com/news/Openclaw/2026030306512.html)
15. [Manus上岸了，其他人呢？ - 投资界](https://news.pedaily.cn/202512/559358.shtml)
