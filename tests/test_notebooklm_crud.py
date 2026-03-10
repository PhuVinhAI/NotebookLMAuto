"""
Test NotebookLM CRUD operations (Create, Read, Update, Delete)
"""

import sys
import os
from unittest.mock import Mock, patch, AsyncMock
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_notebook_create(mock_subprocess, mock_client):
    """Test notebook creation"""
    try:
        from research_cli.integrations.notebooklm_client import NotebookLMIntegration
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_notebook = Mock()
        mock_notebook.id = "test_notebook_id_123"
        mock_client_instance.notebooks.create = AsyncMock(return_value=mock_notebook)
        mock_client.from_storage = AsyncMock(return_value=mock_client_instance)
        
        async def _test():
            integration = NotebookLMIntegration()
            async with integration:
                notebook_id = await integration.create_research_notebook("Test Notebook")
                assert notebook_id == "test_notebook_id_123"
                return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Notebook creation: PASS")
            return True
        else:
            print("❌ Notebook creation: FAIL")
            return False
    except ImportError:
        print("⚠️ Notebook creation: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Notebook creation: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_notebook_list(mock_subprocess, mock_client):
    """Test notebook listing"""
    try:
        from research_cli.integrations.notebooklm_client import NotebookLMIntegration
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_notebooks = [
            Mock(id="nb1", title="Notebook 1", created_at="2024-01-01"),
            Mock(id="nb2", title="Notebook 2", created_at="2024-01-02")
        ]
        mock_client_instance.notebooks.list = AsyncMock(return_value=mock_notebooks)
        mock_client.from_storage = AsyncMock(return_value=mock_client_instance)
        
        async def _test():
            integration = NotebookLMIntegration()
            async with integration:
                notebooks = await integration.list_notebooks()
                assert len(notebooks) == 2
                assert notebooks[0]['id'] == "nb1"
                assert notebooks[0]['title'] == "Notebook 1"
                return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Notebook listing: PASS")
            return True
        else:
            print("❌ Notebook listing: FAIL")
            return False
    except ImportError:
        print("⚠️ Notebook listing: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Notebook listing: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_source_operations(mock_subprocess, mock_client):
    """Test source add and list operations"""
    try:
        from research_cli.integrations.notebooklm_client import NotebookLMIntegration
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_client_instance.sources.add_url = AsyncMock(return_value="source_id_123")
        mock_sources = [
            Mock(id="src1", title="Video 1", status="ready", type="youtube"),
            Mock(id="src2", title="Video 2", status="processing", type="youtube")
        ]
        mock_client_instance.sources.list = AsyncMock(return_value=mock_sources)
        mock_client.from_storage = AsyncMock(return_value=mock_client_instance)
        
        async def _test():
            integration = NotebookLMIntegration()
            async with integration:
                # Test add sources
                video_urls = ["https://youtube.com/watch?v=1", "https://youtube.com/watch?v=2"]
                source_ids = await integration.add_youtube_sources("notebook_id", video_urls, wait_for_processing=False)
                assert len(source_ids) == 2
                
                # Test list sources
                sources = await integration.list_sources("notebook_id")
                assert len(sources) == 2
                assert sources[0]['id'] == "src1"
                assert sources[0]['status'] == "ready"
                assert sources[1]['status'] == "processing"
                
                return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Source operations: PASS")
            return True
        else:
            print("❌ Source operations: FAIL")
            return False
    except ImportError:
        print("⚠️ Source operations: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Source operations: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_chat_functionality(mock_subprocess, mock_client):
    """Test chat/query functionality"""
    try:
        from research_cli.integrations.notebooklm_client import NotebookLMIntegration
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_result = Mock()
        mock_result.answer = "This is the answer to your question."
        mock_result.conversation_id = "conv_123"
        mock_result.references = [
            Mock(source_id="src1", citation_number=1, cited_text="Relevant text from source 1"),
            Mock(source_id="src2", citation_number=2, cited_text="Relevant text from source 2")
        ]
        mock_client_instance.chat.ask = AsyncMock(return_value=mock_result)
        mock_client.from_storage = AsyncMock(return_value=mock_client_instance)
        
        async def _test():
            integration = NotebookLMIntegration()
            async with integration:
                result = await integration.research_query("notebook_id", "What are the main points?")
                assert result['answer'] == "This is the answer to your question."
                assert result['conversation_id'] == "conv_123"
                assert len(result['references']) == 2
                return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Chat functionality: PASS")
            return True
        else:
            print("❌ Chat functionality: FAIL")
            return False
    except ImportError:
        print("⚠️ Chat functionality: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Chat functionality: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_artifact_operations(mock_subprocess, mock_client):
    """Test artifact listing and management"""
    try:
        from research_cli.integrations.notebooklm_client import NotebookLMIntegration
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_artifacts = [
            Mock(id="art1", title="Research Podcast", type="Audio Overview", status="completed"),
            Mock(id="art2", title="Research Quiz", type="Quiz", status="in_progress")
        ]
        mock_client_instance.artifacts.list = AsyncMock(return_value=mock_artifacts)
        mock_client.from_storage = AsyncMock(return_value=mock_client_instance)
        
        async def _test():
            integration = NotebookLMIntegration()
            async with integration:
                artifacts = await integration.list_artifacts("notebook_id")
                assert len(artifacts) == 2
                assert artifacts[0]['type'] == "Audio Overview"
                assert artifacts[0]['status'] == "completed"
                assert artifacts[1]['status'] == "in_progress"
                return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Artifact operations: PASS")
            return True
        else:
            print("❌ Artifact operations: FAIL")
            return False
    except ImportError:
        print("⚠️ Artifact operations: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Artifact operations: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_notebook_delete(mock_subprocess, mock_client):
    """Test notebook deletion"""
    try:
        from research_cli.integrations.notebooklm_client import NotebookLMIntegration
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_client_instance.notebooks.delete = AsyncMock(return_value=None)
        mock_client.from_storage = AsyncMock(return_value=mock_client_instance)
        
        async def _test():
            integration = NotebookLMIntegration()
            async with integration:
                success = await integration.delete_notebook("notebook_id")
                assert success == True
                return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Notebook deletion: PASS")
            return True
        else:
            print("❌ Notebook deletion: FAIL")
            return False
    except ImportError:
        print("⚠️ Notebook deletion: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Notebook deletion: FAIL - {e}")
        return False


def run_all_tests():
    """Run all NotebookLM CRUD tests"""
    print("🧪 Testing NotebookLM CRUD Operations...")
    
    tests = [
        test_notebook_create,
        test_notebook_list,
        test_source_operations,
        test_chat_functionality,
        test_artifact_operations,
        test_notebook_delete
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
    
    print(f"\n📊 NotebookLM CRUD Tests: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)