"""
MCP Tools Verification Script
Sab tools ko test karta hai aur status report deta hai
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ==================== COLOR OUTPUT ====================

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def success(msg): print(f"{Colors.GREEN}  ✅ {msg}{Colors.RESET}")
def error(msg):   print(f"{Colors.RED}  ❌ {msg}{Colors.RESET}")
def warning(msg): print(f"{Colors.YELLOW}  ⚠️  {msg}{Colors.RESET}")
def info(msg):    print(f"{Colors.CYAN}  ℹ️  {msg}{Colors.RESET}")
def header(msg):  print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}\n  {msg}\n{'='*50}{Colors.RESET}")


# ==================== 1. ENV VARIABLES CHECK ====================

def check_env_variables():
    header("1. Environment Variables Check")
    
    required = {
        "GOOGLE_CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID"),
        "GOOGLE_CLIENT_SECRET": os.getenv("GOOGLE_CLIENT_SECRET"),
        "GOOGLE_REFRESH_TOKEN": os.getenv("GOOGLE_REFRESH_TOKEN"),
    }
    
    optional = {
        "NEWSLETTER_FOLDER_ID": os.getenv("NEWSLETTER_FOLDER_ID"),
        "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
        "PRODUCT_HUNT_API_KEY": os.getenv("PRODUCT_HUNT_API_KEY"),
        "TWITTER_BEARER_TOKEN": os.getenv("TWITTER_BEARER_TOKEN"),
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
        "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN"),
    }
    
    all_required_ok = True
    for key, value in required.items():
        if value:
            success(f"{key} = SET ✓")
        else:
            error(f"{key} = MISSING (Required!)")
            all_required_ok = False
    
    print()
    for key, value in optional.items():
        if value:
            success(f"{key} = SET ✓")
        else:
            warning(f"{key} = NOT SET (Optional - feature disabled)")
    
    return all_required_ok


# ==================== 2. PYTHON PACKAGES CHECK ====================

def check_packages():
    header("2. Python Packages Check")
    
    packages = {
        "fastmcp": "FastMCP Server",
        "arxiv": "arXiv Papers",
        "requests": "HTTP Requests",
        "google.oauth2": "Google OAuth",
        "googleapiclient": "Google Drive/Gmail",
        "dotenv": "Environment Variables",
        "groq": "Groq LLM",
        "telegram": "Telegram Bot",
    }
    
    all_ok = True
    for package, description in packages.items():
        try:
            __import__(package)
            success(f"{package} — {description}")
        except ImportError:
            error(f"{package} — {description} (NOT INSTALLED)")
            all_ok = False
    
    return all_ok


# ==================== 3. ARXIV TEST ====================

def check_arxiv():
    header("3. arXiv Papers API Test")
    
    try:
        import arxiv
        from datetime import timedelta
        
        search = arxiv.Search(
            query="artificial intelligence",
            max_results=3,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        papers = list(search.results())
        
        if papers:
            success(f"arXiv working! Found {len(papers)} papers")
            for p in papers[:2]:
                info(f"  → {p.title[:60]}...")
            return True
        else:
            warning("arXiv returned 0 results")
            return False
            
    except Exception as e:
        error(f"arXiv failed: {str(e)}")
        return False


# ==================== 4. GITHUB TEST ====================

def check_github():
    header("4. GitHub Trending API Test")
    
    try:
        import requests
        
        github_token = os.getenv("GITHUB_TOKEN")
        headers = {"Accept": "application/vnd.github.v3+json"}
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        from datetime import timedelta
        date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        response = requests.get(
            "https://api.github.com/search/repositories",
            params={
                "q": f"topic:artificial-intelligence created:>{date}",
                "sort": "stars",
                "per_page": 3
            },
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            count = len(data.get("items", []))
            success(f"GitHub working! Found {count} repos")
            for repo in data.get("items", [])[:2]:
                info(f"  → {repo['full_name']} ⭐ {repo['stargazers_count']}")
            
            if not github_token:
                warning("No GITHUB_TOKEN — rate limit: 60 req/hour (add token for 5000/hour)")
            return True
        elif response.status_code == 403:
            warning(f"GitHub rate limit hit (Status: 403) — Add GITHUB_TOKEN in .env")
            return False
        else:
            error(f"GitHub failed: Status {response.status_code}")
            return False
            
    except Exception as e:
        error(f"GitHub failed: {str(e)}")
        return False


# ==================== 5. PRODUCT HUNT TEST ====================

def check_product_hunt():
    header("5. Product Hunt API Test")
    
    api_key = os.getenv("PRODUCT_HUNT_API_KEY")
    
    if not api_key:
        warning("PRODUCT_HUNT_API_KEY not set — Skipping test")
        info("Get free key at: https://www.producthunt.com/v2/oauth/applications")
        return None
    
    try:
        import requests
        
        query = """
        query {
          posts(order: VOTES, topic: "artificial-intelligence", first: 3) {
            edges {
              node {
                name
                tagline
                votesCount
              }
            }
          }
        }
        """
        
        response = requests.post(
            "https://api.producthunt.com/v2/api/graphql",
            json={"query": query},
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                error(f"Product Hunt API error: {data['errors']}")
                return False
            
            products = data.get("data", {}).get("posts", {}).get("edges", [])
            success(f"Product Hunt working! Found {len(products)} products")
            for p in products[:2]:
                info(f"  → {p['node']['name']}: {p['node']['tagline'][:50]}")
            return True
        else:
            error(f"Product Hunt failed: Status {response.status_code} — {response.text[:100]}")
            return False
            
    except Exception as e:
        error(f"Product Hunt failed: {str(e)}")
        return False


# ==================== 6. TWITTER/X TEST ====================

def check_twitter():
    header("6. Twitter/X API Test")
    
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    
    if not bearer_token:
        warning("TWITTER_BEARER_TOKEN not set — Skipping test")
        info("Get free key at: https://developer.twitter.com")
        info("Note: Twitter free tier has limited search access")
        return None
    
    try:
        import requests
        
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/recent",
            params={
                "query": "#AI -is:retweet lang:en",
                "max_results": 10,
                "tweet.fields": "public_metrics"
            },
            headers={"Authorization": f"Bearer {bearer_token}"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            tweets = data.get("data", [])
            success(f"Twitter working! Found {len(tweets)} tweets")
            return True
        elif response.status_code == 401:
            error("Twitter: Invalid bearer token")
            return False
        elif response.status_code == 403:
            warning("Twitter: Access forbidden — Free tier may not support search")
            info("Twitter free tier sirf read access deta hai, search nahi")
            return False
        else:
            error(f"Twitter failed: Status {response.status_code}")
            info(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        error(f"Twitter failed: {str(e)}")
        return False


# ==================== 7. GOOGLE DRIVE TEST ====================

def check_google_drive():
    header("7. Google Drive API Test")
    
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN")
    
    if not all([client_id, client_secret, refresh_token]):
        warning("Google credentials not set — Skipping test")
        info("Required: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN")
        return None
    
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret
        )
        
        creds.refresh(Request())
        
        service = build('drive', 'v3', credentials=creds)
        results = service.files().list(pageSize=3, fields="files(id, name)").execute()
        files = results.get('files', [])
        
        success(f"Google Drive working! Found {len(files)} files")
        for f in files[:2]:
            info(f"  → {f['name']}")
        return True
        
    except Exception as e:
        error(f"Google Drive failed: {str(e)}")
        return False


# ==================== 8. GMAIL TEST ====================

def check_gmail():
    header("8. Gmail API Test")
    
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN")
    
    if not all([client_id, client_secret, refresh_token]):
        warning("Google credentials not set — Skipping test")
        return None
    
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret
        )
        
        creds.refresh(Request())
        service = build('gmail', 'v1', credentials=creds)
        
        profile = service.users().getProfile(userId='me').execute()
        success(f"Gmail working! Account: {profile.get('emailAddress')}")
        info(f"  Total messages: {profile.get('messagesTotal', 'N/A')}")
        return True
        
    except Exception as e:
        error(f"Gmail failed: {str(e)}")
        return False


# ==================== 9. GROQ TEST ====================

def check_groq():
    header("9. Groq LLM Test")
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        warning("GROQ_API_KEY not set — Skipping test")
        return None
    
    try:
        from groq import Groq
        
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Say 'Groq working!' in exactly 3 words."}],
            max_tokens=20
        )
        
        reply = response.choices[0].message.content
        success(f"Groq working! Response: {reply}")
        return True
        
    except Exception as e:
        error(f"Groq failed: {str(e)}")
        return False


# ==================== 10. TELEGRAM TEST ====================

def check_telegram():
    header("10. Telegram Bot Token Test")
    
    token = os.getenv("TELEGRAM_TOKEN")
    
    if not token:
        warning("TELEGRAM_TOKEN not set — Skipping test")
        return None
    
    try:
        import requests
        
        response = requests.get(
            f"https://api.telegram.org/bot{token}/getMe",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                bot = data["result"]
                success(f"Telegram Bot working!")
                info(f"  Bot Name: {bot.get('first_name')}")
                info(f"  Username: @{bot.get('username')}")
                return True
        
        error(f"Telegram failed: {response.json().get('description', 'Unknown error')}")
        return False
        
    except Exception as e:
        error(f"Telegram failed: {str(e)}")
        return False


# ==================== FINAL REPORT ====================

def print_summary(results):
    header("FINAL SUMMARY REPORT")
    
    total = len([r for r in results.values() if r is not None])
    passed = len([r for r in results.values() if r is True])
    failed = len([r for r in results.values() if r is False])
    skipped = len([r for r in results.values() if r is None])
    
    print(f"\n  Total Tests : {total + skipped}")
    print(f"  {Colors.GREEN}Passed      : {passed}{Colors.RESET}")
    print(f"  {Colors.RED}Failed      : {failed}{Colors.RESET}")
    print(f"  {Colors.YELLOW}Skipped     : {skipped} (API key not set){Colors.RESET}")
    
    print(f"\n  {'Tool':<20} {'Status'}")
    print(f"  {'-'*35}")
    
    status_map = {
        True: f"{Colors.GREEN}✅ WORKING{Colors.RESET}",
        False: f"{Colors.RED}❌ FAILED{Colors.RESET}",
        None: f"{Colors.YELLOW}⚠️  SKIPPED{Colors.RESET}"
    }
    
    for tool, result in results.items():
        print(f"  {tool:<20} {status_map[result]}")
    
    print(f"\n{'='*50}")
    
    if failed == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}  🎉 Sab tools ready hain!{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}  ⚠️  Kuch tools fix karne hain.{Colors.RESET}")
        print(f"  Failed tools ke liye upar error message dekho.")
    
    print(f"{'='*50}\n")


# ==================== MAIN ====================

if __name__ == "__main__":
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("  ╔══════════════════════════════════════╗")
    print("  ║   MCP Tools Verification Script      ║")
    print("  ║   AI Newsletter Bot                  ║")
    print(f"  ║   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}               ║")
    print("  ╚══════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    
    results = {}
    
    # Run all checks
    check_env_variables()
    check_packages()
    
    results["arXiv"] = check_arxiv()
    results["GitHub"] = check_github()
    results["Product Hunt"] = check_product_hunt()
    results["Twitter/X"] = check_twitter()
    results["Google Drive"] = check_google_drive()
    results["Gmail"] = check_gmail()
    results["Groq LLM"] = check_groq()
    results["Telegram Bot"] = check_telegram()
    
    print_summary(results)