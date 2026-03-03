# AI Coding 方式演进：从 Prompt Coding 到 Vibe Coding 再到 Spec Coding

> 代码不再是起点，也不再是终点。AI 编程正在经历一场关于"主对象"的范式迁移。

---

## 引言：我们到底在用 AI 怎么写代码？

2025 年，几乎所有开发者都在用 AI 写代码。但如果你仔细观察，会发现大家用的方式截然不同。

有人在 IDE 里按 Tab 接受 Copilot 的补全建议，逐行审阅每一处改动。有人在 Cursor 里用自然语言描述需求，跑起来看效果，不对就继续说，很少打开 diff 面板。还有人在项目里维护一份 spec 文档，让 AI Agent 按照规格一步步实施，像是在指挥一支自动化施工队。

这三种方式不是个人偏好的差异——它们代表了 AI 编程的三个演化阶段，背后是**人与 AI 协作方式的根本性变化**。

业界对此并非没有讨论。从 Vibe Coding 到 Spec Coding 的跃迁，已经是 2025 下半年以来的行业叙事主线——AWS 推出 Kiro 定位"Beyond Vibe Coding"，Martin Fowler 撰文探讨 Spec-Driven Development，Red Hat 将 SDD 与 Vibe Coding 做了系统对比。但大多数讨论要么聚焦于两两对比（Prompt vs Vibe，或 Vibe vs Spec），要么使用不同的切分维度（如 36 氪用"补全范式 vs Agent 范式"从技术架构层面划分）。

本文试图做的事情是：**将三者串成一条完整的演化链，并给出一个统一的分析轴——"主对象"变了。**

**Prompt Coding → Vibe Coding → Spec Coding**

每一次跃迁，变的不是工具，而是**谁在看代码、谁在负责、什么才是"第一现场"**。

---

## 一、为什么不是 Tab Coding 或 AI-assisted Coding？

在确定这条演化链之前，有两个候选名称需要排除。

### Tab Coding：太窄

"Tab Coding"听起来很形象——在编辑器里写代码，AI 给出 inline 补全建议，你按 Tab 接受。这确实是 GitHub Copilot 早期最典型的交互方式，GitHub 官方至今仍将这类能力描述为"inline suggestions"和"AI-powered pair programmer"。

但问题是，**Tab Coding 只是一种具体的交互动作**。它无法覆盖"在聊天框里让 AI 写一个函数""把报错信息贴给 AI 让它修""让 AI 解释一段遗留代码"这些同样属于早期 AI 编程的场景。用一个 UI 交互细节去命名一整个阶段，格局太小。

### AI-assisted Coding：太宽

"AI-assisted Coding"看似稳妥，但它是一个**总类**。Vibe Coding 是 AI 辅助的，Spec Coding 也是 AI 辅助的——你不能拿总类当作演化链的第一阶段。GitHub 文档本身就把 Copilot 统称为"AI coding assistant / coding agent"，这是一个跨越所有阶段的标签。

### 所以，Prompt Coding

**Prompt Coding** 抓住了第一阶段最核心的特征：**人开始通过 prompt 驱动代码生成，但代码仍然是第一工作对象，工程控制权仍主要在人手里。**

需要说明的是，"Prompt Coding"并非本文首创的术语——已有开发者在博客中使用过这个词来描述与 Vibe Coding 相对的编程方式。但它尚未形成行业共识级别的术语地位，也没有被放进一条三阶段演化链中使用。本文选择它，不是因为它新，而是因为它**精确**——它指向的是那个"人用 prompt 驱动 AI，但代码仍是第一现场"的阶段，不多不少。

---

## 二、三个阶段的深度拆解

### 阶段一：Prompt Coding

**一句话概括：Prompt 是输入手段，Code 是主战场。**

#### 定义

开发者通过 prompt、chat、补全建议等方式驱动 AI 产出代码，但代码本身仍是第一工作对象；人会频繁阅读、修改、拼接、验证生成结果，AI 主要扮演"高阶补全器 / 搭子 / 局部执行者"。

#### 典型状态

- 你让 AI 写一个函数、改一段逻辑、补测试、解释报错
- 你通常还是会看 diff、看代码、自己做集成
- 你的工作流主轴仍是 IDE + code review + 人工判断
- AI 是加速器，不是决策者

#### 典型工具形态

- GitHub Copilot（inline suggestions）
- ChatGPT / Claude 的代码对话
- IDE 内置的 AI Chat 面板
- 各种 AI 代码补全插件

