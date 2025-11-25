#!/usr/bin/env python3
"""
Test script for PublishMediaOnSlike function.
Tests the Slike media publishing API with comprehensive logging.
"""

import logging
import json
from typing import Optional, Dict, Any, List
from slikemedia import PublishMediaOnSlike, SlikeAPIError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

# Constants
SEPARATOR = "=" * 60
DEV_API_URL = "https://local.sli.ke:8443/rpc"
PROD_API_URL = "https://b2b.sli.ke/rpc"


def build_payload_for_logging(
    title: str,
    description: str,
    url: str,
    type: str,
    tags: Optional[List[str]] = None,
    preset_meta: Optional[str] = None,
    asset_type: Optional[str] = None
) -> Dict[str, Any]:
    """Build payload dictionary for logging purposes."""
    payload = {
        "jsonrpc": "2.0",
        "id": 17,
        "method": "media.publish",
        "params": {
            "title": title,
            "desc": description,
            "url": url,
            "type": type,
            "auto_publish": True
        }
    }
    
    if tags:
        payload["params"]["tags"] = tags
    if preset_meta:
        payload["params"]["preset_meta"] = preset_meta
    if asset_type:
        payload["params"]["asset_type"] = asset_type
    
    return payload


def log_request_details(api_url: str, payload: Dict[str, Any], headers: Dict[str, str] = None) -> None:
    """Log the request details in a formatted manner."""
    logger.info("\nRequest Details:")
    logger.info(f"URL: {api_url}")
    if headers:
        logger.info("Headers:")
        logger.info(json.dumps(headers, indent=2))
    logger.info("Payload:")
    logger.info(json.dumps(payload, indent=2))


def log_success(result: Dict[str, Any]) -> None:
    """Log successful API response."""
    logger.info(f"\n{SEPARATOR}")
    logger.info("SUCCESS: Media published successfully!")
    logger.info(SEPARATOR)
    
    # Extract and display only the media ID
    if isinstance(result, dict) and "result" in result:
        media_result = result.get("result", {})
        if isinstance(media_result, dict) and "id" in media_result:
            media_id = media_result.get("id")
            logger.info(f"Media ID: {media_id}")
        else:
            logger.info("Media ID: Not available in response")


def log_error(error_type: str, error_msg: str) -> None:
    """Log error in a formatted manner."""
    logger.error(f"\n{SEPARATOR}")
    logger.error(error_type)
    logger.error(SEPARATOR)
    logger.error(f"Error: {error_msg}")


def main():
    """Main test function."""
    # Test configuration
    test_data = {
        "url": "https://drive.google.com/file/d/1knH6zj4KAL_IfHxf6z-lhx6hd107X9jK/view",
        "title": "test media title arpit 8",
        "description": "test media desc arpit 2",
        "type": "gdrive",
        "tags": ["tag1", "tag2"],
        "asset_type": "shorts",
        "preset_meta": "nph9gl6gzo"
    }
    
    # Token and environment configuration
    token = "8b2a3c03-af9a-35d8-ad37-e7b70bfaf367"  # Authentication token (used for both prod and dev)
    token_dev = None  # Optional: Separate dev token if needed
    environment = ""  # Options: None (defaults to prod), "prod"/"production", "dev"/"development"
    
    # Log test start
    logger.info(SEPARATOR)
    logger.info("Starting PublishMediaOnSlike test")
    logger.info(SEPARATOR)
    
    # Determine API URL
    api_url = DEV_API_URL if environment in ("dev", "development") else PROD_API_URL
    
    # Build headers for logging
    from slikemedia import _build_headers
    headers_log = _build_headers(token if not token_dev else token_dev, environment)
    
    # Build and log payload
    payload_log = build_payload_for_logging(**test_data)
    log_request_details(api_url, payload_log, headers_log)
    
    try:
        logger.info("\nSending request to Slike API...")
        
        # Call the function
        result = PublishMediaOnSlike(
            url=test_data["url"],
            title=test_data["title"],
            description=test_data["description"],
            type=test_data["type"],
            token=token,
            environment=environment,
            preset_meta=test_data["preset_meta"],
            tags=test_data["tags"],
            asset_type=test_data["asset_type"]
        )
        
        log_success(result)
        return result
        
    except ValueError as e:
        log_error("VALIDATION ERROR", str(e))
        logger.debug("Full validation error details:", exc_info=True)
        return None
        
    except SlikeAPIError as e:
        log_error("API ERROR", str(e))
        logger.debug("Full API error details:", exc_info=True)
        return None
        
    except Exception as e:
        log_error("UNEXPECTED ERROR", str(e))
        logger.debug("Full error details:", exc_info=True)
        return None


if __name__ == "__main__":
    main()

