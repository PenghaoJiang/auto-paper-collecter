<div align="center">

🌐 **简体中文** ｜ [English](./README.en.md)

# 📚🔭 auto-paper-collecter

### *你的私人学术雷达 · Your Personal Research Radar*

每天清晨，让 AI 替你逛遍 arXiv、把最新最相关的论文端到你面前 ☕✨

<br>

<img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI">
<img src="https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white" alt="SQLite">
<img src="https://img.shields.io/badge/LLM-powered-8A5CF6?logo=openai&logoColor=white" alt="LLM">
<img src="https://img.shields.io/badge/License-MIT-22c55e" alt="License">
<img src="https://img.shields.io/badge/PRs-welcome-ff69b4" alt="PRs Welcome">
<img src="https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F%20%26%20%E2%98%95-red" alt="Made with love">
<a href="https://skillhub.cn/skills/auto-paper-collecter"><img src="https://img.shields.io/badge/SkillHub-已上架-22c55e" alt="SkillHub"></a>

<br>
<sub>如果它帮你省下了刷 arXiv 的时间，欢迎点一个 ⭐ —— 这是对作者最大的鼓励！</sub>

</div>

---

## 🆕 最新更新 · What's New

### ✨ v1.1 — 体验与智能双升级 · 2026-06-27

<table>
<tr><td>🎨&nbsp;<b>体验</b></td><td>移动端自适应布局 · 精修<b>深色模式</b>（优雅深灰卡片，非纯黑）· 刷新<b>实时进度</b>（生成摘要 12/20…）</td></tr>
<tr><td>🧠&nbsp;<b>更聪明</b></td><td><b>👍/👎 反馈学习</b>（不喜欢的下次自动少推）· 最新 / 最早 / 来源排序 · 全部 / 未读 / 已读筛选</td></tr>
<tr><td>🛰️&nbsp;<b>更多源</b></td><td>新增 <b>HuggingFace</b> 与 <b>Papers with Code</b>；GitHub 改为<b>按 star 排序</b>，只留高质量仓库</td></tr>
<tr><td>🔔&nbsp;<b>多渠道推送</b></td><td><b>微信</b>（企业微信群机器人 / Server酱）· <b>Telegram</b> · <b>Slack</b></td></tr>
<tr><td>⚡&nbsp;<b>更快更稳</b></td><td>摘要并发提速、快速失败兜底；GitHub 用仓库描述、不做 AI 摘要（根治乱码）</td></tr>
<tr><td>🐳&nbsp;<b>一键部署</b></td><td><code>docker compose up -d</code>，数据库持久化到 <code>./data</code></td></tr>
<tr><td>🤖&nbsp;<b>Skill 同步</b></td><td>以上抓取 / 推送相关改进已同步到 Agent Skill 版</td></tr>
</table>

