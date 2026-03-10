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
@click.option('--sources', '-s', multiple=True, help='Specific source IDs to query')
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
@click.pass_context
def ask(ctx, notebook_id: str, question: str, sources: tuple, output_json: bool):
    """Đặt câu hỏi nghiên cứu cho notebook"""
    async def _ask():
        from ..integrations import NotebookLMIntegration
        from ..utils.output import print_error
        
        try:
            async with NotebookLMIntegration() as nlm:
                source_ids = list(sources) if sources else None
                result = await nlm.research_query(notebook_id, question, source_ids)
                
                if output_json:
                    import json
                    click.echo(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    click.echo("🤔 Câu hỏi:")
                    click.echo(f"   {question}")
                    click.echo("\n💡 Trả lời:")
                    click.echo(f"   {result['answer']}")
                    
                    if result.get('references'):
                        click.echo(f"\n📚 Tham khảo ({len(result['references'])} nguồn):")
                        for i, ref in enumerate(result['references'][:3], 1):
                            # Sử dụng thuộc tính thay vì dict access
                            citation_num = ref.get('citation_number', i)
                            cited_text = ref.get('cited_text', 'N/A')
                            click.echo(f"  [{citation_num}] {cited_text[:100]}...")
                    
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
                            status_icon = "✅" if src['is_ready'] else "⏳"  # Sử dụng is_ready
                            type_info = f" ({src.get('type', 'unknown')})" if src.get('type') else ""
                            click.echo(f"  {status_icon} {src['title']}{type_info} (ID: {src['id'][:8]}...)")
                    
        except Exception as e:
            print_error(f"Không thể liệt kê nguồn: {e}")
    
    asyncio.run(_sources())


@notebook_group.command()
@click.argument('notebook_id')
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
@click.pass_context
def artifacts(ctx, notebook_id: str, output_json: bool):
    """Liệt kê artifacts trong notebook"""
    async def _artifacts():
        from ..integrations import NotebookLMIntegration
        from ..utils.output import print_error
        
        try:
            async with NotebookLMIntegration() as nlm:
                artifacts = await nlm.list_artifacts(notebook_id)
                
                if output_json:
                    import json
                    click.echo(json.dumps(artifacts, indent=2, ensure_ascii=False))
                else:
                    if not artifacts:
                        click.echo("🎨 Không có artifact nào")
                    else:
                        click.echo(f"🎨 Có {len(artifacts)} artifact:")
                        for art in artifacts:
                            status_icon = "✅" if art['is_completed'] else "⏳"  # Sử dụng is_completed
                            click.echo(f"  {status_icon} {art['type']}: {art['title']} (ID: {art['id'][:8]}...)")
                    
        except Exception as e:
            print_error(f"Không thể liệt kê artifacts: {e}")
    
    asyncio.run(_artifacts())


@notebook_group.command()
@click.argument('notebook_id')
@click.argument('source_id')
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
@click.pass_context
def fulltext(ctx, notebook_id: str, source_id: str, output_json: bool):
    """Lấy nội dung đầy đủ của nguồn"""
    async def _fulltext():
        from ..integrations import NotebookLMIntegration
        from ..utils.output import print_error
        
        try:
            async with NotebookLMIntegration() as nlm:
                fulltext = await nlm.get_source_fulltext(notebook_id, source_id)
                
                if output_json:
                    import json
                    click.echo(json.dumps(fulltext, indent=2, ensure_ascii=False))
                else:
                    click.echo(f"📄 {fulltext['title']}")
                    click.echo(f"📊 Độ dài: {fulltext['char_count']:,} ký tự")
                    click.echo("=" * 60)
                    click.echo(fulltext['content'][:2000] + "..." if len(fulltext['content']) > 2000 else fulltext['content'])
                    
        except Exception as e:
            print_error(f"Không thể lấy nội dung nguồn: {e}")
    
    asyncio.run(_fulltext())


@notebook_group.command()
@click.argument('notebook_id')
@click.option('--confirm', is_flag=True, help='Xác nhận xóa')
@click.option('--force', '-f', is_flag=True, help='Xóa ngay không cần xác nhận')
@click.pass_context
def delete(ctx, notebook_id: str, confirm: bool, force: bool):
    """Xóa notebook"""
    async def _delete():
        from ..integrations import NotebookLMIntegration
        from ..utils.output import print_success, print_error
        
        if not confirm and not force:
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


@notebook_group.command()
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
@click.pass_context
def languages(ctx, output_json: bool):
    """Liệt kê ngôn ngữ được hỗ trợ"""
    async def _languages():
        from ..integrations import NotebookLMIntegration
        from ..utils.output import print_error
        
        try:
            async with NotebookLMIntegration() as nlm:
                languages = await nlm.list_supported_languages()
                current_lang = await nlm.get_language()
                
                if output_json:
                    import json
                    result = {"current": current_lang, "supported": languages}
                    click.echo(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    click.echo(f"🌐 Ngôn ngữ hiện tại: {current_lang}")
                    click.echo(f"📋 Có {len(languages)} ngôn ngữ được hỗ trợ:")
                    for lang in languages[:10]:  # Show first 10
                        marker = "→" if lang['code'] == current_lang else " "
                        click.echo(f"  {marker} {lang['code']}: {lang.get('native_name', lang['name'])}")
                    if len(languages) > 10:
                        click.echo(f"  ... và {len(languages) - 10} ngôn ngữ khác")
                    
        except Exception as e:
            print_error(f"Không thể liệt kê ngôn ngữ: {e}")
    
    asyncio.run(_languages())


@notebook_group.command()
@click.argument('language_code')
@click.pass_context
def set_language(ctx, language_code: str):
    """Đặt ngôn ngữ cho content generation"""
    async def _set_language():
        from ..integrations import NotebookLMIntegration
        from ..utils.output import print_success, print_error
        
        try:
            async with NotebookLMIntegration() as nlm:
                success = await nlm.set_language(language_code)
                
                if success:
                    print_success(f"Đã đặt ngôn ngữ: {language_code}")
                else:
                    print_error("Không thể đặt ngôn ngữ")
                    
        except Exception as e:
            print_error(f"Lỗi đặt ngôn ngữ: {e}")
    
    asyncio.run(_set_language())


@notebook_group.command()
@click.argument('notebook_id')
@click.option('--public', is_flag=True, help='Chia sẻ công khai với bất kỳ ai có link')
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
@click.pass_context
def share(ctx, notebook_id: str, public: bool, output_json: bool):
    """Chia sẻ notebook và lấy link công khai"""
    async def _share():
        from ..integrations import NotebookLMIntegration
        from ..utils.output import print_success, print_error
        
        try:
            async with NotebookLMIntegration() as nlm:
                access_level = "anyone_with_link" if public else "restricted"
                result = await nlm.share_notebook(notebook_id, access_level)
                
                if output_json:
                    import json
                    click.echo(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    if result['success']:
                        print_success("Notebook đã được chia sẻ!")
                        if result.get('share_link'):
                            click.echo(f"🔗 Link chia sẻ: {result['share_link']}")
                        click.echo(f"🔒 Quyền truy cập: {result['access_level']}")
                    else:
                        print_error(f"Không thể chia sẻ: {result.get('error', 'Unknown error')}")
                    
        except Exception as e:
            print_error(f"Lỗi chia sẻ notebook: {e}")
    
    asyncio.run(_share())


@notebook_group.command()
@click.argument('notebook_id')
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
@click.pass_context
def share_status(ctx, notebook_id: str, output_json: bool):
    """Kiểm tra trạng thái chia sẻ của notebook"""
    async def _share_status():
        from ..integrations import NotebookLMIntegration
        from ..utils.output import print_error
        
        try:
            async with NotebookLMIntegration() as nlm:
                status = await nlm.get_share_status(notebook_id)
                
                if output_json:
                    import json
                    click.echo(json.dumps(status, indent=2, ensure_ascii=False))
                else:
                    if status.get('is_shared'):
                        click.echo("✅ Notebook đang được chia sẻ")
                        if status.get('share_link'):
                            click.echo(f"🔗 Link: {status['share_link']}")
                        click.echo(f"🔒 Quyền: {status.get('access_level', 'Unknown')}")
                    else:
                        click.echo("🔒 Notebook chưa được chia sẻ")
                        if status.get('error'):
                            click.echo(f"⚠️  {status['error']}")
                    
        except Exception as e:
            print_error(f"Lỗi kiểm tra trạng thái: {e}")
    
    asyncio.run(_share_status())


@notebook_group.command()
@click.argument('notebook_id')
@click.option('--artifact-id', help='ID artifact cụ thể để export (optional)')
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
@click.pass_context
def export_docs(ctx, notebook_id: str, artifact_id: str, output_json: bool):
    """Export notebook hoặc artifact lên Google Docs"""
    async def _export_docs():
        from ..integrations import NotebookLMIntegration
        from ..utils.output import print_success, print_error
        
        try:
            async with NotebookLMIntegration() as nlm:
                result = await nlm.export_to_docs(notebook_id, artifact_id)
                
                if output_json:
                    import json
                    click.echo(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    if result['success']:
                        print_success("✅ Export thành công lên Google Docs!")
                        if result.get('docs_link'):
                            click.echo(f"📄 Link Google Docs: {result['docs_link']}")
                    else:
                        print_error(f"❌ Export thất bại: {result.get('error', 'Unknown error')}")
                    
        except Exception as e:
            print_error(f"Lỗi export: {e}")
    
    asyncio.run(_export_docs())


@notebook_group.command()
@click.argument('notebook_id')
@click.option('--artifact-id', help='ID artifact cụ thể để export (optional)')
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
@click.pass_context
def export_sheets(ctx, notebook_id: str, artifact_id: str, output_json: bool):
    """Export dữ liệu notebook lên Google Sheets"""
    async def _export_sheets():
        from ..integrations import NotebookLMIntegration
        from ..utils.output import print_success, print_error
        
        try:
            async with NotebookLMIntegration() as nlm:
                result = await nlm.export_to_sheets(notebook_id, artifact_id)
                
                if output_json:
                    import json
                    click.echo(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    if result['success']:
                        print_success("✅ Export thành công lên Google Sheets!")
                        if result.get('sheets_link'):
                            click.echo(f"📊 Link Google Sheets: {result['sheets_link']}")
                    else:
                        print_error(f"❌ Export thất bại: {result.get('error', 'Unknown error')}")
                    
        except Exception as e:
            print_error(f"Lỗi export: {e}")
    
    asyncio.run(_export_sheets())