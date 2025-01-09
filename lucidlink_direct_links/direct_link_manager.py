import asyncio
import logging
import aiohttp
from typing import Optional, Dict, Any
from urllib.parse import quote

logger = logging.getLogger(__name__)

class DirectLinkManager:
    """Manager for generating direct links using LucidLink API."""
    
    def __init__(
        self,
        port: int,
        mount_point: str,
        version: int = 3,
        max_workers: int = 10,
        retry_attempts: int = 5,
        retry_delay: float = 0.5,
        filespace: str = None
    ):
        """Initialize the direct link manager.
        
        Args:
            port: LucidLink API port
            mount_point: Base mount point for the filespace
            version: API version to use (2 or 3)
            max_workers: Maximum number of concurrent workers
            retry_attempts: Number of retry attempts
            retry_delay: Delay between retries in seconds
            filespace: Optional filespace name for v2 links
        """
        self.port = port
        self.mount_point = mount_point.rstrip('/')
        self.version = version
        self._max_workers = max_workers
        self._retry_attempts = retry_attempts
        self._retry_delay = retry_delay
        self._filespace = filespace
        
        self._request_semaphore = None
        self.session = None
        
    async def __aenter__(self):
        """Initialize async resources."""
        self._request_semaphore = asyncio.Semaphore(self._max_workers)
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup async resources."""
        if self.session:
            await self.session.close()
            
    def _encode_path_for_url(self, path: str) -> str:
        """Encode a file path for use in URLs with special handling for problematic characters.
        
        Args:
            path: The file path to encode
            
        Returns:
            URL-safe encoded path
        """
        # Only encode the absolute minimum required characters
        # Keep path separators and most special characters as is
        safe_chars = "/[](),-_ ."
        return quote(path, safe=safe_chars)
        
    def _get_relative_path(self, path: str) -> str:
        """Convert absolute path to relative path using mount point."""
        if path.startswith(self.mount_point):
            return path[len(self.mount_point):].lstrip('/')
        return path.lstrip('/')
        
    async def get_direct_link(self, file_path: str, fsentry_id: str = None) -> Optional[str]:
        """Get direct link for a file.
        
        Args:
            file_path: Path to the file
            fsentry_id: Optional fsentry ID for v2 links
            
        Returns:
            Direct link string or None if generation fails
        """
        if self.version == 2:
            return await self._get_direct_link_v2(file_path, fsentry_id)
        else:
            return await self._get_direct_link_v3(file_path)
            
    async def _get_direct_link_v2(self, file_path: str, fsentry_id: str = None) -> Optional[str]:
        """Get direct link using v2 API endpoint."""
        try:
            if fsentry_id:
                # Use provided fsentry_id directly - fast path
                if not self._filespace:
                    logger.error("Filespace name not set")
                    return None
                    
                direct_link = f"lucid://{self._filespace}/file/{fsentry_id}"
                logger.debug(f"Generated v2 direct link using provided ID for {file_path}: {direct_link}")
                return direct_link
                
            # Fallback to API call if no ID provided - slow path
            file_path = self._get_relative_path(file_path)
            encoded_path = self._encode_path_for_url(file_path)
            
            # Get the fsEntry ID from the API
            url = f"http://127.0.0.1:{self.port}/fsEntry?path={encoded_path}"
            
            async with self._request_semaphore:
                for attempt in range(self._retry_attempts):
                    try:
                        async with self.session.get(url) as response:
                            if response.status == 400:
                                logger.warning(f"Failed to generate direct link for: {file_path} - Bad Request")
                                return None
                                
                            response.raise_for_status()
                            data = await response.json()
                            
                            if not data or 'id' not in data:
                                logger.error(f"Failed to get fsEntry ID for {file_path}")
                                return None
                                
                            # Construct the direct link using the fsEntry ID
                            fsentry_id = data['id']
                            if not self._filespace:
                                logger.error("Filespace name not set")
                                return None
                                
                            direct_link = f"lucid://{self._filespace}/file/{fsentry_id}"
                            logger.debug(f"Generated v2 direct link via API for {file_path}: {direct_link}")
                            return direct_link
                            
                    except aiohttp.ClientError as e:
                        if attempt == self._retry_attempts - 1:
                            raise
                        await asyncio.sleep(self._retry_delay)
                        
        except Exception as e:
            logger.error(f"Error generating v2 direct link for {file_path}: {e}")
            return None
            
    async def _get_direct_link_v3(self, file_path: str) -> Optional[str]:
        """Get direct link using v3 API endpoint."""
        try:
            if not self.session:
                raise RuntimeError("Session not initialized")

            file_path = self._get_relative_path(file_path)
            encoded_path = self._encode_path_for_url(file_path)
            url = f"http://127.0.0.1:{self.port}/fsEntry/direct-link?path={encoded_path}"
            
            async with self._request_semaphore:
                for attempt in range(self._retry_attempts):
                    try:
                        async with self.session.get(url) as response:
                            if response.status == 400:
                                logger.warning(f"Failed to generate direct link for: {file_path} - Bad Request")
                                return None
                                
                            response.raise_for_status()
                            data = await response.json()
                            
                            if 'result' not in data:
                                logger.warning(f"No result field in response for: {file_path}")
                                return None
                                
                            return data['result']
                            
                    except aiohttp.ClientError as e:
                        if attempt == self._retry_attempts - 1:
                            raise
                        await asyncio.sleep(self._retry_delay)
                        
        except Exception as e:
            logger.error(f"Error generating direct link for {file_path}: {str(e)}")
            return None