#### 这个阶段的本质

开发者的心智模型没有变。你仍然在"写代码"，只是写得更快了。AI 像一个时刻在线的 pair programmer，你说一句它补一段，但**每一行代码最终都要过你的眼**。

这和 GitHub 对 Copilot 的定位完全吻合——即便在 2025 年 Copilot 已经具备 coding agent 能力，GitHub 官方文档仍然强调：开发者要 review、提交、合并与负责。

#### 典型风险

**局部快，全局乱。** 每个片段看着都对，但整体架构可能在不知不觉中走向混乱。因为 AI 在每次补全时没有全局视野，而开发者在享受加速快感时容易忽略整体一致性。

---

### 阶段二：Vibe Coding

**一句话概括：Intent 是主输入，Behavior 是主反馈，Code 退居后台。**

#### 定义

开发者主要用自然语言表达意图，不再持续细读代码，而是通过"跑起来看效果 → 继续改"的方式推进；关注体验和结果，多于关注实现细节。

#### 起源

这个词由 Andrej Karpathy 在 2025 年 2 月 2 日首次提出。他在 X 上描述了自己的编程状态：几乎不碰键盘，全程用语音对 Cursor Composer 描述需求，接受所有建议而不逐行审查 diff，遇到 bug 就把错误信息粘贴给 AI——代码不断增长，已经超出他个人的理解范围，但"它能跑"。随后他正式定义：

> There's a new kind of coding I call "vibe coding", where you fully give in to the vibes, embrace exponentials, and forget that the code even exists.

这条推文迅速走红。2025 年 3 月 Merriam-Webster 将"vibe coding"收录为俚语词条，Google Trends 显示相关搜索量增长了 2400%，Collins 英语词典更将其评为 2025 年度词汇。

Simon Willison 后续多次强调：Vibe Coding 不是泛指 AI 辅助编程，而是"生成代码但并不在意代码本身"的那种方式。

这个区分很重要。**不是所有用 AI 写代码的人都在 Vibe Coding——只有那些"不看代码、只看结果"的人才是。**

#### 典型状态

- 你用自然语言描述你想要的功能："加一个深色模式切换按钮"
- AI 生成了一堆代码，你不看代码，直接运行
- 效果对了，继续下一个需求；效果不对，用自然语言描述问题让 AI 再改
- 你可能完全不理解生成的代码是怎么工作的
- 你的反馈回路是：运行 → 观察 → 描述 → 再运行

#### 典型工具形态

- Cursor（Agent 模式）
- Bolt / Lovable / v0（一句话生成整个应用）
- Replit Agent
- Claude Code（交互式对话开发）

#### 这个阶段的本质

**代码不再是"第一现场"。** 开发者关注的是运行效果——页面长什么样、功能能不能用、交互对不对。代码变成了一种中间产物，就像编译器生成的汇编代码——你知道它在那里，但你不去看它。

这是一个心智模型的质变。在 Prompt Coding 阶段，你还是一个"写代码的人"；在 Vibe Coding 阶段，你更像一个"描述意图的人"。

#### 典型风险

**可维护性差，理解债务高。** Vibe Coding 天然适合原型、MVP、一次性项目。但如果你要长期维护一个系统，不理解代码就意味着你无法调试、无法重构、无法在 AI 犯错时纠正它。

Karpathy 自己也承认：Vibe Coding 适合"throwaway weekend projects"，不适合生产级系统。

---

### 阶段三：Spec Coding

**一句话概括：Spec 是源头，Code 是落实。**

#### 定义

开发不再直接从 prompt 或 vibe 开始，而是先形成 spec / requirements / design / tasks 等结构化约束，再由 AI 依据 spec 实施；spec 成为人和 AI 的共同源头与约束面。

#### 背景

Spec Coding 的出现是对 Vibe Coding 缺陷的直接回应。当人们发现 Vibe Coding 在原型之外难以为继时，一个自然的问题浮出水面：**如果不看代码，那靠什么保证系统的正确性和可维护性？**

答案是：**靠 spec。**

这个方向在 2025 下半年迅速获得了行业级的认可：

