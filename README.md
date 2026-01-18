# Dianping Crawler (大众点评爬虫)

这是一个用于从大众点评抓取特定关键词商户及其评论数据的爬虫项目。

## 功能特点

- **多城市支持**: 可配置多个目标城市，自动获取城市ID并进行遍历。
- **关键词搜索**: 根据指定关键词（如“轻食”）搜索商户。
- **评论抓取**: 获取商户下的用户评论，包含用户名、评分、时间和评论内容。
- **反爬虫机制**:
  - 使用 Playwright 模拟真实浏览器行为。
  - 随机延时策略，模拟人类操作间隔。
  - 检测到验证码（滑块/安全验证）时会自动暂停，支持手动在浏览器中通过验证后继续运行。
- **数据导出**: 抓取结果实时保存为 CSV 文件。

## 环境要求

- Python 3.8+
- Playwright
- BeautifulSoup4

## 安装步骤

1. 克隆本项目到本地。
2. 安装所需的 Python 依赖库：

```bash
pip install playwright beautifulsoup4
```

3. 安装 Playwright 浏览器驱动：

```bash
playwright install
```

## 配置说明

在运行之前，你需要修改 `config.py` 文件以适应你的需求：

- **基础配置**:
  - `MAX_PAGES`: 搜索商户时的最大页数。
  - `COMMENT_PAGES`: 每个商户抓取的评论页数。
  - `SEARCH_KEYWORD`: 你想要搜索的关键词（例如 `'轻食'`）。
  - `CITIES`: 目标城市列表（字典格式，键为城市拼音或英文名）。

- **Cookie 配置**:
  1. 在浏览器中打开大众点评网并登录。
  2. 打开开发者工具 (F12)，刷新页面。
  3. 在 Network 面板找到任意请求，复制 Request Headers 中的 Cookie。
  4. 将 Cookie 字符串填入 `COOKIES` 变量中。

## 使用方法

### 1. 基础运行

直接运行 `main.py` 即可启动爬虫（程序将使用 `config.py` 中的默认配置）：

```bash
python main.py
```

### 2. 命令行参数运行

支持通过命令行参数覆盖 `config.py` 中的默认配置，方便动态调整抓取任务：

| 参数 | 说明 | 默认值 | 示例 |
| :--- | :--- | :--- | :--- |
| `--keyword` | 搜索关键词 | `config.SEARCH_KEYWORD` | `--keyword "烧烤"` |
| `--max_pages` | 搜索商户列表的最大页数 | `config.MAX_PAGES` | `--max_pages 2` |
| `--comment_pages` | 每个商户抓取的评论页数 | `config.COMMENT_PAGES` | `--comment_pages 5` |
| `--output` | 结果保存的 CSV 文件名 | `config.SCV_FILE_NAME` | `--output "bbq.csv"` |
| `--cookies` | 浏览器 Cookie 字符串 | `config.COOKIES` | `--cookies "mysession=..."` |

**示例命令：**

搜索“烧烤”，抓取前 2 页商户，每家商户 1 页评论，保存为 `bbq.csv`：

```bash
python main.py --keyword "烧烤" --max_pages 2 --comment_pages 1 --output "bbq.csv"
```

### 运行流程

1. 程序启动 Playwright 浏览器（默认有头模式 `headless=False`，方便手动过验证）。
2. 初始化 CSV 文件。
3. 遍历 `CITIES` 列表，自动获取每个城市的 `cityId`。
4. 在每个城市中搜索 `SEARCH_KEYWORD`。
5. 获取搜索结果中的商户列表。
6. 进入每个商户，抓取指定页数的评论数据。
7. 数据将追加写入到 `light_food_reviews.csv`（可在配置中修改文件名）。

### 遇到验证码怎么办？

如果程序检测到大众点评的安全验证页面（如“验证中心”或滑块），控制台会输出提示：

```
[!] Detected verification page. Please solve it manually in the opened browser.
```

此时程序会自动暂停。请在弹出的浏览器窗口中手动完成验证。验证通过后，回到终端按 **Enter** 键，程序将继续运行。

## 免责声明

本项目仅供学习和研究使用。请勿用于商业用途或大规模高频抓取，否则可能会导致账号被封禁或IP被限制。使用本工具所产生的任何后果由使用者自行承担。
