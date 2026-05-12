# 🚀 CodeSnippet Pro

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-orange?style=for-the-badge" alt="Platform">
</p>

<p align="center">
  <b>🎯 Intelligent Code Snippet Manager for Developers</b><br>
  A lightweight, powerful CLI tool to collect, organize, search, and reuse your code snippets effortlessly.
</p>

<p align="center">
  <a href="#-english">English</a> •
  <a href="#-简体中文">简体中文</a> •
  <a href="#-繁體中文">繁體中文</a>
</p>

---

## 🇺🇸 English

### 🎉 Introduction

**CodeSnippet Pro** is a modern CLI tool designed for developers who want to efficiently manage their code snippets. Whether you're a software engineer, data scientist, or DevOps specialist, CodeSnippet Pro helps you organize your reusable code pieces with powerful search capabilities and an intuitive interface.

**Key Problems Solved:**
- ❌ Code snippets scattered across notes, files, and browser bookmarks
- ❌ Difficulty finding the right snippet when you need it
- ❌ No easy way to categorize and tag code examples
- ❌ Time wasted rewriting the same code patterns

**Our Solution:**
- ✅ Centralized snippet storage with SQLite database
- ✅ Full-text search with FTS5 support
- ✅ Syntax highlighting for 30+ programming languages
- ✅ Tag-based organization and filtering
- ✅ Import/Export functionality for backup and sharing

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📝 **Easy Addition** | Add snippets interactively or via command-line arguments |
| 🔍 **Powerful Search** | Full-text search across titles, code, descriptions, and tags |
| 🏷️ **Smart Tagging** | Organize snippets with custom tags for quick filtering |
| 🎨 **Syntax Highlighting** | Beautiful code display with support for 30+ languages |
| 📊 **Usage Statistics** | Track which snippets you use most frequently |
| 📤 **Import/Export** | Backup and share snippets in JSON or CSV format |
| 💻 **Cross-Platform** | Works on Windows, macOS, and Linux |
| 🖥️ **Interactive TUI** | Rich terminal interface with intuitive navigation |

### 🚀 Quick Start

#### Requirements
- Python 3.8 or higher
- pip package manager

#### Installation

```bash
# Install from PyPI
pip install codesnippet-pro

# Or install from source
git clone https://github.com/gitstq/snippet-manager-pro.git
cd snippet-manager-pro
pip install -e .
```

#### Basic Usage

```bash
# Add a new snippet
csp add -t "Hello World" -c "print('Hello, World!')" -l python -g "beginner,example"

# Search snippets
csp search "python function"

# List all snippets
csp list

# Show snippet details
csp show 1

# Display statistics
csp stats
```

### 📖 Detailed Usage Guide

#### Adding Snippets

```bash
# Interactive mode
csp add

# Command-line mode
csp add -t "Quick Sort" -c "def quicksort(arr):..." -l python -d "Efficient sorting algorithm" -g "algorithm,sorting"

# From clipboard
csp add --from-clipboard -t "Clipboard Snippet" -l javascript

# From file
csp add --from-file ./example.py -t "File Import"
```

#### Searching Snippets

```bash
# Basic search
csp search "database connection"

# Filter by language
csp search "function" -l python

# Filter by tag
csp search "auth" -g "security"

# Combined filters
csp search "api" -l javascript -g "backend"
```

#### Managing Snippets

```bash
# Edit a snippet
csp edit 1

# Delete a snippet
csp delete 1

# Copy snippet to clipboard
csp show 1 --copy
```

#### Import/Export

```bash
# Export to JSON
csp export backup.json

# Export to CSV
csp export snippets.csv -f csv

# Import from JSON
csp import backup.json

# Import from CSV
csp import snippets.csv -f csv
```

#### Interactive Mode

```bash
# Launch interactive TUI
csp interactive

# Or use alias
csp i
```

### 💡 Design Philosophy

**Why CodeSnippet Pro?**

1. **Developer-First Design**: Every feature is crafted with developer workflows in mind
2. **Lightweight & Fast**: Minimal dependencies, instant startup, responsive interface
3. **Privacy-Focused**: All data stored locally, no cloud dependencies
4. **Extensible**: Clean architecture allows easy customization and extension

**Technical Highlights:**
- SQLite with FTS5 for blazing-fast full-text search
- Rich library for beautiful terminal UI
- Modular architecture for easy maintenance
- Comprehensive test coverage

### 📦 Packaging & Deployment

#### Building from Source

```bash
# Clone repository
git clone https://github.com/gitstq/snippet-manager-pro.git
cd snippet-manager-pro

# Install development dependencies
pip install -e ".[dev]"

# Run tests
make test

# Build package
make build
```

#### Installation Methods

**Via pip (Recommended):**
```bash
pip install codesnippet-pro
```

**Via pipx (Isolated environment):**
```bash
pipx install codesnippet-pro
```

**From source:**
```bash
git clone https://github.com/gitstq/snippet-manager-pro.git
cd snippet-manager-pro
pip install -e .
```