- **AWS 推出 Kiro**——一款 spec-driven 的 AI IDE，其名字取自日语"岐路"（きろ），象征传统开发与 AI 加速的交叉点。Kiro 将 SDD 工作流拆为三个支柱：Requirements（定义做什么）→ Design（设计怎么做）→ Tasks（分解执行计划），每一步都有结构化产出。InfoQ 的报道标题直接用了"Beyond Vibe Coding"。
- **Martin Fowler 发表 *Exploring Gen AI: Spec-Driven Development***——他将 SDD 进一步细分为三种模式：**spec-first**（先写 spec，实现后丢弃 spec）、**spec-anchored**（spec 保留供参考）、**spec-as-source**（spec 成为源头，代码可从 spec 重新生成）。Fowler 认为 spec-as-source 目前仍有些理想化，但行业正在向 spec-anchored 和 spec-as-source 之间收敛。
- **Red Hat Developer** 将 Vibe Coding 比作"爵士即兴——当时精彩，但撑不起一场巡演"，而 SDD 是让 AI 编码达到"95% 以上准确度"的工程化路径。
- **Atlassian** 在推出 Rovo Dev 时引用了 Fowler 关于"语义扩散"的警告，强调 SDD 的定义仍在快速漂移，需要警惕概念被滥用。
- **学术界** 也开始跟进——arXiv 上出现了题为 *Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants* 的论文（2026 年 1 月）。
- **中文社区** 同样活跃：36 氪/InfoQ 的年终盘点提出"Spec 正在蚕食人类编码"；独立开发者博客出现了"发散靠 Vibe，收敛靠 Spec"的两阶段工作流实践。

这不是偶然——这是整个行业在"vibe 不够用"之后的集体回应。

#### 典型状态

- 你先写（或和 AI 共同生成）一份 spec：需求、设计决策、任务分解、验收标准
- AI 按照 spec 逐步实施，每一步都有明确的输入约束和输出验证
- 你不需要逐行审阅代码，但你要审阅 spec 是否被正确遵守
- 测试是 spec 的可执行版本，自动验证实现与规格的一致性
- spec 不是一次性提示词，而是持续锚定实现与演进的核心文档

#### 典型工具形态

- Kiro（AWS 推出的 spec-driven AI IDE）
- Anthropic Claude Code + CLAUDE.md（spec 即 context）
- Cursor Rules / .cursorrules（项目级约束）
- AISDLC（AI Software Development Lifecycle 框架）
- 各种自定义的 spec → task → implement 工作流

#### 这个阶段的本质

**Spec 成为"第一现场"。** 开发者的核心工作从"写代码"或"描述意图"变成了"定义规格"。代码是 spec 的实现，测试是 spec 的验证，文档是 spec 的衍生物。

这看起来像是软件工程的"复古"——瀑布模型不也强调先有规格再实现吗？但关键区别在于：**传统的 spec 是人写给人看的，而 Spec Coding 的 spec 是人写给 AI 执行的。** 这意味着 spec 的颗粒度、结构化程度和可执行性要求远高于传统需求文档。

#### 典型风险

**前置成本高，流程更重。** 写 spec 需要时间和思考，这对于快速原型和探索性开发来说是一种负担。如果 spec 本身有误，AI 会忠实地实现一个错误的系统。此外，spec 的维护也是一个问题——系统演进时，spec 必须同步更新，否则就会变成误导性文档。

值得注意的是，36 氪的年终盘点对此有一个重要的澄清：**Spec 不等同于上下文工程（Context Engineering）**。Spec 是上下文中最关键的稳定部分——"一切用于指导代码生成的契约总和"，而 Context Engineering 是更广义的动态上下文管理。Spec 应被理解为"活的契约"，在 Plan-Execute 闭环中动态校准，而非前置的静态文档——"这反而比传统开发更接近工程真实状态"。

---

## 三、核心对比

### 一张表看清三个阶段

| 维度 | Prompt Coding | Vibe Coding | Spec Coding |
|------|--------------|-------------|-------------|
| **主输入** | prompt / 补全请求 | 意图 / 自然语言 | spec / requirements / tasks |
| **主工作对象** | code | behavior / outcome | spec + code（以 spec 为锚） |
| **主反馈方式** | 看代码、看 diff、跑测试 | 运行效果、界面观感 | 检查是否符合 spec、测试闭环 |
| **人的责任重心** | 写对代码、拼对实现 | 快速试错、结果导向 | 保证一致性、可追踪、可协作 |
| **AI 的角色** | 助手 / 补全器 / 搭子 | 实现代理 / 黑箱实现者 | 受约束的执行者 / 规格解释器 |
| **系统稳定性靠** | 人读代码、测代码 | 快速试错与体感验证 | 规格、分解、测试与追踪闭环 |
| **典型风险** | 局部快，全局乱 | 可维护性差、理解债务 | 前置成本高、流程更重 |
| **适合场景** | 日常开发、已有代码库维护 | 原型、MVP、一次性项目 | 团队协作、长期项目、生产系统 |

