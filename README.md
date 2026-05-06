# 🤖 AI Newsletter Automation MCP Server

<div align="center">

![AI Newsletter Banner](https://img.shields.io/badge/AI-Newsletter-blue?style=for-the-badge&logo=openai&logoColor=white)
![MCP Server](https://img.shields.io/badge/MCP-Server-green?style=for-the-badge&logo=cloud&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-yellow?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM-orange?style=for-the-badge&logo=lightning&logoColor=white)

**Automate your AI newsletter creation with intelligent research, curation, and publishing**

[Features](#-features) • [Installation](#-installation) • [Telegram Bot](#-telegram-bot) • [Usage](#-usage) • [Configuration](#-configuration)

</div>

---

## 📖 What is MCP?

**MCP (Model Context Protocol)** is a framework that allows AI assistants like Claude to interact with external tools and services through standardized interfaces. Think of it as a "plugin system" for AI — it enables Claude to:

- 🔍 Search the web and fetch real-time data
- 📁 Access and manage files in Google Drive
- 📧 Read and send emails via Gmail
- 🛠️ Execute custom functions and APIs

This MCP server provides Claude with tools to automate the entire AI newsletter creation process — from research to publication.

---

## ✨ Features

### 🔍 Research Phase
- **arXiv Papers** — Fetch latest AI research papers with summaries
- **GitHub Trending** — Discover trending AI repositories and projects
- **Reddit Discussions** — Track viral AI discussions from r/MachineLearning, r/artificial, r/LocalLLaMA
- **Product Hunt** — Track new AI tools and products (optional)
- **Twitter/X Trends** — Capture viral AI discussions (optional, paid tier)
- **Gmail Feedback** — Analyze reader feedback and engagement
- **Past Newsletters** — Learn from previous newsletter performance

### ✍️ Editing Phase
- **Smart Content Organization** — Automatically categorize and prioritize content
- **Draft Creation** — Generate structured newsletter drafts
- **Content Validation** — Check completeness and quality
- **Text Preview** — Quick review before publishing

### 🎨 Design Phase
- **HTML Generation** — Beautiful, responsive email templates
- **Multi-Format Export** — HTML, Markdown, and JSON formats
- **Google Drive Integration** — Auto-save to cloud storage
- **Mobile-Friendly** — Responsive design for all devices

### 🤖 Telegram Bot
- **Interactive Commands** — `/newsletter`, `/papers`, `/repos`, `/ask`
- **Groq LLM Powered** — Fast AI responses using Llama 3.3 70B
- **Inline Keyboard** — Easy navigation with buttons
- **Hinglish Support** — Responses in Hindi-English mix

---

## 🚀 Quick Start with FastMCP Cloud

### Option 1: Use the Hosted Server (Recommended)

**No installation required.** Connect directly to the hosted MCP server:

#### Step 1: Open Claude Desktop Configuration

- **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux (Claude Code)**: `~/.claude.json`

#### Step 2: Add This Configuration

```json
{
  "mcpServers": {
    "ai-newsletter": {
      "url": "https://linguistic-chocolate-grouse.fastmcp.app/mcp"
    }
  }
}
```

#### Step 3: Restart Claude Desktop / Claude Code

Close and reopen Claude. The AI Newsletter tools will now be available.

#### Step 4: Start Using It

```
Help me research and create this week's AI newsletter
```

---

## 🛠️ Local Installation

### Prerequisites
- Python 3.8 or higher
- Google Cloud Project with OAuth credentials
- Groq API key (free at console.groq.com)
- Telegram Bot token (free from @BotFather)
- (Optional) API keys for Reddit, Product Hunt, GitHub

### Step 1: Clone the Repository
```bash
git clone https://github.com/kumarAbhishek2004/Ai_Newletter.git
cd Ai_Newletter
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables

Create a `.env` file in the project root:

```env
# Required: Google OAuth (for Drive & Gmail)
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REFRESH_TOKEN=your_refresh_token_here

# Optional: Newsletter folder in Google Drive
NEWSLETTER_FOLDER_ID=your_folder_id_here

# Optional: External APIs
GITHUB_TOKEN=your_github_token_here
PRODUCT_HUNT_API_KEY=your_producthunt_key_here
TWITTER_BEARER_TOKEN=your_twitter_token_here

# Reddit API (free alternative to Twitter)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret

# Telegram Bot
TELEGRAM_TOKEN=your_telegram_bot_token

# Groq LLM (free at console.groq.com)
GROQ_API_KEY=your_groq_api_key
```

### Step 4: Generate Google Refresh Token

```bash
pip install google-auth-oauthlib

python3 -c "
from google_auth_oauthlib.flow import InstalledAppFlow
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.readonly'
]
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=8080)
print('REFRESH TOKEN:', creds.refresh_token)
"
```

### Step 5: Run the MCP Server
```bash
python main.py
```

### Step 6: Configure Claude Code (Linux/Ubuntu)
```bash
claude mcp add ai-newsletter \
  --transport stdio \
  "/path/to/.venv/bin/python3" \
  "/path/to/Ai_Newletter/main.py"
```

---

## 📱 Telegram Bot

A fully functional Telegram bot powered by **Groq LLM** that delivers AI newsletters directly to your Telegram.

### Setup

```bash
# Install dependencies
pip install python-telegram-bot groq arxiv requests python-dotenv

# Run the bot
python telegram_bot.py
```

### Commands

| Command | Description |
|---------|-------------|
| `/start` | Main menu with interactive buttons |
| `/newsletter` | Generate full weekly AI newsletter |
| `/papers` | Latest AI research papers from arXiv |
| `/repos` | Trending GitHub repositories |
| `/ask <question>` | Ask anything about AI |

### Example Usage

```
/ask What is RAG in AI?
/papers
/newsletter
```

### Architecture

```
User (Telegram)
      ↓
Telegram Bot (python-telegram-bot)
      ↓
Groq LLM (llama-3.3-70b-versatile) — Free & Fast
      ↓
Research Tools (arXiv, GitHub, Reddit)
      ↓
Newsletter Generated & Sent to User
```

---

## 🔍 Tool Status & Alternatives

| Tool | Status | Notes |
|------|--------|-------|
| arXiv | ✅ Free | No API key needed |
| GitHub | ✅ Free | Token optional (higher rate limit) |
| Google Drive | ✅ Free | OAuth setup required |
| Gmail | ✅ Free | OAuth setup required |
| Groq LLM | ✅ Free | Fast Llama 3.3 70B |
| Telegram Bot | ✅ Free | Via @BotFather |
| Reddit | ✅ Free | Better Twitter alternative |
| Product Hunt | ⚠️ Optional | API key required |
| Twitter/X | ❌ Paid | Credits deplete on free tier |

---

## ✅ Verify Your Setup

Run the included verification script to check all tools:

```bash
python verify_tools.py
```

Expected output:
```
Tool                 Status
-----------------------------------
arXiv                ✅ WORKING
GitHub               ✅ WORKING
Google Drive         ✅ WORKING
Gmail                ✅ WORKING
Groq LLM             ✅ WORKING
Telegram Bot         ✅ WORKING
Reddit               ✅ WORKING
Product Hunt         ⚠️  OPTIONAL
Twitter/X            ⚠️  OPTIONAL
```

---

## 📋 Usage

### Available MCP Tools

#### Research Tools
| Tool | Description |
|------|-------------|
| `fetch_all_research()` | Batch fetch from all sources simultaneously |
| `search_arxiv_papers()` | Get latest AI/ML research papers |
| `fetch_github_trending()` | Find trending repositories |
| `search_product_hunt()` | Discover new AI products |
| `fetch_twitter_trends()` | Track viral AI conversations |
| `fetch_past_newsletters()` | Analyze previous issues for performance |
| `scan_gmail_feedback()` | Read and summarize reader responses |

#### Editing Tools
| Tool | Description |
|------|-------------|
| `create_newsletter_draft()` | Generate structured newsletter draft |
| `organize_content_sections()` | Prioritize and categorize content |
| `validate_newsletter_content()` | Run quality checks |
| `preview_newsletter()` | Text preview before publishing |

#### Publishing Tools
| Tool | Description |
|------|-------------|
| `generate_html_newsletter()` | Create production-ready HTML email |
| `save_to_drive()` | Upload final files to Google Drive |
| `export_newsletter()` | Export in HTML, Markdown, or JSON |

### Example Workflow

```
You:    "Help me create this week's AI newsletter"
Claude: [fetch_all_research()] → Gathers papers, repos, products
Claude: "Found 10 papers, 8 repos, 5 products. Here's a summary..."

You:    "Organize this and create a draft"
Claude: [create_newsletter_draft()] → Structures all content
Claude: "Draft ready. Shall I generate the HTML version?"

You:    "Yes, and save it to Google Drive"
Claude: [generate_html_newsletter()] → [save_to_drive()]
Claude: "Saved! Here's your newsletter link..."
```

---

## ⚙️ Configuration

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable **Google Drive API** and **Gmail API**
4. Create OAuth 2.0 credentials (choose **Desktop App**)
5. Add your Gmail as a Test User in OAuth consent screen
6. Generate refresh token using the script above
7. Add credentials to your `.env` file

### Groq Setup (Free LLM)

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with Google
3. Go to **API Keys** → **Create API Key**
4. Add to `.env` as `GROQ_API_KEY`

### Telegram Bot Setup

1. Open Telegram → search `@BotFather`
2. Send `/newbot`
3. Give your bot a name and username
4. Copy the token → add to `.env` as `TELEGRAM_TOKEN`

### Reddit Setup (Free Twitter Alternative)

1. Go to [reddit.com/prefs/apps](https://reddit.com/prefs/apps)
2. Click **"Create App"**
3. Select type: **script**
4. Set redirect URI: `http://localhost:8080`
5. Copy `client_id` and `client_secret` → add to `.env`

### Optional API Keys

- **GitHub** — [Create a personal access token](https://github.com/settings/tokens)
- **Product Hunt** — [Get API key](https://www.producthunt.com/v2/oauth/applications)
- **Twitter/X** — [Apply for developer access](https://developer.twitter.com) (paid tier recommended)

---

## 📊 Sample Output

### Text Preview
```
============================================================
 AI Newsletter — Issue #4 | May 06, 2026
============================================================

📊 CONTENT SUMMARY:
  Papers    : 10
  GitHub    :  8
  Products  :  5

🎯 BIG STORY:
  Breakthrough in Multi-Modal AI Reasoning

📄 TOP PAPERS:
  1. Efficient Attention Mechanisms for Transformers
  2. Zero-Shot Learning in Vision-Language Models
  3. Reinforcement Learning for Real-World Robotics
```

### HTML Output
- 📱 Mobile-responsive, 600px max-width layout
- 🎨 Clean, modern aesthetic with inline CSS
- 🔗 Links to all sources
- 💌 Email client compatible
- ♿ Accessible — minimum 4.5:1 contrast ratio

---

## 🙏 Acknowledgments

- [FastMCP](https://github.com/jlowin/fastmcp) — Simplified MCP server creation
- [Anthropic](https://www.anthropic.com) — Claude AI and MCP framework
- [Groq](https://groq.com) — Fast, free LLM inference
- [python-telegram-bot](https://python-telegram-bot.org) — Telegram Bot framework
- [arXiv API](https://arxiv.org/help/api) — Research paper access
- [GitHub API](https://docs.github.com/en/rest) — Repository data
- [Reddit API (PRAW)](https://praw.readthedocs.io) — Reddit discussions
- [Product Hunt API](https://api.producthunt.com/v2/docs) — Product discovery

---

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with 🤖 AI & ❤️ Human creativity

</div>