> **2026-06-27 · 已上架 SkillHub** 🎉
>
> 本 skill 现已登陆 **[SkillHub](https://skillhub.cn/skills/auto-paper-collecter)**，可在平台上直接浏览 / 获取与安装。

> **2026-06-26 · Agent Skill 现可一键安装为 Claude Code 插件，并支持 Codex** 🤖🔌
>
> 除了网页版，本仓库内置一个 **Claude Code / Codex 通用的 Agent Skill** —— 一句话 **「运行我的文献雷达」**
> 就能跑完整条流水线、产出当日文献摘要，**纯 Python 标准库、零依赖、免 AI API key**。
> **一行命令安装**：`/plugin marketplace add PenghaoJiang/auto-paper-collecter` → `/plugin install auto-paper-collecter@auto-paper-collecter`。
> 同时新增 [`AGENTS.md`](AGENTS.md)，让 **Codex / OpenAI 等 agent 也能开箱即用**。👉 详见下方 **「🤖 Skill 版」**。

---

## 🌟 这是什么 · What is this

**auto-paper-collecter** 是一个轻量、自托管的**学术文献自动聚合工具**。

你只要告诉它你关心的几个关键词，它就会每天自动：

> 🛰️ 跨 **arXiv / Crossref(含 IEEE·ACM)/ Semantic Scholar / GitHub / RSS** 多源检索
> 🧠 用 **LLM 做"联想式"扩展检索**，不再只匹配字面关键词
> 🎯 用 **LLM 把跨领域、不相关的论文过滤掉**，只留计算机领域、真正切题的
> ✍️ 为每篇生成**中文摘要**(一句话 TL;DR / 方法 / 核心贡献)
> 📊 分析**领域热点**、生成**每周报告**，还能**邮件 / 浏览器推送**

一个零构建的单页仪表盘，前后端同源，开箱即用。

---

## 🎯 为什么做它 · Motivation

> [!NOTE]
> 做科研最累的事情之一，是**跟踪文献**。
> arXiv 每天上新成百上千篇，关键词搜索要么漏掉同义写法、要么被一堆跨领域结果淹没，
> 手动刷既费时又容易错过。

于是有了这个小工具 —— 把"**每天读一遍最新文献**"这件事**自动化**，并交给 LLM 做最脏最累的两件事：

1. **想得更全**：`C2Rust` 也该搜到 `C-to-Rust translation`、`migrating legacy C to Rust`……
2. **筛得更准**：把"医学里的 *translation*""金融里的 *AI*"这种同名跨领域噪声挡在门外。

让你打开页面，看到的就是**一份干净、按时间排好、带摘要的当日文献流**。🫧

---

## ✨ 功能特性 · Features

| | 功能 | 说明 |
|:--:|---|---|
| 📰 | **今日文献流** | 多源聚合 + 按真实发表时间排序；无新文时智能回填；顶栏实时搜索 |
| 🧠 | **LLM 智能抓取** | 关键词联想扩展 + 计算机领域相关性过滤，召回更广、噪声更少 |
| 🔥 | **领域热点** | LLM 聚合成主流子领域，统计近 7/30 天增量，Top 3 给出**详细方向总结**与对应论文 |
| ⭐ | **收藏与笔记** | 一键收藏、写笔记、复制 **BibTeX** |
| 🗞️ | **每周报告** | 每周精选 + 分方向小结，自动归档 |
| 🔔 | **推送通知** | 浏览器通知 + 可选 **SMTP 邮件摘要**（定时发送） |
| 🛰️ | **GitHub 实时源** | 顺带追踪与主题相关的最新代码仓库 / 论文实现 |
| 🌏 | **本地化** | 界面与摘要中文友好，时区可配 |

---

## 🧩 工作原理 · How it works

```mermaid
flowchart LR
    A([🔑 你的关键词]) --> B{{🧠 LLM 联想扩展}}
    B --> S1[arXiv]
    B --> S2[Crossref]
    B --> S3[Semantic Scholar]
    B --> S4[GitHub]
    B --> S5[RSS]
    S1 --> M[🧹 跨源去重]
    S2 --> M
    S3 --> M
    S4 --> M
    S5 --> M
    M --> F{{🎯 LLM 相关性过滤}}
    F --> Z{{✍️ LLM 中文摘要}}
    Z --> DB[(🗄️ SQLite)]
    DB --> UI([📊 仪表盘 / 邮件 / 周报])
```

<div align="center"><sub>纯 Python 跑确定性流程，把"判断"交给 LLM —— 既快又准。</sub></div>

---

## 🚀 快速开始 · Quick Start

```bash
# 1) 克隆并进入
git clone https://github.com/PenghaoJiang/auto-paper-collecter.git
cd auto-paper-collecter

# 2) 建虚拟环境 & 装依赖
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3) 配置（复制模板后编辑 .env，填入你的 AI 网关等）
cp .env.example .env

# 4) 起飞 🛫
python run.py
```

打开 **http://localhost:8000** → 进入「订阅设置」填关键词 → 点「保存并拓取」即可。

> 🐳 **或用 Docker 一键起飞**：`cp .env.example .env`（可选）→ `docker compose up -d`，数据库会持久化到 `./data`。

> [!TIP]
> 关键词建议用**英文**（各源召回率更高）；界面与摘要是中文。首次抓取 + 摘要约需 1–3 分钟，后台进行，完成后页面自动出结果。

---

## 🤖 Skill 版 · Use as an Agent Skill

除了网页版，本仓库还内置一个 **Claude Code / Codex 通用的 Agent Skill**（[`skills/auto-paper-collecter/`](skills/auto-paper-collecter/) 目录）——
直接对 AI 助手说一句"**运行我的文献雷达**"，它就会跑完整条流水线并产出当日文献摘要，
而且**不需要任何 AI API key**（跑这个 skill 的模型本身就是那个 LLM）。

**方式一 · 作为 Claude Code 插件安装（推荐，一行命令搞定）**

```bash
/plugin marketplace add PenghaoJiang/auto-paper-collecter
/plugin install auto-paper-collecter@auto-paper-collecter
```

**方式二 · 直接复制 skill 目录**

```bash
cp -r skills/auto-paper-collecter ~/.claude/skills/auto-paper-collecter
$EDITOR ~/.claude/skills/auto-paper-collecter/state/config.json   # 编辑你的关键词
```

然后对 Claude Code 说 **「运行我的文献雷达 / 今天有什么新论文」** 即可。脚本是**纯 Python 标准库、零依赖**；
确定性的抓取交给脚本，LLM 的判断（联想扩展 / 相关性过滤 / 中文摘要 / 热点）由运行 skill 的模型完成
（Claude Code → Claude；Codex → GPT）。细节见 [`skills/auto-paper-collecter/SKILL.md`](skills/auto-paper-collecter/SKILL.md)。

> 📦 本 skill 也已上架 **[SkillHub](https://skillhub.cn/skills/auto-paper-collecter)**，可在平台上直接浏览 / 获取。

---

## ⚙️ 配置 · Configuration

所有配置都在 `.env`（参见 `.env.example`）：

| 变量 | 必填 | 说明 |
|---|:--:|---|
| `AI_BASE_URL` / `AI_API_KEY` / `AI_MODEL` | ✅ | 任意 **OpenAI 兼容**网关。`AI_ENABLED=false` 时退回原始摘要、不调 LLM |
| `SEMANTIC_SCHOLAR_KEY` | ⬜ | 可选，不填也能用，仅限速更严 |
| `GITHUB_TOKEN` | ⬜ | 可选，提高 GitHub 检索速率上限 |
| `SMTP_*` / `EMAIL_*` | ⬜ | 可选，填入后定时任务发送当日摘要邮件（Gmail 需**应用专用密码**） |
| `REFRESH_TIMES` / `TIMEZONE` | ⬜ | 每日定时刷新时间与时区（默认 `10:00,22:00` / `Asia/Shanghai`） |
| `BACKFILL_N` / `RSS_FEEDS` | ⬜ | 回填篇数 / 学术新闻 RSS 源 |

> [!IMPORTANT]
> `.env` 已被 `.gitignore` 忽略，**密钥永远不会被提交**。请妥善保管自己的 key 🔐

---

## 🛰️ 数据源 · Data Sources

| 来源 | 内容 | 备注 |
|---|---|---|
| **arXiv** | 预印本（官方 API） | 计算机领域主力 |
| **Crossref** | 期刊/会议元数据 | 含 IEEE·ACM，仅元数据 + 摘要 |
| **Semantic Scholar** | 综合学术检索 | 自带 TLDR；限定计算机领域 |
| **GitHub** | 实时仓库 / 论文代码 | 作为补充信号 |
| **HuggingFace** | 热门预印本（社区点赞） | 与 arXiv 互补 |
| **Papers with Code** | 论文 + 官方代码 | 公共 API 可用时生效 |
| **RSS** | 学术新闻 / 博客 | 可自定义订阅源 |

---

## 📡 API

<details>
<summary>展开查看全部接口</summary>

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET`  | `/api/bootstrap` | 仪表盘一次性取数（feed / 库 / 热点 / 周报 / 设置） |
| `POST` | `/api/refresh` | 后台触发一次抓取（立即返回，前端轮询 `refreshing`） |
| `GET`  | `/api/trends?domain=&window=7` | 领域热点（Top3 + 各方向增量 + 论文） |
| `GET`  | `/api/report/weekly` | 生成 / 取最新周报 |
| `POST` | `/api/library/{paper_id}` | `{saved, read, note}` 收藏 / 已读 / 笔记 |
| `GET·PUT` | `/api/settings` | 关键词 / 来源 / 时间 / 回填 N / 推送 / 邮箱 |
| `POST` | `/api/test-email` | 发送一封测试邮件验证 SMTP |

</details>

---

## 🗺️ 路线图 · Roadmap

- [x] 多源聚合 + LLM 联想扩展 + 相关性过滤
- [x] 领域热点（细分方向 + 详细总结 + 论文清单）
- [x] 收藏 / 笔记 / BibTeX / 每周报告
- [x] 浏览器 + 邮件推送、定时任务
- [x] 更多数据源（HuggingFace · Papers with Code）
- [x] 一键 Docker 部署
- [x] 移动端适配 + 深色模式 + 👍/👎 反馈学习 + 多渠道推送
- [ ] 多用户 + 鉴权（PostgreSQL）
- [ ] 移动端适配

> 欢迎在 [Issues](../../issues) 里提你想要的功能！🙌

---

## 🤝 一起建设 · Contributing

这是一个**业余时间打磨的开源小项目**，它的成长离不开你 —— **非常欢迎大家一起把它做得更好！** 🌱✨

- 🐛 **发现 Bug** → 提个 [Issue](../../issues)
- 💡 **有想法 / 想讨论** → 来 [Discussions](../../discussions) 一起头脑风暴 🧠
- ✨ **想要新功能** → 在 [Issues](../../issues) 许个愿
- 🔧 **想动手** → Fork → 改 → 提一个 **Pull Request**

无论是改一个错别字、补一句文档，还是接一个新数据源，**每一份贡献都同样珍贵** 💗
也欢迎你只是来 [Discussions](../../discussions) 聊聊你的科研工作流、分享你的关键词配置 —— 让我们把这个小雷达一起养大 🚀

---

<div align="center">

### ⭐ 如果觉得有用，点个 Star 支持一下吧！

<sub>你的每一个 Star，都是作者继续维护的动力 🌱</sub>

<sub>有想法、问题或想一起共建？欢迎来 <a href="../../discussions">💬 Discussions</a> 坐坐！</sub>

<br><br>

**📚 Read less, know more. Let the radar do the scanning.** 🔭

<br>

<sub>Made with ❤️ & ☕ · Licensed under <a href="./LICENSE">MIT</a></sub>

</div>
