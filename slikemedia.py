"""
Slike Media Publisher
A module for publishing media to the Slike platform via JSON-RPC API.
"""

__version__ = "0.1.0"
__all__ = ["PublishMediaOnSlike", "SlikeAPIError", "PRODUCTION_URL", "DEVELOPMENT_URL"]

import requests
from typing import Dict, Optional, Any, List

# API URL Configuration
PRODUCTION_URL = "https://app.sli.ke/rpc"
DEVELOPMENT_URL = "https://local.sli.ke:8443/rpc"


class SlikeAPIError(Exception):
    """Custom exception for Slike API errors."""
    pass


def PublishMediaOnSlike(
    url: str,
    title: str,
    description: str,
    type: str,
    token: str,
    token_dev: Optional[str] = None,
    environment: Optional[str] = None,
    preset_meta: Optional[str] = None,
    tags: Optional[List[str]] = None,
    asset_type: Optional[str] = None,
    auto_publish: bool = True,
) -> Dict[str, Any]:
    """
    Publish media to Slike platform.
    
    Args:
        url: Media URL (Google Drive, YouTube, etc.)
        title: Media title
        description: Media description
        type: Media type (e.g., 'gdrive', 'youtube')
        token: Production authentication token (used when environment is None or "production"/"prod")
        token_dev: Optional development authentication token (used when environment is "development"/"dev")
        environment: Optional environment - "production"/"prod" or "development"/"dev" (default: production if not specified)
        preset_meta: Optional preset metadata identifier
        tags: Optional list of tags
        asset_type: Optional asset type (e.g., 'shorts', 'video')
        auto_publish: Whether to auto-publish the media (default: True)
    
    Returns:
        Dict containing the API response
    
    Raises:
        ValueError: If required parameters are invalid
        SlikeAPIError: If API request fails
    """
    # Validate required parameters
    _validate_required_params(url, title, description, token)
    
    # Determine API endpoint based on environment
    api_url = _get_api_url(environment)
    
    # Select appropriate token based on environment
    auth_token = _select_token(token, token_dev, environment)
    
    # Build request payload
    payload = _build_payload(url, title, description, type, tags, preset_meta, asset_type, auto_publish)
    
    # Build request headers
    headers = _build_headers(auth_token, environment)
    
    # Make API request
    return _make_request(api_url, payload, headers)


def _validate_required_params(url: str, title: str, description: str, token: str) -> None:
    """Validate required parameters."""
    if not url or not isinstance(url, str):
        raise ValueError("url parameter is required and must be a non-empty string")
    if not title or not isinstance(title, str):
        raise ValueError("title parameter is required and must be a non-empty string")
    if not description or not isinstance(description, str):
        raise ValueError("description parameter is required and must be a non-empty string")
    if not token or not isinstance(token, str):
        raise ValueError("token parameter is required and must be a non-empty string")


def _get_api_url(environment: Optional[str]) -> str:
    """Determine API URL based on environment. Defaults to production if None or empty."""
    # Default to production if no environment is passed or if empty string
    if not environment:
        return PRODUCTION_URL
    
    environment_lower = environment.lower()
    
    if environment_lower in ("development", "dev"):
        return DEVELOPMENT_URL
    elif environment_lower in ("production", "prod"):
        return PRODUCTION_URL
    else:
        raise ValueError(f"Invalid environment: '{environment}'. Must be 'production'/'prod' or 'development'/'dev'")


def _select_token(token: str, token_dev: Optional[str], environment: Optional[str]) -> str:
    """Select appropriate token based on environment."""
    # If no environment specified or empty string or production, use production token
    if not environment:
        return token
    
    environment_lower = environment.lower()
    
    # Use dev token if environment is dev and token_dev is provided, otherwise fallback to token
    if environment_lower in ("development", "dev"):
        return token_dev if token_dev else token
    
    # Otherwise use production token
    return token


def _build_payload(
    url: str,
    title: str,
    description: str,
    type: str,
    tags: Optional[List[str]],
    preset_meta: Optional[str],
    asset_type: Optional[str],
    auto_publish: bool
) -> Dict[str, Any]:
    """Build JSON-RPC 2.0 payload."""
    params = {
        "title": title,
        "desc": description,
        "url": url,
        "type": type,
        "auto_publish": auto_publish
    }
    
    # Add optional parameters
    if tags:
        if not isinstance(tags, list):
            raise ValueError("tags parameter must be a list of strings")
        params["tags"] = tags
    
    if preset_meta:
        params["preset_meta"] = preset_meta
    
    if asset_type:
        params["asset_type"] = asset_type
    
    return {
        "jsonrpc": "2.0",
        "id": 17,
        "method": "media.publish",
        "params": params
    }


def _build_headers(token: str, environment: Optional[str]) -> Dict[str, str]:
    """Build request headers with authentication token."""
    # Determine the token header key based on environment
    # Use "token-dev" only if environment is explicitly set to dev/development (not empty)
    if environment and environment.lower() in ("development", "dev"):
        token_key = "token-dev"
    else:
        token_key = "token"
    
    headers = {
        "Content-Type": "application/json",
        token_key: token
    }
    
    return headers


def _make_request(api_url: str, payload: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    """Make the API request and handle response."""
    try:
        response = requests.post(api_url, json=payload, headers=headers, verify=True)
        result = _parse_response(response)
        _check_for_errors(response, result)
        return result
    except SlikeAPIError:
        # Re-raise SlikeAPIError without wrapping
        raise
    except requests.exceptions.RequestException as e:
        raise SlikeAPIError(f"Failed to publish media on Slike: {str(e)}")
    except Exception as e:
        raise SlikeAPIError(f"Unexpected error while publishing media: {str(e)}")


def _parse_response(response: requests.Response) -> Dict[str, Any]:
    """Parse JSON response."""
    try:
        return response.json()
    except ValueError:
        raise SlikeAPIError(f"Invalid JSON response: {response.text}")


def _check_for_errors(response: requests.Response, result: Dict[str, Any]) -> None:
    """Check for HTTP and JSON-RPC errors."""
    # Check HTTP status code
    if response.status_code >= 400:
        error_msg = _extract_error_message(result, response.text)
        raise SlikeAPIError(f"HTTP {response.status_code}: {error_msg}")
    
    # Check JSON-RPC errors (only if error field is not empty)
    if isinstance(result, dict) and "error" in result:
        error_obj = result.get("error")
        
        # Skip if error is empty string or None
        if not error_obj:
            return
        
        # Include full error details for debugging
        if isinstance(error_obj, dict):
            error_msg = error_obj.get("message", "Unknown JSON-RPC error")
            error_code = error_obj.get("code", "N/A")
            error_data = error_obj.get("data", "")
            full_error = f"{error_msg} (code: {error_code})"
            if error_data:
                full_error += f" - {error_data}"
        else:
            full_error = str(error_obj)
        
        raise SlikeAPIError(f"JSON-RPC error: {full_error}")


def _extract_error_message(error_obj: Any, default: str) -> str:
    """Extract error message from error object."""
    if isinstance(error_obj, dict):
        return error_obj.get("message", default)
    return str(error_obj) if error_obj else default

