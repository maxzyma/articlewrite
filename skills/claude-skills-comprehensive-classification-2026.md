# Claude Skills 分类清单 (2026)

> 基于skills目录下的三篇核心文档整理
> 生成日期：2026-01-23

## 一、按应用场景分类

### 1. Agent框架与应用开发 🤖

| Skill名称 | Stars | GitHub/官网 | 核心能力 |
|-----------|-------|-------------|----------|
| **Superpowers** | 29.2k | [obra/superpowers](https://github.com/obra/superpowers) | TDD+YAGNI+DRY方法论全套 |
| **multi-agent-patterns** | 5.5k | SkillsMP | 多Agent架构模式设计 |
| **skill-creator** | 38.5k | 官方 | Skill创建向导 |
| **skill-writer** | 96k | SkillsMP | 生成高质量SKILL.md |
| **mcp-builder** | - | [官方文档](https://platform.claude.com/docs) | MCP服务器开发指南 |

### 2. 软件开发工作流增强 💻

| Skill名称 | 热度 | GitHub/官网 | 核心能力 |
|-----------|------|-------------|----------|
| **create-pr** | 169.7k | SkillsMP | 自动创建GitHub PR，格式化标题，CI校验 |
| **skill-lookup** | 142.6k | SkillsMP | 技能查找与安装 |
| **frontend-code-review** | 126.3k | SkillsMP | 前端代码审查（tsx/ts/js） |
| **component-refactoring** | 126.3k | SkillsMP | React组件重构 |
| **github-code-review** | 48.2k | SkillsMP | GitHub代码审查+AI协调 |
| **planning-with-files** | 10k | [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | 多文件任务持久化规划 |

### 3. 文档与知识管理 📚

| Skill名称 | Stars | GitHub/官网 | 核心能力 |
|-----------|-------|-------------|----------|
| **anthropics/skills** | 45.1k | [anthropics/skills](https://github.com/anthropics/skills) | 官方Skills集合（docx/pdf/pptx/xlsx） |
| **notebooklm** | - | [PleasePrompto/notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill) | 连接Google NotebookLM，带引用问答 |
| **doc-coauthoring** | - | 官方 | 文档协作工作流 |

**官方Skills详解**：
- **docx**: Word文档创建、编辑、追踪修改
- **pdf**: 文本/表格提取、合并、表单处理
- **pptx**: 演示文稿生成与调整
- **xlsx**: Excel公式、图表、数据转换

### 4. 前端设计与UI/UX 🎨

| Skill名称 | Stars | GitHub/官网 | 核心能力 |
|-----------|-------|-------------|----------|
| **UI-UX-Pro-Max-Skill** | 17.8k | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | UI/UX设计智能 |
| **web-artifacts-builder** | - | 官方 | 构建复杂Web组件（React+Tailwind+shadcn/ui） |
| **frontend-design** | - | 官方 | 高质量前端界面生成 |
| **brand-guidelines** | - | 官方 | Anthropic品牌规范应用 |
| **theme-factory** | - | 官方 | 10种预设主题系统 |
| **algorithmic-art** | - | 官方 | 算法艺术创作（p5.js） |

### 5. 专业领域与平台集成 🔧

| Skill名称 | 热度 | GitHub/官网 | 覆盖范围 |
|-----------|------|-------------|----------|
| **cloudflare-skill** | 2.8k | SkillsMP | 60+ Cloudflare产品 |
| **electron-chromium-upgrade** | 119.6k | SkillsMP | Electron Chromium版本迁移 |
| **dify-frontend-testing** | 124.9k | SkillsMP | Dify平台前端测试 |
| **zig-syscalls-bun** | 86k | SkillsMP | Bun运行时底层开发 |

### 6. AI/LLM开发优化 🧠

| Skill名称 | 热度 | GitHub/官网 | 核心能力 |
|-----------|------|-------------|----------|
| **cache-components-expert** | 137.2k | SkillsMP | LLM应用缓存策略优化 |
| **opus-4.5-migration** | 47.2k | SkillsMP | 升级到Claude Opus 4.5 |
| **confidence-check** | 19.8k | SkillsMP | 评估Claude回答可靠性 |
| **context-engineering** | 5.5k | SkillsMP | 优化Prompt设计 |
| **llm-project-methodology** | 5.5k | SkillsMP | AI项目最佳实践 |

### 7. 日常生产力工具 🛠️

| Skill名称 | 来源 | GitHub/官网 | 核心能力 |
|-----------|------|-------------|----------|
| **image-generator** | 官方 | 官方 | AI图片生成（Pollinations.ai/DALL-E） |
| **internal-comms** | 官方 | 官方 | 企业内部沟通模板 |
| **slack-gif-creator** | 官方 | 官方 | Slack GIF创作 |
| **webapp-testing** | 官方 | 官方 | Playwright Web应用测试 |
| **xlsx** | 官方 | [anthropics/skills](https://github.com/anthropics/skills) | Excel处理 |
| **pdf** | 官方 | [anthropics/skills](https://github.com/anthropics/skills) | PDF处理 |
| **pptx** | 官方 | [anthropics/skills](https://github.com/anthropics/skills) | PPT处理 |
| **docx** | 官方 | [anthropics/skills](https://github.com/anthropics/skills) | Word处理 |

---

## 二、按用户角色分类

### 👨‍💻 软件开发者

**必备组合**：
```
obra/superpowers              # 开发框架
├── create-pr                # PR自动化
├── frontend-code-review     # 前端审查
├── component-refactoring    # 组件重构
├── planning-with-files      # 任务规划
└── [平台专项]               # cloudflare/electron等
```

### 🎨 产品/设计人员

**设计工具箱**：
```
ui-ux-pro-max-skill          # UI/UX设计
├── frontend-design          # 前端代码生成
├── brand-guidelines         # 品牌规范
├── theme-factory            # 主题系统
├── image-generator          # AI图片
└── web-artifacts-builder    # 复杂组件
```

### 📊 内容/知识工作者

**文档处理**：
```
anthropics/skills            # 官方文档包
├── notebooklm               # 知识库问答
├── doc-coauthoring          # 文档协作
├── internal-comms           # 内部沟通
└── skill-creator            # 创建领域skill
```

### 🏢 企业管理者

**团队管理**：
```
superpowers                  # 统一开发规范
├── awesome-claude-skills    # 技能集合
├── skill-lookup             # 技能查找
├── create-pr                # 标准化Git流程
└── doc-coauthoring          # 协作文档
```

---

## 三、按技术复杂度分类

### Level 1: 开箱即用 ⭐

**无需配置，官方维护**
```
anthropics/skills (docx/pdf/pptx/xlsx)
├── image-generator
├── notebooklm
├── internal-comms
├── create-pr
└── skill-lookup
```

### Level 2: 配置后使用 ⭐⭐

**需要API密钥或领域知识**
```
cloudflare-skill             # Cloudflare API
notebooklm                   # Google账号
image-generator (DALL-E)     # OpenAI API
cache-components-expert      # LLM缓存知识
opus-4.5-migration           # Claude版本迁移
```

### Level 3: 需要二次开发 ⭐⭐⭐

**需要编写代码或深度定制**
```
superpowers                  # 配置团队规范
multi-agent-patterns         # 设计架构
mcp-builder                  # 开发MCP服务器
skill-creator                # 编写SKILL.md
skill-writer                 # 理解技能规范
```

### Level 4: 从零创建 ⭐⭐⭐⭐

**完全自定义，最大化灵活性**
```
使用skill-creator将GitHub项目打包为Skill
示例：yt-dlp、Pake、ArchiveBox、Ciphey
```

---

## 四、快速查找表

| 需求 | 推荐Skill | Stars/热度 | GitHub/官网 |
|------|-----------|-----------|-------------|
| 快速上手 | anthropics/skills | 45.1k | [GitHub](https://github.com/anthropics/skills) |
| 规范化开发 | obra/superpowers | 29.2k | [GitHub](https://github.com/obra/superpowers) |
| PR自动化 | create-pr | 169.7k | SkillsMP |
| 查找Skills | skill-lookup | 142.6k | SkillsMP |
| 前端设计 | ui-ux-pro-max-skill | 17.8k | [GitHub](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |
| 文档处理 | anthropics/skills | 45.1k | [GitHub](https://github.com/anthropics/skills) |
| Cloudflare | cloudflare-skill | 2.8k | SkillsMP |
| LLM优化 | cache-components-expert | 137.2k | SkillsMP |
| 学习参考 | awesome-claude-skills | 21.6k | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) |
| 创建Skill | skill-writer | 96k | SkillsMP |
| 知识库 | notebooklm-skill | 2.1k | [GitHub](https://github.com/PleasePrompto/notebooklm-skill) |
| 任务规划 | planning-with-files | 10k | [GitHub](https://github.com/OthmanAdi/planning-with-files) |

---

## 五、参考资源

| 类型 | 链接 |
|------|------|
| 官方文档 | [platform.claude.com/docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills) |
| 官方仓库 | [github.com/anthropics/skills](https://github.com/anthropics/skills) |
| Skills市场 | [skillsmp.com](https://skillsmp.com) |
| 中文社区 | [claudecn.com](https://claudecn.com) |
| 精选列表 | [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) |

---

*数据来源：skills目录下的三篇文档 + 2026年1月最新搜索结果*
