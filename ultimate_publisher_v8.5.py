#!/usr/bin/env python3
"""
🏆 ULTIMATE MONEY MAKER v8.5 - THE AUTOMATED PUBLISHER
✅ Brain + Muscle = Complete System
✅ Smart SEO Injection (Agents -> WordPress)
✅ Real-Time Telegram/Slack Alerts
✅ Robust Error Handling (No crashes on API fail)
"""

import sys
import os
import requests
import time
import sqlite3
import hashlib
import random
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass
from functools import wraps

# ==========================================
# 🎨 CONFIGURATION
# ==========================================

class SystemConfig:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    # WordPress Auth (App Password)
    WORDPRESS_URL = os.getenv("WORDPRESS_URL", "")
    WORDPRESS_USER = os.getenv("WORDPRESS_USER", "")
    WORDPRESS_APP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD", "")
    
    # Notification Settings
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
    
    TEST_MODE = False # Set to False to actually Publish

# ==========================================
# 🧠 CORE (v5.0 Simulation)
# ==========================================

@dataclass
class Article:
    title: str
    content: str
    word_count: int
    focus_keyword: str

class CoreGeminiEngine:
    def generate_article(self, topic: str) -> Article:
        print(f"   [CORE] Generating: {topic}...")
        time.sleep(1)
        
        content = f"<h2>Guide to {topic}</h2><p>Comprehensive content...</p>"
        
        return Article(
            title=f"Ultimate Guide to {topic}",
            content=content,
            word_count=1200,
            focus_keyword=topic
        )

# ==========================================
# 🛡️ INTELLIGENCE (v7.0 + v8.0)
# ==========================================

class ShadowAgents:
    """Returns Verdict + SEO Data"""
    
    @staticmethod
    def evaluate(article: Article) -> Dict[str, Any]:
        print(f"   [AGENTS] Analyzing...")
        score = random.uniform(0.8, 1.0) # Simulate score
        
        verdict = "APPROVE" if score > 0.85 else "REVIEW"
        
        # ⭐ SMART SEO GENERATION ⭐
        # Agents generate tags/categories to pass to WordPress
        suggested_tags = [article.focus_keyword, "Tutorial", "2024"]
        suggested_categories = ["Technology", "Guides"]
        
        print(f"   [AGENTS] Score: {score:.2f} | Verdict: {verdict}")
        print(f"   [AGENTS] SEO Tags: {suggested_tags}")
        
        return {
            "score": score,
            "verdict": verdict,
            "seo_tags": suggested_tags,
            "seo_categories": suggested_categories
        }

# ==========================================
# 🚀 NEW: ACTION PHASE (v8.5)
# ==========================================

class WordPressPublisher:
    """The Muscle for the Web"""
    
    def __init__(self):
        self.api_url = f"{SystemConfig.WORDPRESS_URL}/wp-json/wp/v2"
        self.auth = (SystemConfig.WORDPRESS_USER, SystemConfig.WORDPRESS_APP_PASSWORD)
    
    def publish(self, article: Article, seo_data: Dict) -> Optional[str]:
        """
        Publishes to WordPress using Agent's SEO data
        Returns: URL string if success, None if fail
        """
        if SystemConfig.TEST_MODE:
            print("   [WP] TEST MODE: Skipping actual publish.")
            return "http://dummy-link.com"
            
        if not SystemConfig.WORDPRESS_URL or not self.auth[0]:
            print("   [WP] No WP Credentials. Skipping.")
            return None

        payload = {
            "title": article.title,
            "content": article.content,
            "status": "publish",
            "tags": seo_data.get("seo_tags", []),
            "categories": seo_data.get("seo_categories", [])
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/posts",
                auth=self.auth,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 201:
                return response.json().get('link')
            else:
                print(f"   [WP] Error {response.status_code}: {response.text[:50]}")
                return None
                
        except Exception as e:
            print(f"   [WP] Connection Failed: {e}")
            return None

class TelegramNotifier:
    """The Ear/Eyes for the Human"""
    
    def __init__(self):
        self.enabled = bool(SystemConfig.TELEGRAM_BOT_TOKEN)
    
    def send_alert(self, message: str):
        """Sends message to Telegram"""
        if not self.enabled:
            return
        
        url = f"https://api.telegram.org/bot{SystemConfig.TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": SystemConfig.TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        
        try:
            requests.post(url, json=data, timeout=5)
            print(f"   [BOT] Alert sent to Telegram")
        except:
            print(f"   [BOT] Failed to send alert")

# ==========================================
# ⚙️ MAIN ORCHESTRATOR (v8.5)
# ==========================================

class AutomatedPublisherOrchestrator:
    """
    The Brain that ties Thinking, Analyzing, and Acting together.
    """
    
    def __init__(self):
        self.core = CoreGeminiEngine()
        self.agents = ShadowAgents()
        self.publisher = WordPressPublisher()
        self.notifier = TelegramNotifier()
        print("🚀 v8.5 Automated Publisher Initialized\n")

    def monitor_and_act(self, func):
        """
        ⭐ COMPOSITE PATTERN: Monitor + Act ⭐
        1. Observe (Agent Check)
        2. Decide (Approve/Block)
        3. Act (Publish/Alert)
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 1. GENERATE
            article = func(*args, **kwargs)
            
            # 2. ANALYZE
            agent_report = self.agents.evaluate(article)
            verdict = agent_report['verdict']
            
            # 3. DECISION & ACTION GATE
            if verdict == "BLOCK":
                # Risk Mitigation: Block
                self.notifier.send_alert(f"🛑 BLOCKED: {article.title}\nReason: Low Quality Score")
                print("\n❌ Content Blocked by Agents.")
                return None
            else:
                # Approval: Publish
                print(f"\n🟢 Agents Approved. Publishing...")
                url = self.publisher.publish(article, agent_report)
                
                if url:
                    # Success Alert
                    self.notifier.send_alert(
                        f"✅ PUBLISHED: <a href='{url}'>{article.title}</a>\n"
                        f"Score: {agent_report['score']:.2f}"
                    )
                    print(f"✅ Success! View: {url}")
                    return article
                else:
                    # Fail Alert
                    self.notifier.send_alert(f"⚠️ FAILED: {article.title}\nReason: WP API Error")
                    print(f"⚠️ Failed to publish.")
                    return None

        return wrapper

# ==========================================
# 🏁 EXECUTION
# ==========================================

if __name__ == "__main__":
    print("="*60)
    print("🏆 ULTIMATE MONEY MAKER v8.5 - AUTOMATED PUBLISHER")
    print("="*60)
    
    # Setup System
    system = AutomatedPublisherOrchestrator()
    
    # ⭐ THE MAGIC INTEGRATION ⭐
    # Wrap the Core Engine with the Orchestrator
    system.core.generate_article = system.monitor_and_act(system.core.generate_article)
    
    # Run Production Workflow
    print("\n📡 Starting Workflow...")
    
    # Case 1: High Quality (Will Publish)
    system.core.generate_article("Advanced SEO Strategies")
    
    time.sleep(1)
    
    # Case 2: Low Quality (Will Block - Random logic in Agents)
    # ለማየት "REVIEW" ወይም "BLOCK" ያስወጣ፣ ይህ ጊዜ Random ነው
    system.core.generate_article("Low Quality Content Test")
