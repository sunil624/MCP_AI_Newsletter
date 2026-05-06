"""
AI Newsletter Telegram Bot
Uses Groq LLM + MCP Tools to generate newsletters
"""

import os
import logging
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)
from groq import Groq
import arxiv
import requests
from datetime import timedelta

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== CONFIG ====================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)


# ==================== RESEARCH TOOLS ====================

def fetch_arxiv_papers(query="artificial intelligence", max_results=5, days_back=7):
    """Fetch latest AI papers from arXiv"""
    try:
        date_threshold = datetime.now() - timedelta(days=days_back)
        search = arxiv.Search(
            query=query,
            max_results=max_results * 2,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        papers = []
        for result in search.results():
            if result.published.replace(tzinfo=None) >= date_threshold:
                papers.append({
                    "title": result.title,
                    "authors": [a.name for a in result.authors[:2]],
                    "summary": result.summary[:300] + "...",
                    "url": result.entry_id,
                    "published": result.published.strftime("%Y-%m-%d")
                })
                if len(papers) >= max_results:
                    break
        return papers
    except Exception as e:
        logger.error(f"arXiv error: {e}")
        return []


def fetch_github_trending(language="python", days_back=7):
    """Fetch trending AI repos from GitHub"""
    try:
        date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        url = "https://api.github.com/search/repositories"
        headers = {"Accept": "application/vnd.github.v3+json"}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"token {GITHUB_TOKEN}"

        params = {
            "q": f"language:{language} created:>{date} topic:artificial-intelligence",
            "sort": "stars",
            "order": "desc",
            "per_page": 5
        }
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        repos = []
        for item in data.get("items", [])[:5]:
            repos.append({
                "name": item["name"],
                "description": item.get("description", "No description")[:200],
                "stars": item["stargazers_count"],
                "url": item["html_url"],
                "language": item.get("language", "N/A")
            })
        return repos
    except Exception as e:
        logger.error(f"GitHub error: {e}")
        return []


def generate_with_groq(prompt, system_prompt=None):
    """Generate content using Groq LLM"""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=2000,
        temperature=0.7
    )
    return response.choices[0].message.content


