#!/usr/bin/env python3
"""
🏆 ULTIMATE MONEY MAKER v9.0 - THE SELF-OPTIMIZING BRAIN
✅ Closed Feedback Loop (WP -> Analytics -> Brain)
✅ Adaptive Learning (Topics improve over time)
✅ Weighted Topic Selection (Promotes winners, ignores losers)
✅ Historical Data Analysis (Decides what to write next)
"""

import sqlite3
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

# ==========================================
# 🧠 1. LEARNING ENGINE (The Memory)
# ==========================================

class LearningEngine:
    """Tracks what works and what doesn't"""
    
    def __init__(self, db_path="brain_memory.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Stores historical performance of Topics
        c.execute('''CREATE TABLE IF NOT EXISTS topic_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_pattern TEXT,
            views INTEGER,
            comments INTEGER,
            success_score REAL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Stores current weights for categories
        c.execute('''CREATE TABLE IF NOT EXISTS category_weights (
            category TEXT PRIMARY KEY,
            weight REAL DEFAULT 1.0,
            posts_count INTEGER DEFAULT 0
        )''')
        
        conn.commit()
        conn.close()
    
    def record_performance(self, category: str, views: int, comments: int):
        """Updates the brain with real-world results"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Calculate Success Score (Simple formula)
        # Views = 1 point, Comments = 50 points (engagement is valuable)
        score = (views * 1.0) + (comments * 50.0)
        
        # Update Topic Stats
        c.execute('''
            INSERT INTO topic_stats (topic_pattern, views, comments, success_score)
            VALUES (?, ?, ?, ?)
        ''', (category, views, comments, score))
        
        # Update Category Weight
        # ⭐ THE LEARNING LOGIC ⭐
        # If score > 1000 (Good), Increase Weight. If < 500, Decrease.
        c.execute("SELECT weight, posts_count FROM category_weights WHERE category = ?", (category,))
        row = c.fetchone()
        
        if row:
            current_weight, count = row
            new_weight = current_weight
            if score > 1000: new_weight += 0.2 # Reward
            elif score < 500: new_weight -= 0.1 # Punish
            
            # Clamp weight between 0.1 and 5.0
            new_weight = max(0.1, min(5.0, new_weight))
            
            c.execute('''
                UPDATE category_weights SET weight = ?, posts_count = posts_count + 1 
                WHERE category = ?
            ''', (new_weight, category))
        else:
            c.execute('''
                INSERT INTO category_weights (category, weight, posts_count)
                VALUES (?, 1.5, 1)
            ''', (category,))
            
        conn.commit()
        conn.close()
        print(f"   [BRAIN] Learned: {category} Score: {score:.0f}")

# ==========================================
# 🎲 2. SMART SELECTOR (The Decision)
# ==========================================

class SmartTopicSelector:
    """Uses learned weights to choose the next topic"""
    
    def __init__(self, learning_engine: LearningEngine):
        self.engine = learning_engine
        self.topics = {
            "Finance": ["Crypto", "Stocks", "Passive Income"],
            "Tech": ["AI", "Python", "SaaS"],
            "Marketing": ["SEO", "Email", "Ads"],
            "Business": ["Startups", "Management", "Scaling"]
        }
    
    def select_category(self) -> str:
        """
        Selects a category based on WEIGHT.
        If 'Finance' has high weight, it is more likely to be picked.
        """
        conn = sqlite3.connect(self.engine.db_path)
        c = conn.cursor()
        
        c.execute("SELECT category, weight FROM category_weights")
        weights = dict(c.fetchall())
        conn.close()
        
        # Build weighted pool
        pool = []
        for cat in self.topics.keys():
            # Get weight from DB, or default to 1.0
            w = weights.get(cat, 1.0)
            # Add the category 'w' times to the pool
            pool.extend([cat] * int(w * 10)) 
        
        if not pool: pool = list(self.topics.keys())
            
        selected_category = random.choice(pool)
        return selected_category
    
    def get_topic(self) -> str:
        """Generates a full topic"""
        cat = self.select_category()
        keyword = random.choice(self.topics[cat])
        return f"The Future of {keyword} in {cat}"

# ==========================================
# 📊 3. ANALYTICS ENGINE (The Eyes)
# ==========================================

class AnalyticsEngine:
    """Simulates fetching stats from WordPress"""
    
    def get_post_performance(self, post_id: int) -> Dict:
        """
        In production, this hits:
        GET /wp-json/wp/v2/stats/views/{post_id}
        """
        # Simulate learning data
        # Let's pretend 'Finance' posts get more views than 'Business'
        return {
            "views": random.randint(500, 2000),
            "comments": random.randint(0, 20)
        }

# ==========================================
# ⚙️ 4. ORCHESTRATOR (The Integration)
# ==========================================

class SelfOptimizingSystem:
    """v9.0: The Feedback Loop in Action"""
    
    def __init__(self):
        print("🧠 Initializing Self-Optimizing Brain v9.0...")
        self.brain = LearningEngine()
        self.selector = SmartTopicSelector(self.brain)
        self.analytics = AnalyticsEngine()
        
        # Simulate WP Auth
        self.wp_url = "https://site.com/wp-json"
    
    def run_cycle(self):
        """One full learning cycle"""
        
        # 1. THINK (Based on Memory)
        print(f"\n🧠 [THINK] Selecting topic based on learned preferences...")
        topic = self.selector.get_topic()
        category = topic.split()[-1] # Extract 'Finance', 'Tech' etc.
        print(f"   [THINK] Selected Category: {category} (Weighted Selection)")
        
        # 2. ACT (Generate & Publish)
        print(f"🚀 [ACT] Generating and Publishing: {topic}")
        post_id = random.randint(100, 999) # Simulate Post ID
        
        # 3. OBSERVE (Check Performance)
        # In real life, we wait 24h. Here we simulate immediate feedback.
        print(f"📊 [OBSERVE] Fetching Analytics for Post #{post_id}...")
        stats = self.analytics.get_post_performance(post_id)
        
        # 4. LEARN (Update Weights)
        print(f"📚 [LEARN] Updating Brain with new data...")
        self.brain.record_performance(category, stats['views'], stats['comments'])
        
        print(f"✅ Cycle Complete.")

    def train_system(self, cycles=10):
        """Run multiple cycles to demonstrate learning"""
        
        print("\n" + "="*60)
        print("TRAINING MODE: Running 10 Cycles to teach the Brain")
        print("="*60)
        
        for i in range(cycles):
            self.run_cycle()
        
        print("\n" + "="*60)
        print("TRAINING COMPLETE. Let's see what the Brain prefers now:")
        print("="*60)
        
        conn = sqlite3.connect(self.brain.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM category_weights ORDER BY weight DESC")
        rows = c.fetchall()
        
        for r in rows:
            cat, weight, count = r
            bar = "█" * int(weight * 10)
            print(f"{cat.ljust(15)} | Weight: {weight:.2f} | Posts: {count} | {bar}")
        
        conn.close()

# ==========================================
# 🏁 EXECUTION
# ==========================================

if __name__ == "__main__":
    system = SelfOptimizingSystem()
    
    # Run Training
    system.train_system(20)
    
    # Now pick a topic again to see the result
    # The category with the highest weight should appear more often
    print(f"\n🎯 FINAL RECOMMENDATION: {system.selector.get_topic()}")
