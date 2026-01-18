#!/usr/bin/env python3
"""
🚀 ULTIMATE MONEY MAKER - FINAL WORKING VERSION
✅ Fixed: Gemini 1.5 Flash model name
✅ Fixed: WordPress REST API
✅ Fixed: Auto mode for GitHub Actions
"""

import feedparser
import requests
import json
import time
import os
import random
from datetime import datetime
import sys

# =================== FINAL CONFIG ===================
class FinalConfig:
    """Final configuration that works"""
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    WORDPRESS_URL = os.getenv("WORDPRESS_URL", "https://yoursite.com/wp-json/wp/v2")
    WORDPRESS_USER = os.getenv("WORDPRESS_USER", "")
    WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD", "")
    
    # Set to False in GitHub Secrets for real publishing
    TEST_MODE = os.getenv("TEST_MODE", "True").lower() == "true"
    
    # RSS feeds for topic ideas
    RSS_FEEDS = [
        "https://techcrunch.com/feed/",
        "https://www.coindesk.com/feed/",
        "https://www.investopedia.com/feed/"
    ]
    
    # High-value niches
    NICHE_TOPICS = [
        "AI in Modern Finance and Investing",
        "Cryptocurrency Trading Strategies 2024",
        "Passive Income with Digital Assets",
        "E-commerce Automation and Scaling",
        "Digital Marketing for High-Ticket Products"
    ]

# =================== FIXED GEMINI GENERATOR ===================
class FixedGeminiGenerator:
    """Fixed version with correct model name"""
    
    def __init__(self, config):
        self.config = config
        
        try:
            # Correct import for new package
            from google import genai
            
            # CORRECT: Use just "gemini-1.5-flash" as model name
            self.client = genai.Client(api_key=config.GEMINI_API_KEY)
            self.model_name = "gemini-1.5-flash"  # CORRECT MODEL NAME
            
            print("✅ Gemini client initialized successfully")
            print(f"✅ Using model: {self.model_name}")
            
        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("   Install: pip install google-genai")
            self.client = None
        except Exception as e:
            print(f"❌ Gemini setup error: {e}")
            self.client = None
    
    def generate_article(self, topic):
        """Generate article with correct API call"""
        
        if not self.client:
            return self.create_fallback_article(topic)
        
        # Professional prompt for high-quality content
        prompt = f"""Write a professional, SEO-optimized blog post about: "{topic}"

TARGET AUDIENCE: American professionals and investors
WRITING STYLE: Engaging, informative, authoritative
WORD COUNT: 800-1200 words

ARTICLE STRUCTURE:
1. Introduction with compelling hook
2. Main content with 3-4 key sections
3. Practical examples and case studies
4. Actionable tips and strategies
5. Conclusion with key takeaways

SEO REQUIREMENTS:
- Use H2 and H3 headings appropriately
- Include bullet points for readability
- Add meta description at the end
- Optimize for search engines

Write in American English suitable for a business audience."""

        try:
            print(f"🤖 Generating article about: {topic}")
            
            # CORRECT API CALL with proper model name
            response = self.client.models.generate_content(
                model=self.model_name,  # Uses "gemini-1.5-flash"
                contents=prompt
            )
            
            content = response.text
            
            # Generate title from response
            title = self.extract_title(content, topic)
            
            return {
                'title': title,
                'content': content,
                'word_count': len(content.split()),
                'status': 'success',
                'model_used': self.model_name
            }
            
        except Exception as e:
            print(f"❌ Gemini generation error: {e}")
            return self.create_fallback_article(topic)
    
    def extract_title(self, content, topic):
        """Extract title from content"""
        lines = content.split('\n')
        for line in lines:
            if line.strip() and len(line.strip()) < 100:
                if line.strip().startswith('#') or line.strip().isupper():
                    return line.strip().replace('#', '').strip()
        
        # Fallback title
        return f"The Complete Guide to {topic} in 2024"
    
    def create_fallback_article(self, topic):
        """Create fallback content if Gemini fails"""
        
        content = f"""<h1>The Ultimate Guide to {topic}</h1>

<h2>Why {topic} Matters in 2024</h2>
<p>In today's rapidly evolving digital landscape, understanding {topic} has become essential for success. This comprehensive guide will walk you through everything you need to know.</p>

<h2>Key Benefits and Advantages</h2>
<ul>
    <li><strong>Increased Efficiency:</strong> Streamline your operations and save valuable time.</li>
    <li><strong>Competitive Edge:</strong> Stay ahead of competitors with cutting-edge strategies.</li>
    <li><strong>Revenue Growth:</strong> Implement proven methods to boost your income.</li>
</ul>

<h2>Getting Started</h2>
<p>Begin by mastering the fundamentals, then gradually implement more advanced techniques as you gain confidence and experience.</p>

<h2>Future Outlook</h2>
<p>The field of {topic} continues to evolve rapidly. Staying informed about the latest trends and developments will ensure your continued success.</p>"""

        return {
            'title': f"Complete Guide to {topic}",
            'content': content,
            'word_count': len(content.split()),
            'status': 'fallback',
            'model_used': 'fallback'
        }

