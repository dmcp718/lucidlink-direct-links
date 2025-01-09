import asyncio
import logging
from lucidlink_direct_links import DirectLinkManager

# Configure logging
logging.basicConfig(level=logging.INFO)

async def main():
    # Initialize the manager
    async with DirectLinkManager(
        port=8280,
        mount_point="/Volumes/filespace",
        version=3,
        max_workers=10,
        retry_attempts=5,
        retry_delay=0.5,
        filespace="myfilespace"
    ) as manager:
        # Example file paths
        files = [
            "/Volumes/filespace/path/to/file1.txt",
            "/Volumes/filespace/path/to/file2[v1].pdf",
            "/Volumes/filespace/path to file3.doc"
        ]
        
        # Generate direct links
        for file_path in files:
            direct_link = await manager.get_direct_link(file_path)
            print(f"File: {file_path}")
            print(f"Direct Link: {direct_link}\n")

if __name__ == "__main__":
    asyncio.run(main())
