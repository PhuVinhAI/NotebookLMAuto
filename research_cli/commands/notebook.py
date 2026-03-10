"""
NotebookLM integration commands
"""

import click
import asyncio


@click.group()
def notebook_group():
    """NotebookLM integration commands"""
    pass


@notebook_group.command()
@click.argument('title')
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
@click.pass_context
def create(ctx, title: str, output_json: bool):
    """Tạo notebook mới trong NotebookLM"""
    async def _create():
        from ..integrations import NotebookLMIntegration
        from ..utils.output import print_success, print_error
        
        try:
            async with NotebookLMIntegration() as nlm:
                notebook_id = await nlm.create_research_notebook(title)
                
                if output_json:
                    click.echo(f'{{"notebook_id": "{notebook_id}", "title": "{title}"}}')
                else:
                    print_success(f"Đã tạo notebook: {title}")
                    click.echo(f"📓 Notebook ID: {notebook_id}")
                    
        except Exception as e:
            print_error(f"Không thể tạo notebook: {e}")
    
    asyncio.run(_create())


@notebook_group.command()
@click.argument('notebook_id')
@click.argument('video_urls', nargs=-1, required=True)
@click.option('--wait', is_flag=True, help='Đợi xử lý hoàn tất')
@click.pass_context
def add_sources(ctx, notebook_id: str, video_urls: tuple, wait: bool):
    """Thêm video YouTube làm nguồn vào notebook"""
    async def _add_sources():
        from ..integrations import NotebookLMIntegration
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with NotebookLMIntegration() as nlm:
                print_info(f"Đang thêm {len(video_urls)} video vào notebook...")
                
                source_ids = await nlm.add_youtube_sources(
                    notebook_id, list(video_urls), wait_for_processing=wait
                )
                
                print_success(f"Đã thêm {len(source_ids)} nguồn video")
                for i, source_id in enumerate(source_ids, 1):
                    click.echo(f"  {i}. Source ID: {source_id}")
                    
        except Exception as e:
            print_error(f"Không thể thêm nguồn: {e}")
    
    asyncio.run(_add_sources())


@notebook_group.command()
@click.argument('notebook_id')
@click.argument('question')
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
@click.pass_context
def ask(ctx, notebook_id: str, question: str, output_json: bool):
    """Đặt câu hỏi nghiên cứu cho notebook"""
    async def _ask():
        from ..integrations import NotebookLMIntegration
        from ..utils.output import print_error
        
        try:
            async with NotebookLMIntegration() as nlm:
                answer = await nlm.research_query(notebook_id, question)
                
                if output_json:
                    click.echo(f'{{"question": "{question}", "answer": "{answer}"}}')
                else:
                    click.echo("🤔 Câu hỏi:")
                    click.echo(f"   {question}")
                    click.echo("\n💡 Trả lời:")
                    click.echo(f"   {answer}")
                    
        except Exception as e:
            print_error(f"Không thể trả lời câu hỏi: {e}")
    
    asyncio.run(_ask())