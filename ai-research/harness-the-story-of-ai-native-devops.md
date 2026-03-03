# Harness 前世今生：从 CD-as-a-Service 到 AI 原生 DevSecOps 平台

> 一个 AppDynamics 创始人的"二次创业"，如何用 8 年时间、8 次收购，构建出估值 55 亿美元的 DevOps 平台？

---

## 引言：代码写完之后的 60%

2025 年底，Harness 完成 2.4 亿美元 E 轮融资，估值 55 亿美元。融资公告里有一句话格外醒目：

**"AI for Everything After Code."**

这个定位精准地切中了一个被 AI coding 浪潮掩盖的事实——工程师 60-70% 的时间不是在写代码，而是在写完代码之后：测试、构建、部署、验证、安全扫描、成本管理、事故响应。当 GitHub Copilot 和 Cursor 们在拼命提升"写代码"的速度时，Harness 押注的是**代码之后的一切自动化**。

这不是一个偶然的定位。从 2017 年创立至今，Harness 的每一步都在为这个终局铺路。

---

## 一、创始人：从 37 亿美元退出到再次从零开始

### Jyoti Bansal 的 AppDynamics 传奇

故事要从 Jyoti Bansal 说起。

Bansal 出生于印度拉贾斯坦邦，在印度理工学院德里分校学习计算机科学，2000 年来到硅谷。一个常被提起的细节是：他想创业，但等了整整 7 年才拿到绿卡。这段经历让他成为美国 H-1B 移民政策讨论中的标志性案例。

2008 年，他创立了 AppDynamics，一个应用性能管理（APM）平台。公司发展迅猛，到 2016 年底已提交 IPO 申请，准备成为当年第一家上市的科技公司。

然后，戏剧性的一幕发生了。

2017 年 1 月，就在 IPO 路演即将开启的前几天，Cisco 突然出价 **37 亿美元**收购。Bansal 后来形容这段经历为"疯狂的过山车"——从准备敲钟上市到接受巨额收购，只用了几天时间。

### 为什么要再来一次？

拿到巨额回报后，Bansal 花了大约半年旅行放松。但他很快意识到自己并不想退休。他喜欢解决问题、构建产品、建立企业。

2017 年，他创立了 **BIG Labs**（Bansal Innovation Group），一个创业工作室。模式很简单：研究大问题领域，原型化解决方案，然后孵化成独立公司。

Harness 是 BIG Labs 孵化的第一个项目。

Bansal 观察到一个行业痛点：**为代码发布编写脚本已经成为一种"手工艺产业"（cottage industry）**。每家公司都在用 Jenkins、Shell 脚本、手工流程来管理部署，大量工作本应被自动化，却一直停留在手工阶段。更关键的是，没有人用机器学习来验证部署是否成功——所有验证都靠人盯仪表盘。

他找到了曾在苹果公司担任 DevOps 平台架构师的 **Rishi Singh**，两人联合创立了 Harness。

核心假设很清晰：**CD（持续交付）不应该是脚本拼凑的产物，而应该是一个智能化的平台服务。**

---

## 二、发展历程：从单点工具到全平台

### 2017-2019：CD-as-a-Service，找到立足点

2017 年 10 月，Harness 从隐身模式亮相，定位为 **CD-as-a-Service** 平台。

这个时期的核心差异点只有一个：**用机器学习验证部署**。传统工具在部署后需要人工检查日志、监控指标、确认服务健康——Harness 的 Continuous Verification（CV）模块用 ML 自动分析日志和指标，检测异常，自动触发回滚。

在 Jenkins 统治的 CI/CD 世界里，这是一个足够锐利的切入点。

2019 年，Harness 完成 6000 万美元 B 轮融资，Google Ventures 领投。这个阶段的 Harness 还是一个纯 CD 工具——但 Bansal 已经在规划平台化扩张。

### 2020-2021：平台化起步，从 CD 到 CI/CD

2020 年是关键转折年。Harness 做了创立以来最重要的一次收购：**Drone.io**。

Drone 由 Brad Rydzewski 于 2012 年创立，是容器原生的开源 CI 平台。在 DockerHub 上有 1 亿次以上拉取，5 万+ 活跃用户，社区用户包括 eBay、Capital One、Cisco。收购 Drone 意味着 Harness 从只做 CD 一跃成为 CI+CD 的完整交付平台。

同年，Harness 营收增长 400%。

2021 年，Harness 完成 8500 万美元 C 轮融资，估值 17 亿美元，正式成为独角兽。更重要的是，Harness 在这一年一口气推出了四个新模块：

- **Service Reliability Management (SRM)** —— SLO 管理和变更影响分析
- **Feature Flags** —— 功能开关
- **Security Testing Orchestration (STO)** —— 安全测试编排
- **Chaos Engineering** —— 混沌工程