### 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: add some amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🇨🇳 简体中文

### 🎉 项目介绍

**CodeSnippet Pro** 是一款专为开发者打造的现代化代码片段管理 CLI 工具。无论您是软件工程师、数据科学家还是 DevOps 专家，CodeSnippet Pro 都能帮助您高效地组织可复用的代码片段。

**解决的核心痛点：**
- ❌ 代码片段散落在笔记、文件和浏览器书签中
- ❌ 需要时难以快速找到合适的代码
- ❌ 缺乏对代码示例进行分类和标签化的便捷方式
- ❌ 重复编写相同的代码模式浪费时间

**我们的解决方案：**
- ✅ 基于 SQLite 的集中式片段存储
- ✅ 支持 FTS5 的全文搜索
- ✅ 支持 30+ 种编程语言的语法高亮
- ✅ 基于标签的组织和筛选
- ✅ 导入/导出功能，便于备份和分享

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📝 **轻松添加** | 支持交互式或命令行参数添加片段 |
| 🔍 **强大搜索** | 支持标题、代码、描述和标签的全文搜索 |
| 🏷️ **智能标签** | 使用自定义标签组织片段，快速筛选 |
| 🎨 **语法高亮** | 支持 30+ 种语言的精美代码展示 |
| 📊 **使用统计** | 追踪您最常用的代码片段 |
| 📤 **导入导出** | 以 JSON 或 CSV 格式备份和分享片段 |
| 💻 **跨平台** | 支持 Windows、macOS 和 Linux |
| 🖥️ **交互式 TUI** | 丰富的终端界面，操作直观 |

### 🚀 快速开始

#### 环境要求
- Python 3.8 或更高版本
- pip 包管理器

#### 安装

```bash
# 从 PyPI 安装
pip install codesnippet-pro

# 或从源码安装
git clone https://github.com/gitstq/snippet-manager-pro.git
cd snippet-manager-pro
pip install -e .
```

#### 基本用法

```bash
# 添加新片段
csp add -t "Hello World" -c "print('Hello, World!')" -l python -g "beginner,example"

# 搜索片段
csp search "python function"

# 列出所有片段
csp list

# 显示片段详情
csp show 1

# 显示统计信息
csp stats
```

### 📖 详细使用指南

#### 添加片段

```bash
# 交互模式
csp add

# 命令行模式
csp add -t "Quick Sort" -c "def quicksort(arr):..." -l python -d "高效排序算法" -g "algorithm,sorting"

# 从剪贴板
csp add --from-clipboard -t "Clipboard Snippet" -l javascript

# 从文件
csp add --from-file ./example.py -t "File Import"
```

#### 搜索片段

```bash
# 基础搜索
csp search "database connection"

# 按语言筛选
csp search "function" -l python

# 按标签筛选
csp search "auth" -g "security"

# 组合筛选
csp search "api" -l javascript -g "backend"
```

#### 管理片段

```bash
# 编辑片段
csp edit 1

# 删除片段
csp delete 1

# 复制到剪贴板
csp show 1 --copy
```

#### 导入导出

```bash
# 导出为 JSON
csp export backup.json

# 导出为 CSV
csp export snippets.csv -f csv

# 从 JSON 导入
csp import backup.json

# 从 CSV 导入
csp import snippets.csv -f csv
```

#### 交互模式

```bash
# 启动交互式 TUI
csp interactive

# 或使用别名
csp i
```

### 💡 设计理念

**为什么选择 CodeSnippet Pro？**

1. **开发者优先设计**：每个功能都围绕开发者工作流程精心设计
2. **轻量快速**：依赖最少，启动迅速，界面响应流畅
3. **注重隐私**：所有数据本地存储，无云端依赖
4. **可扩展**：架构清晰，便于定制和扩展

**技术亮点：**
- 基于 SQLite + FTS5 的极速全文搜索
- 使用 Rich 库打造精美终端界面
- 模块化架构，易于维护
- 全面的测试覆盖

### 📦 打包与部署

#### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/gitstq/snippet-manager-pro.git
cd snippet-manager-pro

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
make test

