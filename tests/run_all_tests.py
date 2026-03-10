"""
Run all tests and provide comprehensive report
"""

import sys
import os
import subprocess
import traceback

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_test_file(test_file):
    """Run a specific test file and capture results"""
    print(f"\n{'='*60}")
    print(f"🧪 Running {test_file}")
    print('='*60)
    
    try:
        # Try to run as module first
        result = subprocess.run([
            sys.executable, '-m', f'tests.{test_file[:-3]}'
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
        
        if result.returncode != 0:
            # If module run fails, try direct execution
            test_path = os.path.join(os.path.dirname(__file__), test_file)
            result = subprocess.run([
                sys.executable, test_path
            ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Failed to run {test_file}: {e}")
        traceback.print_exc()
        return False


def run_direct_import_test():
    """Run import test directly in this process"""
    print(f"\n{'='*60}")
    print("🧪 Running Direct Import Test")
    print('='*60)
    
    try:
        # Test basic imports
        from research_cli.main import cli
        print("✅ Main CLI import: PASS")
        
        from research_cli.core.youtube_client import YouTubeClient
        print("✅ YouTube client import: PASS")
        
        from research_cli.core.filters import VideoFilter
        from research_cli.core.sorters import VideoSorter
        print("✅ Core utilities import: PASS")
        
        from research_cli.commands.search import search_command
        from research_cli.commands.pipeline import pipeline
        print("✅ Commands import: PASS")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct import test failed: {e}")
        traceback.print_exc()
        return False


def run_basic_functionality_test():
    """Test basic functionality without external dependencies"""
    print(f"\n{'='*60}")
    print("🧪 Running Basic Functionality Test")
    print('='*60)
    
    try:
        # Test YouTube client initialization
        from research_cli.core.youtube_client import YouTubeClient
        client = YouTubeClient()
        print("✅ YouTube client initialization: PASS")
        
        # Test filters with sample data
        from research_cli.core.filters import VideoFilter
        sample_videos = [
            {'title': 'Test', 'view_count': 100000, 'video_id': '1'},
            {'title': 'Test2', 'view_count': 50000, 'video_id': '2'}
        ]
        filtered = VideoFilter.by_view_count(sample_videos, min_views=75000)
        assert len(filtered) == 1
        print("✅ Video filtering: PASS")
        
        # Test sorters
        from research_cli.core.sorters import VideoSorter
        sorted_videos = VideoSorter.sort_videos(sample_videos, 'views', reverse=True)
        assert sorted_videos[0]['view_count'] == 100000
        print("✅ Video sorting: PASS")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        traceback.print_exc()
        return False


def run_cli_help_test():
    """Test CLI help commands"""
    print(f"\n{'='*60}")
    print("🧪 Running CLI Help Test")
    print('='*60)
    
    try:
        from click.testing import CliRunner
        from research_cli.main import cli
        
        runner = CliRunner()
        
        # Test main help
        result = runner.invoke(cli, ['--help'])
        if result.exit_code == 0:
            print("✅ Main CLI help: PASS")
        else:
            print(f"❌ Main CLI help: FAIL - exit code {result.exit_code}")
            return False
        
        # Test search help
        result = runner.invoke(cli, ['search', '--help'])
        if result.exit_code == 0:
            print("✅ Search command help: PASS")
        else:
            print(f"❌ Search command help: FAIL - exit code {result.exit_code}")
            return False
        
        # Test pipeline help
        result = runner.invoke(cli, ['pipeline', '--help'])
        if result.exit_code == 0:
            print("✅ Pipeline command help: PASS")
        else:
            print(f"❌ Pipeline command help: FAIL - exit code {result.exit_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ CLI help test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🚀 Research CLI - Comprehensive Test Suite")
    print("="*60)
    
    test_results = {}
    
    # Run direct tests first (most important)
    test_results['Direct Import Test'] = run_direct_import_test()
    test_results['Basic Functionality Test'] = run_basic_functionality_test()
    test_results['CLI Help Test'] = run_cli_help_test()
    
    # Run test files
    test_files = [
        'test_imports.py',
        'test_youtube_client.py', 
        'test_commands.py',
        'test_integration.py',
        'test_notebooklm_auth.py',
        'test_notebooklm_crud.py',
        'test_content_generation.py',
        'test_pipeline_workflows.py'
    ]
    
    for test_file in test_files:
        if os.path.exists(os.path.join(os.path.dirname(__file__), test_file)):
            test_results[test_file] = run_test_file(test_file)
        else:
            print(f"⚠️ Test file {test_file} not found")
            test_results[test_file] = False
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print('='*60)
    
    passed = 0
    failed = 0
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {passed + failed} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        return 0
    else:
        print(f"\n💥 {failed} TESTS FAILED!")
        return 1


if __name__ == "__main__":
    sys.exit(main())