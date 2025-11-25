# Slikemedia

Python SDK for publishing media on the Slike platform via JSON-RPC API.

## Installation

Install the package using pip:

```bash
pip install slikemedia
```

## Requirements

- Python 3.7 or higher
- requests >= 2.25.0

## Quick Start

```python
from slikemedia import PublishMediaOnSlike

# Basic usage - defaults to production
result = PublishMediaOnSlike(
    url="https://drive.google.com/file/d/YOUR_FILE_ID/view",
    title="My Video Title",
    description="My video description",
    type="gdrive",
    token="your-token-here"
)

print(result)
```

## Usage Examples

### Publishing to Production Environment (Default)

```python
from slikemedia import PublishMediaOnSlike

# Production is the default - no environment parameter needed
result = PublishMediaOnSlike(
    url="https://drive.google.com/file/d/1knH6zj4KAL_IfHxf6z-lhx6hd107X9jK/view",
    title="Production Video",
    description="Production video description",
    type="gdrive",
    token="your-production-token"  # Uses b2b.sli.ke (production)
)
```

### Publishing to Development Environment

```python
from slikemedia import PublishMediaOnSlike

result = PublishMediaOnSlike(
    url="https://drive.google.com/file/d/1knH6zj4KAL_IfHxf6z-lhx6hd107X9jK/view",
    title="Test Video",
    description="Test video description",
    type="gdrive",
    token="your-production-token",
    token_dev="your-dev-token",
    environment="dev"  # Uses local.sli.ke:8443 with token_dev
)
```

### Publishing with Optional Parameters

```python
from slikemedia import PublishMediaOnSlike

result = PublishMediaOnSlike(
    url="https://drive.google.com/file/d/1knH6zj4KAL_IfHxf6z-lhx6hd107X9jK/view",
    title="Video with Tags",
    description="Video with additional metadata",
    type="gdrive",
    token="your-production-token",
    tags=["tutorial", "python"],
    asset_type="shorts",
    preset_meta="preset_id_123",
    auto_publish=True
)
```

### Error Handling

```python
from slikemedia import PublishMediaOnSlike, SlikeAPIError

try:
    result = PublishMediaOnSlike(
        url="https://drive.google.com/file/d/YOUR_FILE_ID/view",
        title="My Video",
        description="My description",
        type="gdrive",
        token="your-token"
    )
    print("Success:", result)
except ValueError as e:
    print("Validation error:", e)
except SlikeAPIError as e:
    print("API error:", e)
```

## API Reference

### `PublishMediaOnSlike`

Publish media to the Slike platform.

#### Parameters

- **url** (str, required): Media URL (Google Drive, YouTube, etc.)
- **title** (str, required): Media title
- **description** (str, required): Media description
- **type** (str, required): Media type (e.g., 'gdrive', 'youtube')
- **token** (str, required): Production authentication token (uses `b2b.sli.ke`)
- **token_dev** (str, optional): Development authentication token (used when environment is "dev" or "development")
- **environment** (str, optional): Environment - "production"/"prod" or "development"/"dev" (default: production)
- **preset_meta** (str, optional): Preset metadata identifier
- **tags** (List[str], optional): List of tags for the media
- **asset_type** (str, optional): Asset type (e.g., 'shorts', 'video')
- **auto_publish** (bool, optional): Whether to auto-publish the media (default: True)

#### Returns

- **Dict[str, Any]**: API response containing the result of the publish operation

#### Raises

- **ValueError**: If required parameters are invalid or missing
- **SlikeAPIError**: If the API request fails

#### Notes

- **Production (default)**: If `environment` is not specified or set to `None`, the request will be sent to production (`https://b2b.sli.ke/rpc`) using the `token` parameter
- **Development**: Set `environment="dev"` or `environment="development"` to use the development environment (`https://local.sli.ke:8443/rpc`) with the `token_dev` parameter
- When `environment` is set to "dev"/"development", the `token_dev` parameter is required
- URLs are configured as constants at the top of the module:
  - `PRODUCTION_URL = "https://b2b.sli.ke/rpc"`
  - `DEVELOPMENT_URL = "https://local.sli.ke:8443/rpc"`

### `SlikeAPIError`

Custom exception class for Slike API errors. Inherits from the standard `Exception` class.

## Development

### Installing in Development Mode

```bash
# Clone the repository
git clone https://github.com/yourusername/slikemedia.git
cd slikemedia

# Install in editable mode
pip install -e .
```

### Building the Package

```bash
# Install hatch if not already installed
pip install hatch

# Build the package
hatch build
```

### Running Tests

```bash
# Run the test script
python test_slikemedia.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/yourusername/slikemedia).

