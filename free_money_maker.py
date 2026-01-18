#!/usr/bin/env python3
"""
🚀 WORKING MONEY MAKER - FINAL FIXED VERSION
✅ Fixed: google-genai new API
✅ Fixed: Auto mode for GitHub Actions
✅ Fixed: WordPress REST API
"""

import feedparser
import requests
import json
import time
import os
import random
import hashlib
from datetime import datetime
import sys
from pathlib import Path

# =================== FIXED CONFIG ===================
class WorkingConfig:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    WORDPRESS_URL = os.getenv("WORDPRESS_URL", "")
    WORDPRESS_USER = os.getenv("WORDPRESS_USER", "")
    WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD", "")
    
    # For testing
    TEST_MODE = os.getenv("TEST_MODE", "True").lower() == "true"
    
    # RSS feeds
    RSS_FEEDS = [
        "https://techcrunch.com/feed/",
        "https://www.coindesk.com/feed/",
        "https://www.investopedia.com/feed/"
    ]

# =================== SIMPLE GEMINI GENERATOR ===================
class SimpleGeminiGenerator:
    """Simplified working version with new google-genai API"""
    
    def __init__(self, config):
        self.config = config
        self.client = None
        
        try:
            # NEW API WAY (October 2024+)
            from google import genai
            self.client = genai.Client(api_key=config.GEMINI_API_KEY)
            print("✅ Gemini client initialized successfully")
        except ImportError:
            print("❌ google-genai not installed. Run: pip install google-genai")
        except Exception as e:
            print(f"❌ Gemini init error: {e}")
    
    def generate_article(self, topic):
        """Generate article with Gemini"""
        
        if not self.client:
            return self.create_fallback_article(topic)
        
        prompt = f"""Write a professional 800-word blog post about: {topic}

Target audience: American professionals interested in technology and finance.

Structure:
1. Introduction explaining why this topic matters
2. 3-4 key points with examples
3. Practical applications
4. Future trends
5. Conclusion with actionable advice

Write in engaging, SEO-friendly American English.
Add H2 headings for each section.
Include bullet points for readability."""

        try:
            print(f"🤖 Generating: {topic[:50]}...")
            
            # NEW API CALL
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            
            content = response.text
            
            return {
                'title': topic,
                'content': content,
                'word_count': len(content.split()),
                'status': 'success'
            }
            
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            return self.create_fallback_article(topic)
    
    def create_fallback_article(self, topic):
        """Create simple article if Gemini fails"""
        
        content = f"""<h1>{topic}</h1>
        <p>This is a comprehensive guide about {topic}.</p>
        
        <h2>Why {topic} Matters</h2>
        <p>Understanding {topic} is crucial in today's digital age.</p>
        
        <h2>Key Benefits</h2>
        <ul>
            <li>Increased efficiency</li>
            <li>Better decision making</li>
            <li>Competitive advantage</li>
        </ul>
        
        <h2>Getting Started</h2>
        <p>Begin by researching the basics and then implement step by step.</p>"""
        
        return {
            'title': topic,
            'content': content,
            'word_count': 150,
            'status': 'fallback'
        }

# =================== SIMPLE PUBLISHER ===================
class SimplePublisher:
    """Simple publisher that works with REST API or saves to file"""
    
    def __init__(self, config):
        self.config = config
    
    def publish(self, article):
        """Publish article"""
        
        if self.config.TEST_MODE:
            return self.save_to_file(article)
        
        # Try WordPress REST API
        success = self.try_wordpress(article)
        
        if success:
            return success
        else:
            return self.save_to_file(article)
    
    def try_wordpress(self, article):
        """Try to publish to WordPress"""
        
        if not all([self.config.WORDPRESS_URL, 
                   self.config.WORDPRESS_USER, 
                   self.config.WORDPRESS_PASSWORD]):
            return False
        
        try:
            # WordPress REST API endpoint
            api_url = self.config.WORDPRESS_URL
            if not api_url.endswith("/wp-json/wp/v2/posts"):
                if api_url.endswith("/wp-json/wp/v2"):
                    api_url += "/posts"
                else:
                    api_url = api_url.rstrip("/") + "/wp-json/wp/v2/posts"
            
            # Prepare post data
            post_data = {
                "title": article['title'],
                "content": article['content'],
                "status": "publish"
            }
            
            # Basic authentication
            auth = (self.config.WORDPRESS_USER, self.config.WORDPRESS_PASSWORD)
            
            response = requests.post(
                api_url,
                json=post_data,
                auth=auth,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Published to WordPress! ID: {response.json().get('id')}")
                return True
            else:
                print(f"❌ WordPress error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️ WordPress error: {e}")
            return False
    
    def save_to_file(self, article):
        """Save article to file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"article_{timestamp}.html"
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{article['title']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; }}
        .info {{ background: #f5f5f5; padding: 15px; border-radius: 8px; }}
    </style>
</head>
<body>
    <div class="info">
        <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
        <strong>Status:</strong> {article.get('status', 'unknown')}<br>
        <strong>Words:</strong> {article['word_count']}
    </div>
    
    {article['content']}
    
    <div style="margin-top: 40px; padding: 20px; background: #e8f5e9; border-radius: 8px;">
        <h3>✅ Article Generated Successfully!</h3>
        <p>This article was automatically generated.</p>
    </div>
</body>
</html>"""
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"💾 Saved to: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Save error: {e}")
            return None

