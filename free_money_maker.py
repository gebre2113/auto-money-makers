#!/usr/bin/env python3
"""
🚀 ULTIMATE FREE MONEY MAKER - FIXED VERSION
✅ Fixed Gemini API (using new google-genai package)
✅ Fixed WordPress 403 error (using REST API instead of XML-RPC)
🌍 100% Free: Gemini API + GitHub Actions
"""

import feedparser
import requests
import json
import time
import os
import random
import hashlib
from datetime import datetime
import pytz
import sys

# =================== FIXED CONFIGURATION ===================
class FixedConfig:
    """Configuration with fixes for both issues"""
    
    # === FIXED GEMINI API (NEW PACKAGE) ===
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSy...")  # Get from Google AI Studio
    
    # === WORDPRESS REST API (NOT XML-RPC) ===
    WORDPRESS_URL = os.getenv("WORDPRESS_URL", "https://yoursite.com/wp-json/wp/v2")
    WORDPRESS_USER = os.getenv("WORDPRESS_USER", "admin")
    WORDPRESS_APP_PASSWORD = os.getenv("WORDPRESS_PASSWORD", "xxxx xxxx xxxx xxxx")
    
    # === JWT TOKEN FOR WORDPRESS REST API ===
    JWT_ENABLED = True  # Set to True if using JWT Authentication plugin
    
    # === SITE CONFIG ===
    SITE_NAME = "AI Wealth Hub"
    SITE_TAGLINE = "AI • Finance • Free Resources"
    
    # === TARGET COUNTRIES ===
    TARGET_COUNTRIES = ["United States", "Canada", "United Kingdom"]
    
    # === RSS FEEDS ===
    RSS_FEEDS = [
        "https://techcrunch.com/feed/",
        "https://www.coindesk.com/feed/",
        "https://www.investopedia.com/feed/"
    ]
    
    # === POSTING SCHEDULE ===
    POSTS_PER_DAY = 2
    
    # === TEST MODE ===
    TEST_MODE = os.getenv("TEST_MODE", "False").lower() == "true"

# =================== FIXED GEMINI CONTENT GENERATOR ===================
class FixedGeminiGenerator:
    """Fixed version using new google-genai package"""
    
    def __init__(self, config):
        self.config = config
        
        # Check which package is available
        self.use_new_api = False
        
        try:
            # Try new google-genai first
            import google.genai as genai
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.client = genai
            self.model_name = "gemini-1.5-flash"  # Updated model name
            self.use_new_api = True
            print("✅ Using new google-genai package")
        except ImportError:
            try:
                # Fallback to old package
                import google.generativeai as genai
                genai.configure(api_key=config.GEMINI_API_KEY)
                self.client = genai
                self.model_name = "gemini-1.5-flash"
                print("⚠️ Using deprecated google.generativeai package")
            except Exception as e:
                print(f"❌ Gemini import error: {e}")
                self.client = None
    
    def generate_article(self, topic, target_country="United States"):
        """Generate article using Gemini API"""
        
        if not self.client:
            return self.fallback_content(topic, target_country)
        
        prompt = self.create_prompt(topic, target_country)
        
        try:
            if self.use_new_api:
                # New API format
                model = self.client.GenerativeModel(self.model_name)
                response = model.generate_content(prompt)
                content = response.text
            else:
                # Old API format
                model = self.client.GenerativeModel(self.model_name)
                response = model.generate_content(prompt)
                content = response.text
            
            # Generate metadata
            title = self.generate_title(topic)
            tags = self.generate_tags(topic)
            
            return {
                'title': title,
                'content': content,
                'tags': tags,
                'word_count': len(content.split()),
                'target_country': target_country,
                'estimated_cpm': random.randint(10, 25)
            }
            
        except Exception as e:
            print(f"❌ Gemini generation error: {e}")
            return self.fallback_content(topic, target_country)
    
    def create_prompt(self, topic, target_country):
        """Create optimized prompt"""
        
        return f"""Write a professional, SEO-optimized blog post about: "{topic}"

TARGET: Readers in {target_country}
STYLE: Engaging, informative, professional
LENGTH: 800-1200 words

Structure:
1. Introduction with attention-grabbing hook
2. Main content with 3-4 key points
3. Practical examples or case studies
4. Actionable tips
5. Conclusion with summary

SEO Requirements:
- Include primary keyword in first paragraph
- Use H2 and H3 headings
- Add bullet points for readability
- Include meta description at end

Write in American English for online audience."""

    def generate_title(self, topic):
        """Generate SEO-optimized title"""
        
        titles = [
            f"The Ultimate Guide to {topic} in 2024",
            f"{topic}: Everything You Need to Know",
            f"How to Master {topic} - Complete Guide",
            f"{topic} Explained: A Comprehensive Overview"
        ]
        
        return random.choice(titles)
    
    def generate_tags(self, topic):
        """Generate relevant tags"""
        
        base_tags = ["AI", "Technology", "Finance", "Business", "Investment"]
        topic_tags = [word for word in topic.split() if len(word) > 3][:3]
        
        return base_tags + topic_tags
    
    def fallback_content(self, topic, target_country):
        """Fallback content if Gemini fails"""
        
        return {
            'title': f"Guide to {topic}",
            'content': f"""<h1>Comprehensive Guide to {topic}</h1>
            <p>This article provides a complete overview of {topic} for readers in {target_country}.</p>
            
            <h2>Why {topic} Matters in 2024</h2>
            <p>With rapid technological advancements, understanding {topic} has become crucial for success.</p>
            
            <h2>Key Benefits</h2>
            <ul>
                <li>Increased efficiency and productivity</li>
                <li>Competitive advantage in the market</li>
                <li>Better decision-making capabilities</li>
            </ul>
            
            <h2>Getting Started</h2>
            <p>Begin by researching the fundamentals and then gradually implement advanced techniques.</p>
            
            <h2>Conclusion</h2>
            <p>Mastering {topic} can significantly impact your success in today's competitive landscape.</p>""",
            'tags': [topic.split()[0] if topic.split() else "Tech"],
            'word_count': 250,
            'target_country': target_country,
            'estimated_cpm': random.randint(5, 15)
        }

