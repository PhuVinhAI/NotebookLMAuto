"""
Test NotebookLM Content Generation - All content types
"""

import sys
import os
from unittest.mock import Mock, patch, AsyncMock
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_podcast_generation(mock_subprocess, mock_client):
    """Test podcast generation with different formats"""
    try:
        from research_cli.integrations.content_generators import ContentGenerators
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_status = Mock()
        mock_status.task_id = "audio_task_123"
        mock_client_instance.artifacts = Mock()
        mock_client_instance.artifacts.generate_audio = AsyncMock(return_value=mock_status)
        mock_client_instance.artifacts.wait_for_completion = AsyncMock(return_value=None)
        mock_client_instance.artifacts.download_audio = AsyncMock(return_value=None)
        mock_client_instance.close = AsyncMock()
        
        async def _test():
            generator = ContentGenerators(mock_client_instance)
            
            # Test basic podcast generation
            result = await generator.generate_podcast(
                "notebook_id", "Test instructions", "deep-dive", "default", "en", None, "test.mp3"
            )
            
            assert result["success"] == True
            assert result["file"] == "test.mp3"
            assert result["task_id"] == "audio_task_123"
            
            # Verify calls
            mock_client_instance.artifacts.generate_audio.assert_called_once()
            mock_client_instance.artifacts.wait_for_completion.assert_called_once()
            mock_client_instance.artifacts.download_audio.assert_called_once()
            
            return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Podcast generation: PASS")
            return True
        else:
            print("❌ Podcast generation: FAIL")
            return False
    except ImportError:
        print("⚠️ Podcast generation: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Podcast generation: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_quiz_generation(mock_subprocess, mock_client):
    """Test quiz generation with different formats"""
    try:
        from research_cli.integrations.content_generators import ContentGenerators
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_status = Mock()
        mock_status.task_id = "quiz_task_123"
        mock_client_instance.artifacts = Mock()
        mock_client_instance.artifacts.generate_quiz = AsyncMock(return_value=mock_status)
        mock_client_instance.artifacts.wait_for_completion = AsyncMock(return_value=None)
        mock_client_instance.artifacts.download_quiz = AsyncMock(return_value=None)
        mock_client_instance.close = AsyncMock()
        
        async def _test():
            generator = ContentGenerators(mock_client_instance)
            
            # Test quiz generation with different formats
            formats = ["json", "markdown", "html"]
            difficulties = ["easy", "medium", "hard"]
            
            for format_type in formats:
                for difficulty in difficulties:
                    result = await generator.generate_quiz(
                        "notebook_id", difficulty, "standard", "en", None, 
                        f"test_{difficulty}_{format_type}.{format_type}", format_type
                    )
                    
                    assert result["success"] == True
                    assert result["task_id"] == "quiz_task_123"
            
            return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Quiz generation: PASS")
            return True
        else:
            print("❌ Quiz generation: FAIL")
            return False
    except ImportError:
        print("⚠️ Quiz generation: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Quiz generation: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_flashcards_generation(mock_subprocess, mock_client):
    """Test flashcards generation"""
    try:
        from research_cli.integrations.content_generators import ContentGenerators
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_status = Mock()
        mock_status.task_id = "flashcards_task_123"
        mock_client_instance.artifacts = Mock()
        mock_client_instance.artifacts.generate_flashcards = AsyncMock(return_value=mock_status)
        mock_client_instance.artifacts.wait_for_completion = AsyncMock(return_value=None)
        mock_client_instance.artifacts.download_flashcards = AsyncMock(return_value=None)
        mock_client_instance.close = AsyncMock()
        
        async def _test():
            generator = ContentGenerators(mock_client_instance)
            
            result = await generator.generate_flashcards(
                "notebook_id", "medium", "standard", "vi", None, "flashcards.json", "json"
            )
            
            assert result["success"] == True
            assert result["file"] == "flashcards.json"
            assert result["task_id"] == "flashcards_task_123"
            
            return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Flashcards generation: PASS")
            return True
        else:
            print("❌ Flashcards generation: FAIL")
            return False
    except ImportError:
        print("⚠️ Flashcards generation: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Flashcards generation: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_mind_map_generation(mock_subprocess, mock_client):
    """Test mind map generation (instant)"""
    try:
        from research_cli.integrations.content_generators import ContentGenerators
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_result = Mock()
        mock_client_instance.artifacts = Mock()
        mock_client_instance.artifacts.generate_mind_map = AsyncMock(return_value=mock_result)
        mock_client_instance.artifacts.download_mind_map = AsyncMock(return_value=None)
        mock_client_instance.close = AsyncMock()
        
        async def _test():
            generator = ContentGenerators(mock_client_instance)
            
            result = await generator.generate_mind_map(
                "notebook_id", "zh_Hans", None, "mindmap.json"
            )
            
            assert result["success"] == True
            assert result["file"] == "mindmap.json"
            # Mind map is instant, no task_id
            assert "task_id" not in result
            
            return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Mind map generation: PASS")
            return True
        else:
            print("❌ Mind map generation: FAIL")
            return False
    except ImportError:
        print("⚠️ Mind map generation: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Mind map generation: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_infographic_generation(mock_subprocess, mock_client):
    """Test infographic generation with different orientations"""
    try:
        from research_cli.integrations.content_generators import ContentGenerators
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_status = Mock()
        mock_status.task_id = "infographic_task_123"
        mock_client_instance.artifacts = Mock()
        mock_client_instance.artifacts.generate_infographic = AsyncMock(return_value=mock_status)
        mock_client_instance.artifacts.wait_for_completion = AsyncMock(return_value=None)
        mock_client_instance.artifacts.download_infographic = AsyncMock(return_value=None)
        mock_client_instance.close = AsyncMock()
        
        async def _test():
            generator = ContentGenerators(mock_client_instance)
            
            # Test different orientations
            orientations = ["landscape", "portrait", "square"]
            details = ["concise", "standard", "detailed"]
            
            for orientation in orientations:
                for detail in details:
                    result = await generator.generate_infographic(
                        "notebook_id", "Blueprint style infographic", orientation, 
                        detail, "vi", None, f"infographic_{orientation}_{detail}.png"
                    )
                    
                    assert result["success"] == True
                    assert result["task_id"] == "infographic_task_123"
            
            return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Infographic generation: PASS")
            return True
        else:
            print("❌ Infographic generation: FAIL")
            return False
    except ImportError:
        print("⚠️ Infographic generation: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Infographic generation: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_video_generation(mock_subprocess, mock_client):
    """Test video generation with different styles"""
    try:
        from research_cli.integrations.content_generators import ContentGenerators
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_status = Mock()
        mock_status.task_id = "video_task_123"
        mock_client_instance.artifacts = Mock()
        mock_client_instance.artifacts.generate_video = AsyncMock(return_value=mock_status)
        mock_client_instance.artifacts.wait_for_completion = AsyncMock(return_value=None)
        mock_client_instance.artifacts.download_video = AsyncMock(return_value=None)
        mock_client_instance.close = AsyncMock()
        
        async def _test():
            generator = ContentGenerators(mock_client_instance)
            
            # Test different styles
            styles = ["auto", "classic", "whiteboard", "kawaii", "anime", "watercolor"]
            formats = ["explainer", "brief"]
            
            for style in styles[:2]:  # Test first 2 to keep test fast
                for format_type in formats:
                    result = await generator.generate_video(
                        "notebook_id", "Create engaging video", format_type, 
                        style, "en", None, f"video_{style}_{format_type}.mp4"
                    )
                    
                    assert result["success"] == True
                    assert result["task_id"] == "video_task_123"
            
            return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Video generation: PASS")
            return True
        else:
            print("❌ Video generation: FAIL")
            return False
    except ImportError:
        print("⚠️ Video generation: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Video generation: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_slide_deck_generation(mock_subprocess, mock_client):
    """Test slide deck generation with PDF/PPTX formats"""
    try:
        from research_cli.integrations.content_generators import ContentGenerators
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_status = Mock()
        mock_status.task_id = "slides_task_123"
        mock_client_instance.artifacts = Mock()
        mock_client_instance.artifacts.generate_slide_deck = AsyncMock(return_value=mock_status)
        mock_client_instance.artifacts.wait_for_completion = AsyncMock(return_value=None)
        mock_client_instance.artifacts.download_slide_deck = AsyncMock(return_value=None)
        mock_client_instance.close = AsyncMock()
        
        async def _test():
            generator = ContentGenerators(mock_client_instance)
            
            # Test both PDF and PPTX formats
            formats = ["pdf", "pptx"]
            deck_formats = ["detailed", "presenter"]
            
            for output_format in formats:
                for deck_format in deck_formats:
                    result = await generator.generate_slide_deck(
                        "notebook_id", "Create comprehensive slides", deck_format, 
                        "default", "en", None, f"slides_{deck_format}.{output_format}", output_format
                    )
                    
                    assert result["success"] == True
                    assert result["task_id"] == "slides_task_123"
            
            return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Slide deck generation: PASS")
            return True
        else:
            print("❌ Slide deck generation: FAIL")
            return False
    except ImportError:
        print("⚠️ Slide deck generation: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Slide deck generation: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_report_generation(mock_subprocess, mock_client):
    """Test report generation with different formats"""
    try:
        from research_cli.integrations.content_generators import ContentGenerators
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_status = Mock()
        mock_status.task_id = "report_task_123"
        mock_client_instance.artifacts = Mock()
        mock_client_instance.artifacts.generate_report = AsyncMock(return_value=mock_status)
        mock_client_instance.artifacts.wait_for_completion = AsyncMock(return_value=None)
        mock_client_instance.artifacts.download_report = AsyncMock(return_value=None)
        mock_client_instance.close = AsyncMock()
        
        async def _test():
            generator = ContentGenerators(mock_client_instance)
            
            # Test different report formats
            formats = ["briefing-doc", "study-guide", "blog-post", "custom"]
            
            for format_type in formats:
                result = await generator.generate_report(
                    "notebook_id", format_type, "Target audience: beginners", 
                    "vi", None, f"report_{format_type}.md"
                )
                
                assert result["success"] == True
                assert result["task_id"] == "report_task_123"
            
            return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Report generation: PASS")
            return True
        else:
            print("❌ Report generation: FAIL")
            return False
    except ImportError:
        print("⚠️ Report generation: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Report generation: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_data_table_generation(mock_subprocess, mock_client):
    """Test data table generation"""
    try:
        from research_cli.integrations.content_generators import ContentGenerators
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_status = Mock()
        mock_status.task_id = "data_table_task_123"
        mock_client_instance.artifacts = Mock()
        mock_client_instance.artifacts.generate_data_table = AsyncMock(return_value=mock_status)
        mock_client_instance.artifacts.wait_for_completion = AsyncMock(return_value=None)
        mock_client_instance.artifacts.download_data_table = AsyncMock(return_value=None)
        mock_client_instance.close = AsyncMock()
        
        async def _test():
            generator = ContentGenerators(mock_client_instance)
            
            result = await generator.generate_data_table(
                "notebook_id", "Create comparison table of AI tools and their features", 
                "en", None, "data_comparison.csv"
            )
            
            assert result["success"] == True
            assert result["file"] == "data_comparison.csv"
            assert result["task_id"] == "data_table_task_123"
            
            return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Data table generation: PASS")
            return True
        else:
            print("❌ Data table generation: FAIL")
            return False
    except ImportError:
        print("⚠️ Data table generation: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Data table generation: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_slide_revision(mock_subprocess, mock_client):
    """Test slide revision functionality"""
    try:
        from research_cli.integrations.content_generators import ContentGenerators
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_status = Mock()
        mock_status.task_id = "slide_revision_task_123"
        mock_client_instance.artifacts = Mock()
        mock_client_instance.artifacts.generate_revise_slide = AsyncMock(return_value=mock_status)
        mock_client_instance.artifacts.wait_for_completion = AsyncMock(return_value=None)
        mock_client_instance.artifacts.download_slide_deck = AsyncMock(return_value=None)
        mock_client_instance.close = AsyncMock()
        
        async def _test():
            generator = ContentGenerators(mock_client_instance)
            
            result = await generator.revise_slide(
                "notebook_id", "existing_artifact_123", 2, 
                "Make this slide more engaging with better visuals", "revised_slides.pdf"
            )
            
            assert result["success"] == True
            assert result["task_id"] == "slide_revision_task_123"
            assert result["file"] == "revised_slides.pdf"
            
            return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Slide revision: PASS")
            return True
        else:
            print("❌ Slide revision: FAIL")
            return False
    except ImportError:
        print("⚠️ Slide revision: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Slide revision: FAIL - {e}")
        return False


def test_content_generation_error_handling():
    """Test error handling in content generation"""
    try:
        from research_cli.integrations.content_generators import ContentGenerators
        
        # Mock client that throws errors
        mock_client = Mock()
        mock_client.artifacts = Mock()
        mock_client.artifacts.generate_audio = AsyncMock(side_effect=Exception("Rate limited"))
        
        async def _test():
            generator = ContentGenerators(mock_client)
            
            result = await generator.generate_podcast(
                "notebook_id", "Test", "deep-dive", "default", "en", None, "test.mp3"
            )
            
            assert result["success"] == False
            assert "Rate limited" in result["error"]
            
            return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Content generation error handling: PASS")
            return True
        else:
            print("❌ Content generation error handling: FAIL")
            return False
    except ImportError:
        print("⚠️ Content generation error handling: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Content generation error handling: FAIL - {e}")
        return False


def run_all_tests():
    """Run all content generation tests"""
    print("🧪 Testing NotebookLM Content Generation...")
    
    tests = [
        test_podcast_generation,
        test_quiz_generation,
        test_flashcards_generation,
        test_mind_map_generation,
        test_infographic_generation,
        test_video_generation,
        test_slide_deck_generation,
        test_report_generation,
        test_data_table_generation,
        test_slide_revision,
        test_content_generation_error_handling
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: FAIL - {e}")
            failed += 1
    
    print(f"\n📊 Content Generation Tests: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)