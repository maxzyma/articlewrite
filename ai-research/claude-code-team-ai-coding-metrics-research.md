# Claude Code Team 订阅版 AI Coding 代码比例统计方法调研

_调研日期: 2026-03-04_

## TL;DR

**场景**：公司使用自托管 GitLab + Claude Code Team，需统计 AI Coding 代码比例。

**结论**：

| 维度 | 评估 |
|------|------|
| **Claude Code 原生能力** | 工具端数据丰富（API + OTEL + Dashboard），但**贡献指标仅支持 GitHub，不支持 GitLab** |
| **Cursor Team Dashboard** | **零开发成本**即开即用，commit 级 AI 代码占比统计，**不依赖 git 平台**，但偏高估 |
| **最快落地方案** | **Cursor Dashboard 直读**（0 天）+ Claude Code OTEL/API 看板（1-2 周）— 双工具互补 |
| **最可信方案** | 双工具 API 关联：Claude Code 保守值（下界）+ Cursor 上界 = **置信区间** |
| **最精确方案** | Git AI 行级归因（跨工具统一）或快手编辑距离法 |
| **面向未来** | Agent Trace 开放标准 — 若 Claude Code 加入，可替代所有自建方案 |
| **核心建议** | **不要只看"比例"**，需建立覆盖质量、交付速度、技术债务的多维 AI 效能度量体系 |

**推荐路线**：Phase 1（Cursor Dashboard 即开 + Claude Code OTEL/API 看板，1-2 周）→ Phase 2（双工具 API + GitLab Webhook 关联分析，给出置信区间，2-4 周）→ Phase 3（Git AI 行级归因 + Agent Trace 跟踪评估，可选）

**一个关键警告**：

> "目前大家在业界看到的'代码生成率'指标，基本都是不置信的。" — 快手 AI 研发团队

业界头部数据：DX 报告 22% 合并代码为 AI 生成、GitClear 分析 2.11 亿行得出 26.9%、腾讯报 50%（统计口径未详细披露）。不同口径结果差异巨大，报告中**必须明确标注统计口径**。

**Cursor 对标发现**：Cursor 团队版使用**客户端哈希签名匹配**（本地 SQLite 存储 AI 输出签名，commit 时比对 diff），不依赖 git 标记，在 GitLab 自托管下反而**比 Claude Code 更容易落地**。但其偏高估的归因倾向（AI 标签在改写后仍保留）与 Claude Code 的保守策略形成鲜明对比——**正因如此，双工具组合反而能提供上下界更可信的置信区间**。Cursor 还推动了 **Agent Trace** 开放标准，已获 Devin、Cloudflare、Vercel 等支持。

---

## 背景与需求

公司正在使用自托管 GitLab 服务器，需要建立一套可量化的 AI Coding 统计体系，回答核心问题：**团队中有多少代码是由 AI 辅助生成的？** 本调研聚焦 Claude Code Team 订阅版的能力边界，同时覆盖业界通用方案和自托管 GitLab 的适配路径。

---

## 一、Claude Code Team 原生统计能力

Claude Code Team/Enterprise 提供 **四个数据通道**，从粗到细覆盖不同统计需求。

### 1.1 Co-Authored-By Git Trailer（提交级标记）

Claude Code 创建 git commit 时，默认在 commit message 末尾追加：

```
Generated with Claude Code

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

- GitHub 会将 Claude 识别为共同作者并展示在 commit 页面
- Trailer 中包含使用的具体模型名（Sonnet 4.6 / Opus 4.6 等）
- **可配置**：在 `settings.json` 中自定义或禁用

```json
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

设为空字符串 `""` 可完全禁用。配置作用域覆盖用户级、项目级、本地级和管理员托管级。

**可行性评估**：这是最简单的 AI 代码识别机制，但仅提供 commit 级标记，无聚合分析能力。对于 GitLab 自托管环境，**这是最容易落地的切入点**。

