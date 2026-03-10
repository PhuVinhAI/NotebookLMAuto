#!/usr/bin/env python3
"""
YouTube Search Tool CLI - Tìm kiếm và phân tích video YouTube
Sử dụng yt-dlp để tìm kiếm, lấy thông tin và tải phụ đề
"""

import yt_dlp
import json
import os
import click
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
                click.echo(f"Lỗi khi tìm kiếm: {e}", err=True)
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
                click.echo(f"Lỗi khi lấy thông tin video: {e}", err=True)
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
                click.echo(f"Lỗi khi tải phụ đề: {e}", err=True)
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


# CLI Commands using Click
@click.group()
@click.version_option(version="1.0.0", prog_name="youtube-tool")
def cli():
    """YouTube Search Tool CLI - Tìm kiếm và tải video YouTube"""
    pass


@cli.command()
@click.argument('query')
@click.option('--max-results', '-n', default=10, help='Số lượng kết quả tối đa')
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
def search(query, max_results, output_json):
    """Tìm kiếm video trên YouTube"""
    tool = YouTubeSearchTool()
    videos = tool.search_videos(query, max_results)
    
    if output_json:
        click.echo(json.dumps(videos, ensure_ascii=False, indent=2))
    else:
        if videos:
            click.echo(f"Tìm thấy {len(videos)} video:")
            click.echo("-" * 60)
            for i, video in enumerate(videos, 1):
                click.echo(f"{i}. {video['title']}")
                click.echo(f"   Tác giả: {video['uploader']}")
                click.echo(f"   Lượt xem: {tool.format_view_count(video['view_count'])}")
                click.echo(f"   Thời lượng: {tool.format_duration(video['duration'])}")
                click.echo(f"   URL: {video['url']}")
                click.echo()
        else:
            click.echo("Không tìm thấy video nào.")


@cli.command()
@click.argument('video_url')
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
def info(video_url, output_json):
    """Lấy thông tin chi tiết video"""
    tool = YouTubeSearchTool()
    video_info = tool.get_video_info(video_url)
    
    if video_info:
        if output_json:
            click.echo(json.dumps(video_info, ensure_ascii=False, indent=2))
        else:
            click.echo("=== THÔNG TIN VIDEO ===")
            click.echo(f"Tiêu đề: {video_info['title']}")
            click.echo(f"Tác giả: {video_info['uploader']}")
            click.echo(f"Lượt xem: {tool.format_view_count(video_info['view_count'])}")
            click.echo(f"Lượt thích: {tool.format_view_count(video_info['like_count'])}")
            click.echo(f"Thời lượng: {tool.format_duration(video_info['duration'])}")
            click.echo(f"Ngày tải lên: {video_info['upload_date']}")
            click.echo(f"Phụ đề có sẵn: {', '.join(video_info['subtitles']) if video_info['subtitles'] else 'Không có'}")
            click.echo(f"Phụ đề tự động: {', '.join(video_info['automatic_captions'][:5]) if video_info['automatic_captions'] else 'Không có'}")
    else:
        click.echo("Không thể lấy thông tin video.")


@cli.command()
@click.argument('video_url')
@click.option('--output-dir', '-o', default='subtitles', help='Thư mục lưu phụ đề')
@click.option('--languages', '-l', help='Ngôn ngữ phụ đề (vi,en,zh)')
def subtitles(video_url, output_dir, languages):
    """Tải phụ đề video"""
    tool = YouTubeSearchTool()
    lang_list = [lang.strip() for lang in languages.split(',')] if languages else None
    
    click.echo("Đang tải phụ đề...")
    success = tool.download_subtitles(video_url, output_dir, lang_list)
    
    if success:
        click.echo(f"Tải phụ đề thành công! Kiểm tra thư mục '{output_dir}'.")
    else:
        click.echo("Không thể tải phụ đề.")


@cli.command()
@click.argument('query')
@click.option('--max-results', '-n', default=5, help='Số lượng video')
@click.option('--output', '-o', help='File lưu danh sách URLs')
def urls(query, max_results, output):
    """Tìm kiếm và xuất danh sách URLs video"""
    tool = YouTubeSearchTool()
    videos = tool.search_videos(query, max_results)
    
    if videos:
        urls_list = [video['url'] for video in videos]
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                for url in urls_list:
                    f.write(url + '\n')
            click.echo(f"Đã lưu {len(urls_list)} URLs vào {output}")
        else:
            for url in urls_list:
                click.echo(url)
    else:
        click.echo("Không tìm thấy video nào.")


if __name__ == "__main__":
    cli()