<div align="center">

# Understand Everything

![Understand Everything Banner](promotional-banner.png)

**通过 Git 历史和 AI 分析，将任何代码仓库转换为通俗易懂的交互式文档。**

[🌐 项目网站](https://mor-li.github.io/understand-everything/) |
[📖 verl 示例](https://mor-li.github.io/understand-everything/output/verl/website-2025-12-09/index.html) |
[⚡ Megatron-LM 示例](https://mor-li.github.io/understand-everything/output/Megatron-LM/website-2025-12-09/index.html)

[English](../README.md) | 简体中文

</div>

## 项目简介

这是一个用于深度理解代码仓库的工具链。它通过分析 Git 历史、使用 AI 解读代码、生成层级文档，最终创建一个交互式网站，让你能够轻松理解任何复杂的代码库。

## 核心功能

- **可视化分析**：生成仓库结构热力图，直观展示文件修改频率
- **智能统计**：分析代码规模、修改分布、Token 数量
- **AI 解读**：使用 Gemini 3 Pro Preview 生成通俗易懂的代码解释
- **层级文档**：自底向上递归生成各层级 README
- **交互式网站**：Read the Docs 风格的静态网站，支持文件树导航

## 项目结构

```
understand-everything/
├── scripts/              # 3 个核心脚本（按执行顺序命名）
│   ├── s1_explain_files.py        # AI 解读代码文件
│   ├── s2_generate_readme.py      # 生成层级 README
│   └── s3_website.py              # 生成交互式网站
├── utils/               # 工具脚本
│   ├── s0_add_timestamps.py       # 添加时间戳
│   ├── s1_repo_heatmap_tree.py    # 生成仓库结构热力图
│   ├── s2_analyze_stats.py        # 分析统计信息
│   └── utils.py                   # 通用工具函数
├── repo/                # 待分析的仓库（.gitignore 已忽略）
├── output/              # 生成的所有输出（.gitignore 已忽略）
│   └── <repo_name>/
│       ├── explain/              # AI 解读的 markdown
│       └── website/              # 静态网站
└── pyproject.toml       # 项目配置
```

## 快速开始

### 1. 环境设置

```bash
# 创建虚拟环境
uv venv --seed .venv --python 3.12
source .venv/bin/activate
uv pip install -e .
```

### 2. 配置 API

设置环境变量（用于 Gemini API）：
```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="your-openai-base-url"
```

### 3. 完整分析流程

假设要分析 `repo/your-project` 仓库：

```bash
# Step 1: AI 解读文件（生成通俗解释）
python scripts/s1_explain_files.py repo/your-project --workers 8 --percent 100

# Step 2: 生成层级 README（自底向上汇总）
python scripts/s2_generate_readme.py repo/your-project

# Step 3: 生成交互式网站（最终产物）
python scripts/s3_website.py repo/your-project
```

**可选工具脚本**：

```bash
# 生成仓库热力图（可视化修改频率）
python utils/s1_repo_heatmap_tree.py repo/your-project

# 分析统计信息（了解代码规模）
python utils/s2_analyze_stats.py repo/your-project
```

### 4. 查看结果

启动本地服务器查看网站：
```bash
cd output/your-project/website-<date>
python -m http.server 8000
# 浏览器打开 http://localhost:8000
```

## 核心脚本详细说明

### S1 - AI 解读代码文件

**功能**：使用 Gemini 3 Pro Preview 为每个文件生成通俗易懂的中文解释

**特点**：
- 异步并发处理，支持 `--workers N` 设置并发数（默认 16）
- 支持 `--top N` 或 `--percent N` 选择要解读的文件
- 自动跳过已解读的文件（使用 `--force` 强制重新生成）
- 使用 `tqdm` 显示实时进度条
- Prompt 优化为"step-by-step 讲解"风格

**使用**：
```bash
python scripts/s1_explain_files.py <repo_path> [options]

# 解读所有文件，使用 8 个并发
python scripts/s1_explain_files.py repo/your-project --workers 8 --percent 100

# 解读前 50% 的文件
python scripts/s1_explain_files.py repo/your-project --percent 50

# 强制重新生成
python scripts/s1_explain_files.py repo/your-project --percent 100 --force
```

**输出**：`output/<repo_name>/explain-<date>/*.md`

### S2 - 生成层级 README

**功能**：递归地为每个文件夹生成汇总 README（自底向上）

**特点**：
- 从最底层文件夹开始，逐层向上汇总
- 子文件夹用其 README 代表，文件用其解读代表
- 如果内容超过 200K tokens，等比例截断
- 使用通俗易懂的 Prompt 生成汇总

**使用**：
```bash
python scripts/s2_generate_readme.py <repo_path> [options]

# 示例
python scripts/s2_generate_readme.py repo/your-project

# 强制重新生成
python scripts/s2_generate_readme.py repo/your-project --force
```

**输出**：在解读目录的每个文件夹下生成 `README.md`

### S3 - 生成交互式网站

**功能**：生成 Read the Docs 风格的静态网站

**特点**：
- 左侧可折叠文件树导航，固定缩进对齐
- 点击文件夹显示 README 汇总
- 点击文件显示 AI 解读 + 原始代码（带语法高亮）
- 支持所有文件类型（.py, .cu, .cpp, .h, .md 等）
- 显示隐藏文件（除 .git 目录外）
- 使用 Prism.js 进行代码高亮
- 响应式设计，移动端友好

**使用**：
```bash
python scripts/s3_website.py <repo_path> [options]

# 示例
python scripts/s3_website.py repo/your-project
```

**输出**：
- `output/<repo_name>/website/index.html`
- `output/<repo_name>/website/styles.css`
- `output/<repo_name>/website/app.js`
- `output/<repo_name>/website/sources/` - 源代码
- `output/<repo_name>/website/explanations/` - 解读（HTML）

## 示例项目

已成功分析的开源项目：
- **[verl](https://github.com/volcengine/verl)** (1100+ 文件) - 字节跳动开源的大模型强化学习框架
- **[Megatron-LM](https://github.com/NVIDIA/Megatron-LM)** (1330+ 文件) - NVIDIA 开源的大规模 Transformer 训练框架

## 技术栈

- **Python 3.12+**
- **GitPython** - Git 仓库操作
- **Matplotlib** - 热力图可视化
- **NumPy** - 数值计算
- **Tiktoken** - Token 计数
- **OpenAI SDK** - Gemini API 调用
- **Markdown** - Markdown → HTML 转换
- **Prism.js** - 代码语法高亮
- **TQDM** - 进度条显示

## 设计理念

1. **极简主义**：每个脚本专注一件事，代码简洁明了
2. **顺序清晰**：s1 → s2 → s3，按执行顺序命名
3. **可中断**：每一步都可独立运行，支持增量更新
4. **并发高效**：异步处理，支持多 worker 并发

## 许可证

MIT License

## 致谢

- **Gemini 3 Pro Preview** - 强大的代码理解能力
- **Claude Code** - 优秀的编程助手
