# Skills 分类清单 (2026)

> 基于skills目录下的三篇核心文档整理
> 生成日期：2026-01-23

## 一、按应用场景分类

### 1. Agent框架与应用开发 🤖

| Skill名称 | Stars | GitHub/官网 | 核心能力 |
|-----------|-------|-------------|----------|
| **Superpowers** | 29.2k | [obra/superpowers](https://github.com/obra/superpowers) | 让Claude按TDD流程开发，先写测试再实现，2小时不跑偏 |
| **multi-agent-patterns** | 5.5k | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/multi-agent-patterns) | 设计多Agent协作系统，让AI们分工合作完成任务 |
| **skill-creator** | 38.5k | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | 把GitHub项目一键打包成Skill，几句命令就能封装工具 |
| **skill-writer** | 96k | [skillsmp.com](https://skillsmp.com) | 手把手教你写SKILL.md，从0到1创建自己的技能 |
| **mcp-builder** | - | [官方文档](https://platform.claude.com/docs) | 构建MCP服务器，让Claude能调用外部API和工具 |

### 2. 软件开发工作流增强 💻

| Skill名称 | 热度 | GitHub/官网 | 核心能力 |
|-----------|------|-------------|----------|
| **create-pr** | 169.7k | [skillsmp.com](https://skillsmp.com) | 说"帮我提交这个功能"，自动跑测试、写标题、检查CI、建PR |
| **skill-lookup** | 142.6k | [skillsmp.com](https://skillsmp.com) | 像搜索引擎一样找Skill，"有没有xxx技能"一问就知道 |
| **frontend-code-review** | 126.3k | [skillsmp.com](https://skillsmp.com) | 审查前端代码，检查Hooks用对没、性能咋样、有无bug |
| **component-refactoring** | 126.3k | [skillsmp.com](https://skillsmp.com) | 安全拆分React组件，把臃肿的组件整理得井井有条 |
| **github-code-review** | 126.3k | [skillsmp.com](https://skillsmp.com) | 多个AI协同审查代码，比自己review快3-5倍 |
| **planning-with-files** | 10k | [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | 改代码前先写规划文档，避免改到一半跑偏 |

### 3. 文档与知识管理 📚

| Skill名称 | Stars | GitHub/官网 | 核心能力 |
|-----------|-------|-------------|----------|
| **anthropics/skills** | 45.1k | [anthropics/skills](https://github.com/anthropics/skills) | 官方文档工具箱，Word/PDF/Excel/PPT一把梭 |
| **notebooklm** | - | [PleasePrompto/notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill) | 给AI喂论文和报告，它带引用地回答问题 |
| **doc-coauthoring** | - | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring) | 像找个写作助手，从大纲到成稿全程辅助 |

**官方Skills详解**：
- **docx**: 批量处理Word文档，填表单、改格式、合并文件
- **pdf**: 提取PDF里的文字和表格，100份报告一分钟处理完
- **pptx**: 说"帮我做个PPT"，自动生成带图表的幻灯片
- **xlsx**: 自动生成Excel公式、图表、透视表，数据分析不用手写公式

### 4. 前端设计与UI/UX 🎨

| Skill名称 | Stars | GitHub/官网 | 核心能力 |
|-----------|-------|-------------|----------|
| **UI-UX-Pro-Max-Skill** | 17.8k | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 描述需求，它给出布局建议、组件选择、交互细节 |
| **web-artifacts-builder** | - | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder) | 快速构建复杂Web组件，带状态管理的完整功能 |
| **frontend-design** | - | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | 生成高质量前端代码，避开AI同质化的审美 |
| **brand-guidelines** | - | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines) | 应用企业品牌规范，颜色字体统一不跑偏 |
| **theme-factory** | - | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/theme-factory) | 10种预设主题，一键切换暗色/亮色/品牌色 |
| **algorithmic-art** | - | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/algorithmic-art) | 用p5.js生成算法艺术，让AI帮你做创意设计 |

### 5. 专业领域与平台集成 🔧

| Skill名称 | 热度 | GitHub/官网 | 核心能力 |
|-----------|------|-------------|----------|
| **cloudflare-skill** | 2.8k | [skillsmp.com](https://skillsmp.com) | 60+Cloudflare产品一本通，Workers还是Pages它帮你选 |
| **electron-chromium-upgrade** | 119.6k | [skillsmp.com](https://skillsmp.com) | 升级Electron的Chromium版本，从老版本一键迁移 |
| **dify-frontend-testing** | 124.9k | [skillsmp.com](https://skillsmp.com) | 专为Dify平台优化的前端测试，自动化测试没烦恼 |
| **zig-syscalls-bun** | 86k | [skillsmp.com](https://skillsmp.com) | Bun运行时底层开发，系统调用级别的性能优化 |

### 6. AI/LLM开发优化 🧠

| Skill名称 | 热度 | GitHub/官网 | 核心能力 |
|-----------|------|-------------|----------|
| **cache-components-expert** | 137.2k | [skillsmp.com](https://skillsmp.com) | 优化LLM应用缓存，成本从$0.5降到$0.05，省90% |
| **opus-4.5-migration** | 47.2k | [skillsmp.com](https://skillsmp.com) | 升级到Claude Opus 4.5，API代码平滑迁移不踩坑 |
| **confidence-check** | 19.8k | [skillsmp.com](https://skillsmp.com) | 让Claude自己评估"这题我有几成把握"，避免瞎答 |
| **context-engineering** | 5.5k | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/context-engineering) | 优化Prompt设计，用更少的Token办更多的事 |
| **llm-project-methodology** | 5.5k | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/llm-project-methodology) | AI项目最佳实践，从立项到上线的完整指南 |

### 7. 日常生产力工具 🛠️

| Skill名称 | 来源 | GitHub/官网 | 核心能力 |
|-----------|------|-------------|----------|
| **image-generator** | 官方 | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/image-generator) | AI生成图片，免费用Pollinations或付费DALL-E |
| **internal-comms** | 官方 | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/internal-comms) | 自动生成企业内部沟通邮件、状态更新、周报 |
| **slack-gif-creator** | 官方 | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/slack-gif-creator) | 制作Slack GIF动图，团队沟通更生动 |
| **webapp-testing** | 官方 | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) | 用Playwright自动测试Web应用，点点点就能测 |
| **xlsx** | 官方 | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/xlsx) | 批量处理Excel，自动生成公式图表透视表 |
| **pdf** | 官方 | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/pdf) | 批量提取PDF文字和表格，100份报告1分钟处理完 |
| **pptx** | 官方 | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/pptx) | 说"帮我做个PPT"，自动生成带图表的幻灯片 |
| **docx** | 官方 | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/docx) | 批量处理Word文档，填表单、改格式、合并文件 |

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
| PR自动化 | create-pr | 169.7k | [SkillsMP](https://skillsmp.com) |
| 查找Skills | skill-lookup | 142.6k | [SkillsMP](https://skillsmp.com) |
| 前端设计 | ui-ux-pro-max-skill | 17.8k | [GitHub](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |
| 文档处理 | anthropics/skills | 45.1k | [GitHub](https://github.com/anthropics/skills) |
| Cloudflare | cloudflare-skill | 2.8k | [SkillsMP](https://skillsmp.com) |
| LLM优化 | cache-components-expert | 137.2k | [SkillsMP](https://skillsmp.com) |
| 学习参考 | awesome-claude-skills | 21.6k | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills) |
| 创建Skill | skill-writer | 96k | [SkillsMP](https://skillsmp.com) |
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
