#!/usr/bin/env python3
"""
Code Generation Example
Demonstrates how to generate complete code from natural language descriptions.
"""

import asyncio
import httpx
import os
from typing import Dict, Any, Optional


class CodeGeneratorClient:
    """Client for AI-powered code generation."""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key or os.getenv("AI_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_code(
        self,
        description: str,
        language: str = "python",
        requirements: list = None,
        include_tests: bool = False,
        include_documentation: bool = True,
        framework: str = None
    ) -> Dict[str, Any]:
        """
        Generate code from natural language description.
        
        Args:
            description: What the code should do
            language: Programming language
            requirements: Additional requirements
            include_tests: Whether to generate tests
            include_documentation: Whether to generate documentation
            framework: Specific framework to use
            
        Returns:
            Generated code, tests, and documentation
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/ai/generate",
                json={
                    "description": description,
                    "language": language,
                    "requirements": requirements or [],
                    "include_tests": include_tests,
                    "include_documentation": include_documentation,
                    "framework": framework
                },
                headers=self.headers,
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()


async def example_simple_function():
    """Example: Generate a simple function."""
    print("\n" + "="*60)
    print("Example 1: Generate Simple Function")
    print("="*60)
    
    client = CodeGeneratorClient()
    
    description = "Create a function that validates email addresses using regex"
    
    print(f"Description: {description}")
    print("\nGenerating code...")
    
    try:
        result = await client.generate_code(
            description=description,
            language="python",
            include_tests=True,
            include_documentation=True
        )
        
        print("\n--- Generated Code ---")
        print(result.get("code", ""))
        
        if result.get("tests"):
            print("\n--- Generated Tests ---")
            print(result.get("tests", ""))
        
        if result.get("documentation"):
            print("\n--- Documentation ---")
            print(result.get("documentation", ""))
    
    except Exception as e:
        print(f"Error: {e}")


async def example_rest_api():
    """Example: Generate REST API endpoint."""
    print("\n" + "="*60)
    print("Example 2: Generate REST API Endpoint")
    print("="*60)
    
    client = CodeGeneratorClient()
    
    description = """
    Create a FastAPI endpoint for user registration that:
    - Accepts email, password, and name
    - Validates the input
    - Hashes the password
    - Saves to database
    - Returns JWT token
    """
    
    print(f"Description: {description}")
    print("\nGenerating API code...")
    
    try:
        result = await client.generate_code(
            description=description,
            language="python",
            framework="fastapi",
            requirements=[
                "use pydantic for validation",
                "include error handling",
                "add rate limiting"
            ],
            include_tests=True
        )
        
        print("\n--- Generated API Code ---")
        print(result.get("code", ""))
        
        if result.get("explanation"):
            print("\n--- Explanation ---")
            print(result.get("explanation", ""))
    
    except Exception as e:
        print(f"Error: {e}")


async def example_data_processing():
    """Example: Generate data processing pipeline."""
    print("\n" + "="*60)
    print("Example 3: Generate Data Processing Pipeline")
    print("="*60)
    
    client = CodeGeneratorClient()
    
    description = """
    Create a data processing pipeline that:
    1. Reads CSV file with sales data
    2. Cleans and validates the data
    3. Calculates monthly aggregations
    4. Exports results to JSON
    """
    
    print(f"Description: {description}")
    print("\nGenerating pipeline code...")
    
    try:
        result = await client.generate_code(
            description=description,
            language="python",
            requirements=[
                "use pandas for data processing",
                "include error handling",
                "add logging",
                "type hints required"
            ],
            include_tests=False,
            include_documentation=True
        )
        
        print("\n--- Generated Code ---")
        print(result.get("code", ""))
    
    except Exception as e:
        print(f"Error: {e}")


async def example_async_scraper():
    """Example: Generate async web scraper."""
    print("\n" + "="*60)
    print("Example 4: Generate Async Web Scraper")
    print("="*60)
    
    client = CodeGeneratorClient()
    
    description = """
    Create an async web scraper that:
    - Takes a list of URLs
    - Fetches them concurrently
    - Extracts title and meta description
    - Handles errors gracefully
    - Returns structured data
    """
    
    print(f"Description: {description}")
    print("\nGenerating scraper code...")
    
    try:
        result = await client.generate_code(
            description=description,
            language="python",
            requirements=[
                "use aiohttp for async requests",
                "use BeautifulSoup for parsing",
                "add retry logic",
                "include rate limiting"
            ],
            include_tests=True,
            include_documentation=True
        )
        
        print("\n--- Generated Code ---")
        print(result.get("code", ""))
        
        if result.get("tests"):
            print("\n--- Generated Tests ---")
            print(result.get("tests", ""))
    
    except Exception as e:
        print(f"Error: {e}")


async def example_javascript_component():
    """Example: Generate React component."""
    print("\n" + "="*60)
    print("Example 5: Generate React Component")
    print("="*60)
    
    client = CodeGeneratorClient()
    
    description = """
    Create a React component for a user profile card that:
    - Displays avatar, name, email, bio
    - Has edit mode
    - Validates inputs
    - Uses TypeScript
    - Includes loading and error states
    """
    
    print(f"Description: {description}")
    print("\nGenerating React component...")
    
    try:
        result = await client.generate_code(
            description=description,
            language="typescript",
            framework="react",
            requirements=[
                "use functional components with hooks",
                "include prop types",
                "add CSS modules",
                "follow React best practices"
            ],
            include_tests=True
        )
        
        print("\n--- Generated Component ---")
        print(result.get("code", ""))
        
        if result.get("tests"):
            print("\n--- Generated Tests ---")
            print(result.get("tests", ""))
    
    except Exception as e:
        print(f"Error: {e}")


async def example_cli_tool():
    """Example: Generate CLI tool."""
    print("\n" + "="*60)
    print("Example 6: Generate CLI Tool")
    print("="*60)
    
    client = CodeGeneratorClient()
    
    description = """
    Create a CLI tool for file management that:
    - Lists files in a directory
    - Supports filtering by extension
    - Can organize files by date
    - Includes progress bars
    - Has verbose and quiet modes
    """
    
    print(f"Description: {description}")
    print("\nGenerating CLI tool...")
    
    try:
        result = await client.generate_code(
            description=description,
            language="python",
            requirements=[
                "use click for CLI",
                "use rich for formatting",
                "include help text",
                "add config file support"
            ],
            include_tests=True,
            include_documentation=True
        )
        
        print("\n--- Generated Code ---")
        print(result.get("code", ""))
        
        if result.get("documentation"):
            print("\n--- Usage Documentation ---")
            print(result.get("documentation", ""))
    
    except Exception as e:
        print(f"Error: {e}")


async def main():
    """Run all examples."""
    print("\n" + "="*80)
    print(" AI-POWERED CODE GENERATION EXAMPLES ".center(80, "="))
    print("="*80)
    print("\nThese examples demonstrate code generation from natural language.")
    print("Make sure the AI Coding Environment API is running on http://localhost:8000")
    print("\nNote: You need a valid API token. Set AI_API_KEY environment variable.")
    
    # Run examples
    await example_simple_function()
    await example_rest_api()
    await example_data_processing()
    await example_async_scraper()
    await example_javascript_component()
    await example_cli_tool()
    
    print("\n" + "="*80)
    print(" EXAMPLES COMPLETED ".center(80, "="))
    print("="*80)
    print("\nTips:")
    print("- Be specific in your descriptions")
    print("- Mention frameworks and libraries you want to use")
    print("- Specify requirements like error handling, logging, etc.")
    print("- Request tests and documentation for better results")


if __name__ == "__main__":
    asyncio.run(main())