# ==================== BOT COMMANDS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message"""
    keyboard = [
        [InlineKeyboardButton("📰 Full Newsletter", callback_data="newsletter")],
        [InlineKeyboardButton("📄 AI Papers", callback_data="papers"),
         InlineKeyboardButton("💻 GitHub Repos", callback_data="repos")],
        [InlineKeyboardButton("🤖 Ask AI", callback_data="ask")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚀 *AI Newsletter Bot*\n\n"
        "Main tumhare liye latest AI research, trending repos, "
        "aur weekly newsletter generate kar sakta hoon!\n\n"
        "Kya chahiye?",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help message"""
    await update.message.reply_text(
        "📋 *Available Commands:*\n\n"
        "/start — Main menu\n"
        "/newsletter — Full weekly newsletter\n"
        "/papers — Latest AI research papers\n"
        "/repos — Trending GitHub repositories\n"
        "/ask <question> — Ask anything about AI\n"
        "/help — Yeh message\n\n"
        "💡 *Tip:* /ask What is RAG in AI?",
        parse_mode="Markdown"
    )


async def papers_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetch and display AI papers"""
    msg = await update.message.reply_text("📄 arXiv se papers fetch kar raha hoon... ⏳")

    papers = fetch_arxiv_papers(max_results=5)

    if not papers:
        await msg.edit_text("❌ Papers fetch karne mein error. Thodi der baad try karo.")
        return

    # Use Groq to summarize
    papers_text = "\n".join([f"- {p['title']}: {p['summary']}" for p in papers])
    summary = generate_with_groq(
        f"Yeh AI research papers hain. Inhe concise aur engaging way mein summarize karo Hindi-English mix mein:\n\n{papers_text}",
        system_prompt="Tum ek AI newsletter editor ho. Short, engaging summaries likhte ho."
    )

    response = "📄 *Latest AI Research Papers*\n\n"
    for i, paper in enumerate(papers, 1):
        response += f"*{i}. {paper['title']}*\n"
        response += f"👥 {', '.join(paper['authors'])}\n"
        response += f"📅 {paper['published']}\n"
        response += f"🔗 [Read Paper]({paper['url']})\n\n"

    response += f"---\n🤖 *AI Summary:*\n{summary}"

    await msg.edit_text(response[:4096], parse_mode="Markdown", disable_web_page_preview=True)


async def repos_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetch trending GitHub repos"""
    msg = await update.message.reply_text("💻 GitHub se trending repos fetch kar raha hoon... ⏳")

    repos = fetch_github_trending()

    if not repos:
        await msg.edit_text("❌ Repos fetch karne mein error. Thodi der baad try karo.")
        return

    response = "💻 *Trending AI GitHub Repositories*\n\n"
    for i, repo in enumerate(repos, 1):
        response += f"*{i}. {repo['name']}*\n"
        response += f"📝 {repo['description']}\n"
        response += f"⭐ {repo['stars']:,} stars | 💻 {repo['language']}\n"
        response += f"🔗 [View Repo]({repo['url']})\n\n"

    await msg.edit_text(response[:4096], parse_mode="Markdown", disable_web_page_preview=True)


async def newsletter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate full newsletter"""
    msg = await update.message.reply_text(
        "📰 Weekly newsletter generate kar raha hoon...\n"
        "⏳ Thoda time lagega (30-60 seconds)..."
    )

    # Fetch all data
    await msg.edit_text("📄 AI Papers fetch kar raha hoon... (1/3)")
    papers = fetch_arxiv_papers(max_results=5)

    await msg.edit_text("💻 GitHub repos fetch kar raha hoon... (2/3)")
    repos = fetch_github_trending()

    await msg.edit_text("🤖 Groq se newsletter generate kar raha hoon... (3/3)")

    # Prepare content for Groq
    papers_text = "\n".join([f"- {p['title']} by {', '.join(p['authors'])}: {p['summary']}" for p in papers[:3]])
    repos_text = "\n".join([f"- {r['name']} ({r['stars']} stars): {r['description']}" for r in repos[:3]])

    newsletter_prompt = f"""
Aaj ki date: {datetime.now().strftime("%B %d, %Y")}

Latest AI Papers:
{papers_text}

Trending GitHub Repos:
{repos_text}

Inke basis pe ek engaging weekly AI newsletter likho jo:
1. Ek catchy headline ho
2. Is week ka "Big Story" ho (papers se)
3. Top 3 papers ka brief mention ho
4. Top 3 repos ka mention ho
5. Closing thought ho

Format: Hinglish (Hindi + English mix) mein likho, professional lekin friendly tone.
"""

    newsletter = generate_with_groq(
        newsletter_prompt,
        system_prompt="Tum ek expert AI newsletter editor ho jo engaging, informative content likhte ho."
    )

    # Send newsletter
    header = (
        f"📰 *AI Weekly Newsletter*\n"
        f"📅 {datetime.now().strftime('%B %d, %Y')}\n"
        f"{'─' * 30}\n\n"
    )

    full_newsletter = header + newsletter

    # Split if too long
    if len(full_newsletter) > 4096:
        parts = [full_newsletter[i:i+4096] for i in range(0, len(full_newsletter), 4096)]
        await msg.edit_text(parts[0], parse_mode="Markdown")
        for part in parts[1:]:
            await update.message.reply_text(part, parse_mode="Markdown")
    else:
        await msg.edit_text(full_newsletter, parse_mode="Markdown")


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Answer AI questions using Groq"""
    if not context.args:
        await update.message.reply_text(
            "❓ Kuch poochho!\n\nExample:\n`/ask What is transformer architecture?`",
            parse_mode="Markdown"
        )
        return

    question = " ".join(context.args)
    msg = await update.message.reply_text(f"🤔 Soch raha hoon: _{question}_...", parse_mode="Markdown")

    answer = generate_with_groq(
        question,
        system_prompt="Tum ek AI expert ho. Concise, accurate aur helpful answers dete ho. Hinglish mein baat karo."
    )

    await msg.edit_text(
        f"❓ *{question}*\n\n{answer}",
        parse_mode="Markdown"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard buttons"""
    query = update.callback_query
    await query.answer()

    if query.data == "newsletter":
        await query.message.reply_text("📰 Newsletter generate karna shuru karo:")
        await newsletter_command(query, context)
    elif query.data == "papers":
        await papers_command(query, context)
    elif query.data == "repos":
        await repos_command(query, context)
    elif query.data == "ask":
        await query.message.reply_text(
            "💬 Koi bhi AI question poochho:\n\n`/ask <tumhara sawaal>`",
            parse_mode="Markdown"
        )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages"""
    text = update.message.text

    msg = await update.message.reply_text("🤔 Soch raha hoon...")

    answer = generate_with_groq(
        text,
        system_prompt="Tum ek helpful AI assistant ho jo AI/ML topics mein expert ho. Hinglish mein baat karo."
    )

    await msg.edit_text(answer[:4096])


# ==================== MAIN ====================

def main():
    """Start the bot"""
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN not set!")
        return
    if not GROQ_API_KEY:
        logger.error("GROQ_API_KEY not set!")
        return

    logger.info("Bot starting...")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("papers", papers_command))
    app.add_handler(CommandHandler("repos", repos_command))
    app.add_handler(CommandHandler("newsletter", newsletter_command))
    app.add_handler(CommandHandler("ask", ask_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    logger.info("Bot is running!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
