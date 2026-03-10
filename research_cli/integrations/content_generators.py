"""
NotebookLM Content Generation - Podcast, Quiz, Infographic, etc.
"""

import asyncio
import logging
from typing import Optional, Dict, List

try:
    # Import các Enums để mapping từ string
    from notebooklm.rpc.types import AudioFormat, QuizDifficulty, FlashcardDifficulty
except ImportError:
    AudioFormat = None
    QuizDifficulty = None
    FlashcardDifficulty = None

logger = logging.getLogger(__name__)


class ContentGenerators:
    """Content generation utilities for NotebookLM"""
    
    def __init__(self, client):
        """Initialize with NotebookLM client"""
        self.client = client
        
        # Mapping từ string sang Enum để tránh lỗi TypeError
        self.audio_format_map = {
            "deep-dive": AudioFormat.DEEP_DIVE if AudioFormat else "deep-dive",
            "overview": AudioFormat.OVERVIEW if AudioFormat else "overview", 
            "interview": AudioFormat.INTERVIEW if AudioFormat else "interview"
        }
        
        self.quiz_difficulty_map = {
            "easy": QuizDifficulty.EASY if QuizDifficulty else "easy",
            "medium": QuizDifficulty.MEDIUM if QuizDifficulty else "medium",
            "hard": QuizDifficulty.HARD if QuizDifficulty else "hard"
        }
        
        self.flashcard_difficulty_map = {
            "easy": FlashcardDifficulty.EASY if FlashcardDifficulty else "easy", 
            "medium": FlashcardDifficulty.MEDIUM if FlashcardDifficulty else "medium",
            "hard": FlashcardDifficulty.HARD if FlashcardDifficulty else "hard"
        }