### 三条本质分界线

**第一条：代码是不是"第一现场"**

- Prompt Coding：**是**，代码就是第一现场，你在代码里工作
- Vibe Coding：**不是**，运行效果才是第一现场，代码是黑箱
- Spec Coding：**也不是**，spec 才是第一现场，代码是 spec 的落实

**第二条：AI 被当成什么**

- Prompt Coding：**助手**——你在写，它在帮你写得更快
- Vibe Coding：**代理**——你在说，它在替你做
- Spec Coding：**执行者**——你在定义规则，它在规则内执行

**第三条：系统稳定性靠什么保证**

- Prompt Coding：靠**人读代码、测代码**——传统工程能力仍是核心
- Vibe Coding：靠**快速试错与体感验证**——如果跑起来没问题就是没问题
- Spec Coding：靠**规格、任务分解、测试与追踪闭环**——形式化保证

---

## 四、这不是线性替代，而是光谱共存

一个常见的误解是：后一个阶段会"替代"前一个。事实并非如此。

**即使在 Spec Coding 成熟的今天，一个资深开发者的日常工作很可能同时使用三种方式：**

- 修一个小 bug → Prompt Coding（让 AI 补全修复代码，自己 review）
- 探索一个新 UI 方案 → Vibe Coding（快速生成几个版本，看哪个感觉对）
- 实现一个核心业务模块 → Spec Coding（先定义规格和测试，再让 AI 实施）

选择哪种方式取决于三个因素：

1. **项目的寿命**：一次性脚本 vs 长期维护的系统
2. **错误的代价**：内部工具 vs 面向用户的核心功能
3. **协作的需求**：个人项目 vs 团队协作

光谱的一端是最大自由度（Vibe Coding），另一端是最大可控性（Spec Coding），Prompt Coding 在中间提供了灵活的平衡点。

---

## 五、演化背后的深层逻辑

为什么 AI 编程会沿着这条路径演化？因为背后有一个更深的驱动力：**随着 AI 能力的增强，人类可以委托的粒度越来越大，但对约束机制的需求也随之增加。**

### 委托粒度的扩大

- Prompt Coding：委托的是**行级**和**函数级**的代码生成
- Vibe Coding：委托的是**功能级**和**页面级**的实现
- Spec Coding：委托的是**模块级**和**系统级**的工程落地

### 约束机制的升级

委托粒度变大，失控的风险也变大。每一次跃迁都需要新的约束机制来保证质量：

- Prompt Coding 的约束机制：**人工 code review**
- Vibe Coding 的约束机制：**运行时验证**（跑起来看）
- Spec Coding 的约束机制：**形式化规格 + 自动化测试**

这和软件工程的历史是同构的：从汇编到高级语言，从手工测试到自动化测试，从瀑布到敏捷——每一次抽象层级的提升，都伴随着新的约束机制的建立。AI 编程只是在重复这个模式，只不过这次被抽象掉的不是机器细节，而是代码本身。

### 与其他分析框架的关系

需要指出的是，本文的"Prompt → Vibe → Spec"并非唯一的切分方式。不同的分析维度会产出不同的框架：

- **36 氪用"补全范式 vs Agent 范式"**——这是从**技术架构**角度切的。补全范式受时延约束，模型规模和上下文长度受限；Agent 范式则"直接接管任务，从需求分析到代码生成、工具调用到结果验证"。
- **IBM Research 的 Ismael Faro 提出 "Objective-Validation Protocol"**——用户定义目标并验证，Agent 集群自主执行，在关键检查点请求人类批准。这是从**人机交互协议**角度切的。
- **Martin Fowler 在 Spec Coding 内部又分出三层**——spec-first / spec-anchored / spec-as-source，这是对 Spec 阶段本身的纵深拆解。

这些框架不矛盾，而是**互补**的。本文选择"主对象变了"这一轴，是因为它最直接地解释了**开发者日常体验的变化**——你到底在看什么、在改什么、在对什么负责。技术架构的变化（补全 vs Agent）是底层驱动力，人机协议的演化（prompt vs spec）是上层表现，而"主对象迁移"恰好在中间，连接了两者。

### 终极方向：Code as Artifact

