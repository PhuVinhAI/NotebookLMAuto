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
        # Create client from storage (handles authentication automatically)
        self.client = await NotebookLMClient.from_storage()
        # The client itself is also an async context manager
        await self.client.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)
        self.client = None
    
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
                source = await self.client.sources.add_url(notebook_id, url)
                source_ids.append(source.id)
                logger.info(f"Added source: {source.id}")
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Failed to add source {url}: {e}")
                continue
        
        # Wait for all sources to be processed if requested
        if wait_for_processing and source_ids:
            try:
                await self.client.sources.wait_for_sources(notebook_id, source_ids, timeout=300)
                logger.info(f"All {len(source_ids)} sources processed successfully")
            except Exception as e:
                logger.warning(f"Some sources may still be processing: {e}")
        
        return source_ids
    
    async def research_query(self, notebook_id: str, question: str, 
                           source_ids: Optional[List[str]] = None) -> Dict:
        """Ask a research question to the notebook
        
        Args:
            notebook_id: Notebook ID
            question: Research question
            source_ids: Specific sources to query (optional)
            
        Returns:
            Dict with answer and references
        """
        try:
            if source_ids:
                result = await self.client.chat.ask(notebook_id, question, source_ids=source_ids)
            else:
                result = await self.client.chat.ask(notebook_id, question)
            
            logger.info(f"Research query completed: {question}")
            
            return {
                "answer": result.answer,
                "conversation_id": result.conversation_id,
                "references": getattr(result, 'references', [])
            }
        except Exception as e:
            logger.error(f"Research query failed: {e}")
            raise
    
    async def list_notebooks(self) -> List[Dict]:
        """List all notebooks"""
        try:
            notebooks = await self.client.notebooks.list()
            return [{"id": nb.id, "title": nb.title, "created_at": getattr(nb, 'created_at', '')} for nb in notebooks]
        except Exception as e:
            logger.error(f"Failed to list notebooks: {e}")
            raise
    
    async def list_sources(self, notebook_id: str) -> List[Dict]:
        """List sources in notebook"""
        try:
            sources = await self.client.sources.list(notebook_id)
            return [{"id": src.id, "title": src.title, "status": src.status, "type": getattr(src, 'type', '')} for src in sources]
        except Exception as e:
            logger.error(f"Failed to list sources: {e}")
            raise
    
    async def list_artifacts(self, notebook_id: str) -> List[Dict]:
        """List artifacts in notebook"""
        try:
            artifacts = await self.client.artifacts.list(notebook_id)
            result = []
            for art in artifacts:
                artifact_dict = {
                    "id": art.id,
                    "title": getattr(art, 'title', 'Untitled'),
                    "type": getattr(art, 'type', getattr(art, 'artifact_type', 'Unknown')),
                    "status": getattr(art, 'status', 'Unknown')
                }
                result.append(artifact_dict)
            return result
        except Exception as e:
            logger.error(f"Failed to list artifacts: {e}")
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
    
    async def get_source_fulltext(self, notebook_id: str, source_id: str) -> Dict:
        """Get full text content of a source"""
        try:
            fulltext = await self.client.sources.get_fulltext(notebook_id, source_id)
            return {
                "source_id": source_id,
                "title": fulltext.title,
                "content": fulltext.content,
                "char_count": len(fulltext.content)
            }
        except Exception as e:
            logger.error(f"Failed to get source fulltext: {e}")
            raise
    
    async def wait_for_source_processing(self, notebook_id: str, source_id: str, timeout: int = 300) -> bool:
        """Wait for source to be processed"""
        try:
            await self.client.sources.wait_until_ready(notebook_id, source_id, timeout=timeout)
            return True
        except Exception as e:
            logger.error(f"Source processing timeout or failed: {e}")
            return False
    
    async def set_language(self, language_code: str) -> bool:
        """Set language for content generation"""
        try:
            # NotebookLM API handles language per generation, not globally
            # We'll store it for use in content generation
            self._language = language_code
            logger.info(f"Language preference set to: {language_code}")
            return True
        except Exception as e:
            logger.error(f"Failed to set language: {e}")
            return False
    
    async def get_language(self) -> str:
        """Get current language setting"""
        return getattr(self, '_language', 'en')
    
    async def list_supported_languages(self) -> List[Dict]:
        """List all supported languages"""
        # Common languages supported by NotebookLM
        languages = [
            {"code": "en", "name": "English", "native_name": "English"},
            {"code": "vi", "name": "Vietnamese", "native_name": "Tiếng Việt"},
            {"code": "zh_Hans", "name": "Chinese Simplified", "native_name": "中文（简体）"},
            {"code": "zh_Hant", "name": "Chinese Traditional", "native_name": "中文（繁體）"},
            {"code": "ja", "name": "Japanese", "native_name": "日本語"},
            {"code": "ko", "name": "Korean", "native_name": "한국어"},
            {"code": "es", "name": "Spanish", "native_name": "Español"},
            {"code": "fr", "name": "French", "native_name": "Français"},
            {"code": "de", "name": "German", "native_name": "Deutsch"},
            {"code": "pt_BR", "name": "Portuguese (Brazil)", "native_name": "Português (Brasil)"},
            {"code": "it", "name": "Italian", "native_name": "Italiano"},
            {"code": "ru", "name": "Russian", "native_name": "Русский"},
            {"code": "ar", "name": "Arabic", "native_name": "العربية"},
            {"code": "hi", "name": "Hindi", "native_name": "हिन्दी"},
            {"code": "th", "name": "Thai", "native_name": "ไทย"}
        ]
        return languages