class ContentGenerators:
    """Content generation utilities for NotebookLM"""
    
    def __init__(self, client):
        """Initialize with NotebookLM client"""
        self.client = client
    
    async def generate_podcast(self, notebook_id: str, instructions: str = None,
                             format_type: str = "deep-dive", length: str = "default",
                             language: str = None, source_ids: List[str] = None,
                             output_file: str = "research_podcast.mp3") -> Dict:
        """Generate and download research podcast
        
        Args:
            notebook_id: Notebook ID
            instructions: Custom instructions for podcast
            format_type: Podcast format (deep-dive, brief, critique, debate)
            length: Podcast length (short, default, long)
            language: Output language (optional)
            source_ids: Specific sources to use (optional)
            output_file: Output filename
            
        Returns:
            Dict with success status and details
        """
        try:
            # Generate audio
            kwargs = {}
            if instructions:
                kwargs['instructions'] = instructions
            if format_type != "deep-dive":
                # Map string to Enum
                kwargs['format'] = self.audio_format_map.get(format_type, format_type)
            if length != "default":
                kwargs['length'] = length
            if language:
                kwargs['language'] = language
            if source_ids:
                kwargs['source_ids'] = source_ids
            
            task = await self.client.artifacts.generate_audio(notebook_id, **kwargs)
            
            # Wait for completion (podcast takes 10-20 minutes)
            await self.client.artifacts.wait_for_completion(notebook_id, task.task_id, timeout=1200)
            
            # Download
            await self.client.artifacts.download_audio(notebook_id, output_file)
            
            logger.info(f"Podcast generated: {output_file}")
            return {"success": True, "file": output_file, "task_id": task.task_id}
            
        except Exception as e:
            logger.error(f"Podcast generation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def generate_quiz(self, notebook_id: str, difficulty: str = "medium",
                           quantity: str = "standard", language: str = None,
                           source_ids: List[str] = None,
                           output_file: str = "research_quiz.json", 
                           output_format: str = "json") -> Dict:
        """Generate and download research quiz
        
        Args:
            notebook_id: Notebook ID
            difficulty: Quiz difficulty (easy, medium, hard)
            quantity: Number of questions (fewer, standard, more)
            language: Output language (optional)
            source_ids: Specific sources to use (optional)
            output_file: Output filename
            output_format: Output format (json, markdown, html)
            
        Returns:
            Dict with success status and details
        """
        try:
            # Generate quiz
            kwargs = {}
            if difficulty != "medium":
                # Map string to Enum
                kwargs['difficulty'] = self.quiz_difficulty_map.get(difficulty, difficulty)
            if quantity != "standard":
                kwargs['quantity'] = quantity
            if language:
                kwargs['language'] = language
            if source_ids:
                kwargs['source_ids'] = source_ids
            
            task = await self.client.artifacts.generate_quiz(notebook_id, **kwargs)
            
            # Wait for completion
            await self.client.artifacts.wait_for_completion(notebook_id, task.task_id)
            
            # Download with specified format
            await self.client.artifacts.download_quiz(notebook_id, output_file, format=output_format)
            
            logger.info(f"Quiz generated: {output_file}")
            return {"success": True, "file": output_file, "task_id": task.task_id}
            
        except Exception as e:
            logger.error(f"Quiz generation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def generate_flashcards(self, notebook_id: str, difficulty: str = "medium",
                                 quantity: str = "standard", language: str = None,
                                 source_ids: List[str] = None,
                                 output_file: str = "research_flashcards.json",
                                 output_format: str = "json") -> Dict:
        """Generate and download flashcards"""
        try:
            kwargs = {}
            if difficulty != "medium":
                # Map string to Enum
                kwargs['difficulty'] = self.flashcard_difficulty_map.get(difficulty, difficulty)
            if quantity != "standard":
                kwargs['quantity'] = quantity
            if language:
                kwargs['language'] = language
            if source_ids:
                kwargs['source_ids'] = source_ids
            
            task = await self.client.artifacts.generate_flashcards(notebook_id, **kwargs)
            await self.client.artifacts.wait_for_completion(notebook_id, task.task_id)
            await self.client.artifacts.download_flashcards(notebook_id, output_file, format=output_format)
            
            logger.info(f"Flashcards generated: {output_file}")
            return {"success": True, "file": output_file, "task_id": task.task_id}
            
        except Exception as e:
            logger.error(f"Flashcards generation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def generate_mind_map(self, notebook_id: str, language: str = None,
                               source_ids: List[str] = None,
                               output_file: str = "research_mindmap.json") -> Dict:
        """Generate and download research mind map (instant)"""
        try:
            kwargs = {}
            # Mind map API doesn't support language parameter, skip it
            if source_ids:
                kwargs['source_ids'] = source_ids
            
            # Generate mind map (instant, no waiting needed)
            result = await self.client.artifacts.generate_mind_map(notebook_id, **kwargs)
            
            # Download
            await self.client.artifacts.download_mind_map(notebook_id, output_file)
            
            logger.info(f"Mind map generated: {output_file}")
            return {"success": True, "file": output_file}
            
        except Exception as e:
            logger.error(f"Mind map generation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def generate_infographic(self, notebook_id: str, instructions: str = None,
                                  orientation: str = "landscape", detail: str = "standard",
                                  language: str = None, source_ids: List[str] = None,
                                  output_file: str = "research_infographic.png") -> Dict:
        """Generate and download research infographic"""
        try:
            kwargs = {}
            if instructions:
                kwargs['instructions'] = instructions
            if orientation != "landscape":
                kwargs['orientation'] = orientation
            if detail != "standard":
                kwargs['detail'] = detail
            if language:
                kwargs['language'] = language
            if source_ids:
                kwargs['source_ids'] = source_ids
            
            task = await self.client.artifacts.generate_infographic(notebook_id, **kwargs)
            await self.client.artifacts.wait_for_completion(notebook_id, task.task_id)
            await self.client.artifacts.download_infographic(notebook_id, output_file)
            
            logger.info(f"Infographic generated: {output_file}")
            return {"success": True, "file": output_file, "task_id": task.task_id}
            
        except Exception as e:
            logger.error(f"Infographic generation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def generate_video(self, notebook_id: str, instructions: str = None,
                            format_type: str = "explainer", style: str = "auto",
                            language: str = None, source_ids: List[str] = None,
                            output_file: str = "research_video.mp4") -> Dict:
        """Generate and download research video"""
        try:
            kwargs = {}
            if instructions:
                kwargs['instructions'] = instructions
            if format_type != "explainer":
                kwargs['format'] = format_type
            if style != "auto":
                kwargs['style'] = style
            if language:
                kwargs['language'] = language
            if source_ids:
                kwargs['source_ids'] = source_ids
            
            task = await self.client.artifacts.generate_video(notebook_id, **kwargs)
            await self.client.artifacts.wait_for_completion(notebook_id, task.task_id)
            await self.client.artifacts.download_video(notebook_id, output_file)
            
            logger.info(f"Video generated: {output_file}")
            return {"success": True, "file": output_file, "task_id": task.task_id}
            
        except Exception as e:
            logger.error(f"Video generation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def generate_slide_deck(self, notebook_id: str, instructions: str = None,
                                 format_type: str = "detailed", length: str = "default",
                                 language: str = None, source_ids: List[str] = None,
                                 output_file: str = "research_slides.pdf",
                                 output_format: str = "pdf") -> Dict:
        """Generate and download slide deck"""
        try:
            kwargs = {}
            if instructions:
                kwargs['instructions'] = instructions
            if format_type != "detailed":
                kwargs['format'] = format_type
            if length != "default":
                kwargs['length'] = length
            if language:
                kwargs['language'] = language
            if source_ids:
                kwargs['source_ids'] = source_ids
            
            task = await self.client.artifacts.generate_slide_deck(notebook_id, **kwargs)
            await self.client.artifacts.wait_for_completion(notebook_id, task.task_id)
            
            # Download with specified format (pdf or pptx)
            await self.client.artifacts.download_slide_deck(notebook_id, output_file, format=output_format)
            
            logger.info(f"Slide deck generated: {output_file}")
            return {"success": True, "file": output_file, "task_id": task.task_id}
            
        except Exception as e:
            logger.error(f"Slide deck generation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def generate_report(self, notebook_id: str, format_type: str = "briefing-doc",
                             append_instructions: str = None, language: str = None,
                             source_ids: List[str] = None,
                             output_file: str = "research_report.md") -> Dict:
        """Generate and download research report"""
        try:
            kwargs = {}
            if format_type != "briefing-doc":
                kwargs['format'] = format_type
            if append_instructions:
                kwargs['append'] = append_instructions
            if language:
                kwargs['language'] = language
            if source_ids:
                kwargs['source_ids'] = source_ids
            
            task = await self.client.artifacts.generate_report(notebook_id, **kwargs)
            await self.client.artifacts.wait_for_completion(notebook_id, task.task_id)
            await self.client.artifacts.download_report(notebook_id, output_file)
            
            logger.info(f"Report generated: {output_file}")
            return {"success": True, "file": output_file, "task_id": task.task_id}
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def generate_data_table(self, notebook_id: str, description: str,
                                 language: str = None, source_ids: List[str] = None,
                                 output_file: str = "research_data.csv") -> Dict:
        """Generate and download data table"""
        try:
            kwargs = {"description": description}
            if language:
                kwargs['language'] = language
            if source_ids:
                kwargs['source_ids'] = source_ids
            
            task = await self.client.artifacts.generate_data_table(notebook_id, **kwargs)
            await self.client.artifacts.wait_for_completion(notebook_id, task.task_id)
            await self.client.artifacts.download_data_table(notebook_id, output_file)
            
            logger.info(f"Data table generated: {output_file}")
            return {"success": True, "file": output_file, "task_id": task.task_id}
            
        except Exception as e:
            logger.error(f"Data table generation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def revise_slide(self, notebook_id: str, artifact_id: str, slide_number: int,
                          prompt: str, output_file: str = None) -> Dict:
        """Revise a specific slide in a slide deck"""
        try:
            kwargs = {
                "prompt": prompt,
                "artifact_id": artifact_id,
                "slide": slide_number
            }
            
            task = await self.client.artifacts.revise_slide(notebook_id, **kwargs)
            await self.client.artifacts.wait_for_completion(notebook_id, task.task_id)
            
            if output_file:
                await self.client.artifacts.download_slide_deck(notebook_id, output_file)
            
            logger.info(f"Slide {slide_number} revised in artifact {artifact_id}")
            return {"success": True, "task_id": task.task_id, "file": output_file}
            
        except Exception as e:
            logger.error(f"Slide revision failed: {e}")
            return {"success": False, "error": str(e)}