如果延续这条演化线，一个可能的终局是：**代码完全变成一种中间制品（artifact）**——就像今天的字节码、IL 代码、编译产物一样，人类不再直接阅读和编写它。

人类的工作将完全发生在 spec 层：定义需求、设计约束、验收标准。AI 负责从 spec 到 code 的全部转换，并通过自动化测试保证一致性。

这正是 Martin Fowler 所说的"spec-as-source"——spec 不只是参考文档，而是**唯一的源头**，代码可以从 spec 重新生成。虽然 Fowler 认为这在当下仍有些理想化，但行业正在加速向这个方向收敛。

这不是科幻。这就是 Spec Coding 正在走向的方向。

---

## 六、对开发者的实际意义

### 如果你还在纯 Prompt Coding 阶段

你的工程能力仍然是核心竞争力，但你可能正在错过效率的巨大提升。尝试在低风险场景下放手让 AI 多做一些——不是每一行代码都需要你亲眼过目。

### 如果你正在享受 Vibe Coding

享受它带来的创造力释放，但要对它的边界保持清醒。Vibe Coding 是一种非常强大的探索工具，但它不是构建可靠系统的方法。当项目从原型走向产品时，你需要引入更多的结构和约束。

### 如果你正在实践 Spec Coding

你走在了前面。但要注意不要过度工程化——不是所有任务都需要完整的 spec 流程。关键是判断什么时候需要 spec 的严谨性，什么时候 vibe 的灵活性反而更合适。

### 对所有开发者

**最重要的能力变化是：从"写代码的能力"转向"定义问题的能力"。** 在 Prompt Coding 阶段，你需要知道怎么写代码；在 Vibe Coding 阶段，你需要知道你想要什么；在 Spec Coding 阶段，你需要精确地定义"什么是对的"。

这三种能力是递进的，而不是替代的。最好的开发者会同时掌握三种模式，并根据场景灵活切换。

---

## 结语：一句话总结

**Prompt Coding → Vibe Coding → Spec Coding**

代表 AI 编程从"代码中心的人控生成"，演化到"结果中心的高委托生成"，再演化到"规格中心的受约束生成"。

代码正在从"开发者的作品"变成"AI 的输出物"。在这个转变中，**定义"什么是对的"**比"怎么写代码"更加重要。

这不是代码的消亡。这是代码的归位——回到它本来就应该在的位置：一种实现手段，而非最终目的。

---

## 参考与延伸阅读

- Andrej Karpathy, ["Vibe Coding" 原始推文](https://x.com/karpathy/status/1886192184808149383), 2025-02-02
- Martin Fowler, [Exploring Gen AI: Spec-Driven Development](https://martinfowler.com/articles/exploring-gen-ai.html), 2025
- AWS, [Introducing Kiro: Agentic AI development from prototype to production](https://kiro.dev/blog/introducing-kiro/), 2025
- InfoQ, [Beyond Vibe Coding: Amazon Introduces Kiro, the Spec-Driven Agentic AI IDE](https://www.infoq.com/news/2025/08/aws-kiro-spec-driven-agent/), 2025
- Red Hat Developer, [How spec-driven development improves AI coding quality](https://developers.redhat.com/articles/2025/10/22/how-spec-driven-development-improves-ai-coding-quality), 2025
- Atlassian, [Spec-Driven Development with Rovo Dev](https://www.atlassian.com/blog/developer/spec-driven-development-with-rovo-dev), 2025
- Daniel Sogl, [Spec Driven Development (SDD): The Evolution Beyond Vibe Coding](https://danielsogl.medium.com/spec-driven-development-sdd-the-evolution-beyond-vibe-coding-1e431ae7d47b), Medium
- arXiv, [Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants](https://arxiv.org/html/2602.00180v1), 2026-01
- 36 氪 / InfoQ, [AI Coding 年终盘点：Spec 正在蚕食人类编码](https://36kr.com/p/3617659484013831), 2025
- xkcoding, [从 Vibe 到 Spec：我的 AI Coding 工作流](https://xkcoding.com/2026-01-22-vibe-to-spec-ai-coding-workflow.html), 2026-01
- Bobm, [Prompt Coding vs. Vibe Coding: Navigating the Future of AI-Assisted Development](https://medium.com/@bobm67/prompt-coding-vs-vibe-coding-navigating-the-future-of-ai-assisted-development-039d6946308c), Medium
- Wikipedia, [Vibe coding](https://en.wikipedia.org/wiki/Vibe_coding)

---

*写于 2026 年 3 月*
