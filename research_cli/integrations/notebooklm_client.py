"""
NotebookLM Python API Integration - Core Client
"""

import asyncio
import logging
from typing import List, Dict, Optional
from pathlib import Path

try:
    from notebooklm import NotebookLMClient
except ImportError:
    NotebookLMClient = None

logger = logging.getLogger(__name__)


class NotebookLMIntegration:
    """Professional NotebookLM integration with Python API"""
    
    def __init__(self):
        """Initialize NotebookLM integration"""
        if NotebookLMClient is None:
            raise ImportError("notebooklm-py not installed. Run: pip install notebooklm-py")
        
        self.client = None
        self.current_notebook = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.client = await NotebookLMClient.from_storage()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.client:
            await self.client.close()
    
    async def create_research_notebook(self, title: str) -> str:
        """Create a new research notebook
        
        Args:
            title: Notebook title
            
        Returns:
            Notebook ID
        """
        try:
            notebook = await self.client.notebooks.create(title)
            self.current_notebook = notebook.id
            logger.info(f"Created notebook: {title} ({notebook.id})")
            return notebook.id
        except Exception as e:
            logger.error(f"Failed to create notebook: {e}")
            raise
    
    async def add_youtube_sources(self, notebook_id: str, video_urls: List[str], 
                                 wait_for_processing: bool = True) -> List[str]:
        """Add YouTube videos as sources to notebook
        
        Args:
            notebook_id: Target notebook ID
            video_urls: List of YouTube URLs
            wait_for_processing: Wait for sources to be processed
            
        Returns:
            List of source IDs
        """
        source_ids = []
        
        for url in video_urls:
            try:
                logger.info(f"Adding YouTube source: {url}")
                source_id = await self.client.sources.add_url(
                    notebook_id, url, wait=wait_for_processing
                )
                source_ids.append(source_id)
                logger.info(f"Added source: {source_id}")
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Failed to add source {url}: {e}")
                continue
        
        return source_ids
    
    async def research_query(self, notebook_id: str, question: str) -> str:
        """Ask a research question to the notebook
        
        Args:
            notebook_id: Notebook ID
            question: Research question
            
        Returns:
            Answer from NotebookLM
        """
        try:
            result = await self.client.chat.ask(notebook_id, question)
            logger.info(f"Research query completed: {question}")
            return result.answer
        except Exception as e:
            logger.error(f"Research query failed: {e}")
            raise
    
    async def list_notebooks(self) -> List[Dict]:
        """List all notebooks"""
        try:
            notebooks = await self.client.notebooks.list()
            return [{"id": nb.id, "title": nb.title} for nb in notebooks]
        except Exception as e:
            logger.error(f"Failed to list notebooks: {e}")
            raise
    
    async def list_sources(self, notebook_id: str) -> List[Dict]:
        """List sources in notebook"""
        try:
            sources = await self.client.sources.list(notebook_id)
            return [{"id": src.id, "title": src.title, "status": src.status} for src in sources]
        except Exception as e:
            logger.error(f"Failed to list sources: {e}")
            raise
    
    async def delete_notebook(self, notebook_id: str) -> bool:
        """Delete a notebook"""
        try:
            await self.client.notebooks.delete(notebook_id)
            logger.info(f"Deleted notebook: {notebook_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete notebook: {e}")
            return False