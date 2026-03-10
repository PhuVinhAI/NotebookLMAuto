"""
Test all imports and module structure
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_core_imports():
    """Test core module imports"""
    try:
        from research_cli.core import YouTubeClient, VideoFilter, VideoSorter
        print("✅ Core imports: PASS")
        return True
    except ImportError as e:
        print(f"❌ Core imports: FAIL - {e}")
        return False


def test_command_imports():
    """Test command module imports"""
    try:
        from research_cli.commands import (
            search_command, info_command, notebook_group, 
            generate_group, export_command, pipeline
        )
        print("✅ Command imports: PASS")
        return True
    except ImportError as e:
        print(f"❌ Command imports: FAIL - {e}")
        return False


def test_integration_imports():
    """Test integration module imports"""
    try:
        from research_cli.integrations import NotebookLMIntegration, ContentGenerators
        print("✅ Integration imports: PASS")
        return True
    except ImportError as e:
        print(f"❌ Integration imports: FAIL - {e}")
        return False


def test_utils_imports():
    """Test utils module imports"""
    try:
        from research_cli.utils.output import print_success, print_error, print_info
        print("✅ Utils imports: PASS")
        return True
    except ImportError as e:
        print(f"❌ Utils imports: FAIL - {e}")
        return False


def test_main_cli_import():
    """Test main CLI import"""
    try:
        from research_cli.main import cli
        print("✅ Main CLI import: PASS")
        return True
    except ImportError as e:
        print(f"❌ Main CLI import: FAIL - {e}")
        return False


def test_individual_commands():
    """Test individual command imports"""
    commands_to_test = [
        ('search', 'research_cli.commands.search'),
        ('info', 'research_cli.commands.info'),
        ('export', 'research_cli.commands.export'),
        ('notebook', 'research_cli.commands.notebook'),
        ('generate', 'research_cli.commands.generate'),
        ('pipeline', 'research_cli.commands.pipeline')
    ]
    
    all_passed = True
    for cmd_name, module_path in commands_to_test:
        try:
            __import__(module_path)
            print(f"✅ {cmd_name} command import: PASS")
        except ImportError as e:
            print(f"❌ {cmd_name} command import: FAIL - {e}")
            all_passed = False
    
    return all_passed


def test_optional_dependencies():
    """Test optional dependencies"""
    # Test yt-dlp
    try:
        import yt_dlp
        print("✅ yt-dlp available: PASS")
    except ImportError:
        print("⚠️ yt-dlp not available: This will cause YouTube functionality to fail")
    
    # Test click
    try:
        import click
        print("✅ click available: PASS")
    except ImportError:
        print("❌ click not available: CLI will not work")
    
    # Test notebooklm-py (optional)
    try:
        import notebooklm
        print("✅ notebooklm-py available: PASS")
    except ImportError:
        print("⚠️ notebooklm-py not available: NotebookLM features will not work")
    
    # Test asyncio
    try:
        import asyncio
        print("✅ asyncio available: PASS")
    except ImportError:
        print("❌ asyncio not available: Async features will not work")


def test_package_structure():
    """Test package structure"""
    expected_files = [
        'research_cli/__init__.py',
        'research_cli/main.py',
        'research_cli/core/__init__.py',
        'research_cli/core/youtube_client.py',
        'research_cli/core/filters.py',
        'research_cli/core/sorters.py',
        'research_cli/commands/__init__.py',
        'research_cli/commands/search.py',
        'research_cli/commands/info.py',
        'research_cli/commands/export.py',
        'research_cli/commands/notebook.py',
        'research_cli/commands/generate.py',
        'research_cli/commands/pipeline.py',
        'research_cli/integrations/__init__.py',
        'research_cli/integrations/notebooklm_client.py',
        'research_cli/integrations/content_generators.py',
        'research_cli/utils/__init__.py',
        'research_cli/utils/output.py'
    ]
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    missing_files = []
    
    for file_path in expected_files:
        full_path = os.path.join(base_dir, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Package structure: FAIL - Missing files: {missing_files}")
        return False
    else:
        print("✅ Package structure: PASS")
        return True


if __name__ == "__main__":
    print("🧪 Testing Imports and Package Structure...")
    
    all_tests_passed = True
    
    # Test package structure first
    if not test_package_structure():
        all_tests_passed = False
    
    # Test imports
    if not test_core_imports():
        all_tests_passed = False
    
    if not test_command_imports():
        all_tests_passed = False
    
    if not test_integration_imports():
        all_tests_passed = False
    
    if not test_utils_imports():
        all_tests_passed = False
    
    if not test_main_cli_import():
        all_tests_passed = False
    
    if not test_individual_commands():
        all_tests_passed = False
    
    # Test dependencies
    print("\n🔍 Checking Dependencies...")
    test_optional_dependencies()
    
    if all_tests_passed:
        print("\n🎉 All import tests PASSED!")
    else:
        print("\n💥 Some import tests FAILED!")
        sys.exit(1)