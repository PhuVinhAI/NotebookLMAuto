"""
NotebookLM Content Generation - Podcast, Quiz, Infographic, etc.
"""

import asyncio
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ContentGenerators:
    """Content generation utilities for NotebookLM"""
    
    def __init__(self, client):
        """Initialize with NotebookLM client"""
        self.client = client
    
    async def generate_podcast(self, notebook_id: str, instructions: str = None,
                             output_file: str = "research_podcast.mp3") -> bool:
        """Generate and download research podcast
        
        Args:
            notebook_id: Notebook ID
            instructions: Custom instructions for podcast
            output_file: Output filename
            
        Returns:
            True if successful
        """
        try:
            # Generate audio
            instructions = instructions or "Create an engaging podcast summarizing the key insights"
            status = await self.client.artifacts.generate_audio(notebook_id, instructions=instructions)
            
            # Wait for completion
            await self.client.artifacts.wait_for_completion(notebook_id, status.task_id)
            
            # Download
            await self.client.artifacts.download_audio(notebook_id, output_file)
            
            logger.info(f"Podcast generated: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Podcast generation failed: {e}")
            return False
    
    async def generate_quiz(self, notebook_id: str, difficulty: str = "medium",
                           output_file: str = "research_quiz.json") -> bool:
        """Generate and download research quiz
        
        Args:
            notebook_id: Notebook ID
            difficulty: Quiz difficulty (easy, medium, hard)
            output_file: Output filename
            
        Returns:
            True if successful
        """
        try:
            # Generate quiz
            status = await self.client.artifacts.generate_quiz(
                notebook_id, difficulty=difficulty
            )
            
            # Wait for completion
            await self.client.artifacts.wait_for_completion(notebook_id, status.task_id)
            
            # Download as JSON
            await self.client.artifacts.download_quiz(
                notebook_id, output_file, output_format="json"
            )
            
            logger.info(f"Quiz generated: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Quiz generation failed: {e}")
            return False
    
    async def generate_mind_map(self, notebook_id: str, 
                               output_file: str = "research_mindmap.json") -> bool:
        """Generate and download research mind map
        
        Args:
            notebook_id: Notebook ID
            output_file: Output filename
            
        Returns:
            True if successful
        """
        try:
            # Generate mind map (instant)
            result = await self.client.artifacts.generate_mind_map(notebook_id)
            
            # Download
            await self.client.artifacts.download_mind_map(notebook_id, output_file)
            
            logger.info(f"Mind map generated: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Mind map generation failed: {e}")
            return False
    
    async def generate_infographic(self, notebook_id: str, instructions: str = None,
                                  output_file: str = "research_infographic.png") -> bool:
        """Generate and download research infographic
        
        Args:
            notebook_id: Notebook ID
            instructions: Custom instructions
            output_file: Output filename
            
        Returns:
            True if successful
        """
        try:
            # Generate infographic
            instructions = instructions or "Create a visual summary of key insights"
            status = await self.client.artifacts.generate_infographic(
                notebook_id, instructions=instructions
            )
            
            # Wait for completion
            await self.client.artifacts.wait_for_completion(notebook_id, status.task_id)
            
            # Download
            await self.client.artifacts.download_infographic(notebook_id, output_file)
            
            logger.info(f"Infographic generated: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Infographic generation failed: {e}")
            return False
    
    async def generate_video(self, notebook_id: str, instructions: str = None,
                            output_file: str = "research_video.mp4") -> bool:
        """Generate and download research video
        
        Args:
            notebook_id: Notebook ID
            instructions: Custom instructions
            output_file: Output filename
            
        Returns:
            True if successful
        """
        try:
            # Generate video
            instructions = instructions or "Create an educational video explaining the key concepts"
            status = await self.client.artifacts.generate_video(
                notebook_id, instructions=instructions
            )
            
            # Wait for completion
            await self.client.artifacts.wait_for_completion(notebook_id, status.task_id)
            
            # Download
            await self.client.artifacts.download_video(notebook_id, output_file)
            
            logger.info(f"Video generated: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Video generation failed: {e}")
            return False