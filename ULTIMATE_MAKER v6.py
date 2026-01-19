#!/usr/bin/env python3
"""
🏆 ULTIMATE MONEY MAKER v6.0 - THE SHADOW EDITION
✅ Core Logic: UNTOUCHED (Stable)
✅ NEW: Multi-Agent Shadow Mode
✅ NEW: Agent A (SEO Validator)
✅ NEW: Agent B (Quality Scorer)
✅ NEW: Agent C (Safety Guardrail)
✅ NEW: Shadow Confidence Score

Architecture:
  Main Pipeline:  Topic -> Gemini -> WordPress
  Shadow Pipeline: Article -> Agent A -> Agent B -> Agent C -> Confidence Score
"""

import os
import sys
import json
import time
import random
import re
import hashlib
import html
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

# Import External Libs
import feedparser
import requests

# Import Previous Core Components (Assuming v5 logic is embedded)
# For this snippet, I'll re-include the essentials to make it runnable standalone.

# =================== COLORS & UTILS ===================
class Colors:
    HEADER = '\033[95m'; OKBLUE = '\033[94m'; OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'; WARNING = '\033[93m'; FAIL = '\033[91m'
    ENDC = '\033[0m'; BOLD = '\033[1m'

# =================== DATA MODELS ===================

class ContentStatus(Enum): SUCCESS = "success"; FALLBACK = "fallback"; ERROR = "error"

@dataclass
class SEOData:
    focus_keyword: str; meta_description: str; excerpt: str; tags: List[str]; slug: str

@dataclass
class Article:
    title: str; content: str; seo_data: SEOData
    categories: List[str]; featured_image_url: str
    word_count: int; status: ContentStatus; model_used: str
    article_hash: str = ""

# =================== THE NEW SHADOW SYSTEM (ADD-ON) ===================

@dataclass
class AgentReport:
    """Report from a single shadow agent"""
    agent_name: str
    score: float  # 0.0 to 1.0
    verdict: str   # PASS, WARN, FAIL
    details: List[str]

class ShadowAgent:
    """Abstract Base Class for all Agents"""
    
    def __init__(self, name: str):
        self.name = name
    
    def evaluate(self, article: Article) -> AgentReport:
        """Evaluate the article and return a report"""
        raise NotImplementedError

class SEOScoringAgent(ShadowAgent):
    """Agent A: Checks SEO optimization"""
    
    def evaluate(self, article: Article) -> AgentReport:
        issues = []
        score = 1.0
        
        # 1. Check Headings
        if not re.search(r'<h2>', article.content):
            issues.append("Missing H2 headers")
            score -= 0.3
        
        # 2. Check Keyword presence in Title
        keyword = article.seo_data.focus_keyword.lower()
        if keyword not in article.title.lower():
            issues.append(f"Keyword '{keyword}' not in Title")
            score -= 0.2
            
        # 3. Check Content Length
        if article.word_count < 800:
            issues.append(f"Content too short ({article.word_count} words)")
            score -= 0.2
            
        verdict = "PASS" if score > 0.7 else ("WARN" if score > 0.4 else "FAIL")
        return AgentReport(self.name, score, verdict, issues)

class ReadabilityAgent(ShadowAgent):
    """Agent B: Checks reading quality"""
    
    def evaluate(self, article: Article) -> AgentReport:
        issues = []
        score = 1.0
        
        # 1. Check for long paragraphs (> 300 words)
        paragraphs = article.content.split('\n')
        long_paras = [p for p in paragraphs if len(p.split()) > 300]
        
        if long_paras:
            issues.append(f"{len(long_paras)} extremely long paragraphs found")
            score -= 0.2
            
        # 2. Check List usage
        if not re.search(r'<ul>|<ol>', article.content):
            issues.append("No lists found (hard to read)")
            score -= 0.1
            
        verdict = "PASS" if score > 0.8 else "WARN"
        return AgentReport(self.name, score, verdict, issues)

class SafetyGuardAgent(ShadowAgent):
    """Agent C: Ethical & Safety Check"""
    
    def __init__(self):
        super().__init__("SafetyGuard")
        # Basic hallucination/exaggeration filters
        self.trigger_words = [
            "100% guaranteed", "instant profit", "get rich quick", 
            "cure cancer", "hack the stock market", "illegal"
        ]
    
    def evaluate(self, article: Article) -> AgentReport:
        issues = []
        score = 1.0
        content_lower = article.content.lower()
        
        for word in self.trigger_words:
            if word in content_lower:
                issues.append(f"Potential risk word: '{word}'")
                score -= 0.3 # Heavy penalty
                
        verdict = "PASS" if score >= 1.0 else ("WARN" if score >= 0.7 else "FAIL")
        return AgentReport(self.name, score, verdict, issues)

class ShadowOrchestrator:
    """Manages all shadow agents"""
    
    def __init__(self, enable_shadow_mode: bool = True):
        self.enable_shadow_mode = enable_shadow_mode
        self.agents = [
            SEOScoringAgent("SEOValidator"),
            ReadabilityAgent("ReadabilityChecker"),
            SafetyGuardAgent()
        ]
        
    def evaluate_article(self, article: Article) -> Optional[Dict]:
        """Run all agents on the article"""
        if not self.enable_shadow_mode:
            return None
            
        print(f"\n{Colors.OKCYAN}👁️  SHADOW MODE: Running {len(self.agents)} Agents...{Colors.ENDC}")
        
        reports = []
        total_score = 0.0
        
        for agent in self.agents:
            report = agent.evaluate(article)
            reports.append(report)
            total_score += report.score
            
            # Log Agent Result
            symbol = "✅" if report.verdict == "PASS" else ("⚠️" if report.verdict == "WARN" else "❌")
            print(f"   {symbol} {agent.name}: {report.verdict} (Score: {report.score:.2f})")
            if report.details:
                for detail in report.details:
                    print(f"      • {detail}")
        
        avg_score = total_score / len(self.agents)
        
        # Calculate Confidence
        confidence = "LOW" if avg_score < 0.6 else ("MEDIUM" if avg_score < 0.85 else "HIGH")
        
        print(f"\n{Colors.BOLD}🤖 SHADOW CONSENSUS: {confidence} ({avg_score:.2%}){Colors.ENDC}")
        
        # Save Shadow Report
        report_data = {
            'article_hash': article.article_hash,
            'title': article.title,
            'timestamp': datetime.now().isoformat(),
            'overall_confidence': avg_score,
            'verdict': confidence,
            'agent_reports': [
                {
                    'agent': r.agent_name,
                    'score': r.score,
                    'verdict': r.verdict,
                    'issues': r.details
                } for r in reports
            ]
        }
        
        # Save to File
        os.makedirs("shadow_reports", exist_ok=True)
        with open(f"shadow_reports/{article.article_hash}.json", 'w') as f:
            json.dump(report_data, f, indent=2)
            
        return report_data

# =================== CORE ENGINE (Simplified for Demo) ===================

class DummyGeminiEngine:
    """Simulates the Engine for demo purposes"""
    def generate_article(self, topic: str) -> Article:
        print(f"   Generating: {topic}...")
        time.sleep(0.5)
        
        # Create a dummy article with some flaws to test agents
        html_content = f"""
        <h2>Introduction to {topic}</h2>
        <p>{topic} is 100% guaranteed to change your life. It is the best.</p>
        <p>This is a very long paragraph that repeats many times just to test the readability agent. It goes on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on.</p>
        <p>Here are some points:</p>
        <ul><li>Point 1</li><li>Point 2</li></ul>
        """
        
        return Article(
            title=f"Mastering {topic}",
            content=html_content,
            seo_data=SEOData(
                focus_keyword="Success", # Mismatch to test SEO agent
                meta_description="...", excerpt="...", tags=[], slug="test"
            ),
            categories=["Tech"],
            featured_image_url="",
            word_count=100,
            status=ContentStatus.SUCCESS,
            model_used="dummy",
            article_hash=hashlib.md5(topic.encode()).hexdigest()[:8]
        )

# =================== MAIN ORCHESTRATOR ===================

class UltimateMoneyMakerV6:
    """Orchestrator integrating the Shadow System"""
    
    def __init__(self):
        self.engine = DummyGeminiEngine()
        # Initialize Shadow Mode
        self.shadow_orchestrator = ShadowOrchestrator(enable_shadow_mode=True)
        
    def run(self, topic: str):
        print(f"{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}🚀 RUNNING v6.0 SHADOW EDITION{Colors.ENDC}")
        print(f"{Colors.BOLD}{'='*60}{Colors.ENDC}\n")
        
        # 1. CORE GENERATION (Original Logic)
        article = self.engine.generate_article(topic)
        print(f"\n{Colors.OKGREEN}✅ Core Generation Complete{Colors.ENDC}\n")
        
        # 2. SHADOW EVALUATION (New Add-On - DOES NOT BLOCK)
        # If you want it to block, check shadow_report['verdict']
        shadow_report = self.shadow_orchestrator.evaluate_article(article)
        
        # 3. PUBLISH DECISION (Smart Decision)
        if shadow_report:
            if shadow_report['verdict'] == "LOW":
                print(f"\n{Colors.FAIL}🛑 BLOCKED: Shadow agents detected LOW confidence.{Colors.ENDC}")
                print("   Article saved to drafts instead of publishing.")
                # Logic: Save as Draft
            else:
                print(f"\n{Colors.OKGREEN}✅ PROCEEDING: Publishing with {shadow_report['verdict']} confidence.{Colors.ENDC}")
                # Logic: Publish to WordPress
        
        return article, shadow_report

if __name__ == "__main__":
    system = UltimateMoneyMakerV6()
    # Test with a topic that has "guaranteed" to trigger Safety Agent
    system.run("How to get rich quick with AI")
