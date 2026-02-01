"""
Perplexity Service - Research using Perplexity AI API.

Educational Note: Perplexity AI provides comprehensive research capabilities:
- Online mode with real-time web search
- Citation tracking for sources
- Structured research output

This service provides a consistent interface for research operations.
"""

import os
import requests
from typing import Dict, Any, List, Optional


class PerplexityService:
    """
    Service class for Perplexity AI research.

    Educational Note: Perplexity provides "sonar" models optimized for research
    with online search capabilities built in.
    """

    # Perplexity API endpoint
    API_URL = "https://api.perplexity.ai/chat/completions"
    
    # Default model for research
    DEFAULT_MODEL = "sonar"  # Online model with search

    def __init__(self):
        """Initialize the Perplexity service."""
        self._api_key = None

    def _get_api_key(self) -> str:
        """
        Get the Perplexity API key from environment.

        Returns:
            API key string

        Raises:
            ValueError: If PERPLEXITY_API_KEY is not configured
        """
        if self._api_key is None:
            api_key = os.getenv('PERPLEXITY_API_KEY')
            if not api_key:
                raise ValueError(
                    "PERPLEXITY_API_KEY not found in environment. "
                    "Please configure it in App Settings."
                )
            self._api_key = api_key
        return self._api_key

    def research(
        self,
        topic: str,
        description: str,
        links: List[str] = None,
        model: str = None
    ) -> Dict[str, Any]:
        """
        Execute comprehensive research on a topic using Perplexity.

        Educational Note: Perplexity's sonar model combines:
        - Real-time web search
        - LLM synthesis
        - Citation tracking

        Args:
            topic: The main research topic
            description: Focus areas and questions to answer
            links: Optional list of reference URLs to include in research
            model: Override default model (defaults to "sonar")

        Returns:
            Dict with success status, content, and citations:
            {
                "success": bool,
                "content": str,        # Research report text
                "citations": [...],    # Source URLs cited
                "usage": {...},        # Token usage info
                "error": str           # Error message if failed
            }
        """
        try:
            api_key = self._get_api_key()
            
            # Build research prompt
            prompt = self._build_research_prompt(topic, description, links)
            
            print(f"[Perplexity] Starting research on: {topic}")
            if links:
                print(f"[Perplexity] Including {len(links)} reference links")

            # Call Perplexity API
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model or self.DEFAULT_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a research assistant. Provide comprehensive, well-structured research reports with proper citations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.2,  # Lower temperature for factual research
                "max_tokens": 4000,  # Allow comprehensive output
                "return_citations": True,  # Get source URLs
                "return_images": False  # We only need text
            }

            response = requests.post(
                self.API_URL,
                headers=headers,
                json=payload,
                timeout=120  # 2 min timeout for research
            )
            
            response.raise_for_status()
            data = response.json()

            # Extract response content
            content = ""
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0].get("message", {}).get("content", "")

            # Extract citations
            citations = data.get("citations", [])
            
            # Extract usage info
            usage = data.get("usage", {})

            if not content:
                return {
                    "success": False,
                    "error": "Perplexity returned empty content"
                }

            print(f"[Perplexity] Research complete: {len(content)} chars, {len(citations)} citations")

            return {
                "success": True,
                "content": content,
                "citations": citations,
                "usage": usage
            }

        except ValueError as e:
            # API key not configured
            return {
                "success": False,
                "error": str(e)
            }
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Perplexity API request timed out (>2 minutes)"
            }
        except requests.exceptions.HTTPError as e:
            error_msg = f"Perplexity API error: {e.response.status_code}"
            if e.response.status_code == 401:
                error_msg = "Invalid Perplexity API key"
            elif e.response.status_code == 429:
                error_msg = "Perplexity API rate limit exceeded"
            return {
                "success": False,
                "error": error_msg
            }
        except Exception as e:
            print(f"Perplexity research error: {e}")
            return {
                "success": False,
                "error": f"Research failed: {str(e)}"
            }

    def _build_research_prompt(
        self,
        topic: str,
        description: str,
        links: List[str] = None
    ) -> str:
        """
        Build a comprehensive research prompt for Perplexity.

        Educational Note: A well-structured prompt is key to getting
        quality research output from Perplexity.

        Args:
            topic: Main research topic
            description: Focus areas and questions
            links: Optional reference links

        Returns:
            Formatted prompt string
        """
        prompt_parts = [
            f"# Research Topic: {topic}",
            "",
            "## Research Objectives",
            description,
            "",
            "## Instructions",
            "Please conduct comprehensive research on this topic and provide:",
            "1. A thorough overview of the subject",
            "2. Key findings and insights",
            "3. Recent developments and trends",
            "4. Relevant examples and case studies",
            "5. Practical applications and implications",
            "",
            "Structure your response with clear headings and sections.",
            "Cite all sources used in your research."
        ]

        # Add reference links if provided
        if links:
            prompt_parts.extend([
                "",
                "## Reference Links to Include",
                "Please incorporate information from these sources:",
                ""
            ])
            for link in links:
                prompt_parts.append(f"- {link}")

        return "\n".join(prompt_parts)

    def is_configured(self) -> bool:
        """
        Check if Perplexity API key is configured.

        Returns:
            True if API key is set, False otherwise
        """
        return bool(os.getenv('PERPLEXITY_API_KEY'))


# Singleton instance
perplexity_service = PerplexityService()
