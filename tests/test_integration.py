"""
Test integration functionality (NotebookLM, etc.) - without pytest
"""

import sys
import os
from unittest.mock import Mock, patch, AsyncMock
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_notebooklm_integration_import():
    """Test NotebookLM integration import"""
    try:
        from research_cli.integrations.notebooklm_client import NotebookLMIntegration
        from research_cli.integrations.content_generators import ContentGenerators
        print("✅ NotebookLM integration imports: PASS")
        return True
    except ImportError as e:
        if "notebooklm-py not installed" in str(e):
            print("⚠️ NotebookLM integration imports: SKIP - notebooklm-py not installed")
            return True
        else:
            print(f"❌ NotebookLM integration imports: FAIL - {e}")
            return False
    except Exception as e:
        print(f"❌ NotebookLM integration imports: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_notebooklm_init_mock(mock_subprocess, mock_client):
    """Test NotebookLM integration initialization with mocks"""
    try:
        from research_cli.integrations.notebooklm_client import NotebookLMIntegration
        
        # Mock successful auth check
        mock_subprocess.return_value.returncode = 0
        
        integration = NotebookLMIntegration()
        assert integration is not None
        print("✅ NotebookLM integration init (mocked): PASS")
        return True
    except ImportError as e:
        if "notebooklm-py not installed" in str(e):
            print("⚠️ NotebookLM integration init: SKIP - notebooklm-py not installed")
            return True
        else:
            print(f"❌ NotebookLM integration init: FAIL - {e}")
            return False
    except Exception as e:
        print(f"❌ NotebookLM integration init: FAIL - {e}")
        return False


def test_content_generators_mock():
    """Test content generators with mock client"""
    try:
        from research_cli.integrations.content_generators import ContentGenerators
        
        # Create mock client
        mock_client = Mock()
        content_gen = ContentGenerators(mock_client)
        
        assert content_gen is not None
        assert content_gen.client == mock_client
        print("✅ Content generators init: PASS")
        return True
    except Exception as e:
        print(f"❌ Content generators init: FAIL - {e}")
        return False


async def test_content_generation_async():
    """Test async content generation methods"""
    try:
        from research_cli.integrations.content_generators import ContentGenerators
        
        # Mock client with async methods
        mock_client = Mock()
        mock_status = Mock()
        mock_status.task_id = "test_task_id"
        
        mock_client.artifacts.generate_audio = AsyncMock(return_value=mock_status)
        mock_client.artifacts.wait_for_completion = AsyncMock()
        mock_client.artifacts.download_audio = AsyncMock()
        
        content_gen = ContentGenerators(mock_client)
        
        result = await content_gen.generate_podcast(
            "test_notebook", "test instructions", "deep-dive", "default", "en", None, "test.mp3"
        )
        
        assert result['success'] == True
        assert result['file'] == "test.mp3"
        print("✅ Async content generation: PASS")
        return True
    except Exception as e:
        print(f"❌ Async content generation: FAIL - {e}")
        return False


def run_all_tests():
    """Run all integration tests"""
    print("🧪 Testing Integration...")
    
    tests = [
        test_notebooklm_integration_import,
        test_notebooklm_init_mock,
        test_content_generators_mock
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
    
    # Run async test
    try:
        result = asyncio.run(test_content_generation_async())
        if result:
            passed += 1
        else:
            failed += 1
    except Exception as e:
        print(f"❌ test_content_generation_async: FAIL - {e}")
        failed += 1
    
    print(f"\n📊 Integration Tests: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)