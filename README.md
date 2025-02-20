# LucidLink Direct Links

A Python module for generating and managing direct links for LucidLink files. This tool provides efficient handling of direct link generation for both v2 and v3 filespace using the local client LucidLink REST API.

### Installation

1. Clone this repository:
```bash
git clone https://github.com/your-org/lucidlink-direct-links.git
cd lucidlink-direct-links
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the package and its dependencies:
```bash
# Install required dependencies
pip install -r requirements.txt

# Copy the direct_link_manager.py module to your project
cp lucidlink_direct_links/direct_link_manager.py /path/to/your/project/
```

### Getting the Port Number (Version 3)

If you are using version 3 of the API, retrieve the port number by running:
```bash
lucid3 list
```
This command outputs information similar to:
```
INSTANCE ID        FILESPACE               PORT        MODE        
2000               production.dmpfs        9778        live
```
Use the PORT from this output when configuring the `DirectLinkManager`.

### Getting the Port Number (Version 2)

For version 2 of the API, get the port by running:
```bash
lucid2 list
```

### Usage

1. Import the module in your Python code:
```python
from direct_link_manager import DirectLinkManager
```

2. Configure the DirectLinkManager with your LucidLink settings:
```python
manager = DirectLinkManager(
    port=9778,  # Port from lucid2/lucid3 list command
    mount_point="/Volumes/filespace",
    version=3,  # API version (2 or 3)
    max_workers=10  # Optional: configure concurrent workers
)
```

3. Generate direct links:
```python
async with manager:
    direct_link = await manager.get_direct_link("/path/to/file")
    print(f"Direct link: {direct_link}")
```

For a complete example, see `examples/basic_usage.py`:
```bash
python3 examples/basic_usage.py
```

The output will display each file's path and its corresponding direct link:
```
File: /path/to/file
Direct Link: <direct_link_url>
```

## Features

- Async support for high-performance direct link generation
- Support for both v2 and v3 LucidLink API versions
- Robust URL encoding for handling special characters in filenames
- Configurable retry logic and error handling
- Batch processing capabilities

## Configuration Options

The DirectLinkManager supports the following options:

- `port`: LucidLink API port (found using lucid2/lucid3 list command)
- `mount_point`: Base mount point for the filespace
- `version`: API version to use (2 or 3)
- `max_workers`: Maximum number of concurrent workers (default: 10)
- `retry_attempts`: Number of retry attempts for failed requests (default: 3)
- `retry_delay`: Delay between retries in seconds (default: 1)

```python
from lucidlink_direct_links import DirectLinkManager

# Initialize the manager
manager = DirectLinkManager(
    port=9778,  # Port from lucid2/lucid3 list command
    mount_point="/path/to/filespace",
    version=3,  # API version (2 or 3)
    max_workers=10
)

# Generate a direct link
async with manager:
    direct_link = await manager.get_direct_link("/path/to/file")
    print(f"Direct link: {direct_link}")
```
