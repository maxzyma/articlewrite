# A2A 协议 Message 与 Artifact 统一提案讨论总结

> 基于 GitHub Issue #1313: "[Feat]: Unify `Message` and `Artifact` to simplify streaming and semantics"
>
> 发起人: matoushavlena | 发起日期: 2025-12-16 | 状态: 讨论中

## 背景概述

A2A (Agent-to-Agent) 协议当前将 `Message` 和 `Artifact` 视为独立概念，但两者之间的边界模糊，导致：
- 实现方式分歧
- 开发者对同一行为做出不同选择
- 生态系统中的不兼容模式
- 破坏互操作性承诺

## 提案核心内容

### 问题陈述

当前协议的六大痛点：

| 编号 | 痛点 | 描述 |
|------|------|------|
| PP1 | Message 与 Artifact 区分模糊 | "通信"和"输出"的边界主观且不清晰 |
| PP2 | 流式传输绑定到 Artifact | Message 无原生流式支持，迫使开发者通过 Artifact 路由流式文本 |
| PP3 | 客户端/SDK 复杂度增加 | 多种响应形状实现同一结果，增加代码复杂度和测试负担 |
| PP4 | 对话时间线断裂 | Artifacts 存储在 `Task.artifacts[]`，与 `Task.history[]` 分离 |
| PP5 | 分块消息污染历史 | 流式 Message 的每个分块独立存储，传输机制而非逻辑消息 |
| PP6 | 状态转换与内容传递混合 | `TaskStatusUpdateEvent` 和 `TaskArtifactUpdateEvent` 都被用于传递用户可见内容 |

### 建议方案

**核心思想**：以 Message 为内容单元，Artifact 是通过 `name` 标识的 Message 的语义角色，而非独立的传输或流式机制。

**分阶段实施路径**：

```
Phase A (无破坏性变更)
├── 为 Message 添加 append、last_chunk 字段
├── 新增 TaskMessageUpdateEvent 到 StreamResponse
├── 明确语义指南（状态更新 vs 内容传递）
└── 保持 Artifact 不变

Phase B (向后兼容)
├── 为 Message 添加 name、description 字段
├── 废弃 Artifact 和 TaskArtifactUpdateEvent
├── Task.artifacts[] 包含 legacy Artifact 和 named Message
└── 所有 named Message 也出现在 Task.history[]

Phase C (完成迁移)
├── 移除废弃的 Artifact 和 TaskArtifactUpdateEvent
├── Task.history[] 作为内容时间线的唯一来源
└── Task.artifacts[] 作为 named Message 的过滤视图
```

## 各方观点分析

### 1. 提案方观点 (matoushavlena)

- 当前协议边界模糊导致实现分歧
- 提案可增量采用，降低风险
- Phase A 仅添加性变更，风险低

### 2. 反对统一观点 (darrelmiller)

**核心立场**：反对统一 Message 和 Artifact，认为这会破坏 A2A 的核心价值主张。

关键论点：
- **Message 是简单、不可变的**：用于传输意图，内容一旦发送不应更改
- **Artifact 是语义丰富的**：代表任务输出，可持续更新、有生命周期、可评价和分享
- **Phase A 会让问题更糟**：引入类似 MCP 的流恢复挑战
- **如果做 Phase B，不如加入 MCP**：A2A 的初始价值主张正是 input/output 的清晰区分
- **Message 只应用于预协商场景**：有意义的交互应该使用 Task

> "I don't believe anyone should be returning Agent output in status messages. That seems like a clear violation of intent."

**替代建议**：考虑使用不同类型的 Message 类来减少复杂性，而非统一。

**语义区分**：
- Message: 简单机制，Id + 内容，内容代表完整要传达的信息，不可变
- Artifact: 语义更丰富的概念，代表任务输出，可持续更新，有完成标识，可被评价和分享

### 3. 客户端复杂度担忧 (bparees)

**核心关注**：Phase A 中 TaskStatusUpdateEvent 包含流式 Message 会增加客户端复杂度。

- 状态更新消息通常不大，不需要分块流式传输
- 客户端需要处理 `last_chunk` 为 false 的情况，增加了实现难度
- 建议保留"非流式"消息/工件类型用于不应被追加/更新的负载类型

### 4. 多轮对话/客户端集成场景 (tomkis)

**核心论点**：
- **多轮对话场景**：需要支持逐消息流式传输，或使用 Artifacts 实现传统流式
- **通用客户端集成**：聊天客户端与 Agent 通信，流式消息是常见需求
- **使用 Artifacts 的问题**：对话历史需要同时追踪 Artifacts 和 Messages，实现繁琐
- **哲学问题**：A2A 是否应该支持非 Agent 客户端？文档对此不清晰

> "Consider a simple chat client communicating with an assistant-like agent. One of the most common requirements for this use case is the ability to stream messages (conversational content) to the UI."

### 5. v1 优先级与幂等性方案 (darrelmiller)

**最新进展**（1月7日评论）：
- v1 最高优先级是满足 Agent-to-Agent 通信
- 但支持 Agent 返回包含 A2UI 响应的 Message
- **新思路**：通过 `SendMessage/SendStreamingMessage` 的幂等性解决流式弹性问题
  - 协商阶段不应有持久影响，流中断可安全重发
  - Artifact 支持可恢复流，Message 提供瞬时幂等流
- 计划在 v1.1 实现

> "Which leaves us with, artifacts enable resumable streams, messages provide transient, idempotent streams."

## 观点分布矩阵

| 立场 | 代表人物 | 主要诉求 |
|------|----------|----------|
| 支持提案 | matoushavlena | 统一简化协议，解决流式问题 |
| 反对统一 | darrelmiller | 保持分离，保留差异价值 |
| 谨慎/有条件支持 | bparees, tomkis | 关注客户端复杂度、多场景需求 |
| 倾向折中 | darrelmiller (最新) | 保留 Message/Artifact 分离，但支持流式 Message |

## 相关 Issue 关联

| Issue | 关联内容 |
|-------|----------|
| #1261 | Make Message streaming possible |
| #822 | Message object for streaming |
| #783 | How to support message stream |
| #982 | Integrate artifacts into task history |
| #301 | Timestamped Task History via statusHistory |
| #763 | Use TaskStatusUpdateEvent or TaskArtifactUpdateEvent? |
| #1253 | Valid to create TaskStatusUpdateEvent with same status but update message? |
| #1252 | Clarify agent responsibilities for including state messages in Task message history |
| #1232 | Is 'final' property necessary given terminal states? |

## 结论与展望

### 当前状态

讨论仍在进行中（截至 2026-01-21），尚未达成最终共识。主要分歧在于：

1. **是否统一**：Message 和 Artifact 是否应该合并为单一概念
2. **流式支持**：Message 是否应该支持流式传输
3. **客户端场景**：A2A 是否应该支持非 Agent 客户端的多轮对话场景
4. **v1 范围**：哪些特性应该纳入 v1，哪些可以延后

### 可能的方向

1. **保留分离，添加流式**：类似 darrelmiller 的最新建议，保留 Message/Artifact 区别，但为 Message 添加幂等性流式支持
2. **区分消息类型**：使用不同的 Message 类来处理不同场景，而非统一
3. **文档澄清**：无论最终技术方案如何，都需要更清晰的文档说明协议适用范围和最佳实践

## 参考链接

- [Issue #1313 原文](https://github.com/a2aproject/A2A/issues/1313)
- [A2A Protocol Specification](https://a2a-proTOCOL.org)
