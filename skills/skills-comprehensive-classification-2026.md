# Claude Skills 全方位指南：从框架开发到日常工具

> 全面整理 Claude Code Skills 生态，涵盖 Agent 框架、软件开发工作流、文档处理、前端设计、专业领域集成和日常生产力工具
> 数据来源：GitHub 实际验证 + SkillsMP 聚合平台 | 更新日期：2026-01-23

## 按应用场景分类

### 1. Agent框架与技能开发 🤖

| Skill名称 | 仓库Stars | 复杂度 | 仓库地址 | 核心能力 |
|-----------|----------|--------|-------------|----------|
| **skill-creator** | 50.6k | ⭐⭐⭐ | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | 把GitHub项目一键打包成Skill，几句命令就能封装工具 |
| **mcp-builder** | 50.6k | ⭐⭐⭐ | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) | 构建MCP服务器，让Claude能调用外部API和工具 |
| **confidence-check** | 20.4k | ⭐ | [SuperClaude-Org/SuperClaude_Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework/tree/master/.claude/skills/confidence-check) | 让Claude自己评估"这题我有几成把握"，避免瞎答 |
| **context-engineering** | 7.7k | ⭐⭐ | [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) | 优化Prompt设计，用更少的Token办更多的事 |

---

### 2. 软件开发工作流增强 💻

| Skill名称 | 仓库Stars | 复杂度 | 仓库地址 | 核心能力 |
|-----------|----------|--------|-------------|----------|
| **Superpowers** | 34.2k | ⭐⭐⭐ | [obra/superpowers](https://github.com/obra/superpowers) | 让Claude按TDD流程开发，先写测试再实现，2小时不跑偏 |
| **create-pr** | 170.8k | ⭐ | [n8n-io/n8n](https://github.com/n8n-io/n8n/tree/master/.claude/skills/create-pr) | 说"帮我提交这个功能"，自动跑测试、写标题、检查CI、建PR |
| **skill-lookup** | 143.3k | ⭐ | [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) | 像搜索引擎一样找Skill，"有没有xxx技能"一问就知道 |
| **frontend-code-review** | 127k | ⭐ | [langgenius/dify](https://github.com/langgenius/dify/tree/main/.claude/skills/frontend-code-review) | 审查前端代码，检查Hooks用对没、性能咋样、有无bug |
| **component-refactoring** | 127k | ⭐ | [langgenius/dify](https://github.com/langgenius/dify/tree/main/.claude/skills/component-refactoring) | 安全拆分React组件，把臃肿的组件整理得井井有条 |
| **planning-with-files** | 11k | ⭐ | [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | 改代码前先写规划文档，避免改到一半跑偏 |

---

### 3. 文档与知识管理 📚

| Skill名称 | 仓库Stars | 复杂度 | 仓库地址 | 核心能力 |
|-----------|----------|--------|-------------|----------|
| **docx** | 50.6k | ⭐ | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/docx) | 批量处理Word文档，填表单、改格式、合并文件 |
| **pdf** | 50.6k | ⭐ | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/pdf) | 提取PDF里的文字和表格，100份报告一分钟处理完 |
| **pptx** | 50.6k | ⭐ | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/pptx) | 说"帮我做个PPT"，自动生成带图表的幻灯片 |
| **xlsx** | 50.6k | ⭐ | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/xlsx) | 自动生成Excel公式、图表、透视表，数据分析不用手写公式 |
| **notebooklm** | 2.5k | ⭐⭐ | [PleasePrompto/notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill) | 给AI喂论文和报告，它带引用地回答问题 |
| **doc-coauthoring** | 50.6k | ⭐ | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring) | 像找个写作助手，从大纲到成稿全程辅助 |

---

### 4. 前端设计与UI/UX 🎨

| Skill名称 | 仓库Stars | 复杂度 | 仓库地址 | 核心能力 |
|-----------|----------|--------|-------------|----------|
| **UI-UX-Pro-Max-Skill** | 21.6k | ⭐ | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 描述需求，它给出布局建议、组件选择、交互细节 |
| **web-artifacts-builder** | 50.6k | ⭐ | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder) | 快速构建复杂Web组件，带状态管理的完整功能 |
| **frontend-design** | 50.6k | ⭐ | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | 生成高质量前端代码，避开AI同质化的审美 |
| **brand-guidelines** | 50.6k | ⭐ | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines) | 应用企业品牌规范，颜色字体统一不跑偏 |
| **theme-factory** | 50.6k | ⭐ | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/theme-factory) | 10种预设主题，一键切换暗色/亮色/品牌色 |
| **algorithmic-art** | 50.6k | ⭐ | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/algorithmic-art) | 用p5.js生成算法艺术，让AI帮你做创意设计 |

---

### 5. 专业领域与平台集成 🔧

