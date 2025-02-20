# LucidLink Direct Links

A utility for generating and managing direct links for LucidLink files. This tool provides efficient handling of direct link generation for both v2 and v3 of the LucidLink API.

## Features

- Async support for high-performance direct link generation
- Support for both v2 and v3 LucidLink API versions
- Robust URL encoding for handling special characters in filenames
- Configurable retry logic and error handling
- Batch processing capabilities

## Installation

```bash
pip install -r requirements.txt
```

## Usage

First, find your LucidLink filespace port using the `lucid2 list` command:

```bash
lucid2 list

# Example output:
# INSTANCE ID        FILESPACE           PORT        MODE        
# 503               example.dpfs         8281        live      
```

Then use the port in your code:

```python
from lucidlink_direct_links import DirectLinkManager

# Initialize the manager
manager = DirectLinkManager(
    port=8281,  # Port from lucid2 list command
    mount_point="/path/to/filespace",
    version=3,  # API version (2 or 3)
    max_workers=10
)

# Generate a direct link
async with manager:
    direct_link = await manager.get_direct_link("/path/to/file")
    print(f"Direct link: {direct_link}")
```

## Configuration

The DirectLinkManager supports various configuration options:

- `port`: LucidLink API port (found using `lucid2 list` command)
- `mount_point`: Base mount point for the filespace
- `version`: API version to use (2 or 3)
- `max_workers`: Maximum number of concurrent workers
- `retry_attempts`: Number of retry attempts for failed requests
- `retry_delay`: Delay between retries in seconds
