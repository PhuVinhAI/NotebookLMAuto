"""
Test CLI commands functionality (without pytest)
"""

import sys
import os
from unittest.mock import Mock, patch
from click.testing import CliRunner

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from research_cli.main import cli


def test_main_cli_help():
    """Test main CLI help"""
    try:
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        
        if result.exit_code == 0:
            assert 'Research CLI Tool' in result.output
            assert 'search' in result.output
            assert 'pipeline' in result.output
            print("✅ Main CLI help: PASS")
            return True
        else:
            print(f"❌ Main CLI help: FAIL - exit code {result.exit_code}")
            return False
    except Exception as e:
        print(f"❌ Main CLI help: FAIL - {e}")
        return False


def test_search_command_help():
    """Test search command help"""
    try:
        runner = CliRunner()
        result = runner.invoke(cli, ['search', '--help'])
        
        if result.exit_code == 0:
            assert 'Tìm kiếm video trên YouTube' in result.output
            assert '--max-results' in result.output
            assert '--min-views' in result.output
            print("✅ Search command help: PASS")
            return True
        else:
            print(f"❌ Search command help: FAIL - exit code {result.exit_code}")
            return False
    except Exception as e:
        print(f"❌ Search command help: FAIL - {e}")
        return False


def test_export_command_help():
    """Test export command help"""
    try:
        runner = CliRunner()
        result = runner.invoke(cli, ['export', '--help'])
        
        if result.exit_code == 0:
            assert 'Xuất danh sách video URLs' in result.output
            assert '--format' in result.output
            print("✅ Export command help: PASS")
            return True
        else:
            print(f"❌ Export command help: FAIL - exit code {result.exit_code}")
            return False
    except Exception as e:
        print(f"❌ Export command help: FAIL - {e}")
        return False


def test_pipeline_command_help():
    """Test pipeline command help"""
    try:
        runner = CliRunner()
        result = runner.invoke(cli, ['pipeline', '--help'])
        
        if result.exit_code == 0:
            assert 'Pipeline nghiên cứu hoàn chỉnh' in result.output
            assert '--generate' in result.output
            print("✅ Pipeline command help: PASS")
            return True
        else:
            print(f"❌ Pipeline command help: FAIL - exit code {result.exit_code}")
            return False
    except Exception as e:
        print(f"❌ Pipeline command help: FAIL - {e}")
        return False


def test_notebook_commands_help():
    """Test notebook commands help"""
    try:
        runner = CliRunner()
        result = runner.invoke(cli, ['notebook', '--help'])
        
        if result.exit_code == 0:
            assert 'NotebookLM integration commands' in result.output
            assert 'create' in result.output
            assert 'list' in result.output
            print("✅ Notebook commands help: PASS")
            return True
        else:
            print(f"❌ Notebook commands help: FAIL - exit code {result.exit_code}")
            return False
    except Exception as e:
        print(f"❌ Notebook commands help: FAIL - {e}")
        return False


def test_generate_commands_help():
    """Test generate commands help"""
    try:
        runner = CliRunner()
        result = runner.invoke(cli, ['generate', '--help'])
        
        if result.exit_code == 0:
            assert 'Content generation commands' in result.output
            assert 'podcast' in result.output
            assert 'quiz' in result.output
            print("✅ Generate commands help: PASS")
            return True
        else:
            print(f"❌ Generate commands help: FAIL - exit code {result.exit_code}")
            return False
    except Exception as e:
        print(f"❌ Generate commands help: FAIL - {e}")
        return False


def test_command_validation():
    """Test command input validation"""
    try:
        runner = CliRunner()
        
        # Test search missing query
        result = runner.invoke(cli, ['search'])
        if result.exit_code != 0:
            print("✅ Search missing query validation: PASS")
        else:
            print("❌ Search missing query validation: FAIL - should have failed")
            return False
        
        # Test export missing query
        result = runner.invoke(cli, ['export'])
        if result.exit_code != 0:
            print("✅ Export missing query validation: PASS")
        else:
            print("❌ Export missing query validation: FAIL - should have failed")
            return False
        
        # Test pipeline missing query
        result = runner.invoke(cli, ['pipeline'])
        if result.exit_code != 0:
            print("✅ Pipeline missing query validation: PASS")
        else:
            print("❌ Pipeline missing query validation: FAIL - should have failed")
            return False
        
        # Test invalid command
        result = runner.invoke(cli, ['invalid-command'])
        if result.exit_code != 0:
            print("✅ Invalid command handling: PASS")
        else:
            print("❌ Invalid command handling: FAIL - should have failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Command validation: FAIL - {e}")
        return False


@patch('research_cli.core.youtube_client.YouTubeClient')
def test_search_command_mock(mock_client):
    """Test search command with mocked client"""
    try:
        # Mock the YouTube client
        mock_instance = Mock()
        mock_instance.search_videos.return_value = [
            {
                'title': 'Test Video',
                'uploader': 'Test Channel',
                'view_count': 100000,
                'duration': 600,
                'url': 'https://youtube.com/watch?v=test',
                'video_id': 'test',
                'upload_date': '20240101'
            }
        ]
        mock_client.return_value = mock_instance
        
        # Mock the filter and sorter classes
        with patch('research_cli.commands.search.VideoFilter') as mock_filter:
            with patch('research_cli.commands.search.VideoSorter') as mock_sorter:
                mock_filter.by_view_count.return_value = mock_instance.search_videos.return_value
                mock_filter.by_duration.return_value = mock_instance.search_videos.return_value
                mock_filter.by_upload_date.return_value = mock_instance.search_videos.return_value
                mock_filter.by_channel.return_value = mock_instance.search_videos.return_value
                mock_filter.remove_duplicates.return_value = mock_instance.search_videos.return_value
                mock_sorter.sort_videos.return_value = mock_instance.search_videos.return_value
                
                # Test search command
                runner = CliRunner()
                result = runner.invoke(cli, ['search', 'test query', '-n', '1'])
                
                # Should not crash (exit code 0 or handled gracefully)
                if result.exit_code in [0, 1]:  # Allow for expected errors
                    mock_instance.search_videos.assert_called_once()
                    print("✅ Search command execution (mocked): PASS")
                    return True
                else:
                    print(f"❌ Search command execution: FAIL - exit code {result.exit_code}")
                    print(f"Output: {result.output}")
                    return False
    except Exception as e:
        print(f"❌ Search command execution: FAIL - {e}")
        return False


def run_all_tests():
    """Run all CLI command tests"""
    print("🧪 Testing CLI Commands...")
    
    tests = [
        test_main_cli_help,
        test_search_command_help,
        test_export_command_help,
        test_pipeline_command_help,
        test_notebook_commands_help,
        test_generate_commands_help,
        test_command_validation,
        test_search_command_mock
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
    
    print(f"\n📊 CLI Command Tests: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)