> 来源：[Claude Code Settings - Attribution](https://code.claude.com/docs/en/settings)、[How to Use Git with Claude Code](https://www.deployhq.com/blog/how-to-use-git-with-claude-code-understanding-the-co-authored-by-attribution)

### 1.2 Analytics Dashboard（Web 管理看板）

Team/Enterprise 管理员可访问 `claude.ai/analytics/claude-code` 查看：

**使用指标**：
- Lines of code accepted（采纳的代码行数）
- Suggestion accept rate（编辑/写入/Notebook 建议的采纳率）
- 每日活跃用户与会话数
- 随时间变化的采纳趋势

**贡献指标**（Public Beta，需 GitHub 集成）：
- 有/无 Claude Code 协助的 PR 合并数
- 有/无 Claude Code 协助的代码提交行数
- 每个用户的 PR 数量
- Top 10 贡献者排行
- 全量 CSV 数据导出

**归因算法逻辑**：
1. PR 合并时提取 diff 中的新增行
2. 匹配在时间窗口内（合并前 21 天至合并后 2 天）编辑过相同文件的 Claude Code 会话
3. 行级匹配：归一化后比对（去首尾空格、合并多空格、统一引号、转小写）
4. 匹配成功的 PR 自动打上 `claude-code-assisted` 标签
5. 自动排除锁文件、构建产物、protobuf 输出、压缩文件、超 1000 字符的行

**关键限制**：
- 贡献指标**仅支持 GitHub**，不支持 GitLab
- 启用 Zero Data Retention 的组织不可用
- 归因是保守的：被开发者大幅改写（>20% 差异）的代码不计入 AI 贡献

> 来源：[Track team usage with analytics](https://code.claude.com/docs/en/analytics)、[Contribution Metrics](https://claude.com/blog/contribution-metrics)

### 1.3 Analytics API（程序化接口）

`GET /v1/organizations/usage_report/claude_code` 提供每日、每用户粒度的结构化数据。

```bash
curl "https://api.anthropic.com/v1/organizations/usage_report/claude_code?\
  starting_at=2025-09-08&limit=20" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ADMIN_API_KEY"
```

**返回字段**：

| 类别 | 字段 |
|------|------|
| 维度 | `date`, `actor`(email), `organization_id`, `terminal_type` |
| 核心 | `num_sessions`, `lines_of_code.added/removed`, `commits_by_claude_code`, `pull_requests_by_claude_code` |
| 工具动作 | `edit_tool.accepted/rejected`, `write_tool.accepted/rejected` 等 |
| 模型维度 | 每模型: `tokens.input/output/cache_read`, `estimated_cost.amount`(美分) |

- 日聚合，游标分页（每页最多 1000 条）
- 数据延迟约 1 小时
- 仅追踪 1st-party Claude API 调用（不含 Bedrock/Vertex AI）

**可行性评估**：**与 git 平台无关**，即使使用 GitLab 也能获取 Claude Code 侧的使用数据。可以回答"谁在用 Claude Code？用了多少？"但无法精确回答"最终入库的代码中多少来自 AI"。

> 来源：[Claude Code Analytics API](https://platform.claude.com/docs/en/build-with-claude/claude-code-analytics-api)

### 1.4 OpenTelemetry 监控（实时遥测）

Claude Code 原生支持 OTLP 导出，是粒度最细的监控选项。

**指标示例**：

| 指标 | 说明 |
|------|------|
| `claude_code.lines_of_code.count` | 新增/删除行数 |
| `claude_code.commit.count` | 创建的 commit 数 |
| `claude_code.pull_request.count` | 创建的 PR 数 |
| `claude_code.cost.usage` | 会话成本（USD） |
| `claude_code.code_edit_tool.decision` | 采纳/拒绝决策 |

**企业级托管部署**（通过 MDM 分发，用户不可覆盖）：

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.example.com:4317"
  }
}
```

兼容 Prometheus、Grafana、Datadog、Honeycomb、ClickHouse 等所有 OTLP 后端。

**可行性评估**：**最推荐的企业级方案**。与 git 平台完全解耦，可以在 Grafana 中构建团队级 AI 使用看板。但同样只能统计 Claude Code 侧数据，无法与最终入库代码精确关联。

> 来源：[Claude Code Monitoring](https://code.claude.com/docs/en/monitoring-usage)、[Claude Code + Grafana](https://quesma.com/blog/track-claude-code-usage-and-limits-with-grafana-cloud/)

---

## 二、Claude Code 原生方案的局限性

| 能力 | 能否在 GitLab 自托管环境使用 |
|------|---------------------------|
| Co-Authored-By trailer | **可以** — 纯 git 机制，与平台无关 |
| Analytics Dashboard 贡献指标 | **不可以** — 仅支持 GitHub |
| Analytics API | **可以** — 统计 Claude Code 侧数据，与 git 平台无关 |
| OpenTelemetry | **可以** — 与 git 平台完全解耦 |

**核心差距**：Claude Code 的原生统计只覆盖"AI 工具端"的数据，无法直接回答"最终入库到 GitLab 的代码中，多少行来自 AI"。需要将 Claude Code 侧数据与 GitLab 侧数据**关联**才能得到完整图景。

---

## 三、Cursor 团队版的统计机制（对比参考）

Cursor 的 AI 代码统计与 Claude Code 采用了**完全不同的技术路径**，是目前 IDE 类工具中统计粒度最细的方案，值得深入拆解作为对标参考。

### 3.1 核心机制：客户端哈希签名匹配

Cursor 的追踪**不依赖 git 标记**（不添加 Co-Authored-By），而是在 IDE 侧完成全部归因计算：

```
AI 生成代码 → 哈希签名存入本地 SQLite → 用户 commit 时比对 diff → 计算归因比例 → 同步到 Cursor 服务器
```

**具体流程**：

1. **生成时记录**：每次 AI 生成代码（Tab 补全或 Composer/Agent），Cursor 对生成的行创建哈希签名
2. **本地存储**：签名存入 `~/.cursor/ai-tracking/ai-code-tracking.db`（SQLite，通常 4-8 MB）
3. **提交时比对**：用户 commit 时，Cursor 拦截 diff，将变更行与存储的 AI 签名比对
4. **三分类归因**：每行代码被归为 `tabLines`（Tab 补全）、`composerLines`（Composer/Agent）、`nonAiLines`（人工）
5. **上报服务器**：归因结果同步至 Cursor Dashboard

### 3.2 本地数据库结构（逆向工程揭示）

`ai-code-tracking.db` 包含 6 张表，核心两张：

**`ai_code_hashes` — AI 输出签名表**：

| 字段 | 说明 |
|------|------|
| `hash` | AI 输出的哈希签名（主键） |
| `source` | 来源类型：`"composer"` / `"autocomplete"` |
| `model` | 使用的模型：`"claude-4.5-sonnet"` / `"gpt-4o"` 等 |
| `fileExtension` | 文件扩展名 |
| `conversationId` | 关联的对话 ID |
| `timestamp` | 生成时间 |

**`scored_commits` — 已评分提交表**：

| 字段 | 说明 |
|------|------|
| `commitHash` + `branchName` | 联合主键 |
| `tabLinesAdded/Deleted` | Tab 补全贡献行数 |
| `composerLinesAdded/Deleted` | Composer/Agent 贡献行数 |
| `humanLinesAdded/Deleted` | 人工贡献行数 |
| `v1AiPercentage` / `v2AiPercentage` | AI 贡献比例（两个版本的算法） |

> `v1` / `v2` 的存在说明 Cursor 已迭代过评分算法，社区曾报告历史指标变化。

> 来源：[I Reverse-Engineered Cursor's AI Agent (DEV Community)](https://dev.to/vikram_ray/i-reverse-engineered-cursors-ai-agent-heres-everything-it-does-behind-the-scenes-3d0a)

### 3.3 Dashboard 提供的指标

| 图表 | 度量内容 |
|------|---------|
| **AI Share of Committed Code** | AI 贡献行占提交代码的百分比（Tab + Composer vs Human） |
| **Agent Edits** | Agent/Cmd+K 的代码修改量及采纳率 |
| **Tab Completions** | Tab 补全次数 |
| **Messages Sent** | 按模式和模型分类的用户消息数 |
| **Active Users** | 每日活跃用户 |
| **Repository Insights** | 按仓库的 AI 代码占比 |
| **Usage Leaderboard** | 按用户排名（chat 数、Tab 次数、Agent 行数） |

- 支持按用户（最多 10 人）、AD 组、日期范围（最多 90 天连续）、时区过滤
- Enterprise 额外提供 **Conversation Insights**：将对话分类为 Bug 修复、重构、代码解释等

### 3.4 API 层次

| API | 可用版本 | 粒度 | 关键字段 |
|-----|---------|------|---------|
| **Team Analytics API** | Team ($40/人/月) | 团队聚合 | agent-edits、tabs、dau、models、leaderboard 等 12 个端点 |
| **AI Code Tracking API** | Enterprise only (alpha) | 每 commit、每 change | `tabLinesAdded`、`composerLinesAdded`、`nonAiLinesAdded`、`model`、per-file 明细 |

Enterprise 的 AI Code Tracking API 还提供 **commit 详情端点**：返回 `rangeAnnotations`（文件级 blame 数据）和关联的 `conversations`（含标题、摘要、TLDR）。

### 3.5 关键限制

| 限制 | 影响 |
|------|------|
| **同机要求** | 必须在生成 AI 代码的同一台机器上 commit，否则归因丢失 |
| **仅 Cursor 内提交** | 外部终端、其他 IDE、GUI 工具的 commit 不被追踪 |
| **格式化干扰** | 自动格式化工具（Prettier 等）运行后，AI 签名失效 |
| **过度归因倾向** | AI 生成的代码即使被大幅改写，仍保留 AI 标签 |
| **单工作区限制** | 多根工作区只追踪第一个项目 |
| **隐私问题** | 企业订阅下遥测无法关闭，包括个人侧项目也会被收集 |

### 3.6 Cursor vs Claude Code：两种统计哲学

| 维度 | Cursor | Claude Code |
|------|--------|-------------|
| **追踪时机** | **生成时**（前向匹配到 commit） | **合并时**（后向匹配到会话） |
| **追踪机制** | 客户端哈希签名 + 本地 SQLite | 服务端会话-PR diff 匹配 |
| **git 标记** | **无** — 不修改 git 历史 | **有** — Co-Authored-By trailer + PR 标签 |
| **归因粒度** | 行级、每 commit、每 change、含模型+来源 | PR 级（GitHub）；commit 级仅限 trailer |
| **归因倾向** | **偏高估** — AI 标签在改写后仍保留 | **偏保守** — 改写 >20% 则不归因 |
| **格式化韧性** | **差** — 格式化后签名失效 | **好** — 归一化空格/引号/大小写后匹配 |
| **平台依赖** | 无 — IDE 遥测，与 git 平台无关 | GitHub — 贡献指标需 GitHub App |
| **GitLab 自托管** | **可用**（IDE 遥测不依赖平台） | **部分可用**（API+OTEL 可用，贡献指标不可用） |
| **隐私控制** | 企业版无法关闭 | 可配置禁用归因 |

**核心洞察**：

- Cursor 的方案在 **GitLab 自托管环境下反而有优势** — 其追踪完全基于 IDE 遥测，不需要 git 平台集成
- 但 Cursor 的 **精确度存疑** — 格式化干扰 + 过度归因会导致数据偏高
- Claude Code 的方案更 **保守可信** — 但在 GitLab 下损失了最强大的 PR 级归因能力
- 如果团队同时使用两个工具，需要 Git AI 或 Agent Trace 等**跨工具方案**来统一归因

### 3.7 Agent Trace：Cursor 推动的行业开放标准

2026 年 1 月，Cursor 发布了 **Agent Trace** 规范，试图建立跨工具的 AI 代码归因标准：

- **行级精度**，4 种贡献者类型：`human`、`ai`、`mixed`、`unknown`
- **模型标识**：`provider/model-name` 格式（如 `anthropic/claude-opus-4-5`）
- **内容哈希**：`murmur3:9f2e8a1b`，位置无关追踪
- **多 VCS 支持**：git、Jujutsu、Mercurial、SVN
- **已获支持**：Cursor、Cognition (Devin)、Cloudflare、Vercel、git-ai、Google Jules、Amp、OpenCode

如果 Agent Trace 成为事实标准，将解决当前各工具归因机制不兼容的问题。**Claude Code 目前未加入**，值得关注后续动向。

> 来源：[Agent Trace 规范](https://agent-trace.dev/)、[GitHub: cursor/agent-trace](https://github.com/cursor/agent-trace)

---

## 四、业界 AI Coding 度量方法论（含 Cursor 对照）

### 4.1 快手：严格编辑距离法

快手 AI 研发团队提出了目前**公开披露最严格的企业级度量方法**：

- **分母**：新增代码行 — 统计公司内所有最终入库的 Commit 中的代码行
- **分子**：将分母的每一行代码与 AI 生成的代码比对，编辑距离 < 50%（相似度高）则纳入统计
- 实现路径：需要代码平台 + AI 编程工具**双端数据**在离线数据层进行精确计算
- 结果：从 1% 达到 30%+，部分业务线达到 40%+

快手同时揭示了一个重要不等式：**"用 AI 工具 ≠ 个人提效 ≠ 组织提效"** — 大部分工程师虽然主观感受编码效率提升 20-40%，但并没有接纳更多需求，交付数未显著提升。

> 来源：[快手 AI 研发范式升级 - InfoQ](https://www.infoq.cn/article/9rX1Ov951gKtaTmQb8Jq)

### 4.2 腾讯：CodeBuddy + WeDev 工具链统计

《2025 腾讯研发大数据报告》披露：
- 50% 的新增代码由 AI 辅助生成
- 超过 90% 的工程师使用 AI 编程助手 CodeBuddy
- AI 参与代码评审达 94%，其中 28% 缺陷由 AI 发现并被采纳
- 平均编码时间缩短 40%，整体研发效能提升超 20%

但**统计口径未公开详细披露**，可能是工具端采纳率而非入库代码行级匹配。

> 来源：[腾讯 2025 研发大数据报告](https://cloud.tencent.com/developer/news/3143570)

### 4.3 思码逸（Merico）：区分"接受"与"采纳"

思码逸提出了更精细的度量框架，区分两个容易混淆的概念：

- **接受（Accept）**：开发者在 IDE 中点击接受 AI 建议的动作
- **采纳（Adoption）**：AI 建议的代码最终入库并保留

两种生成占比指标：
- 行生成占比 = 采纳行数 / 新增行数
- 字符生成占比 = 采纳字符数 / 新增字符数

> 来源：[思码逸 AI 效能度量](https://www.merico.cn/blog/ai-metrics-and-measuring-ai-in-ee)

### 4.4 行业量化基准

| 来源 | AI 代码比例 | 统计方法 |
|------|-----------|---------|
| DX Q4 2025 Report (266 家企业) | **22%** 合并代码为 AI 生成 | 开发者调研 + 校准 |
| GitClear (2.11 亿行分析) | **26.9%** 生产代码为 AI 生成 | Git diff 分析 |
| Google | **25%** | 内部统计 |
| Microsoft | **20-30%** | 内部统计 |
| GitHub Octoverse 2025 | **46%** 新增代码 | 平台全量统计 |
| Stack Overflow 2025 | **84%** 开发者使用 AI 工具 | 全球开发者调研 |

> 来源：[DX Q4 Impact Report](https://getdx.com/blog/ai-assisted-engineering-q4-impact-report-2025/)、[GitClear 2025 Research](https://www.gitclear.com/ai_assistant_code_quality_2025_research)

### 4.5 行业研究的"反面数据"

| 来源 | 关键发现 |
|------|---------|
| METR 研究 (arXiv, 2025.07) | 开发者预估 AI 缩短 24% 完成时间，实测反而**变慢 19%** — 仅限资深开源开发者场景 |
| Faros AI Paradox Report | 高 AI 采纳团队完成多 21% 任务、合并多 98% PR，但 PR review 时间增加 91% |
| Cortex 2026 Report | AI 助手带来 20% PR 提升，但 incidents/PR 增加 23.5%，变更失败率增加 30% |
| Veracode 2025 GenAI Security Report | **45% 的 AI 代码样本未通过安全测试** |
| GitClear Code Churn | AI 采纳后代码复制粘贴首次超过代码移动，克隆量增长 4 倍 |

**共识**：单纯统计"AI 代码比例"是**虚荣指标**，需结合质量、交付速度、技术债务等多维度度量。60% 的工程领导者表示"缺乏清晰指标"是 AI 采纳最大挑战。

> 来源：[METR Study](https://arxiv.org/abs/2507.09089)、[Faros AI Report](https://www.faros.ai/blog/ai-software-engineering)、[Cortex Framework](https://www.cortex.io/post/a-framework-for-measuring-effective-ai-adoption-in-engineering)、[Veracode Report](https://www.veracode.com/blog/genai-code-security-report/)、[GitClear](https://www.gitclear.com/ai_assistant_code_quality_2025_research)

---

## 五、适配自托管 GitLab 的技术方案

### 方案 A：Co-Authored-By Trailer 解析（最小成本落地）

**原理**：解析 GitLab 中 commit message 的 `Co-Authored-By` trailer，识别 AI 参与的提交。

**实现路径**：

```
GitLab Push Webhook → 解析服务 → 分析 commit message → 写入数据库 → 看板展示
```

1. **确保 Claude Code 统一添加 trailer**：在项目级 `.claude/settings.json` 中配置

```json
{
  "attribution": {
    "commit": "Generated with Claude Code\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
  }
}
```

2. **GitLab Webhook 接收 push 事件**：push 事件 payload 包含 `commits[]` 数组，每个 commit 含 `message` 字段

3. **利用 GitLab Commits API 原生 Trailer 解析**：GitLab API 返回的 commit 对象自带 `trailers` 和 `extended_trailers` 字段，**无需手动解析 commit message**：

```python
import gitlab

gl = gitlab.Gitlab('https://git-inner.yunxuetang.com.cn', private_token=TOKEN)
project = gl.projects.get(PROJECT_ID)

for commit in project.commits.list(since='2026-03-01', per_page=100, iterator=True):
    # GitLab API 原生解析 trailers，无需正则
    trailers = commit.trailers or {}
    extended = getattr(commit, 'extended_trailers', {}) or {}

    co_authors = extended.get('Co-Authored-By', [])
    if not co_authors and 'Co-Authored-By' in trailers:
        co_authors = [trailers['Co-Authored-By']]

    is_ai = any('claude' in a.lower() or 'anthropic' in a.lower() for a in co_authors)
```

如果不想调用 API，也可以用纯 git 命令快速验证：

```bash
# 按 co-author 统计（含原始 author），一条命令看全貌
git shortlog -ns --group=author --group=trailer:co-authored-by --since='1 month ago'

# 只看 AI 参与的 commits
git log --grep="Co-authored-by: Claude" --oneline --since='1 month ago'

# 提取所有 AI trailer 并统计频次
git log --format='%(trailers:key=Co-Authored-By,valueonly)' | sort | uniq -c | sort -rn
```

4. **通过 GitLab API 获取 diff 行数**：`GET /api/v4/projects/:id/repository/commits/:sha`（commit 对象含 `stats.additions/deletions`）

5. **存入 PostgreSQL，Metabase/Grafana 展示**

**统计指标**：
- AI 参与 commit 占比 = 含 AI Co-Authored-By 的 commit 数 / 总 commit 数
- AI 参与代码行占比 = AI commit 中 additions 总行数 / 总 additions 行数
- 按人/团队/时间维度切分

**优点**：实现成本极低，一天可上线。**缺点**：将整个 commit 的所有改动都归因为 AI，粒度过粗；且开发者可能手动修改 AI 生成的代码后再提交。

### 方案 B：Git AI 工具（行级精确归因）

**[Git AI](https://github.com/git-ai-project/git-ai)** 是专为 AI 代码追踪设计的 git 扩展，提供全生命周期追踪。

**工作原理**：
- 支持的 AI 工具（包括 Claude Code、Cursor、Copilot、Codex、Gemini CLI 等）通过 pre/post edit hooks 报告生成的代码
- 每次 AI 编辑生成一个 checkpoint（小 diff），存储在 `.git/ai/` 中
- Commit 时将 checkpoints 整合为 Authorship Log，通过 **Git Notes** 附加到 commit
- 跨 rebase、merge、squash、cherry-pick 自动重写归因日志

**关键特性**：
- **不猜测** — 由 Agent 精确报告生成的行，而非启发式检测
- **Local-first** — 100% 离线工作，无需登录，无 filewatcher/keylogger
- **Git 原生** — 使用 Git Notes 开放标准，不污染 commit 历史
- **高性能** — 基于 git plumbing 命令，大仓库中 <100ms（已在 Chromium 测试）
- VSCode 集成：gutline 高亮 AI 生成代码，hover 展示使用的模型

**GitLab 兼容性**：Git Notes 是 git 原生功能，GitLab 支持。但需确认自托管 GitLab 的 Git Notes 同步策略（默认 `git push` 不推送 notes，需 `git push origin refs/notes/*`）。

**优点**：行级精确归因，业界目前精度最高的方案。**缺点**：需要在所有开发者机器上安装，有一定推广成本。

> 来源：[Git AI](https://github.com/git-ai-project/git-ai)、[usegitai.com](https://usegitai.com/)

### 方案 C：双工具 API + GitLab API 关联（推荐组合）

**原理**：将 Claude Code 和 Cursor 两侧的 API 数据与 GitLab 侧数据关联，构建**多数据源交叉验证**的全景视图。

```
Claude Code Analytics API    Cursor Team Analytics API    GitLab Commits API
         │                           │                          │
         └──────────────── 关联引擎 ──────────────────────────┘
                              │
                        关联维度：
                        - 用户（email 匹配）
                        - 时间窗口
                        - 文件路径
                        - Co-Authored-By trailer
                              │
                  聚合数据库 → 统一看板（Grafana）
```

**实现步骤**：

1. **定时拉取 Claude Code Analytics API 数据**：每日 cron，获取每个用户的 `lines_of_code.added`、`commits_by_claude_code`、会话数、成本

2. **定时拉取 Cursor Team Analytics API 数据**（$40/人/月即可用，无需 Enterprise）：
   - `GET /api/usage/ai-code` — 团队 AI 代码占比
   - `GET /api/usage/agent-edits` — Agent 编辑量及采纳率
   - `GET /api/usage/tabs` — Tab 补全次数
   - `GET /api/usage/leaderboard` — 按用户排名

3. **定时拉取 GitLab Commits API 数据**：`GET /api/v4/projects/:id/repository/commits`，获取入库代码行数

4. **关联逻辑**：
   - 按用户 email 匹配三方数据
   - Claude Code 侧：API 报告的 commits 数 + Co-Authored-By trailer 验证
   - Cursor 侧：Dashboard 报告的 AI 代码百分比（偏高估上界）
   - GitLab 侧：实际入库代码行数（真实分母）
   - **交叉校验**：Claude Code 保守数据为**下界**，Cursor 激进数据为**上界**，真实值在区间内

5. **计算指标**：
   - AI 使用渗透率 = 使用任意 AI 工具的开发者 / 全部开发者
   - AI 辅助代码行比例（区间估算）= [Claude Code 保守值, Cursor 上界值]
   - 人均 AI 使用成本与效能关联（两工具合计）
   - 工具偏好分布：Claude Code vs Cursor 使用占比

**优点**：利用双工具官方 API 交叉校验，比单工具更可信；不依赖 GitHub；提供置信区间而非单一数字。**缺点**：需同时维护两个 API 集成；Cursor API 需要 Team 订阅。

### 方案 D：SonarQube AI Code Assurance（代码质量视角）

SonarQube Server 2025.1+ 提供 **AI Code Assurance** 功能：

- 自动检测 GitHub Copilot 使用（当前仅支持 Copilot + GitHub）
- 项目级 "CONTAINS AI CODE" 状态标识
- 专门的 AI 代码质量门禁 "Sonar way for AI Code"
- 更严格的覆盖率（80%→90%）和重复率（3%→1%）阈值

**GitLab 适配性**：SonarQube 自托管版本可以与 GitLab 集成做代码质量分析，但 AI Code Assurance 的**自动检测功能目前仅支持 GitHub Copilot**。可以手动标记项目为"contains AI code"，但失去了自动化优势。

> 来源：[SonarQube AI Code Assurance](https://docs.sonarsource.com/sonarqube-cloud/ai-capabilities/ai-code-assurance)、[Auto-Detect AI-Generated Code](https://www.sonarsource.com/blog/auto-detect-and-review-ai-generated-code-from-github-copilot/)

### 方案 E：ai-code-tracker（轻量 Python 工具）

[ai-code-tracker](https://pypi.org/project/ai-code-tracker/) 是一个 PyPI 包，分析 Git 仓库中 AI vs 人类代码贡献。

**工作原理**：
- 通过 git 作者信息区分 AI commit 和人类 commit
- 需要配置独立的 git 作者信息用于 AI 提交
- 生成交互式图表（按日/周聚合）
- 支持 time-prompting 指标标注

**局限**：依赖于 commit 作者信息区分，如果 AI 和人共同编写的 commit 用同一作者，则无法区分。更适合作为辅助工具而非主方案。

### 方案 F：AgentBlame（开源 PR 级归因）

**[AgentBlame](https://github.com/mesa-dot-dev/agentblame)** 是一个开源工具，提供 PR 级别的 AI 归因：
- PR 摘要中添加 AI 贡献百分比 badge
- 文件级 AI 代码比例标注
- 行级 gutter 标记

适合作为 MR/PR 流程中的可视化补充。

### 方案 G：商业工程效能平台

| 平台 | AI 代码追踪能力 | GitLab 支持 | 定价模型 |
|------|----------------|-------------|---------|
| **Exceeds AI** | 仓库级 AI/人类代码分离、AI Usage Diff Mapping（PR 内行级标记）、30+ 天纵向追踪 | 支持（连接仓库） | 商业 |
| **Jellyfish** | 追踪 Copilot、Cursor、Gemini Code Assist 使用 | 支持 GitLab | 商业 |
| **DX (DevEx)** | AI Measurement Framework（与 GitHub/Dropbox/Atlassian 共建），跨 435 家企业 13.5 万开发者数据 | 支持 | 商业 |
| **GitClear** | Git diff 深度分析、代码 churn 追踪、AI 代码持久率、集成 Cursor/Copilot/Claude Code API | 支持 GitLab | 商业 |
| **LinearB** | Commit 级归因（AI 辅助 vs AI 生成 vs 人工）、DORA + SPACE、gitStream 工作流 | 支持 GitLab | 商业 |
| **Swarmia** | DORA/SPACE 指标，AI 工具采纳追踪 | 有限支持 | 商业 |
| **Opsera** | 统一 Cursor + Windsurf + Copilot 看板 | 支持 | 商业 |

**推荐关注**：
- **GitClear** 数据最扎实（2.11 亿行分析），已发布多份行业基准报告
- **DX** 框架最成熟，与头部公司共建，提供 Utilization + Impact + Cost 三维度量
- **Exceeds AI** 宣称可行级标记，但博客有较强营销倾向，需 POC 验证

> 来源：[Exceeds AI](https://blog.exceeds.ai/)、[Jellyfish AI Impact](https://thenewstack.io/jellyfish-tracks-ai-impact-across-four-major-coding-tools/)、[DX AI Measurement Hub](https://getdx.com/blog/ai-measurement-hub/)、[GitClear Research](https://www.gitclear.com/ai_assistant_code_quality_2025_research)、[LinearB Framework](https://linearb.io/blog/ai-measurement-framework)

### 方案 H：Cursor Team Dashboard 直读（零开发成本）

**前提**：团队同时使用 Cursor（Team $40/人/月）。

**原理**：Cursor 的 AI 代码统计完全基于 IDE 遥测，**不依赖 git 平台**。只要团队成员在 Cursor 内编码和提交，Dashboard 即自动显示 AI 代码占比——**无需任何开发工作**。

**直接可用的指标**：
- AI Share of Committed Code（按 Tab 补全 / Composer/Agent / 人工三分类）
- 按仓库的 AI 代码占比
- 按用户排名（chat 数、Tab 次数、Agent 行数）
- 每日活跃用户

**适用场景**：
- 团队已在使用或计划使用 Cursor → **直接启用 Dashboard，零开发成本获取 AI 代码统计**
- 作为快速验证手段：先用 Cursor Dashboard 建立基线数据，再投入开发自建方案

**关键注意**：
- Cursor 统计**偏高估**（AI 标签在改写后仍保留），不适合作为唯一数据源
- 仅追踪在 Cursor IDE 内完成的提交，外部终端/其他 IDE 的 commit 不计入
- 格式化工具（Prettier 等）可能干扰签名匹配
- Enterprise 版本提供更细粒度的 AI Code Tracking API（per-commit、per-file）

**优点**：**零开发成本**，开箱即用；commit 级粒度比 Claude Code 的 PR 级更细；不依赖 GitHub。**缺点**：仅覆盖 Cursor 内的编码活动；归因偏高估；Team 版 API 为团队聚合级，无 per-commit 明细。

### 方案 I：Agent Trace 开放标准（面向未来）

**原理**：采用 Cursor 主导的 Agent Trace 开放规范，建立跨工具的统一 AI 代码归因层。

**当前支持状态**（2026 年 3 月）：

| 工具 | Agent Trace 支持 |
|------|----------------|
| Cursor | 原生支持（规范发起者） |
| Devin (Cognition) | 已支持 |
| Cloudflare Workers AI | 已支持 |
| Vercel v0 | 已支持 |
| Git AI | 已支持 |
| Google Jules | 已支持 |
| Amp / OpenCode | 已支持 |
| **Claude Code** | **未支持** — 值得关注 |

**为什么值得关注**：
- 如果 Agent Trace 成为事实标准，将**一次性解决多工具归因不兼容问题**
- 行级精度 + 4 种贡献者类型（human/ai/mixed/unknown）+ 模型标识
- 基于内容哈希（murmur3），位置无关追踪
- 支持 git、Jujutsu、Mercurial、SVN

**现阶段建议**：
- **不建议现在投入开发**，标准仍在 alpha 阶段
- 持续关注 Claude Code 是否加入 Agent Trace 生态
- 若 Claude Code 加入，可替代方案 A-C 成为统一解决方案

> 来源：[Agent Trace 规范](https://agent-trace.dev/)、[GitHub: cursor/agent-trace](https://github.com/cursor/agent-trace)

---

## 六、推荐实施路线图

基于自托管 GitLab 环境、Claude Code Team + Cursor Team 双工具组合的约束，推荐**分阶段递进**：

### Phase 1：快速起步（1-2 周）

**目标**：回答"团队中谁在用 AI？用了多少？"

**Claude Code 侧**：
1. 统一配置 `settings.json`，确保所有用户开启 Co-Authored-By
2. 配置 OpenTelemetry 导出至公司 Prometheus/Grafana
3. 启用 Analytics API 定时拉取，写入数据库

**Cursor 侧**（如果团队同时使用）：
4. 启用 Cursor Team Dashboard — **零开发成本，直接获取 AI 代码占比**
5. Cursor Dashboard 数据作为**快速基线**：立即可见的 "AI Share of Committed Code"

**统一看板**：
6. Grafana 展示：Claude Code DAU/会话数/成本 + Cursor AI 代码占比基线

**交付物**：双工具 AI 使用看板（Cursor Dashboard 即开即用 + Claude Code Grafana 看板）

### Phase 2：关联分析（2-4 周）

**目标**：回答"入库代码中多少与 AI 相关？"（给出置信区间）

1. 部署 GitLab Push Webhook 监听服务
2. 解析 commit message 中的 Co-Authored-By trailer（Claude Code 标记）
3. 通过 GitLab API 获取 commit diff 行数
4. **双工具 API 关联**：
   - Claude Code Analytics API 数据（保守下界）
   - Cursor Team Analytics API 数据（激进上界）
   - GitLab commit 数据（真实分母）
5. **交叉校验计算**：AI 代码占比 = [Claude Code 保守值, Cursor 上界值] 区间
6. 扩展 Grafana 看板：AI commit 占比、AI 代码行**区间估算**、按团队/人/工具切分

**交付物**：AI Coding 多源关联分析看板（三方数据交叉验证）

### Phase 3：精确归因 + 标准化（可选，4-8 周）

**目标**：回答"具体哪些代码行来自 AI？"+ 建立长期统一标准

**精确归因（二选一）**：
1. 评估 Git AI 工具 POC — 在试点团队安装，**跨工具行级归因**（同时支持 Claude Code 和 Cursor）
2. 或评估商业平台 POC（GitClear / Exceeds AI）

**深度度量**：
3. 建立编辑距离比对服务（参考快手方法论）
4. 构建多维 AI 效能度量体系（比例 + 质量 + 交付速度 + 技术债务）

**面向未来**：
5. 持续关注 **Agent Trace** 开放标准 — 若 Claude Code 加入，可替代自建方案成为统一归因层
6. 评估 Cursor Enterprise AI Code Tracking API（per-commit、per-file 粒度）是否值得升级

**交付物**：行级 AI 代码归因系统 + Agent Trace 跟踪评估报告

---

## 七、统计口径对比

| 口径 | 定义 | 精度 | 归因倾向 | 实现难度 |
|------|------|------|---------|---------|
| **工具端采纳率** | AI 建议被用户 accept 的比例 | 低 — 不反映最终入库 | 偏高 | 最低（Claude Code 原生） |
| **commit 级归因** | 含 AI Co-Authored-By 的 commit 数占比 | 中 — 整个 commit 归因，粒度粗 | 取决于 commit 粒度 | 低（webhook + 解析） |
| **IDE 哈希签名匹配** | AI 输出哈希 vs commit diff 比对（Cursor 方案） | 中高 — 行级，但格式化干扰 | **偏高估** — 改写后仍保留 AI 标签 | 零（Cursor Dashboard 即开即用） |
| **服务端 PR 回溯匹配** | 合并时回溯匹配 AI 会话 diff（Claude Code 方案） | 中高 — 行级归一化匹配 | **偏保守** — >20% 改写不归因 | 零（仅限 GitHub） |
| **双工具区间估算** | Claude Code 保守值为下界 + Cursor 上界 = 置信区间 | 中 — 区间而非点值 | 上下界明确 | 中（双 API 关联） |
| **行级精确** | 逐行比对 AI 输出与入库代码（编辑距离 <50%） | 高 — 快手级严格度量 | 最准确 | 高（需双端数据+离线计算） |
| **行级报告** | AI Agent 主动报告生成的行（Git AI） | 最高 — Agent 精确标记 | 准确 | 中高（需推广安装） |
| **跨工具标准** | Agent Trace 开放规范（行级 + 模型标识） | 最高 — 跨工具统一 | 标准化 | 未来（标准 alpha 阶段） |

---

## 八、关键风险与注意事项

### 7.1 推荐度量指标体系

基于 DX 框架和业界最佳实践，建议追踪以下多维指标而非单一"AI 代码比例"：

| 类别 | 指标 | 为何重要 |
|------|------|---------|
| **采用率** | AI 工具 DAU/WAU | 基线利用率 |
| **归因** | AI 参与的 commit 占比 | 代码量级追踪 |
| **归因** | AI 参与的代码行占比 | 更细粒度追踪 |
| **质量** | AI 代码 Rework Rate（30 天内被修改的比例） | 衡量代码持久性 |
| **质量** | AI PR vs 人工 PR 的变更失败率 | 安全信号 |
| **速度** | 端到端 Cycle Time（非仅编码时间） | 避免"编码快、交付慢"陷阱 |
| **评审** | AI 代码 vs 人工代码的 review 时长 | 检测评审瓶颈 |
| **安全** | 密钥泄露率、漏洞密度 | AI 特有风险 |
| **成本** | 人均 AI 工具成本 | ROI 计算基础 |
| **业务** | 需求交付速度 | 唯一真正重要的指标 |

> 来源：[DX AI Measurement Framework](https://getdx.com/blog/how-to-implement-ai-measurement-framework/)

### 7.2 统计口径的可信度

> "目前大家在业界看到的'代码生成率'指标，基本都是不置信的，要么只统计了编程工具里的代码作为分子分母，要么在分母上做了限定。" — 快手 AI 研发团队

- 不同统计口径可能相差数倍，需在报告中**明确标注口径**
- 避免将工具端采纳率直接等同于"AI 代码比例"

### 7.3 AI 代码质量风险

研究数据显示：
- AI 生成代码引入的特权提升路径多 322%，设计缺陷多 153%（Exceeds AI）
- AI 辅助 PR 的问题数是人工 PR 的 1.7 倍（Cortex 2026 Report）
- AI 采纳后技术债务增加 30-41%

**建议**：AI 代码比例统计应与**代码质量指标联动**，避免产生"追求比例"的错误激励。

### 7.4 多工具覆盖与归因冲突

如果团队同时使用 Claude Code 和 Cursor（常见组合），需注意**两套归因体系的哲学冲突**：

| 维度 | Claude Code | Cursor | 冲突影响 |
|------|------------|--------|---------|
| 归因倾向 | 保守（>20% 改写不归因） | 激进（改写后仍保留 AI 标签） | 同一段代码两工具给出不同结论 |
| 追踪机制 | 服务端回溯匹配 | 客户端前向哈希 | 无法直接合并 |
| 数据范围 | 仅 Claude Code 生成 | 仅 Cursor 内生成 | 跨工具编辑不可追踪 |

**应对策略**：
- **短期**：分别统计，向管理层报告置信区间（Claude Code 下界 ~ Cursor 上界）
- **中期**：通过 Git AI 工具建立统一的行级归因（支持两工具）
- **长期**：关注 Agent Trace 标准是否被 Claude Code 采纳，实现真正的跨工具统一归因
- **永远不要**：简单相加两工具的数据（会重复计算）

### 7.5 GitLab 贡献指标的缺失

Claude Code 的 Contribution Metrics（最精确的官方归因）**当前仅支持 GitHub**。这是自托管 GitLab 环境的最大限制。建议关注 Anthropic 后续是否扩展 GitLab 支持。

---

## 参考资料

### Claude Code 官方文档
- [Track team usage with analytics](https://code.claude.com/docs/en/analytics)
- [Claude Code Analytics API](https://platform.claude.com/docs/en/build-with-claude/claude-code-analytics-api)
- [Claude Code Monitoring](https://code.claude.com/docs/en/monitoring-usage)
- [Claude Code Settings](https://code.claude.com/docs/en/settings)
- [Contribution Metrics Blog](https://claude.com/blog/contribution-metrics)

### 业界实践
- [快手 AI 研发范式升级 - InfoQ](https://www.infoq.cn/article/9rX1Ov951gKtaTmQb8Jq)
- [腾讯 2025 研发大数据报告](https://cloud.tencent.com/developer/news/3143570)
- [思码逸 AI 效能度量](https://www.merico.cn/blog/ai-metrics-and-measuring-ai-in-ee)
- [METR Study - AI Developer Productivity](https://arxiv.org/abs/2507.09089)
- [Faros AI Productivity Paradox](https://www.faros.ai/blog/ai-software-engineering)
- [Cortex AI Adoption Framework](https://www.cortex.io/post/a-framework-for-measuring-effective-ai-adoption-in-engineering)
- [DX Q4 2025 AI Impact Report](https://getdx.com/blog/ai-assisted-engineering-q4-impact-report-2025/)
- [DX AI Measurement Framework](https://getdx.com/blog/how-to-implement-ai-measurement-framework/)
- [GitClear 2025 AI Code Quality Research](https://www.gitclear.com/ai_assistant_code_quality_2025_research)
- [Veracode GenAI Security Report](https://www.veracode.com/blog/genai-code-security-report/)

### Cursor 官方文档
- [Cursor Team Analytics Dashboard](https://cursor.com/docs/account/teams/analytics)
- [Cursor Analytics API](https://cursor.com/docs/account/teams/analytics-api)
- [Cursor AI Code Tracking API (Enterprise)](https://cursor.com/docs/account/teams/ai-code-tracking-api)
- [Agent Trace Specification](https://agent-trace.dev/)
- [Agent Trace GitHub](https://github.com/cursor/agent-trace)
- [I Reverse-Engineered Cursor's AI Agent](https://dev.to/vikram_ray/i-reverse-engineered-cursors-ai-agent-heres-everything-it-does-behind-the-scenes-3d0a)

### 工具与平台
- [Git AI - Track AI Code](https://github.com/git-ai-project/git-ai)
- [AgentBlame - PR Level Attribution](https://github.com/mesa-dot-dev/agentblame)
- [ai-code-tracker (PyPI)](https://pypi.org/project/ai-code-tracker/)
- [SonarQube AI Code Assurance](https://docs.sonarsource.com/sonarqube-server/2025.1/instance-administration/analysis-functions/ai-code-assurance/quality-gates-for-ai-code)
- [Exceeds AI](https://blog.exceeds.ai/)
- [Jellyfish AI Impact](https://thenewstack.io/jellyfish-tracks-ai-impact-across-four-major-coding-tools/)
- [DX AI Measurement Hub](https://getdx.com/blog/ai-measurement-hub/)
- [LinearB AI Framework](https://linearb.io/blog/ai-measurement-framework)
- [GitClear Developer Productivity](https://www.gitclear.com/developer_ai_productivity_analysis_tools_research_2026)
- [Copilot Metrics Dashboard (开源)](https://github.com/microsoft/copilot-metrics-dashboard)

### GitLab 文档
- [GitLab Webhook Events](https://docs.gitlab.com/user/project/integrations/webhook_events/)
- [GitLab Commits API](https://docs.gitlab.com/api/commits.html)
- [GitLab Duo Self-Hosted](https://docs.gitlab.com/administration/gitlab_duo_self_hosted/)
- [GitLab 18.7 Release - Duo Analytics](https://about.gitlab.com/releases/2025/12/18/gitlab-18-7-released/)
- [python-gitlab Library](https://python-gitlab.readthedocs.io/en/stable/)
