"""
Test NotebookLM authentication and setup
"""

import sys
import os
from unittest.mock import Mock, patch, AsyncMock
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_notebooklm_import():
    """Test NotebookLM integration import"""
    try:
        from research_cli.integrations.notebooklm_client import NotebookLMIntegration
        print("✅ NotebookLM integration import: PASS")
        return True
    except ImportError as e:
        if "notebooklm-py not installed" in str(e):
            print("⚠️ NotebookLM integration import: SKIP - notebooklm-py not installed")
            return True  # This is expected if not installed
        else:
            print(f"❌ NotebookLM integration import: FAIL - {e}")
            return False
    except Exception as e:
        print(f"❌ NotebookLM integration import: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_auth_check_success(mock_subprocess, mock_client):
    """Test successful auth check"""
    try:
        from research_cli.integrations.notebooklm_client import NotebookLMIntegration
        
        # Mock successful auth check
        mock_subprocess.return_value.returncode = 0
        
        async def _test():
            integration = NotebookLMIntegration()
            await integration._ensure_authenticated()
            return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Auth check success: PASS")
            return True
        else:
            print("❌ Auth check success: FAIL")
            return False
    except ImportError:
        print("⚠️ Auth check success: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Auth check success: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_auth_check_failure_and_login(mock_subprocess, mock_client):
    """Test auth check failure and auto-login"""
    try:
        from research_cli.integrations.notebooklm_client import NotebookLMIntegration
        
        # Mock failed auth check, then successful login
        mock_subprocess.side_effect = [
            Mock(returncode=1),  # Auth check fails
            Mock(returncode=0)   # Login succeeds
        ]
        
        async def _test():
            integration = NotebookLMIntegration()
            await integration._ensure_authenticated()
            return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Auth failure and auto-login: PASS")
            return True
        else:
            print("❌ Auth failure and auto-login: FAIL")
            return False
    except ImportError:
        print("⚠️ Auth failure and auto-login: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Auth failure and auto-login: FAIL - {e}")
        return False


@patch('research_cli.integrations.notebooklm_client.NotebookLMClient')
@patch('subprocess.run')
def test_language_support(mock_subprocess, mock_client):
    """Test language support functionality"""
    try:
        from research_cli.integrations.notebooklm_client import NotebookLMIntegration
        
        # Mock successful auth
        mock_subprocess.return_value.returncode = 0
        
        # Mock client methods
        mock_client_instance = Mock()
        mock_client_instance.language.get = AsyncMock(return_value="en")
        mock_client_instance.language.set = AsyncMock(return_value=None)
        mock_client_instance.language.list = AsyncMock(return_value=[
            Mock(code="en", name="English", native_name="English"),
            Mock(code="vi", name="Vietnamese", native_name="Tiếng Việt"),
            Mock(code="zh_Hans", name="Chinese Simplified", native_name="中文（简体）")
        ])
        mock_client.from_storage = AsyncMock(return_value=mock_client_instance)
        
        async def _test():
            integration = NotebookLMIntegration()
            async with integration:
                # Test get language
                lang = await integration.get_language()
                assert lang == "en"
                
                # Test set language
                success = await integration.set_language("vi")
                assert success == True
                
                # Test list languages
                languages = await integration.list_supported_languages()
                assert len(languages) == 3
                assert languages[0]['code'] == "en"
                
                return True
        
        result = asyncio.run(_test())
        if result:
            print("✅ Language support: PASS")
            return True
        else:
            print("❌ Language support: FAIL")
            return False
    except ImportError:
        print("⚠️ Language support: SKIP - notebooklm-py not installed")
        return True
    except Exception as e:
        print(f"❌ Language support: FAIL - {e}")
        return False


def test_without_notebooklm_py():
    """Test proper error handling without notebooklm-py"""
    try:
        with patch('research_cli.integrations.notebooklm_client.NotebookLMClient', None):
            from research_cli.integrations.notebooklm_client import NotebookLMIntegration
            try:
                NotebookLMIntegration()
                print("❌ Should fail without notebooklm-py: FAIL")
                return False
            except ImportError as e:
                if "notebooklm-py not installed" in str(e):
                    print("✅ Proper error without notebooklm-py: PASS")
                    return True
                else:
                    print(f"❌ Wrong error message: FAIL - {e}")
                    return False
    except Exception as e:
        print(f"❌ Error handling test: FAIL - {e}")
        return False


def run_all_tests():
    """Run all NotebookLM auth tests"""
    print("🧪 Testing NotebookLM Authentication...")
    
    tests = [
        test_notebooklm_import,
        test_auth_check_success,
        test_auth_check_failure_and_login,
        test_language_support,
        test_without_notebooklm_py
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
    
    print(f"\n📊 NotebookLM Auth Tests: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)