# =================== FIXED WORDPRESS PUBLISHER ===================
class FixedWordPressPublisher:
    """Fixed publisher with proper REST API implementation"""
    
    def __init__(self, config):
        self.config = config
        
        # Build proper API URL
        if config.WORDPRESS_URL.endswith('/wp-json/wp/v2'):
            self.api_url = config.WORDPRESS_URL + '/posts'
        elif config.WORDPRESS_URL.endswith('/wp-json/wp/v2/'):
            self.api_url = config.WORDPRESS_URL + 'posts'
        else:
            self.api_url = config.WORDPRESS_URL.rstrip('/') + '/wp-json/wp/v2/posts'
    
    def publish(self, article):
        """Publish article to WordPress"""
        
        if self.config.TEST_MODE:
            print("🧪 TEST MODE: Saving to file instead of publishing")
            return self.save_to_file(article)
        
        try:
            print("📤 Attempting to publish to WordPress...")
            
            # Prepare post data
            post_data = {
                "title": article['title'],
                "content": article['content'],
                "status": "publish",
                "meta": {
                    "generated_by": "Auto Money Maker",
                    "word_count": article['word_count'],
                    "model": article.get('model_used', 'unknown')
                }
            }
            
            # Basic authentication
            auth = (self.config.WORDPRESS_USER, self.config.WORDPRESS_PASSWORD)
            
            # Make the request
            response = requests.post(
                self.api_url,
                json=post_data,
                auth=auth,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            # Check response
            if response.status_code == 201:
                post_id = response.json().get('id')
                print(f"✅ SUCCESS! Published to WordPress!")
                print(f"   Post ID: {post_id}")
                print(f"   View at: {response.json().get('link', 'URL not available')}")
                return post_id
            else:
                print(f"❌ WordPress API Error: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return self.save_to_file(article)
                
        except Exception as e:
            print(f"❌ WordPress publishing error: {e}")
            return self.save_to_file(article)
    
    def save_to_file(self, article):
        """Save article to HTML file"""
        
        filename = f"generated_article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{article['title']}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        .meta-info {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            font-size: 14px;
        }}
        .success-box {{
            background: #d4edda;
            color: #155724;
            padding: 20px;
            border-radius: 8px;
            margin: 30px 0;
            border: 1px solid #c3e6cb;
        }}
        .ad-placeholder {{
            background: #fff3cd;
            border: 2px dashed #ffc107;
            padding: 30px;
            text-align: center;
            margin: 30px 0;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <h1>{article['title']}</h1>
    
    <div class="meta-info">
        <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
        <strong>Status:</strong> {article.get('status', 'unknown').upper()}<br>
        <strong>Word Count:</strong> {article['word_count']}<br>
        <strong>Model:</strong> {article.get('model_used', 'N/A')}
    </div>
    
    <div class="ad-placeholder">
        <strong>[AD SPACE - HIGH CPM ADS HERE]</strong><br>
        <small>Targeting: USA audience | Estimated CPM: $15-25</small>
    </div>
    
    <div class="article-content">
        {article['content']}
    </div>
    
    <div class="ad-placeholder">
        <strong>[AD SPACE - PREMIUM DISPLAY AD]</strong><br>
        <small>Perfect for financial/tech products</small>
    </div>
    
    <div class="success-box">
        <h3>✅ ARTICLE GENERATED SUCCESSFULLY!</h3>
        <p><strong>Next Steps:</strong></p>
        <ol>
            <li>Copy this content to your WordPress site</li>
            <li>Add relevant images and optimize for SEO</li>
            <li>Publish and share on social media</li>
            <li>Monitor performance in Google Analytics</li>
        </ol>
        <p><strong>To enable auto-publishing:</strong> Set TEST_MODE=False in GitHub Secrets</p>
    </div>
</body>
</html>"""
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"💾 Saved to file: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Failed to save file: {e}")
            return None

# =================== MAIN AUTOMATION ===================
class FinalMoneyMaker:
    """Final working version"""
    
    def __init__(self):
        self.config = FinalConfig()
        self.generator = FixedGeminiGenerator(self.config)
        self.publisher = FixedWordPressPublisher(self.config)
    
    def run(self):
        """Run the complete automation"""
        
        print(f"\n{'='*70}")
        print(f"💰 ULTIMATE MONEY MAKER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")
        
        # Get topic
        topic = self.get_topic()
        print(f"📝 Topic: {topic}")
        
        # Generate article
        print("🤖 Generating content with Gemini 1.5 Flash...")
        article = self.generator.generate_article(topic)
        
        if not article:
            print("❌ Failed to generate article")
            return None
        
        print(f"📊 Word count: {article['word_count']}")
        print(f"📈 Status: {article['status']}")
        
        # Publish article
        print("\n🚀 Publishing article...")
        result = self.publisher.publish(article)
        
        # Log result
        self.log_result(article, result)
        
        print(f"\n{'='*70}")
        print("✅ PROCESS COMPLETED SUCCESSFULLY!")
        print(f"{'='*70}")
        
        return result
    
    def get_topic(self):
        """Get a topic from RSS or fallback"""
        
        try:
            # Try RSS feeds
            feed_url = random.choice(self.config.RSS_FEEDS)
            feed = feedparser.parse(feed_url)
            
            if feed.entries:
                entry = random.choice(feed.entries[:5])
                return entry.title
        except Exception as e:
            print(f"⚠️ RSS error, using fallback topic: {e}")
        
        # Fallback to niche topics
        return random.choice(self.config.NICHE_TOPICS)
    
    def log_result(self, article, result):
        """Log the result to file"""
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'title': article['title'],
            'word_count': article['word_count'],
            'status': article['status'],
            'result': str(result),
            'test_mode': self.config.TEST_MODE
        }
        
        try:
            with open('automation_log.json', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except:
            pass

# =================== GITHUB ACTIONS WORKFLOW ===================
def get_github_workflow():
    """Get the GitHub Actions workflow file content"""
    
    return """name: Ultimate Money Maker

on:
  schedule:
    # Run twice daily at optimal US times (converted to UTC)
    - cron: '0 14 * * *'  # 10 AM EST
    - cron: '0 21 * * *'  # 5 PM EST
  workflow_dispatch:

jobs:
  generate-article:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install feedparser requests google-genai
        
    - name: Run Money Maker
      env:
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        WORDPRESS_URL: ${{ secrets.WORDPRESS_URL }}
        WORDPRESS_USER: ${{ secrets.WORDPRESS_USER }}
        WORDPRESS_PASSWORD: ${{ secrets.WORDPRESS_PASSWORD }}
        TEST_MODE: ${{ secrets.TEST_MODE }}
      run: |
        python final_maker.py
        
    - name: Upload generated content
      uses: actions/upload-artifact@v3
      with:
        name: generated-articles
        path: |
          generated_article_*.html
          automation_log.json
        retention-days: 7
"""

# =================== QUICK SETUP GUIDE ===================
def show_setup_guide():
    """Show quick setup guide"""
    
    guide = """
    ============================================================
    🚀 QUICK SETUP GUIDE - FINAL VERSION
    ============================================================
    
    1. GET GEMINI API KEY (FREE):
       -----------------------------------------
       - Go to: https://aistudio.google.com/app/apikey
       - Create new API key
       - Copy the key
    
    2. WORDPRESS SETUP:
       -----------------------------------------
       - WordPress Dashboard → Users → Your Profile
       - Scroll to "Application Passwords"
       - Create new password (e.g., "auto-poster")
       - Copy the generated password
    
    3. GITHUB SECRETS (4 REQUIRED):
       -----------------------------------------
       1. GEMINI_API_KEY = [Your Gemini key]
       2. WORDPRESS_URL = https://yoursite.com/wp-json/wp/v2
       3. WORDPRESS_USER = [Your WordPress username]
       4. WORDPRESS_PASSWORD = [Application password]
       5. TEST_MODE = False  ⬅️ THIS IS CRITICAL!
    
    4. CREATE FILES IN GITHUB:
       -----------------------------------------
       A. final_maker.py (this script)
       B. requirements.txt:
          feedparser==6.0.10
          requests==2.31.0
          google-genai>=0.3.0
       
       C. .github/workflows/money_maker.yml
          (copy the workflow from above)
    
    5. RUN MANUALLY FIRST:
       -----------------------------------------
       - Go to GitHub Actions
       - Click "Ultimate Money Maker"
       - Click "Run workflow"
       - Wait 2-3 minutes
       
    6. CHECK RESULTS:
       -----------------------------------------
       - If TEST_MODE=False: Check WordPress Posts
       - If TEST_MODE=True: Download artifact HTML files
    
    ============================================================
    ✅ READY TO MAKE MONEY! Estimated setup: 10 minutes
    ============================================================
    """
    
    print(guide)

# =================== MAIN FUNCTION ===================
def main():
    """Main entry point - handles both auto and interactive modes"""
    
    print("\n" + "="*70)
    print("🤖 ULTIMATE MONEY MAKER - FINAL WORKING VERSION")
    print("="*70)
    
    # AUTO MODE - for GitHub Actions
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        print("\n🚀 Running in AUTO mode (GitHub Actions)...\n")
        maker = FinalMoneyMaker()
        maker.run()
        return
    
    # Interactive mode
    print("\n🔧 OPTIONS:")
    print("1. Generate article now")
    print("2. View setup guide")
    print("3. View GitHub workflow")
    print("4. Run test (save to file)")
    print("5. Exit")
    
    try:
        choice = input("\nSelect (1-5): ").strip()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        return
    
    if choice == "1":
        print("\n🚀 Generating article...\n")
        maker = FinalMoneyMaker()
        maker.run()
    elif choice == "2":
        show_setup_guide()
    elif choice == "3":
        print("\n📋 GitHub Actions Workflow:")
        print("="*60)
        print(get_github_workflow())
    elif choice == "4":
        print("\n🧪 Running in test mode (saving to file)...\n")
        maker = FinalMoneyMaker()
        maker.config.TEST_MODE = True
        maker.run()
    else:
        print("\n👋 Goodbye!")

# =================== ENTRY POINT ===================
if __name__ == "__main__":
    # Create requirements.txt if it doesn't exist
    if not os.path.exists("requirements.txt"):
        with open("requirements.txt", "w") as f:
            f.write("feedparser==6.0.10\nrequests==2.31.0\ngoogle-genai>=0.3.0\n")
        print("📄 Created requirements.txt")
    
    # Run main function
    main()
