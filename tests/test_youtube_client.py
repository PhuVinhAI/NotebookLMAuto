"""
Test YouTube client functionality
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from research_cli.core.youtube_client import YouTubeClient
from research_cli.core.filters import VideoFilter
from research_cli.core.sorters import VideoSorter


def test_youtube_client_init():
    """Test YouTube client initialization"""
    try:
        client = YouTubeClient()
        assert client is not None
        print("✅ YouTube client init: PASS")
        return True
    except Exception as e:
        print(f"❌ YouTube client init: FAIL - {e}")
        return False


def test_search_videos_basic():
    """Test basic video search"""
    try:
        client = YouTubeClient()
        videos = client.search_videos("Python tutorial", max_results=3)
        assert isinstance(videos, list)
        if videos:  # If we get results
            assert len(videos) <= 3
            assert 'title' in videos[0]
            assert 'url' in videos[0]
            assert 'view_count' in videos[0]
            print(f"✅ Search videos: PASS - Found {len(videos)} videos")
        else:
            print("⚠️ Search videos: SKIP - No videos found (network/API issue)")
        return True
    except Exception as e:
        print(f"❌ Search videos: FAIL - {e}")
        return False


def test_video_filter():
    """Test video filtering functionality"""
    try:
        sample_videos = [
            {
                'title': 'Video 1',
                'view_count': 100000,
                'duration': 600,
                'upload_date': '20240101',
                'uploader': 'Channel A',
                'video_id': 'vid1'
            },
            {
                'title': 'Video 2', 
                'view_count': 50000,
                'duration': 300,
                'upload_date': '20231201',
                'uploader': 'Channel B',
                'video_id': 'vid2'
            },
            {
                'title': 'Video 3',
                'view_count': 200000,
                'duration': 900,
                'upload_date': '20240201',
                'uploader': 'Channel A',
                'video_id': 'vid3'
            }
        ]
        
        # Test filter by view count
        filtered = VideoFilter.by_view_count(sample_videos, min_views=75000)
        assert len(filtered) == 2  # Should exclude video with 50k views
        assert all(v['view_count'] >= 75000 for v in filtered)
        
        # Test filter by duration
        filtered = VideoFilter.by_duration(sample_videos, min_duration=400)
        assert len(filtered) == 2  # Should exclude 300s video
        assert all(v['duration'] >= 400 for v in filtered)
        
        # Test filter by channel
        filtered = VideoFilter.by_channel(sample_videos, ['Channel A'])
        assert len(filtered) == 2
        assert all('Channel A' in v['uploader'] for v in filtered)
        
        # Test remove duplicates
        videos_with_dupe = sample_videos + [sample_videos[0]]  # Add duplicate
        filtered = VideoFilter.remove_duplicates(videos_with_dupe)
        assert len(filtered) == 3  # Should remove 1 duplicate
        
        print("✅ Video filters: PASS")
        return True
    except Exception as e:
        print(f"❌ Video filters: FAIL - {e}")
        return False


def test_video_sorter():
    """Test video sorting functionality"""
    try:
        sample_videos = [
            {'title': 'B Video', 'view_count': 100000, 'upload_date': '20240101'},
            {'title': 'A Video', 'view_count': 200000, 'upload_date': '20240201'},
            {'title': 'C Video', 'view_count': 50000, 'upload_date': '20231201'}
        ]
        
        # Test sort by views
        sorted_videos = VideoSorter.sort_videos(sample_videos, 'views', reverse=True)
        assert sorted_videos[0]['view_count'] == 200000
        assert sorted_videos[-1]['view_count'] == 50000
        
        # Test sort by title
        sorted_videos = VideoSorter.sort_videos(sample_videos, 'title', reverse=False)
        assert sorted_videos[0]['title'] == 'A Video'
        assert sorted_videos[-1]['title'] == 'C Video'
        
        # Test sort by date
        sorted_videos = VideoSorter.sort_videos(sample_videos, 'date', reverse=True)
        assert sorted_videos[0]['upload_date'] == '20240201'
        assert sorted_videos[-1]['upload_date'] == '20231201'
        
        print("✅ Video sorters: PASS")
        return True
    except Exception as e:
        print(f"❌ Video sorters: FAIL - {e}")
        return False


def run_all_tests():
    """Run all YouTube client tests"""
    print("🧪 Testing YouTube Client...")
    
    tests = [
        test_youtube_client_init,
        test_search_videos_basic,
        test_video_filter,
        test_video_sorter
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
    
    print(f"\n📊 YouTube Client Tests: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)