| Skill名称 | 仓库Stars | 复杂度 | 仓库地址 | 核心能力 |
|-----------|----------|--------|-------------|----------|
| **cloudflare-skill** | 4.3k | ⭐⭐ | [cloudflare/cloudflare-docs](https://github.com/cloudflare/cloudflare-docs/tree/main/public/well-known/skills) | 60+Cloudflare产品一本通，Workers还是Pages它帮你选 |
| **dify-frontend-testing** | 127k | ⭐ | [langgenius/dify](https://github.com/langgenius/dify/tree/main/.claude/skills/frontend-testing) | 专为Dify平台优化的前端测试，自动化测试没烦恼 |

---

### 6. 日常生产力工具 🛠️

| Skill名称 | 仓库Stars | 复杂度 | 仓库地址 | 核心能力 |
|-----------|----------|--------|-------------|----------|
| **image-generator** | 50.6k | ⭐⭐ | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/image-generator) | AI生成图片，免费用Pollinations或付费DALL-E |
| **internal-comms** | 50.6k | ⭐ | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/internal-comms) | 自动生成企业内部沟通邮件、状态更新、周报 |
| **slack-gif-creator** | 50.6k | ⭐ | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/slack-gif-creator) | 制作Slack GIF动图，团队沟通更生动 |
| **webapp-testing** | 50.6k | ⭐ | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) | 用Playwright自动测试Web应用，点点点就能测 |

---

## 复杂度说明

### ⭐ 开箱即用
无需配置即可使用，Claude 可以直接应用这些技能。

### ⭐⭐ 配置后使用
需要一些配置或设置才能使用，例如环境变量、API密钥等。

### ⭐⭐⭐ 需要二次开发
需要编写代码或进行开发工作，例如创建自定义函数、集成外部服务等。

### ⭐⭐⭐⭐ 从零创建
需要完全从头开始创建，包括设计架构、编写完整代码等。

---

## Skills聚合平台 🌐

### SkillsMP - 最大的Skills市场

**基本信息**：
- **网址**：[skillsmp.com](https://skillsmp.com)
- **Skills数量**：84,192+
- **定位**：Agent Skills市场生态聚合平台

**核心功能**：
```
$ search --ai
智能搜索：用自然语言描述需求，AI帮你找到合适的Skill

$ cd /categories
分类浏览：12大分类（Tools/Development/Data-AI/Business等）

$ watch stats
趋势分析：查看24小时热门和增长趋势
```

**特色亮点**：
- 🤖 **AI语义搜索**：说"帮我找交易相关的skill"，它理解你想要什么
- 📊 **热度排行**：实时追踪Skill流行度（create-pr 170.6k热度排第一）
- 🏷️ **分类清晰**：Tools(28,400)、Development(24,633)、Data&AI(16,250)
- 🔗 **一键安装**：每个Skill都有GitHub源链接，复制即用
- 📈 **趋势图表**：可视化展示Skills增长趋势（2025年11月至今）

---

### skills.sh - 安装排行榜

**基本信息**：
- **网址**：[skills.sh](https://skills.sh)
- **定位**：Skills安装排行榜和命令行工具
- **安装命令**：`npx skills add <owner/repo>`

**核心功能**：
```
$ skills leaderboard
查看安装排行：TOP 200 Skills按安装量排序

$ npx skills add vercel-labs/agent-skills
一键安装：从GitHub直接安装Skill到你的Agent

$ skills trending
查看24小时热门：发现新晋热门Skills
```

**排行榜TOP 5**：
| 排名 | Skill | 安装量 | 来源仓库 |
|------|-------|--------|----------|
| 1 | vercel-react-best-practices | 33.1K | vercel-labs/agent-skills |
| 2 | web-design-guidelines | 25.1K | vercel-labs/agent-skills |
| 3 | remotion-best-practices | 13.3K | remotion-dev/skills |
| 4 | frontend-design | 4.3K | anthropics/skills |
| 5 | skill-creator | 2.7K | anthropics/skills |

**支持的Agent平台**：
- Claude Code、Cursor、GitHub Copilot
- OpenAI Codex、Gemini、Windsurf
- Cline、Roo、Droid等16+平台

---

### awesome-claude-skills - 精选列表

**基本信息**：
- **网址**：[github.com/ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- **Stars**：24.6k
- **定位**：人工精选的Skills资源列表

**核心价值**：
```
不是简单的聚合，而是经过验证的高质量Skills集合

✅ 每个Skill都经过人工审核
✅ 按功能分类（测试/调试/协作/文档等）
✅ 提供使用场景说明
✅ 持续更新，收录最新优质Skills
```

**分类结构**：
- **测试与质量**：TDD、代码覆盖率检查、测试驱动开发
- **调试与排障**：系统化调试、日志分析
- **协作与工作流**：Git提交、PR创建、代码审查
- **文档处理**：Word/PDF/PPT/Excel自动化

---

### 三大平台对比

| 平台 | Skills数量 | 核心价值 | 适合场景 |
|------|-----------|----------|----------|
| **SkillsMP** | 84,192+ | 市场聚合+AI搜索 | 搜索发现、查看热度、浏览分类 |
| **skills.sh** | 排行榜形式 | 安装排行+一键安装 | 看流行度、命令行安装 |
| **awesome-list** | 50+精选 | 人工精选+质量保证 | 找高质量Skill、学习参考 |

**使用建议**：
```
1. 探索发现 → 去 SkillsMP 用AI搜索
2. 看什么火 → 去 skills.sh 查看排行榜
3. 找精品 → 去 awesome-list 看精选推荐
4. 安装使用 → 三者都提供GitHub源链接
```

---

## 参考资源

| 类型 | 链接 |
|------|------|
| 官方文档 | [platform.claude.com/docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills) |
| 官方仓库 | [github.com/anthropics/skills](https://github.com/anthropics/skills) |
| Skills市场 | [skillsmp.com](https://skillsmp.com) |
| 中文社区 | [claudecn.com](https://claudecn.com) |
| 精选列表 | [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) |

---

*数据来源：GitHub API 实际验证（2026-01-23）+ SkillsMP 聚合平台*
