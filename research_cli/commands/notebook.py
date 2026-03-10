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


@notebook_group.command()
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
@click.pass_context
def list(ctx, output_json: bool):
    """Liệt kê tất cả notebook"""
    async def _list():
        from ..integrations import NotebookLMIntegration
        from ..utils.output import print_error
        
        try:
            async with NotebookLMIntegration() as nlm:
                notebooks = await nlm.list_notebooks()
                
                if output_json:
                    import json
                    click.echo(json.dumps(notebooks, indent=2, ensure_ascii=False))
                else:
                    if not notebooks:
                        click.echo("📓 Không có notebook nào")
                    else:
                        click.echo(f"📓 Có {len(notebooks)} notebook:")
                        for nb in notebooks:
                            click.echo(f"  • {nb['title']} (ID: {nb['id'][:8]}...)")
                    
        except Exception as e:
            print_error(f"Không thể liệt kê notebook: {e}")
    
    asyncio.run(_list())


@notebook_group.command()
@click.argument('notebook_id')
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
@click.pass_context
def sources(ctx, notebook_id: str, output_json: bool):
    """Liệt kê nguồn trong notebook"""
    async def _sources():
        from ..integrations import NotebookLMIntegration
        from ..utils.output import print_error
        
        try:
            async with NotebookLMIntegration() as nlm:
                sources = await nlm.list_sources(notebook_id)
                
                if output_json:
                    import json
                    click.echo(json.dumps(sources, indent=2, ensure_ascii=False))
                else:
                    if not sources:
                        click.echo("📄 Không có nguồn nào")
                    else:
                        click.echo(f"📄 Có {len(sources)} nguồn:")
                        for src in sources:
                            status_icon = "✅" if src['status'] == 'ready' else "⏳"
                            click.echo(f"  {status_icon} {src['title']} (ID: {src['id'][:8]}...)")
                    
        except Exception as e:
            print_error(f"Không thể liệt kê nguồn: {e}")
    
    asyncio.run(_sources())


@notebook_group.command()
@click.argument('notebook_id')
@click.option('--confirm', is_flag=True, help='Xác nhận xóa')
@click.pass_context
def delete(ctx, notebook_id: str, confirm: bool):
    """Xóa notebook"""
    async def _delete():
        from ..integrations import NotebookLMIntegration
        from ..utils.output import print_success, print_error
        
        if not confirm:
            if not click.confirm(f"Bạn có chắc muốn xóa notebook {notebook_id}?"):
                click.echo("Đã hủy")
                return
        
        try:
            async with NotebookLMIntegration() as nlm:
                success = await nlm.delete_notebook(notebook_id)
                
                if success:
                    print_success(f"Đã xóa notebook: {notebook_id}")
                else:
                    print_error("Không thể xóa notebook")
                    
        except Exception as e:
            print_error(f"Lỗi xóa notebook: {e}")
    
    asyncio.run(_delete())