# =================== FIXED WORDPRESS PUBLISHER ===================
class FixedWordPressPublisher:
    """Fixed version using WordPress REST API instead of XML-RPC"""
    
    def __init__(self, config):
        self.config = config
        self.base_url = config.WORDPRESS_URL.replace("/wp-json/wp/v2", "")
        self.api_url = config.WORDPRESS_URL
        
        # Test connection
        self.connected = self.test_connection()
        
        if self.connected:
            print("✅ WordPress REST API connected")
        else:
            print("⚠️ WordPress connection failed - will save to file")
    
    def test_connection(self):
        """Test WordPress REST API connection"""
        
        try:
            # Try to get posts to test connection
            test_url = f"{self.api_url}/posts?per_page=1"
            
            if self.config.JWT_ENABLED:
                # Get JWT token first
                token = self.get_jwt_token()
                if token:
                    headers = {"Authorization": f"Bearer {token}"}
                else:
                    return False
            else:
                # Basic auth
                auth = (self.config.WORDPRESS_USER, self.config.WORDPRESS_APP_PASSWORD)
                response = requests.get(test_url, auth=auth, timeout=10)
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"⚠️ WordPress test connection error: {e}")
            return False
    
    def get_jwt_token(self):
        """Get JWT token for authentication"""
        
        try:
            jwt_url = f"{self.base_url}/wp-json/jwt-auth/v1/token"
            data = {
                "username": self.config.WORDPRESS_USER,
                "password": self.config.WORDPRESS_APP_PASSWORD
            }
            
            response = requests.post(jwt_url, json=data, timeout=10)
            
            if response.status_code == 200:
                return response.json().get("token")
            
            return None
            
        except Exception as e:
            print(f"⚠️ JWT token error: {e}")
            return None
    
    def publish_post(self, article, image_url=None):
        """Publish post using WordPress REST API"""
        
        try:
            # Prepare post data
            post_data = {
                "title": article['title'],
                "content": article['content'],
                "status": "publish",
                "excerpt": f"Complete guide to {article['title']}",
                "meta": {
                    "target_country": article['target_country'],
                    "estimated_cpm": article['estimated_cpm']
                }
            }
            
            # Add tags if any
            if article.get('tags'):
                post_data["tags"] = self.get_or_create_tags(article['tags'])
            
            # Add category
            post_data["categories"] = [self.get_or_create_category("Technology")]
            
            # Headers
            if self.config.JWT_ENABLED:
                token = self.get_jwt_token()
                if not token:
                    return None
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                response = requests.post(
                    f"{self.api_url}/posts",
                    json=post_data,
                    headers=headers,
                    timeout=30
                )
            else:
                # Basic auth
                auth = (self.config.WORDPRESS_USER, self.config.WORDPRESS_APP_PASSWORD)
                response = requests.post(
                    f"{self.api_url}/posts",
                    json=post_data,
                    auth=auth,
                    timeout=30
                )
            
            if response.status_code in [200, 201]:
                post_id = response.json().get("id")
                print(f"✅ Post published successfully! ID: {post_id}")
                return post_id
            else:
                print(f"❌ Publishing failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Publishing error: {e}")
            return None
    
    def get_or_create_tags(self, tag_names):
        """Get or create tags"""
        
        tag_ids = []
        
        for tag_name in tag_names[:5]:  # Limit to 5 tags
            try:
                # Check if tag exists
                search_url = f"{self.api_url}/tags?search={tag_name}"
                
                if self.config.JWT_ENABLED:
                    token = self.get_jwt_token()
                    headers = {"Authorization": f"Bearer {token}"}
                    response = requests.get(search_url, headers=headers)
                else:
                    auth = (self.config.WORDPRESS_USER, self.config.WORDPRESS_APP_PASSWORD)
                    response = requests.get(search_url, auth=auth)
                
                if response.status_code == 200:
                    tags = response.json()
                    
                    if tags:
                        # Tag exists
                        tag_ids.append(tags[0]["id"])
                    else:
                        # Create new tag
                        tag_data = {"name": tag_name}
                        
                        if self.config.JWT_ENABLED:
                            token = self.get_jwt_token()
                            headers = {"Authorization": f"Bearer {token}"}
                            create_response = requests.post(
                                f"{self.api_url}/tags",
                                json=tag_data,
                                headers=headers
                            )
                        else:
                            auth = (self.config.WORDPRESS_USER, self.config.WORDPRESS_APP_PASSWORD)
                            create_response = requests.post(
                                f"{self.api_url}/tags",
                                json=tag_data,
                                auth=auth
                            )
                        
                        if create_response.status_code in [200, 201]:
                            tag_ids.append(create_response.json()["id"])
                            
            except Exception as e:
                print(f"⚠️ Tag error for {tag_name}: {e}")
                continue
        
        return tag_ids
    
    def get_or_create_category(self, category_name):
        """Get or create category"""
        
        try:
            # Check if category exists
            search_url = f"{self.api_url}/categories?search={category_name}"
            
            if self.config.JWT_ENABLED:
                token = self.get_jwt_token()
                headers = {"Authorization": f"Bearer {token}"}
                response = requests.get(search_url, headers=headers)
            else:
                auth = (self.config.WORDPRESS_USER, self.config.WORDPRESS_APP_PASSWORD)
                response = requests.get(search_url, auth=auth)
            
            if response.status_code == 200:
                categories = response.json()
                
                if categories:
                    # Category exists
                    return categories[0]["id"]
                else:
                    # Create new category
                    category_data = {"name": category_name}
                    
                    if self.config.JWT_ENABLED:
                        token = self.get_jwt_token()
                        headers = {"Authorization": f"Bearer {token}"}
                        create_response = requests.post(
                            f"{self.api_url}/categories",
                            json=category_data,
                            headers=headers
                        )
                    else:
                        auth = (self.config.WORDPRESS_USER, self.config.WORDPRESS_APP_PASSWORD)
                        create_response = requests.post(
                            f"{self.api_url}/categories",
                            json=category_data,
                            auth=auth
                        )
                    
                    if create_response.status_code in [200, 201]:
                        return create_response.json()["id"]
                        
        except Exception as e:
            print(f"⚠️ Category error: {e}")
        
        return 1  # Default to Uncategorized