# 构建包
make build
```

#### 安装方式

**通过 pip（推荐）：**
```bash
pip install codesnippet-pro
```

**通过 pipx（隔离环境）：**
```bash
pipx install codesnippet-pro
```

**从源码安装：**
```bash
git clone https://github.com/gitstq/snippet-manager-pro.git
cd snippet-manager-pro
pip install -e .
```

### 🤝 贡献指南

我们欢迎贡献！请参阅我们的 [贡献指南](CONTRIBUTING.md) 了解详情。

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: add some amazing feature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 📄 开源协议

本项目采用 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

## 🇹🇼 繁體中文

### 🎉 專案介紹

**CodeSnippet Pro** 是一款專為開發者打造的現代化程式碼片段管理 CLI 工具。無論您是軟體工程師、資料科學家還是 DevOps 專家，CodeSnippet Pro 都能幫助您高效地組織可重複使用的程式碼片段。

**解決的核心痛點：**
- ❌ 程式碼片段散落在筆記、檔案和瀏覽器書籤中
- ❌ 需要時難以快速找到合適的程式碼
- ❌ 缺乏對程式碼範例進行分類和標籤化的便捷方式
- ❌ 重複編寫相同的程式碼模式浪費時間

**我們的解決方案：**
- ✅ 基於 SQLite 的集中式片段儲存
- ✅ 支援 FTS5 的全文搜尋
- ✅ 支援 30+ 種程式語言的語法高亮
- ✅ 基於標籤的組織和篩選
- ✅ 匯入/匯出功能，便於備份和分享

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📝 **輕鬆新增** | 支援互動式或命令列參數新增片段 |
| 🔍 **強大搜尋** | 支援標題、程式碼、描述和標籤的全文搜尋 |
| 🏷️ **智慧標籤** | 使用自訂標籤組織片段，快速篩選 |
| 🎨 **語法高亮** | 支援 30+ 種語言的精美程式碼展示 |
| 📊 **使用統計** | 追蹤您最常用的程式碼片段 |
| 📤 **匯入匯出** | 以 JSON 或 CSV 格式備份和分享片段 |
| 💻 **跨平台** | 支援 Windows、macOS 和 Linux |
| 🖥️ **互動式 TUI** | 豐富的終端介面，操作直觀 |

### 🚀 快速開始

#### 環境要求
- Python 3.8 或更高版本
- pip 套件管理器

#### 安裝

```bash
# 從 PyPI 安裝
pip install codesnippet-pro

# 或從原始碼安裝
git clone https://github.com/gitstq/snippet-manager-pro.git
cd snippet-manager-pro
pip install -e .
```

#### 基本用法

```bash
# 新增片段
csp add -t "Hello World" -c "print('Hello, World!')" -l python -g "beginner,example"

# 搜尋片段
csp search "python function"

# 列出所有片段
csp list

# 顯示片段詳情
csp show 1

# 顯示統計資訊
csp stats
```

### 📖 詳細使用指南

#### 新增片段

```bash
# 互動模式
csp add

# 命令列模式
csp add -t "Quick Sort" -c "def quicksort(arr):..." -l python -d "高效排序演算法" -g "algorithm,sorting"

# 從剪貼簿
csp add --from-clipboard -t "Clipboard Snippet" -l javascript

# 從檔案
csp add --from-file ./example.py -t "File Import"
```

#### 搜尋片段

```bash
# 基礎搜尋
csp search "database connection"

# 按語言篩選
csp search "function" -l python

# 按標籤篩選
csp search "auth" -g "security"

# 組合篩選
csp search "api" -l javascript -g "backend"
```

#### 管理片段

```bash
# 編輯片段
csp edit 1

# 刪除片段
csp delete 1

# 複製到剪貼簿
csp show 1 --copy
```

#### 匯入匯出

```bash
# 匯出為 JSON
csp export backup.json

# 匯出為 CSV
csp export snippets.csv -f csv

# 從 JSON 匯入
csp import backup.json

# 從 CSV 匯入
csp import snippets.csv -f csv
```

#### 互動模式

```bash
# 啟動互動式 TUI
csp interactive

# 或使用別名
csp i
```

### 💡 設計理念

**為什麼選擇 CodeSnippet Pro？**

1. **開發者優先設計**：每個功能都圍繞開發者工作流程精心設計
2. **輕量快速**：依賴最少，啟動迅速，介面回應流暢
3. **注重隱私**：所有資料本地儲存，無雲端依賴
4. **可擴展**：架構清晰，便於定製和擴展

**技術亮點：**
- 基於 SQLite + FTS5 的極速全文搜尋
- 使用 Rich 庫打造精美終端介面
- 模組化架構，易於維護
- 全面的測試覆蓋

### 📦 打包與部署

#### 從原始碼構建

```bash
# 克隆倉庫
git clone https://github.com/gitstq/snippet-manager-pro.git
cd snippet-manager-pro

# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
make test

# 構建包
make build
```

#### 安裝方式

**通過 pip（推薦）：**
```bash
pip install codesnippet-pro
```

**通過 pipx（隔離環境）：**
```bash
pipx install codesnippet-pro
```

**從原始碼安裝：**
```bash
git clone https://github.com/gitstq/snippet-manager-pro.git
cd snippet-manager-pro
pip install -e .
```

### 🤝 貢獻指南

我們歡迎貢獻！請參閱我們的 [貢獻指南](CONTRIBUTING.md) 了解詳情。

1. Fork 本倉庫
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: add some amazing feature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 建立 Pull Request

### 📄 開源協議

本專案採用 MIT 協議開源 - 詳見 [LICENSE](LICENSE) 檔案。

---

<p align="center">
  Made with ❤️ by developers, for developers
</p>
