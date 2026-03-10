"""
Main CLI entry point for YouTube Tool
"""

import click
import logging
from typing import Optional

from .commands.search import search_command
from .__init__ import __version__


# Configure logging
def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


@click.group()
@click.version_option(version=__version__, prog_name="youtube-cli")
@click.option('--verbose', '-v', is_flag=True, help='Bật chế độ verbose')
@click.pass_context
def cli(ctx, verbose: bool):
    """YouTube CLI Tool - Professional YouTube search and analysis
    
    Công cụ tìm kiếm và phân tích YouTube chuyên nghiệp
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    
    # Setup logging
    setup_logging(verbose)


# Register commands
cli.add_command(search_command, name='search')


@cli.command()
@click.argument('video_url')
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
@click.pass_context
def info(ctx, video_url: str, output_json: bool):
    """Lấy thông tin chi tiết video"""
    from .core import YouTubeClient
    from .utils.output import format_json_output, print_error
    
    verbose = ctx.obj.get('verbose', False)
    client = YouTubeClient(quiet=not verbose)
    
    if verbose:
        click.echo(f"🔍 Đang lấy thông tin video: {video_url}")
    
    video_info = client.get_video_info(video_url)
    
    if video_info:
        if output_json:
            click.echo(format_json_output(video_info))
        else:
            click.echo("📺 THÔNG TIN VIDEO")
            click.echo("=" * 50)
            click.echo(f"📝 Tiêu đề: {video_info['title']}")
            click.echo(f"👤 Kênh: {video_info['uploader']}")
            click.echo(f"👀 Lượt xem: {client.format_view_count(video_info['view_count'])}")
            click.echo(f"👍 Lượt thích: {client.format_view_count(video_info['like_count'])}")
            click.echo(f"⏱️  Thời lượng: {client.format_duration(video_info['duration'])}")
            click.echo(f"📅 Ngày tải: {video_info['upload_date_formatted']}")
            
            subtitles = video_info.get('subtitles', [])
            auto_captions = video_info.get('automatic_captions', [])
            
            click.echo(f"📝 Phụ đề: {', '.join(subtitles[:5]) if subtitles else 'Không có'}")
            click.echo(f"🤖 Phụ đề tự động: {', '.join(auto_captions[:5]) if auto_captions else 'Không có'}")
            
            if video_info.get('tags'):
                click.echo(f"🏷️  Tags: {', '.join(video_info['tags'][:10])}")
    else:
        print_error("Không thể lấy thông tin video.")


@cli.command()
@click.argument('query')
@click.option('--min-views', '-m', default=100000, help='Lượt xem tối thiểu (mặc định 100K)')
@click.option('--max-results', '-n', default=10, help='Số lượng kết quả')
@click.option('--days-ago', default=365, help='Video trong N ngày qua (mặc định 365)')
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
@click.pass_context
def trending(ctx, query: str, min_views: int, max_results: int, days_ago: int, output_json: bool):
    """Tìm video trending (lượt xem cao) về chủ đề"""
    from .core import YouTubeClient, VideoFilter, VideoSorter
    from .utils.output import format_trending_list, format_json_output, print_info, print_error
    
    verbose = ctx.obj.get('verbose', False)
    client = YouTubeClient(quiet=not verbose)
    
    print_info(f"Tìm video trending về '{query}' (tối thiểu {client.format_view_count(min_views)} views)")
    
    # Search with expanded results for filtering
    search_limit = max_results * 10
    videos = client.search_videos(query, search_limit)
    
    if not videos:
        print_error("Không tìm thấy video nào.")
        return
    
    # Apply trending filters
    trending_videos = VideoFilter.trending_videos(videos, min_views, days_ago)
    
    if not trending_videos:
        print_error(f"Không tìm thấy video trending nào với điều kiện: >{client.format_view_count(min_views)} views, {days_ago} ngày qua.")
        click.echo("💡 Thử giảm --min-views hoặc tăng --days-ago")
        return
    
    # Sort by engagement score for better trending detection
    trending_videos = VideoSorter.rank_by_engagement(trending_videos)
    
    # Limit results
    trending_videos = trending_videos[:max_results]
    
    # Output results
    if output_json:
        click.echo(format_json_output(trending_videos))
    else:
        click.echo(format_trending_list(trending_videos, client))


@cli.command()
@click.argument('query')
@click.option('--format', 'export_format', default='urls', 
              type=click.Choice(['urls', 'json', 'csv']),
              help='Định dạng xuất: urls, json, csv')
@click.option('--output', '-o', help='File đầu ra')
@click.option('--max-results', '-n', default=10, help='Số lượng video')
@click.option('--sort-by', '-s', default='views', 
              type=click.Choice(['views', 'date', 'duration', 'relevance']),
              help='Sắp xếp theo tiêu chí')
@click.option('--min-views', '-m', default=10000, help='Lượt xem tối thiểu')
@click.pass_context
def export(ctx, query: str, export_format: str, output: Optional[str], 
          max_results: int, sort_by: str, min_views: int):
    """Xuất danh sách video theo định dạng chỉ định"""
    from .core import YouTubeClient, VideoFilter, VideoSorter
    from .utils.output import format_json_output, format_export_summary, print_error, print_info
    import csv
    import json
    
    verbose = ctx.obj.get('verbose', False)
    client = YouTubeClient(quiet=not verbose)
    
    print_info(f"Tìm kiếm và xuất video về '{query}'...")
    
    # Search with expanded results for filtering
    search_limit = max(max_results * 5, 50)
    videos = client.search_videos(query, search_limit)
    
    if not videos:
        print_error("Không tìm thấy video nào.")
        return
    
    # Apply filters
    if min_views > 0:
        videos = VideoFilter.by_view_count(videos, min_views)
        print_info(f"Lọc video có ít nhất {client.format_view_count(min_views)} lượt xem...")
    
    # Sort videos
    videos = VideoSorter.sort_videos(videos, sort_by, reverse=True)
    
    # Limit results
    videos = videos[:max_results]
    
    if not videos:
        print_error("Không có video nào thỏa mãn điều kiện.")
        return
    
    # Show selected videos
    click.echo(f"\n📋 Đã chọn {len(videos)} video hàng đầu:")
    for i, video in enumerate(videos, 1):
        click.echo(f"  {i}. {video['title']} - {client.format_view_count(video['view_count'])} views")
    
    # Export based on format
    if export_format == 'urls':
        urls = [video['url'] for video in videos]
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                for url in urls:
                    f.write(url + '\n')
        else:
            click.echo("\n🔗 DANH SÁCH URLs:")
            for url in urls:
                click.echo(url)
    
    elif export_format == 'json':
        json_data = format_json_output(videos)
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(json_data)
        else:
            click.echo(json_data)
    
    elif export_format == 'csv':
        if not output:
            output = f"youtube_export_{query.replace(' ', '_')}.csv"
        
        with open(output, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'uploader', 'view_count', 'duration', 'upload_date_formatted', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for video in videos:
                row = {field: video.get(field, '') for field in fieldnames}
                writer.writerow(row)
    
    # Show export summary
    if output:
        click.echo(f"\n{format_export_summary(videos, export_format, output)}")


if __name__ == '__main__':
    cli()