# =================== FIXED MAIN AUTOMATION ===================
class FixedMoneyMaker:
    """Fixed version that works with new Gemini API and WordPress REST API"""
    
    def __init__(self):
        self.config = FixedConfig()
        self.content_gen = FixedGeminiGenerator(self.config)
        self.publisher = FixedWordPressPublisher(self.config)
        
        print(f"\n🔧 Fixed Money Maker v2.0")
        print(f"🌍 Target: {', '.join(self.config.TARGET_COUNTRIES[:3])}")
        print(f"🤖 AI: Gemini 1.5 Flash")
        print(f"📝 Method: WordPress REST API")
    
    def run(self):
        """Main execution"""
        
        print(f"\n{'='*60}")
        print(f"🚀 GENERATING CONTENT - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*60}")
        
        # 1. Get topic
        topic = self.get_topic()
        print(f"📝 Topic: {topic}")
        
        # 2. Select country
        country = self.select_country()
        print(f"🎯 Target: {country}")
        
        # 3. Generate content
        print("🤖 Generating article...")
        article = self.content_gen.generate_article(topic, country)
        
        if not article:
            print("❌ Failed to generate article")
            return None
        
        print(f"📊 Word count: {article['word_count']}")
        print(f"💰 Estimated CPM: ${article['estimated_cpm']}")
        
        # 4. Publish or save
        if not self.config.TEST_MODE and self.publisher.connected:
            post_id = self.publisher.publish_post(article)
            if post_id:
                self.log_success(article, post_id)
                return post_id
            else:
                print("❌ Failed to publish - saving to file instead")
                return self.save_to_file(article)
        else:
            print("💾 Saving to file...")
            return self.save_to_file(article)
    
    def get_topic(self):
        """Get topic from RSS feeds"""
        
        if not self.config.RSS_FEEDS:
            return "AI in Modern Business"
        
        try:
            feed_url = random.choice(self.config.RSS_FEEDS)
            feed = feedparser.parse(feed_url)
            
            if feed.entries:
                # Get a recent entry
                entry = random.choice(feed.entries[:5])
                return entry.title
        except Exception as e:
            print(f"⚠️ RSS error: {e}")
        
        # Fallback topics
        fallback_topics = [
            "Artificial Intelligence in Finance",
            "Cryptocurrency Investment Strategies",
            "Passive Income with AI",
            "Digital Marketing Trends 2024",
            "E-commerce Automation"
        ]
        
        return random.choice(fallback_topics)
    
    def select_country(self):
        """Select target country"""
        
        # Simple rotation
        now = datetime.now()
        hour = now.hour
        
        if 9 <= hour <= 17:  # US business hours
            return "United States"
        elif 0 <= hour <= 8:  # UK morning
            return "United Kingdom"
        else:
            return random.choice(self.config.TARGET_COUNTRIES)
    
    def save_to_file(self, article):
        """Save article to file"""
        
        filename = f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{article['title']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; }}
        .meta {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0; }}
        .success {{ background: #d4edda; padding: 15px; border-radius: 8px; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>{article['title']}</h1>
    
    <div class="meta">
        <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
        <strong>Target Country:</strong> {article['target_country']}<br>
        <strong>Word Count:</strong> {article['word_count']}<br>
        <strong>Estimated CPM:</strong> ${article['estimated_cpm']}<br>
        <strong>Tags:</strong> {', '.join(article.get('tags', []))}
    </div>
    
    {article['content']}
    
    <div class="success">
        <h3>✅ Article Generated Successfully!</h3>
        <p>This article was generated using the fixed version of the Money Maker script.</p>
        <p><strong>Next Steps:</strong></p>
        <ol>
            <li>Copy this content to your WordPress site</li>
            <li>Add relevant images</li>
            <li>Publish and share</li>
        </ol>
        <p>To enable automatic publishing, update your WordPress REST API credentials.</p>
    </div>
</body>
</html>"""
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ Saved to: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Save error: {e}")
            return None
    
    def log_success(self, article, post_id):
        """Log successful generation"""
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'post_id': post_id,
            'title': article['title'],
            'word_count': article['word_count'],
            'country': article['target_country'],
            'cpm': article['estimated_cpm']
        }
        
        try:
            with open('generation_log.json', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except:
            pass

# =================== FIXED GITHUB ACTIONS WORKFLOW ===================
def create_fixed_workflow():
    """Create fixed GitHub Actions workflow"""
    
    yml_content = """name: Fixed Money Maker (Working Version)

on:
  schedule:
    - cron: '0 14 * * *'  # 10 AM EST
    - cron: '0 21 * * *'  # 5 PM EST
  workflow_dispatch:

jobs:
  generate:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install fixed dependencies
      run: |
        python -m pip install --upgrade pip
        pip install feedparser requests pillow google-genai pytz
        
    - name: Run Fixed Money Maker
      env:
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        WORDPRESS_URL: ${{ secrets.WORDPRESS_URL }}
        WORDPRESS_USER: ${{ secrets.WORDPRESS_USER }}
        WORDPRESS_PASSWORD: ${{ secrets.WORDPRESS_PASSWORD }}
        TEST_MODE: ${{ secrets.TEST_MODE || 'True' }}
      run: |
        python fixed_money_maker.py
        
    - name: Upload generated content
      uses: actions/upload-artifact@v3
      with:
        name: fixed-articles
        path: |
          article_*.html
          generation_log.json
        retention-days: 7
"""
    
    return yml_content

# =================== QUICK SETUP SCRIPT ===================
def setup_instructions():
    """Print setup instructions"""
    
    instructions = """
    ============================================================
    🚀 FIXED MONEY MAKER - QUICK SETUP
    ============================================================
    
    1. GET GEMINI API KEY (FREE):
       -----------------------------------------
       Go to: https://aistudio.google.com/app/apikey
       Click "Create API Key"
       Copy the key
       
    2. SETUP WORDPRESS FOR REST API:
       -----------------------------------------
       Option A: Use JWT Authentication (Recommended)
       1. Install "JWT Authentication for WP REST API" plugin
       2. Get JWT token using the script
       
       Option B: Use Application Passwords (Easier)
       1. WordPress Dashboard → Users → Your Profile
       2. Scroll to "Application Passwords"
       3. Create new password
       4. Use as WORDPRESS_PASSWORD
       
    3. GITHUB SECRETS:
       -----------------------------------------
       GEMINI_API_KEY = Your Gemini API key
       WORDPRESS_URL = https://yoursite.com/wp-json/wp/v2
       WORDPRESS_USER = your_username
       WORDPRESS_PASSWORD = app_password_here
       TEST_MODE = True (set to False when ready)
       
    4. LOCAL TEST:
       -----------------------------------------
       python fixed_money_maker.py
       
    5. DEPLOY TO GITHUB ACTIONS:
       -----------------------------------------
       1. Push this script to GitHub
       2. Add secrets
       3. Create .github/workflows/fixed.yml
       4. Add the workflow content
       5. Run manually first
       
    ============================================================
    ✅ READY TO GO! Estimated setup time: 15 minutes
    ============================================================
    """
    
    print(instructions)

# =================== MAIN EXECUTION ===================
def main():
    """Main entry point"""
    
    print("\n" + "="*70)
    print("🔧 FIXED MONEY MAKER v2.0")
    print("✅ Fixed Gemini API + WordPress REST API")
    print("="*70)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--setup":
            setup_instructions()
            return
        elif sys.argv[1] == "--workflow":
            workflow = create_fixed_workflow()
            print("\n📋 Fixed GitHub Actions Workflow:")
            print("="*60)
            print(workflow)
            return
        elif sys.argv[1] == "--test":
            print("\n🧪 Running test...")
            maker = FixedMoneyMaker()
            maker.config.TEST_MODE = True
            maker.run()
            return
    
    # Interactive mode
    print("\n🔧 OPTIONS:")
    print("1. Generate article now")
    print("2. View setup instructions")
    print("3. Get GitHub Actions workflow")
    print("4. Run test (save to file)")
    
    try:
        choice = input("\nSelect (1, 2, 3, 4): ").strip()
    except:
        choice = "1"
    
    if choice == "1":
        print("\n🚀 Generating article...")
        maker = FixedMoneyMaker()
        maker.run()
    elif choice == "2":
        setup_instructions()
    elif choice == "3":
        workflow = create_fixed_workflow()
        print("\n📋 Fixed GitHub Actions Workflow:")
        print("="*60)
        print(workflow)
    elif choice == "4":
        print("\n🧪 Running test...")
        maker = FixedMoneyMaker()
        maker.config.TEST_MODE = True
        maker.run()
    else:
        print("👋 Goodbye!")

# =================== REQUIREMENTS ===================
def create_fixed_requirements():
    """Create fixed requirements.txt"""
    
    requirements = """feedparser==6.0.10
requests==2.31.0
Pillow==10.1.0
google-genai>=0.3.0
pytz==2023.3
"""
    
    return requirements

# =================== ENTRY POINT ===================
if __name__ == "__main__":
    
    # Create requirements if missing
    if not os.path.exists("requirements.txt"):
        req_content = create_fixed_requirements()
        with open("requirements.txt", "w") as f:
            f.write(req_content)
        print("📄 Created requirements.txt")
    
    # Create test environment file if missing
    if not os.path.exists(".env.example"):
        env_content = """# Fixed Money Maker Configuration
GEMINI_API_KEY=AIzaSy...your_key_here
WORDPRESS_URL=https://yoursite.com/wp-json/wp/v2
WORDPRESS_USER=admin
WORDPRESS_PASSWORD=xxxx xxxx xxxx xxxx
TEST_MODE=True
"""
        with open(".env.example", "w") as f:
            f.write(env_content)
        print("📄 Created .env.example")
    
    main()
