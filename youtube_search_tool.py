#!/usr/bin/env python3
"""
Công cụ tìm kiếm YouTube tùy chỉnh sử dụng yt-dlp
Tính năng: Tìm kiếm, lấy thông tin video và tải phụ đề
"""

import yt_dlp
import json
import os
from typing import List, Dict, Optional


class YouTubeSearchTool:
    def __init__(self):
        """Khởi tạo công cụ tìm kiếm YouTube"""
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
    
    def search_videos(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Tìm kiếm video trên YouTube
        
        Args:
            query: Từ khóa tìm kiếm
            max_results: Số lượng kết quả tối đa
            
        Returns:
            Danh sách thông tin video
        """
        search_url = f"ytsearch{max_results}:{query}"
        
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                search_results = ydl.extract_info(search_url, download=False)
                videos = []
                
                for entry in search_results.get('entries', []):
                    if entry:
                        video_info = {
                            'title': entry.get('title', 'N/A'),
                            'uploader': entry.get('uploader', 'N/A'),
                            'view_count': entry.get('view_count', 0),
                            'duration': entry.get('duration', 0),
                            'url': entry.get('webpage_url', ''),
                            'video_id': entry.get('id', ''),
                            'upload_date': entry.get('upload_date', ''),
                            'description': entry.get('description', '')[:200] + '...' if entry.get('description') else 'N/A'
                        }
                        videos.append(video_info)
                
                return videos
                
            except Exception as e:
                print(f"Lỗi khi tìm kiếm: {e}")
                return []
    
    def get_video_info(self, video_url: str) -> Optional[Dict]:
        """
        Lấy thông tin chi tiết của một video
        
        Args:
            video_url: URL hoặc ID của video
            
        Returns:
            Thông tin chi tiết video
        """
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                info = ydl.extract_info(video_url, download=False)
                
                return {
                    'title': info.get('title', 'N/A'),
                    'uploader': info.get('uploader', 'N/A'),
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'duration': info.get('duration', 0),
                    'upload_date': info.get('upload_date', ''),
                    'description': info.get('description', 'N/A'),
                    'tags': info.get('tags', []),
                    'categories': info.get('categories', []),
                    'subtitles': list(info.get('subtitles', {}).keys()) if info.get('subtitles') else [],
                    'automatic_captions': list(info.get('automatic_captions', {}).keys()) if info.get('automatic_captions') else []
                }
                
            except Exception as e:
                print(f"Lỗi khi lấy thông tin video: {e}")
                return None
    
    def download_subtitles(self, video_url: str, output_dir: str = "subtitles", 
                          languages: List[str] = None) -> bool:
        """
        Tải xuống phụ đề của video
        
        Args:
            video_url: URL hoặc ID của video
            output_dir: Thư mục lưu phụ đề
            languages: Danh sách ngôn ngữ cần tải (mặc định: tất cả)
            
        Returns:
            True nếu thành công, False nếu thất bại
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        subtitle_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'skip_download': True,
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
            'subtitleslangs': languages or ['vi', 'en', 'all'],
            'subtitlesformat': 'srt/best',
        }
        
        with yt_dlp.YoutubeDL(subtitle_opts) as ydl:
            try:
                ydl.download([video_url])
                return True
            except Exception as e:
                print(f"Lỗi khi tải phụ đề: {e}")
                return False
    
    def format_duration(self, seconds: int) -> str:
        """Chuyển đổi giây thành định dạng mm:ss hoặc hh:mm:ss"""
        if seconds == 0:
            return "N/A"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def format_view_count(self, count: int) -> str:
        """Định dạng số lượt xem"""
        if count >= 1_000_000:
            return f"{count/1_000_000:.1f}M"
        elif count >= 1_000:
            return f"{count/1_000:.1f}K"
        else:
            return str(count)


def main():
    """Hàm chính để demo công cụ"""
    tool = YouTubeSearchTool()
    
    while True:
        print("\n=== CÔNG CỤ TÌM KIẾM YOUTUBE ===")
        print("1. Tìm kiếm video")
        print("2. Lấy thông tin chi tiết video")
        print("3. Tải phụ đề video")
        print("4. Thoát")
        
        choice = input("\nChọn chức năng (1-4): ").strip()
        
        if choice == '1':
            query = input("Nhập từ khóa tìm kiếm: ").strip()
            if query:
                max_results = input("Số kết quả (mặc định 10): ").strip()
                max_results = int(max_results) if max_results.isdigit() else 10
                
                print(f"\nĐang tìm kiếm '{query}'...")
                videos = tool.search_videos(query, max_results)
                
                if videos:
                    print(f"\nTìm thấy {len(videos)} video:")
                    print("-" * 80)
                    for i, video in enumerate(videos, 1):
                        print(f"{i}. {video['title']}")
                        print(f"   Tác giả: {video['uploader']}")
                        print(f"   Lượt xem: {tool.format_view_count(video['view_count'])}")
                        print(f"   Thời lượng: {tool.format_duration(video['duration'])}")
                        print(f"   URL: {video['url']}")
                        print()
                else:
                    print("Không tìm thấy video nào.")
        
        elif choice == '2':
            url = input("Nhập URL hoặc ID video: ").strip()
            if url:
                print("Đang lấy thông tin...")
                info = tool.get_video_info(url)
                
                if info:
                    print(f"\n=== THÔNG TIN VIDEO ===")
                    print(f"Tiêu đề: {info['title']}")
                    print(f"Tác giả: {info['uploader']}")
                    print(f"Lượt xem: {tool.format_view_count(info['view_count'])}")
                    print(f"Lượt thích: {tool.format_view_count(info['like_count'])}")
                    print(f"Thời lượng: {tool.format_duration(info['duration'])}")
                    print(f"Ngày tải lên: {info['upload_date']}")
                    print(f"Phụ đề có sẵn: {', '.join(info['subtitles']) if info['subtitles'] else 'Không có'}")
                    print(f"Phụ đề tự động: {', '.join(info['automatic_captions']) if info['automatic_captions'] else 'Không có'}")
                    print(f"Mô tả: {info['description'][:200]}...")
                else:
                    print("Không thể lấy thông tin video.")
        
        elif choice == '3':
            url = input("Nhập URL hoặc ID video: ").strip()
            if url:
                languages = input("Ngôn ngữ phụ đề (vi,en hoặc để trống cho tất cả): ").strip()
                lang_list = [lang.strip() for lang in languages.split(',')] if languages else None
                
                print("Đang tải phụ đề...")
                success = tool.download_subtitles(url, languages=lang_list)
                
                if success:
                    print("Tải phụ đề thành công! Kiểm tra thư mục 'subtitles'.")
                else:
                    print("Không thể tải phụ đề.")
        
        elif choice == '4':
            print("Tạm biệt!")
            break
        
        else:
            print("Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()