# =================== MAIN WORKFLOW ===================
class WorkingMoneyMaker:
    """Working money maker - simple and reliable"""
    
    def __init__(self):
        self.config = WorkingConfig()
        self.generator = SimpleGeminiGenerator(self.config)
        self.publisher = SimplePublisher(self.config)
    
    def run(self):
        """Main workflow"""
        
        print(f"\n{'='*60}")
        print(f"🚀 WORKING MONEY MAKER - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*60}")
        
        # 1. Get topic
        topic = self.get_topic()
        print(f"📝 Topic: {topic}")
        
        # 2. Generate content
        print("🤖 Generating article...")
        article = self.generator.generate_article(topic)
        
        # 3. Publish/save
        print("📤 Publishing...")
        result = self.publisher.publish(article)
        
        # 4. Log result
        self.log_result(article, result)
        
        print(f"\n✅ Process completed!")
        
        return result
    
    def get_topic(self):
        """Get topic from RSS or fallback"""
        
        try:
            feed_url = random.choice(self.config.RSS_FEEDS)
            feed = feedparser.parse(feed_url)
            
            if feed.entries:
                entry = random.choice(feed.entries[:5])
                return entry.title
        except:
            pass
        
        # Fallback topics
        topics = [
            "AI in Modern Business",
            "Cryptocurrency Investment Strategies",
            "Passive Income Online",
            "Digital Marketing Trends 2024",
            "E-commerce Automation"
        ]
        
        return random.choice(topics)
    
    def log_result(self, article, result):
        """Log the result"""
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'title': article['title'],
            'word_count': article['word_count'],
            'status': article.get('status', 'unknown'),
            'result': str(result)[:100]
        }
        
        try:
            with open('success_log.json', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except:
            pass

# =================== SIMPLE GITHUB WORKFLOW ===================
def create_simple_workflow():
    """Create simple GitHub workflow"""
    
    return """name: Simple Money Maker

on:
  schedule:
    - cron: '0 14 * * *'  # 10 AM EST
    - cron: '0 21 * * *'  # 5 PM EST
  workflow_dispatch:

jobs:
  generate:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install feedparser requests google-genai
    
    - name: Run Money Maker
      env:
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        WORDPRESS_URL: ${{ secrets.WORDPRESS_URL }}
        WORDPRESS_USER: ${{ secrets.WORDPRESS_USER }}
        WORDPRESS_PASSWORD: ${{ secrets.WORDPRESS_PASSWORD }}
        TEST_MODE: ${{ secrets.TEST_MODE || 'True' }}
      run: |
        python working_maker.py --auto
    
    - name: Upload articles
      uses: actions/upload-artifact@v3
      with:
        name: articles
        path: |
          article_*.html
          success_log.json
"""

# =================== MAIN ===================
def main():
    """Main function - handles both auto and interactive mode"""
    
    print("\n" + "="*60)
    print("💰 WORKING MONEY MAKER - SIMPLE & RELIABLE")
    print("="*60)
    
    # AUTO MODE - for GitHub Actions
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        print("\n🤖 Running in AUTO mode (GitHub Actions)...")
        maker = WorkingMoneyMaker()
        maker.run()
        return
    
    # INTERACTIVE MODE
    print("\n1. Generate article now")
    print("2. Generate 5 test articles")
    print("3. View GitHub workflow")
    print("4. Exit")
    
    try:
        choice = input("\nChoose (1-4): ").strip()
    except:
        choice = "1"
    
    if choice == "1":
        maker = WorkingMoneyMaker()
        maker.run()
    elif choice == "2":
        print("\n🧪 Generating 5 test articles...")
        for i in range(5):
            print(f"\n--- Article {i+1} ---")
            maker = WorkingMoneyMaker()
            maker.config.TEST_MODE = True
            maker.run()
            time.sleep(2)
    elif choice == "3":
        print("\n📋 GitHub Workflow:")
        print(create_simple_workflow())
    else:
        print("\n👋 Goodbye!")

# =================== QUICK TEST ===================
def quick_test():
    """Quick test function"""
    
    print("\n⚡ QUICK TEST - Checking setup...")
    
    # Test Gemini
    try:
        from google import genai
        print("✅ google-genai package: OK")
    except ImportError:
        print("❌ google-genai not installed")
        print("   Run: pip install google-genai")
    
    # Test environment
    config = WorkingConfig()
    
    if config.GEMINI_API_KEY:
        print("✅ GEMINI_API_KEY: Set")
    else:
        print("❌ GEMINI_API_KEY: Not set")
    
    if config.WORDPRESS_URL:
        print("✅ WORDPRESS_URL: Set")
    else:
        print("❌ WORDPRESS_URL: Not set")
    
    # Generate one test article
    print("\n🚀 Generating test article...")
    maker = WorkingMoneyMaker()
    maker.config.TEST_MODE = True
    maker.run()
    
    print("\n✅ Test completed!")

# =================== REQUIREMENTS ===================
def show_requirements():
    """Show requirements"""
    
    requirements = """# Requirements for Working Money Maker
feedparser==6.0.10
requests==2.31.0
google-genai>=0.3.0

# Installation
pip install feedparser requests google-genai
"""
    
    print(requirements)

# =================== ENTRY POINT ===================
if __name__ == "__main__":
    
    # Check for test command
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        quick_test()
    elif len(sys.argv) > 1 and sys.argv[1] == "--requirements":
        show_requirements()
    else:
        main()
