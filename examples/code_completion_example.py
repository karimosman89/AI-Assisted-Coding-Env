#!/usr/bin/env python3
"""
Code Completion Example
Demonstrates how to use the AI-Assisted Coding Environment for intelligent code completion.
"""

import asyncio
import httpx
import os
from typing import List, Dict, Any


class CodeCompletionClient:
    """Client for AI-powered code completion."""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        """
        Initialize the code completion client.
        
        Args:
            base_url: Base URL of the AI coding environment API
            api_key: JWT token for authentication
        """
        self.base_url = base_url
        self.api_key = api_key or os.getenv("AI_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def get_completions(
        self,
        code: str,
        language: str = "python",
        cursor_position: int = None,
        max_suggestions: int = 5,
        context: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Get code completion suggestions.
        
        Args:
            code: The code to complete
            language: Programming language
            cursor_position: Position of cursor in the code
            max_suggestions: Maximum number of suggestions to return
            context: Additional context (file path, project info, etc.)
            
        Returns:
            List of completion suggestions
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/ai/complete",
                json={
                    "code": code,
                    "language": language,
                    "cursor_position": cursor_position or len(code),
                    "max_suggestions": max_suggestions,
                    "context": context or {}
                },
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def get_inline_completion(
        self,
        code: str,
        language: str = "python"
    ) -> str:
        """
        Get single inline completion suggestion.
        
        Args:
            code: The code to complete
            language: Programming language
            
        Returns:
            Completion suggestion text
        """
        completions = await self.get_completions(
            code=code,
            language=language,
            max_suggestions=1
        )
        
        if completions and completions.get("suggestions"):
            return completions["suggestions"][0].get("text", "")
        return ""


async def example_basic_completion():
    """Example: Basic code completion."""
    print("\n" + "="*60)
    print("Example 1: Basic Function Completion")
    print("="*60)
    
    client = CodeCompletionClient()
    
    # Incomplete function
    code = """def calculate_fibonacci("""
    
    print(f"Input code:\n{code}")
    print("\nGetting completions...")
    
    try:
        result = await client.get_completions(code, language="python")
        
        print("\nSuggestions:")
        for idx, suggestion in enumerate(result.get("suggestions", []), 1):
            print(f"\n{idx}. {suggestion.get('text')}")
            print(f"   Confidence: {suggestion.get('confidence', 0):.2%}")
            if suggestion.get('documentation'):
                print(f"   Doc: {suggestion.get('documentation')}")
    except Exception as e:
        print(f"Error: {e}")


async def example_class_completion():
    """Example: Class method completion."""
    print("\n" + "="*60)
    print("Example 2: Class Method Completion")
    print("="*60)
    
    client = CodeCompletionClient()
    
    code = """
class UserManager:
    def __init__(self, database):
        self.db = database
    
    def create_user(
"""
    
    print(f"Input code:\n{code}")
    print("\nGetting completions...")
    
    try:
        result = await client.get_completions(
            code,
            language="python",
            context={
                "file_path": "src/managers/user_manager.py",
                "project_type": "web_application"
            }
        )
        
        print("\nSuggestions:")
        for idx, suggestion in enumerate(result.get("suggestions", []), 1):
            print(f"\n{idx}. {suggestion.get('text')}")
    except Exception as e:
        print(f"Error: {e}")


async def example_multi_language():
    """Example: Multi-language completion."""
    print("\n" + "="*60)
    print("Example 3: Multi-Language Completion")
    print("="*60)
    
    client = CodeCompletionClient()
    
    examples = [
        ("python", "async def fetch_data("),
        ("javascript", "const fetchData = async ("),
        ("typescript", "async function fetchData("),
        ("go", "func FetchData("),
    ]
    
    for language, code in examples:
        print(f"\n{language.upper()}:")
        print(f"Input: {code}")
        
        try:
            completion = await client.get_inline_completion(code, language=language)
            print(f"Suggestion: {completion}")
        except Exception as e:
            print(f"Error: {e}")


async def example_context_aware():
    """Example: Context-aware completion."""
    print("\n" + "="*60)
    print("Example 4: Context-Aware Completion")
    print("="*60)
    
    client = CodeCompletionClient()
    
    code = """
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str

@app.post("/users/")
async def create_user(
"""
    
    print(f"Input code:\n{code}")
    print("\nGetting completions with context...")
    
    try:
        result = await client.get_completions(
            code,
            language="python",
            context={
                "file_path": "src/api/routes/users.py",
                "project_files": ["models.py", "database.py", "auth.py"],
                "framework": "fastapi"
            }
        )
        
        print("\nContext-aware suggestions:")
        for idx, suggestion in enumerate(result.get("suggestions", []), 1):
            print(f"\n{idx}. {suggestion.get('text')}")
            print(f"   Reasoning: {suggestion.get('reasoning', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")


async def example_real_time_completion():
    """Example: Real-time streaming completion."""
    print("\n" + "="*60)
    print("Example 5: Real-Time Streaming Completion")
    print("="*60)
    
    # This would use WebSocket for real-time streaming
    # See websocket_example.py for full implementation
    print("For real-time streaming, use WebSocket connection.")
    print("See examples/websocket_example.py")


async def main():
    """Run all examples."""
    print("\n" + "="*80)
    print(" AI-ASSISTED CODE COMPLETION EXAMPLES ".center(80, "="))
    print("="*80)
    print("\nThese examples demonstrate various code completion capabilities.")
    print("Make sure the AI Coding Environment API is running on http://localhost:8000")
    print("\nNote: You need a valid API token. Set AI_API_KEY environment variable.")
    
    # Run examples
    await example_basic_completion()
    await example_class_completion()
    await example_multi_language()
    await example_context_aware()
    await example_real_time_completion()
    
    print("\n" + "="*80)
    print(" EXAMPLES COMPLETED ".center(80, "="))
    print("="*80)


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