从"CI/CD 工具"到"DevOps 平台"的野心暴露无遗。

### 2022-2024：收购驱动的版图扩张

如果说 2020 年收购 Drone 是"补短板"，那 2022-2024 年的收购策略就是"建护城河"。

| 时间 | 被收购方 | 金额 | 整合为 |
|------|---------|------|--------|
| 2021.09 | Lightwing | — | Cloud Cost Management 模块 |
| 2021.09 | Propelo (LevelOps) | — | Software Engineering Insights 模块 |
| 2022.03 | ChaosNative | — | Chaos Engineering 模块 (LitmusChaos) |
| 2024.01 | Armory | ~$7M | CD 能力增强 (Spinnaker 生态) |
| 2024.05 | Split Software | — | Feature Flags 模块 |

注意 Armory 的收购价格：**仅 700 万美元**。这是一家曾经融资超过 8000 万的 CD 公司，基于 Netflix 开源的 Spinnaker 构建。它的困境恰好说明了独立 CD 工具的生存困难——而 Harness 以极低成本吸收了它的客户和技术。

2022 年 4 月，Harness 完成 **2.3 亿美元 D 轮融资**，估值飙升至 **37 亿美元**。这个数字恰好与 AppDynamics 的收购价格持平——Bansal 的第二家公司在估值上追平了第一家。

到 2024 年底，Harness 的 ARR 达到 1.56 亿美元，拥有超过 1000 家企业客户，入选 **Gartner Magic Quadrant DevOps 平台领导者象限**。

### 2025-2026：合并 Traceable，冲刺 IPO

2025 年 3 月，Harness 与 Bansal 的另一家公司 **Traceable**（API 安全平台）完成合并。这不是一次简单的收购——Traceable 本身有独立的外部融资（1.1 亿美元），合并后 Harness 获得了完整的应用安全能力。

9 月，Harness 又收购了 **Qwiet AI**（前 ShiftLeft），补上了代码漏洞检测和可达性分析的最后一块拼图。

12 月，2.4 亿美元 E 轮融资落地，Goldman Sachs 领投，估值 **55 亿美元**。加上历次债务融资，Harness 的总融资额已超过 **8 亿美元**。

营收增长轨迹清晰地指向 IPO 窗口：

```
2021:  $32M
2022:  $80M   (+150%)
2023: $105M   (+31%)
2024: $156M   (+49%)
2025: $250M+  (预计 ARR)
```

---

## 三、产品全景：12 个模块覆盖完整 SDLC

今天的 Harness 已经从一个 CD 工具演变为拥有 12+ 模块的完整平台：

**软件交付层：**
- **Continuous Integration (CI)** —— 智能缓存、云构建、测试优化
- **Continuous Delivery & GitOps** —— 金丝雀/蓝绿部署、ML 验证、ArgoCD 集成
- **Code Repository** —— 内置代码托管（基于 Gitness）
- **Feature Flags** —— 功能开关与实验平台

**安全层：**
- **Security Testing Orchestration (STO)** —— SAST/DAST/SCA 编排
- **Software Supply Chain Assurance (SSCA)** —— 供应链安全
- **Application Security** —— API 安全 + 漏洞检测

**运维与洞察层：**
- **Cloud Cost Management (CCM)** —— 云成本可视化与优化
- **Chaos Engineering** —— 基于 LitmusChaos 的韧性测试
- **Service Reliability Management (SRM)** —— SLO 管理
- **Internal Developer Portal (IDP)** —— 基于 Backstage 的开发者门户
- **Software Engineering Insights (SEI)** —— 工程效率指标

**AI 层：**
- **AIDA** —— 贯穿全平台的 AI 开发助手

每个模块可以独立购买和使用，也可以组合成完整平台。这种**可组合架构（composable architecture）**是 Harness 区别于 GitLab 等"all-in-one"竞品的关键设计决策——企业可以逐步采纳，而不是被迫一次性迁移。

---

## 四、技术架构：为什么 ML 验证是核心壁垒

### Delegate 架构：解决企业安全合规

Harness 的架构设计有一个巧妙之处：**Harness Manager 是 SaaS 控制平面，而 Delegate 是部署在客户环境内的轻量级执行代理。**

Delegate 运行在客户的网络、集群或 VPC 内，负责连接代码仓库、基础设施、云提供商和制品库。所有敏感操作（拉取代码、部署到生产环境、访问密钥）都在客户侧完成，数据不出客户网络。

这种"控制平面 SaaS + 数据平面客户侧"的模式，完美解决了企业客户"想用 SaaS 的便利性，但不想把敏感数据交给第三方"的矛盾。这也是 Harness 能进入美国空军 Platform One 等高合规场景的关键。

