"""
Workflow automation commands
"""

import click
import asyncio
from typing import Optional


@click.group()
def workflow_group():
    """Automated workflow commands"""
    pass


@workflow_group.command()
@click.argument('topic')
@click.option('--min-views', '-m', default=50000, help='Lượt xem tối thiểu')
@click.option('--max-videos', '-n', default=5, help='Số video tối đa')
@click.option('--notebook-title', help='Tiêu đề notebook (tự động nếu không có)')
@click.option('--question', '-q', help='Câu hỏi nghiên cứu cụ thể')
@click.option('--generate', '-g', multiple=True, 
              type=click.Choice(['podcast', 'quiz', 'infographic', 'mindmap', 'video']),
              help='Tạo nội dung (có thể chọn nhiều)')
@click.pass_context
def research(ctx, topic: str, min_views: int, max_videos: int, 
            notebook_title: Optional[str], question: Optional[str], generate: tuple):
    """Workflow nghiên cứu tự động: YouTube → NotebookLM → Analysis"""
    async def _research():
        from ..integrations import ResearchAutomation
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with ResearchAutomation() as automation:
                print_info(f"🚀 Bắt đầu nghiên cứu về: {topic}")
                
                # Custom notebook title
                if not notebook_title:
                    notebook_title = f"Research: {topic}"
                
                # Run research pipeline
                results = await automation.full_research_pipeline(
                    topic=topic,
                    min_views=min_views,
                    max_videos=max_videos,
                    generate_content=list(generate) if generate else None
                )
                
                # Display results
                print_success("✅ Nghiên cứu hoàn tất!")
                click.echo(f"📓 Notebook ID: {results['notebook_id']}")
                click.echo(f"📹 Videos analyzed: {results['videos_analyzed']}")
                
                # Show research answer
                if results['research_answer']:
                    click.echo("\n💡 KẾT QUẢ NGHIÊN CỨU:")
                    click.echo("=" * 60)
                    click.echo(results['research_answer'])
                
                # Show generated content
                if results['generated_content']:
                    click.echo("\n🎨 NỘI DUNG ĐÃ TẠO:")
                    for content_type, filename in results['generated_content'].items():
                        click.echo(f"  {content_type}: {filename}")
                
                # Ask custom question if provided
                if question:
                    click.echo(f"\n🤔 Trả lời câu hỏi: {question}")
                    answer = await automation.notebooklm.research_query(
                        results['notebook_id'], question
                    )
                    click.echo(f"💡 {answer}")
                    
        except Exception as e:
            print_error(f"Workflow nghiên cứu thất bại: {e}")
    
    asyncio.run(_research())


@workflow_group.command()
@click.argument('topic')
@click.option('--question', '-q', help='Câu hỏi cụ thể')
@click.pass_context
def quick(ctx, topic: str, question: Optional[str]):
    """Nghiên cứu nhanh với 3 video chất lượng cao"""
    async def _quick():
        from ..integrations import ResearchAutomation
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with ResearchAutomation() as automation:
                print_info(f"⚡ Nghiên cứu nhanh về: {topic}")
                
                answer = await automation.quick_research(topic, question)
                
                print_success("✅ Nghiên cứu nhanh hoàn tất!")
                click.echo("\n💡 KẾT QUẢ:")
                click.echo("=" * 50)
                click.echo(answer)
                
        except Exception as e:
            print_error(f"Nghiên cứu nhanh thất bại: {e}")
    
    asyncio.run(_quick())


@workflow_group.command()
@click.argument('topic')
@click.option('--days-back', '-d', default=30, help='Số ngày quay lại tìm trending')
@click.pass_context
def trending(ctx, topic: str, days_back: int):
    """Phân tích nội dung trending về chủ đề"""
    async def _trending():
        from ..integrations import ResearchAutomation
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with ResearchAutomation() as automation:
                print_info(f"🔥 Phân tích trending về: {topic}")
                
                results = await automation.trending_analysis(topic, days_back)
                
                if 'error' in results:
                    print_error(results['error'])
                    return
                
                print_success("✅ Phân tích trending hoàn tất!")
                click.echo(f"📓 Notebook ID: {results['notebook_id']}")
                click.echo(f"🔥 Trending videos: {results['trending_videos_count']}")
                
                click.echo("\n📈 TOP TRENDING VIDEOS:")
                for i, video in enumerate(results['top_videos'], 1):
                    views = video['views']
                    formatted_views = f"{views/1000000:.1f}M" if views >= 1000000 else f"{views/1000:.1f}K"
                    click.echo(f"  {i}. {video['title']} - {formatted_views} views")
                
                click.echo("\n💡 PHÂN TÍCH TRENDING:")
                click.echo("=" * 60)
                click.echo(results['analysis'])
                
        except Exception as e:
            print_error(f"Phân tích trending thất bại: {e}")
    
    asyncio.run(_trending())