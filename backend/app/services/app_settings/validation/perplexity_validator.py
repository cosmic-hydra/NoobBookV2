"""
Perplexity API key validator.

Educational Note: Validates Perplexity API keys by making a minimal
test request. Perplexity is an AI research API with online search.
"""
from typing import Tuple
import requests


def validate_perplexity_key(api_key: str) -> Tuple[bool, str]:
    """
    Validate Perplexity API key by making a test request.

    Educational Note: We make a minimal chat completion request
    with a simple prompt to verify the key works.

    Args:
        api_key: The Perplexity API key to validate

    Returns:
        Tuple of (is_valid, message)
    """
    if not api_key or api_key == '':
        return False, "API key is empty"

    try:
        # Make a minimal test request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "sonar",  # Use the online research model
            "messages": [
                {
                    "role": "user",
                    "content": "test"
                }
            ],
            "max_tokens": 10  # Minimal response to save costs
        }

        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        # Check response status
        if response.status_code == 200:
            return True, "Valid Perplexity API key"
        elif response.status_code == 401:
            return False, "Invalid API key"
        elif response.status_code == 429:
            return True, "Valid API key (rate limited)"
        elif response.status_code == 403:
            return False, "API key does not have required permissions"
        else:
            return False, f"API returned status {response.status_code}"

    except requests.exceptions.Timeout:
        return False, "Request timed out - API may be down"
    except requests.exceptions.ConnectionError:
        return False, "Connection error - check internet connection"
    except Exception as e:
        error_message = str(e).lower()

        # Check for common error types
        if 'invalid' in error_message or 'unauthorized' in error_message:
            return False, "Invalid API key"
        elif 'quota' in error_message or 'limit' in error_message:
            return True, "Valid API key (quota exceeded)"
        elif 'rate' in error_message:
            return True, "Valid API key (rate limited)"
        else:
            print(f"Perplexity validation error: {type(e).__name__}: {str(e)}")
            return False, f"Validation failed: {str(e)[:100]}"