### ML 驱动的 Continuous Verification

Harness 从第一天就把机器学习作为部署验证的核心，而不是事后添加的附加功能。系统能做到：

1. **自动分析部署日志**，关联错误消息与已知问题
2. **在构建发起前预测潜在错误**
3. **在金丝雀部署过程中实时检测异常**，自动触发回滚
4. **替代人工编写的验证脚本**

这是 Jenkins、GitHub Actions 等工具完全不具备的能力。当你的部署流水线每天执行数千次时，人工验证不可能覆盖每一次——ML 验证变成了规模化运维的刚需。

### Pipeline as Code + 模板系统

Harness 的流水线采用 YAML 定义，支持 Git 存储和 PR 管理。但更有价值的是它的**模板系统**：

平台团队可以创建可复用的部署模式，编码最佳实践和治理策略。当模板变更时，所有下游流水线自动继承更新。这解决了大型组织中"几百条流水线各自为战、无法统一治理"的经典问题。

---

## 五、开源策略：从 Drone 到 Gitness

Harness 的开源策略值得单独讨论，因为它经历了一次有趣的演变。

### Drone CI：开源 CI 的标杆

Drone.io 在被收购前已经是容器原生 CI 的代表作品。Harness 收购后承诺保持 Drone 的开源状态（Apache 2.0 许可），并将其作为 Harness CI 的社区版本运营。

### Gitness：从 CI 到端到端平台

2023 年，Harness 推出 **Gitness**，定位为 Drone 的下一代演进。但 Gitness 的野心远超 CI——它包含：

- Git 版本控制（代码托管）
- CI/CD Pipeline as Code
- 开发者环境（Gitspaces）
- 制品仓库（Artifact Registries）

换句话说，Gitness 要做一个开源的 GitHub/GitLab 替代品。这使得 Harness 在代码托管层与 GitHub 和 GitLab 形成了直接竞争。

### 开放核心模式

Harness 整体采用**开放核心（Open Core）**策略：核心基础能力开源（Gitness、LitmusChaos），企业级治理、安全、AI 功能和 SaaS 服务商业化。这是一个在基础设施软件领域被反复验证的商业模式——HashiCorp、GitLab、Elastic 都走过类似的路。

---

## 六、AIDA：AI 不是功能，是平台的底层逻辑

### 从工具到 Agent

2023 年，Harness 正式发布 **AIDA（AI Development Assistant）**。但 AIDA 不是一个独立产品——它是嵌入 Harness 全平台的 AI 能力层。

初始三大功能切中了开发者最痛的点：

1. **构建/部署失败辅助修复**：分析日志，关联已知问题，建议修复方案。不再需要人肉翻阅几百行报错日志。
2. **安全漏洞自动修复**：基于所有已知 CVE/CWE 训练，减少 50-75% 的漏洞修复工作量。
3. **自然语言云成本管理**：用自然语言定义云成本治理策略，而不是写复杂的 FinOps 规则。

2024-2025 年间，AIDA 的能力持续扩展到 Pipeline 编写、混沌工程实验设计、自动代码审查、AI SRE 等场景。

### Software Delivery Knowledge Graph

2025 年推出的**软件交付知识图谱**是 Harness AI 战略的技术基座。它将以下元素关联映射：

```
代码变更 → 服务 → 部署 → 测试 → 环境 → 事件 → 策略 → 成本
```

这个知识图谱为 AI Agent 提供了精确的上下文——当一个部署失败时，AI 不仅知道错误日志，还知道这次部署涉及哪些代码变更、影响哪些服务、在哪个环境、历史上类似的变更是否出过问题。

### 2026 年最新动态

2026 年初，Harness 推出了两个引人注目的 AI 功能：

**Human-Aware Change Agent**（1 月）：将人类在 Slack、Teams、Zoom 中的事件讨论作为运营数据的一等公民，转化为结构化信号，与生产故障的变更关联分析。这意味着 AI 不仅看代码和日志，还"听"人类的对话来辅助根因分析。

**可达性漏洞优先级排序**（2 月）：不是简单列出所有漏洞，而是根据漏洞是否真正可从应用代码路径到达来排序。一个存在于依赖库中但永远不会被你的代码调用的漏洞，优先级自然应该降低。AI 还能自动生成修复代码并开启 PR。

---

## 七、竞争格局：一张图看懂 DevOps 战场

