#!/usr/bin/env python3
"""
Code Analysis Example
Demonstrates how to analyze code for quality, bugs, security issues, and performance.
"""

import asyncio
import httpx
import os
from typing import Dict, Any, List


class CodeAnalyzerClient:
    """Client for AI-powered code analysis."""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key or os.getenv("AI_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def analyze_code(
        self,
        code: str,
        language: str = "python",
        checks: List[str] = None,
        detailed: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze code for various issues.
        
        Args:
            code: Code to analyze
            language: Programming language
            checks: Types of checks to perform
            detailed: Include detailed explanations
            
        Returns:
            Analysis results with issues and suggestions
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/ai/analyze",
                json={
                    "code": code,
                    "language": language,
                    "checks": checks or ["complexity", "bugs", "security", "performance", "style"],
                    "detailed": detailed
                },
                headers=self.headers,
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()


async def example_complexity_analysis():
    """Example: Analyze code complexity."""
    print("\n" + "="*60)
    print("Example 1: Complexity Analysis")
    print("="*60)
    
    client = CodeAnalyzerClient()
    
    code = """
def process_order(order):
    if order.status == 'pending':
        if order.payment_method == 'credit_card':
            if order.amount > 1000:
                if verify_card(order.card):
                    if check_fraud(order):
                        process_payment(order)
                        send_confirmation(order)
                        return True
                    else:
                        flag_order(order)
                        return False
                else:
                    reject_order(order)
                    return False
            else:
                process_small_payment(order)
                return True
        elif order.payment_method == 'paypal':
            process_paypal(order)
            return True
        else:
            return False
    return False
"""
    
    print("Analyzing code complexity...")
    
    try:
        result = await client.analyze_code(
            code=code,
            language="python",
            checks=["complexity"]
        )
        
        print("\n--- Analysis Results ---")
        print(f"Quality Score: {result.get('quality_score', 0)}/10")
        
        complexity = result.get('complexity', {})
        print(f"\nComplexity Metrics:")
        print(f"  Cyclomatic Complexity: {complexity.get('cyclomatic', 0)}")
        print(f"  Cognitive Complexity: {complexity.get('cognitive', 0)}")
        print(f"  Nesting Depth: {complexity.get('max_nesting', 0)}")
        
        if result.get('issues'):
            print("\n--- Issues Found ---")
            for issue in result['issues']:
                print(f"\n• {issue.get('message')}")
                print(f"  Severity: {issue.get('severity')}")
                print(f"  Line: {issue.get('line')}")
                if issue.get('suggestion'):
                    print(f"  Suggestion: {issue.get('suggestion')}")
    
    except Exception as e:
        print(f"Error: {e}")


async def example_bug_detection():
    """Example: Detect potential bugs."""
    print("\n" + "="*60)
    print("Example 2: Bug Detection")
    print("="*60)
    
    client = CodeAnalyzerClient()
    
    code = """
def divide_numbers(a, b):
    return a / b

def get_user_age(user_dict):
    return user_dict['age']

def process_list(items):
    total = 0
    for i in range(len(items) + 1):
        total += items[i]
    return total

def compare_values(x, y):
    if x = y:  # Bug: assignment instead of comparison
        return True
    return False
"""
    
    print("Detecting bugs...")
    
    try:
        result = await client.analyze_code(
            code=code,
            language="python",
            checks=["bugs"]
        )
        
        print("\n--- Bug Detection Results ---")
        bugs = result.get('bugs_found', [])
        print(f"Total bugs found: {len(bugs)}")
        
        for idx, bug in enumerate(bugs, 1):
            print(f"\n{idx}. {bug.get('type')}")
            print(f"   Line: {bug.get('line')}")
            print(f"   Severity: {bug.get('severity')}")
            print(f"   Description: {bug.get('description')}")
            if bug.get('fix_suggestion'):
                print(f"   Fix: {bug.get('fix_suggestion')}")
    
    except Exception as e:
        print(f"Error: {e}")


async def example_security_analysis():
    """Example: Security vulnerability detection."""
    print("\n" + "="*60)
    print("Example 3: Security Analysis")
    print("="*60)
    
    client = CodeAnalyzerClient()
    
    code = """
import sqlite3

def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()

def save_password(password):
    # Storing password in plain text
    with open('passwords.txt', 'a') as f:
        f.write(password + '\\n')

import pickle

def load_data(filename):
    # Insecure deserialization
    with open(filename, 'rb') as f:
        return pickle.load(f)
"""
    
    print("Analyzing security...")
    
    try:
        result = await client.analyze_code(
            code=code,
            language="python",
            checks=["security"]
        )
        
        print("\n--- Security Analysis ---")
        vulnerabilities = result.get('security_issues', [])
        print(f"Vulnerabilities found: {len(vulnerabilities)}")
        
        for idx, vuln in enumerate(vulnerabilities, 1):
            print(f"\n{idx}. {vuln.get('type')}")
            print(f"   Severity: {vuln.get('severity')}")
            print(f"   Line: {vuln.get('line')}")
            print(f"   Risk: {vuln.get('risk_description')}")
            print(f"   Recommendation: {vuln.get('recommendation')}")
    
    except Exception as e:
        print(f"Error: {e}")


async def example_performance_analysis():
    """Example: Performance analysis."""
    print("\n" + "="*60)
    print("Example 4: Performance Analysis")
    print("="*60)
    
    client = CodeAnalyzerClient()
    
    code = """
def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates

def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result

def concatenate_strings(strings):
    result = ""
    for s in strings:
        result = result + s
    return result
"""
    
    print("Analyzing performance...")
    
    try:
        result = await client.analyze_code(
            code=code,
            language="python",
            checks=["performance"]
        )
        
        print("\n--- Performance Analysis ---")
        issues = result.get('performance_issues', [])
        print(f"Performance issues found: {len(issues)}")
        
        for idx, issue in enumerate(issues, 1):
            print(f"\n{idx}. {issue.get('issue')}")
            print(f"   Impact: {issue.get('impact')}")
            print(f"   Line: {issue.get('line')}")
            print(f"   Current Complexity: {issue.get('current_complexity')}")
            print(f"   Suggested Approach: {issue.get('suggested_approach')}")
            if issue.get('optimized_code'):
                print(f"\n   Optimized Code:")
                print(f"   {issue.get('optimized_code')}")
    
    except Exception as e:
        print(f"Error: {e}")


async def example_style_analysis():
    """Example: Code style analysis."""
    print("\n" + "="*60)
    print("Example 5: Style Analysis")
    print("="*60)
    
    client = CodeAnalyzerClient()
    
    code = """
def calculateTotalPrice(items, discount):
    Total=0
    for Item in items:
        Total+=Item['price']
    if discount>0:
        Total=Total-discount
    return Total

class userManager():
    def __init__(self,db):
        self.Database=db
    
    def GetUser(self, ID):
        return self.Database.query(ID)
"""
    
    print("Analyzing code style...")
    
    try:
        result = await client.analyze_code(
            code=code,
            language="python",
            checks=["style"]
        )
        
        print("\n--- Style Analysis ---")
        style_issues = result.get('style_issues', [])
        print(f"Style issues found: {len(style_issues)}")
        
        for idx, issue in enumerate(style_issues, 1):
            print(f"\n{idx}. {issue.get('issue')}")
            print(f"   Line: {issue.get('line')}")
            print(f"   Convention: {issue.get('convention')}")
            print(f"   Suggestion: {issue.get('suggestion')}")
    
    except Exception as e:
        print(f"Error: {e}")


async def example_comprehensive_analysis():
    """Example: Comprehensive code analysis."""
    print("\n" + "="*60)
    print("Example 6: Comprehensive Analysis")
    print("="*60)
    
    client = CodeAnalyzerClient()
    
    code = """
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/user/<username>')
def get_user(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE name='{username}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result == None:
        return {"error": "Not found"}
    return {"user": result}

def process_data(data):
    result = []
    for i in range(len(data)):
        if data[i] != None:
            if data[i] > 0:
                if data[i] < 100:
                    result.append(data[i] * 2)
    return result
"""
    
    print("Running comprehensive analysis...")
    
    try:
        result = await client.analyze_code(
            code=code,
            language="python",
            checks=["complexity", "bugs", "security", "performance", "style"]
        )
        
        print("\n--- Comprehensive Analysis Report ---")
        print(f"Overall Quality Score: {result.get('quality_score', 0)}/10")
        
        print("\n📊 Metrics:")
        metrics = result.get('metrics', {})
        for key, value in metrics.items():
            print(f"  {key}: {value}")
        
        print("\n⚠️  All Issues:")
        all_issues = result.get('issues', [])
        
        # Group by severity
        critical = [i for i in all_issues if i.get('severity') == 'critical']
        high = [i for i in all_issues if i.get('severity') == 'high']
        medium = [i for i in all_issues if i.get('severity') == 'medium']
        low = [i for i in all_issues if i.get('severity') == 'low']
        
        print(f"  Critical: {len(critical)}")
        print(f"  High: {len(high)}")
        print(f"  Medium: {len(medium)}")
        print(f"  Low: {len(low)}")
        
        if critical or high:
            print("\n🔴 High Priority Issues:")
            for issue in critical + high:
                print(f"\n  • {issue.get('message')}")
                print(f"    Line: {issue.get('line')}")
                print(f"    Fix: {issue.get('suggestion', 'N/A')}")
        
        print("\n💡 Recommendations:")
        for rec in result.get('recommendations', []):
            print(f"  • {rec}")
    
    except Exception as e:
        print(f"Error: {e}")


async def main():
    """Run all examples."""
    print("\n" + "="*80)
    print(" AI-POWERED CODE ANALYSIS EXAMPLES ".center(80, "="))
    print("="*80)
    print("\nThese examples demonstrate various code analysis capabilities.")
    print("Make sure the AI Coding Environment API is running on http://localhost:8000")
    print("\nNote: You need a valid API token. Set AI_API_KEY environment variable.")
    
    # Run examples
    await example_complexity_analysis()
    await example_bug_detection()
    await example_security_analysis()
    await example_performance_analysis()
    await example_style_analysis()
    await example_comprehensive_analysis()
    
    print("\n" + "="*80)
    print(" EXAMPLES COMPLETED ".center(80, "="))
    print("="*80)
    print("\nKey Takeaways:")
    print("✓ Regular code analysis helps maintain quality")
    print("✓ Address critical and high severity issues first")
    print("✓ Security analysis should be part of every code review")
    print("✓ Performance optimization can significantly impact user experience")
    print("✓ Consistent code style improves maintainability")


if __name__ == "__main__":
    asyncio.run(main())