| 维度 | Harness | Jenkins | GitLab CI/CD | GitHub Actions | ArgoCD |
|------|---------|---------|-------------|---------------|--------|
| **部署方式** | SaaS + 自托管 | 自托管 | SaaS + 自托管 | SaaS | 自托管 (K8s) |
| **CI** | 有 | 有 (核心) | 有 | 有 | 无 |
| **CD** | 有 (核心) | 插件 | 有 | 基础 | 有 (核心) |
| **AI 能力** | AIDA (全平台) | 无 | Duo (代码为主) | Copilot (代码为主) | 无 |
| **ML 部署验证** | 原生支持 | 无 | 无 | 无 | 无 |
| **安全** | STO + AppSec | 插件 | 内置 SAST/DAST | Dependabot + 第三方 | 无 |
| **成本管理** | CCM | 无 | 无 | 无 | 无 |
| **混沌工程** | LitmusChaos | 无 | 无 | 无 | 无 |
| **定价** | 模块化 | 免费 | 按用户 | 按分钟 | 免费 |

Harness 的竞争定位不是"更好的 Jenkins"或"更好的 GitLab CI"——而是**唯一一个在整个 SDLC 生命周期中深度嵌入 AI 的平台**。

- **vs. Jenkins**：Harness 是 Jenkins 的现代替代。AI 失败诊断是 Jenkins 完全没有的能力。
- **vs. GitHub Actions / GitLab CI**：Harness 不锁定于单一代码托管平台，支持多 VCS。企业可以同时使用 GitHub、GitLab、Bitbucket 而用 Harness 统一交付。
- **vs. ArgoCD**：Harness 既支持传统 Pipeline CD 也支持 GitOps，且提供商业支持和可视化界面。

---

## 八、8 次收购的战略逻辑

回顾 Harness 的 8 次收购，一个清晰的模式浮现：

```
2020  Drone.io          → CI 能力            ← 补核心短板
2021  Lightwing         → 云成本管理          ← 拓宽平台
2021  Propelo           → 工程效率洞察        ← 拓宽平台
2022  ChaosNative       → 混沌工程           ← 拓宽平台
2024  Armory ($7M)      → CD 增强 (Spinnaker) ← 低价吸收竞品
2024  Split Software    → Feature Flags       ← 补关键模块
2025  Traceable (合并)   → API 安全           ← 进入安全市场
2025  Qwiet AI          → 代码漏洞检测        ← 深化安全能力
```

每次收购都精准填补平台的一块空白。而且多数是以较低价格收购有技术实力但融资困难的公司——这是一个"等待行业洗牌、低价收购资产"的经典私募策略。

Armory 的案例尤其值得玩味：一家累计融资 8000 万美元的公司，最终以 700 万美元被收购。独立 CD 工具的生存空间已经被平台型玩家挤压殆尽。

---

## 九、对开发者和团队的意味

### 如果你是个人开发者

Harness 对你最有价值的部分可能是 **Gitness**（开源，免费）和 **Harness CI 社区版**（基于 Drone）。你可以自托管一套完整的 CI/CD 环境，不花一分钱。

### 如果你是平台工程团队

Harness 的**模板系统 + OPA 策略引擎 + IDP**组合，可能是目前最完整的平台工程解决方案。你可以定义标准化的部署模式，通过策略引擎强制执行，再通过开发者门户让业务团队自助使用。

### 如果你是技术决策者

Harness 的核心价值主张是**减少 SDLC 中"代码之后"环节的人工参与**。如果你的组织正在被"部署太慢、验证太慢、安全扫描太慢、事故响应太慢"困扰，Harness 的 AI 能力是值得评估的。

但也要注意：Harness 的完整平台在规模化后成本不低，模块定价的复杂性可能导致预算不可预测。建议从 1-2 个最痛的模块开始试用，而不是一次性采购全平台。

---

## 结语：二次创业者的平台化野心

Jyoti Bansal 的 Harness 故事，是一个教科书级的平台化扩张案例：

1. **从一个锐利的切入点出发**（ML 驱动的 CD 验证）
2. **通过收购快速补齐短板**（Drone → CI，ChaosNative → 混沌工程）
3. **用 AI 构建跨模块的统一差异化**（AIDA + Knowledge Graph）
4. **在行业洗牌期低价吸收竞品资产**（Armory $7M）

从 2017 年的 CD-as-a-Service 到 2026 年的"AI for Everything After Code"，Harness 用 8 年时间证明了一件事：**在 DevOps 领域，平台打败工具，智能打败脚本。**

而对于整个行业来说，Harness 的演进路径暗示了一个更大的趋势：当 AI coding 工具把"写代码"的效率推到极致后，**瓶颈会转移到代码之后的一切环节**。谁能用 AI 解决这些环节的自动化问题，谁就抓住了下一个十年的机会。

---

*参考资料：Harness 官方博客、TechCrunch、VentureBeat、Gartner Magic Quadrant for DevOps Platforms 2024、PR Newswire 融资公告。*
