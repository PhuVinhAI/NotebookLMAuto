"""
Content generation commands
"""

import click
import asyncio
from typing import Optional


@click.group()
def generate_group():
    """Content generation commands"""
    pass


@generate_group.command()
@click.argument('notebook_id')
@click.option('--instructions', '-i', help='Hướng dẫn tùy chỉnh cho podcast')
@click.option('--format', '-f', default='deep-dive',
              type=click.Choice(['deep-dive', 'brief', 'critique', 'debate']),
              help='Định dạng podcast')
@click.option('--length', '-l', default='default',
              type=click.Choice(['short', 'default', 'long']),
              help='Độ dài podcast')
@click.option('--language', help='Ngôn ngữ đầu ra (VD: vi, en, zh_Hans)')
@click.option('--sources', '-s', multiple=True, help='Source IDs cụ thể')
@click.option('--output', '-o', default='podcast.mp3', help='Tên file đầu ra')
@click.pass_context
def podcast(ctx, notebook_id: str, instructions: Optional[str], format: str, 
           length: str, language: Optional[str], sources: tuple, output: str):
    """Tạo podcast từ notebook"""
    async def _generate():
        from ..integrations import NotebookLMIntegration, ContentGenerators
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with NotebookLMIntegration() as nlm:
                content_gen = ContentGenerators(nlm.client)
                
                print_info("Đang tạo podcast... (có thể mất 10-20 phút)")
                
                source_ids = list(sources) if sources else None
                result = await content_gen.generate_podcast(
                    notebook_id, instructions, format, length, language, source_ids, output
                )
                
                if result['success']:
                    print_success(f"Podcast đã được tạo: {result['file']}")
                else:
                    print_error(f"Không thể tạo podcast: {result.get('error', 'Unknown error')}")
                    
        except Exception as e:
            print_error(f"Lỗi tạo podcast: {e}")
    
    asyncio.run(_generate())


@generate_group.command()
@click.argument('notebook_id')
@click.option('--difficulty', '-d', default='medium', 
              type=click.Choice(['easy', 'medium', 'hard']), help='Độ khó quiz')
@click.option('--quantity', '-q', default='standard',
              type=click.Choice(['fewer', 'standard', 'more']), help='Số lượng câu hỏi')
@click.option('--language', help='Ngôn ngữ đầu ra')
@click.option('--sources', '-s', multiple=True, help='Source IDs cụ thể')
@click.option('--output', '-o', default='quiz.json', help='Tên file đầu ra')
@click.option('--format', '-f', default='json',
              type=click.Choice(['json', 'markdown', 'html']), help='Định dạng đầu ra')
@click.pass_context
def quiz(ctx, notebook_id: str, difficulty: str, quantity: str, language: Optional[str],
         sources: tuple, output: str, format: str):
    """Tạo quiz từ notebook"""
    async def _generate():
        from ..integrations import NotebookLMIntegration, ContentGenerators
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with NotebookLMIntegration() as nlm:
                content_gen = ContentGenerators(nlm.client)
                
                print_info("Đang tạo quiz...")
                
                source_ids = list(sources) if sources else None
                result = await content_gen.generate_quiz(
                    notebook_id, difficulty, quantity, language, source_ids, output, format
                )
                
                if result['success']:
                    print_success(f"Quiz đã được tạo: {result['file']}")
                else:
                    print_error(f"Không thể tạo quiz: {result.get('error', 'Unknown error')}")
                    
        except Exception as e:
            print_error(f"Lỗi tạo quiz: {e}")
    
    asyncio.run(_generate())


@generate_group.command()
@click.argument('notebook_id')
@click.option('--difficulty', '-d', default='medium', 
              type=click.Choice(['easy', 'medium', 'hard']), help='Độ khó flashcards')
@click.option('--quantity', '-q', default='standard',
              type=click.Choice(['fewer', 'standard', 'more']), help='Số lượng thẻ')
@click.option('--language', help='Ngôn ngữ đầu ra')
@click.option('--sources', '-s', multiple=True, help='Source IDs cụ thể')
@click.option('--output', '-o', default='flashcards.json', help='Tên file đầu ra')
@click.option('--format', '-f', default='json',
              type=click.Choice(['json', 'markdown', 'html']), help='Định dạng đầu ra')
@click.pass_context
def flashcards(ctx, notebook_id: str, difficulty: str, quantity: str, language: Optional[str],
              sources: tuple, output: str, format: str):
    """Tạo flashcards từ notebook"""
    async def _generate():
        from ..integrations import NotebookLMIntegration, ContentGenerators
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with NotebookLMIntegration() as nlm:
                content_gen = ContentGenerators(nlm.client)
                
                print_info("Đang tạo flashcards...")
                
                source_ids = list(sources) if sources else None
                result = await content_gen.generate_flashcards(
                    notebook_id, difficulty, quantity, language, source_ids, output, format
                )
                
                if result['success']:
                    print_success(f"Flashcards đã được tạo: {result['file']}")
                else:
                    print_error(f"Không thể tạo flashcards: {result.get('error', 'Unknown error')}")
                    
        except Exception as e:
            print_error(f"Lỗi tạo flashcards: {e}")
    
    asyncio.run(_generate())


@generate_group.command()
@click.argument('notebook_id')
@click.option('--instructions', '-i', help='Hướng dẫn tùy chỉnh cho infographic')
@click.option('--orientation', default='landscape',
              type=click.Choice(['landscape', 'portrait', 'square']), help='Hướng infographic')
@click.option('--detail', default='standard',
              type=click.Choice(['concise', 'standard', 'detailed']), help='Mức độ chi tiết')
@click.option('--language', help='Ngôn ngữ đầu ra')
@click.option('--sources', '-s', multiple=True, help='Source IDs cụ thể')
@click.option('--output', '-o', default='infographic.png', help='Tên file đầu ra')
@click.pass_context
def infographic(ctx, notebook_id: str, instructions: Optional[str], orientation: str,
               detail: str, language: Optional[str], sources: tuple, output: str):
    """Tạo infographic từ notebook"""
    async def _generate():
        from ..integrations import NotebookLMIntegration, ContentGenerators
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with NotebookLMIntegration() as nlm:
                content_gen = ContentGenerators(nlm.client)
                
                print_info("Đang tạo infographic...")
                
                source_ids = list(sources) if sources else None
                result = await content_gen.generate_infographic(
                    notebook_id, instructions, orientation, detail, language, source_ids, output
                )
                
                if result['success']:
                    print_success(f"Infographic đã được tạo: {result['file']}")
                else:
                    print_error(f"Không thể tạo infographic: {result.get('error', 'Unknown error')}")
                    
        except Exception as e:
            print_error(f"Lỗi tạo infographic: {e}")
    
    asyncio.run(_generate())


@generate_group.command()
@click.argument('notebook_id')
@click.option('--language', help='Ngôn ngữ đầu ra')
@click.option('--sources', '-s', multiple=True, help='Source IDs cụ thể')
@click.option('--output', '-o', default='mindmap.json', help='Tên file đầu ra')
@click.pass_context
def mindmap(ctx, notebook_id: str, language: Optional[str], sources: tuple, output: str):
    """Tạo mind map từ notebook"""
    async def _generate():
        from ..integrations import NotebookLMIntegration, ContentGenerators
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with NotebookLMIntegration() as nlm:
                content_gen = ContentGenerators(nlm.client)
                
                print_info("Đang tạo mind map...")
                
                source_ids = list(sources) if sources else None
                result = await content_gen.generate_mind_map(notebook_id, language, source_ids, output)
                
                if result['success']:
                    print_success(f"Mind map đã được tạo: {result['file']}")
                else:
                    print_error(f"Không thể tạo mind map: {result.get('error', 'Unknown error')}")
                    
        except Exception as e:
            print_error(f"Lỗi tạo mind map: {e}")
    
    asyncio.run(_generate())


@generate_group.command()
@click.argument('notebook_id')
@click.option('--instructions', '-i', help='Hướng dẫn tùy chỉnh cho video')
@click.option('--format', '-f', default='explainer',
              type=click.Choice(['explainer', 'brief']), help='Định dạng video')
@click.option('--style', default='auto',
              type=click.Choice(['auto', 'classic', 'whiteboard', 'kawaii', 'anime', 'watercolor', 'retro-print', 'heritage', 'paper-craft']),
              help='Phong cách video')
@click.option('--language', help='Ngôn ngữ đầu ra')
@click.option('--sources', '-s', multiple=True, help='Source IDs cụ thể')
@click.option('--output', '-o', default='video.mp4', help='Tên file đầu ra')
@click.pass_context
def video(ctx, notebook_id: str, instructions: Optional[str], format: str, style: str,
          language: Optional[str], sources: tuple, output: str):
    """Tạo video từ notebook"""
    async def _generate():
        from ..integrations import NotebookLMIntegration, ContentGenerators
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with NotebookLMIntegration() as nlm:
                content_gen = ContentGenerators(nlm.client)
                
                print_info("Đang tạo video... (có thể mất 15-45 phút)")
                
                source_ids = list(sources) if sources else None
                result = await content_gen.generate_video(
                    notebook_id, instructions, format, style, language, source_ids, output
                )
                
                if result['success']:
                    print_success(f"Video đã được tạo: {result['file']}")
                else:
                    print_error(f"Không thể tạo video: {result.get('error', 'Unknown error')}")
                    
        except Exception as e:
            print_error(f"Lỗi tạo video: {e}")
    
    asyncio.run(_generate())


@generate_group.command()
@click.argument('notebook_id')
@click.option('--instructions', '-i', help='Hướng dẫn tùy chỉnh cho slide deck')
@click.option('--format', '-f', default='detailed',
              type=click.Choice(['detailed', 'presenter']), help='Định dạng slide deck')
@click.option('--length', '-l', default='default',
              type=click.Choice(['default', 'short']), help='Độ dài slide deck')
@click.option('--language', help='Ngôn ngữ đầu ra')
@click.option('--sources', '-s', multiple=True, help='Source IDs cụ thể')
@click.option('--output', '-o', default='slides.pdf', help='Tên file đầu ra')
@click.option('--output-format', default='pdf',
              type=click.Choice(['pdf', 'pptx']), help='Định dạng file đầu ra')
@click.pass_context
def slides(ctx, notebook_id: str, instructions: Optional[str], format: str, length: str,
           language: Optional[str], sources: tuple, output: str, output_format: str):
    """Tạo slide deck từ notebook"""
    async def _generate():
        from ..integrations import NotebookLMIntegration, ContentGenerators
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with NotebookLMIntegration() as nlm:
                content_gen = ContentGenerators(nlm.client)
                
                print_info("Đang tạo slide deck...")
                
                source_ids = list(sources) if sources else None
                result = await content_gen.generate_slide_deck(
                    notebook_id, instructions, format, length, language, source_ids, output, output_format
                )
                
                if result['success']:
                    print_success(f"Slide deck đã được tạo: {result['file']}")
                else:
                    print_error(f"Không thể tạo slide deck: {result.get('error', 'Unknown error')}")
                    
        except Exception as e:
            print_error(f"Lỗi tạo slide deck: {e}")
    
    asyncio.run(_generate())


@generate_group.command()
@click.argument('notebook_id')
@click.option('--format', '-f', default='briefing-doc',
              type=click.Choice(['briefing-doc', 'study-guide', 'blog-post', 'custom']),
              help='Định dạng báo cáo')
@click.option('--append', help='Hướng dẫn bổ sung cho template')
@click.option('--language', help='Ngôn ngữ đầu ra')
@click.option('--sources', '-s', multiple=True, help='Source IDs cụ thể')
@click.option('--output', '-o', default='report.md', help='Tên file đầu ra')
@click.pass_context
def report(ctx, notebook_id: str, format: str, append: Optional[str], language: Optional[str],
           sources: tuple, output: str):
    """Tạo báo cáo từ notebook"""
    async def _generate():
        from ..integrations import NotebookLMIntegration, ContentGenerators
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with NotebookLMIntegration() as nlm:
                content_gen = ContentGenerators(nlm.client)
                
                print_info(f"Đang tạo báo cáo định dạng {format}...")
                
                source_ids = list(sources) if sources else None
                result = await content_gen.generate_report(
                    notebook_id, format, append, language, source_ids, output
                )
                
                if result['success']:
                    print_success(f"Báo cáo đã được tạo: {result['file']}")
                else:
                    print_error(f"Không thể tạo báo cáo: {result.get('error', 'Unknown error')}")
                    
        except Exception as e:
            print_error(f"Lỗi tạo báo cáo: {e}")
    
    asyncio.run(_generate())


@generate_group.command()
@click.argument('notebook_id')
@click.argument('description', help='Mô tả bảng dữ liệu cần tạo')
@click.option('--language', help='Ngôn ngữ đầu ra')
@click.option('--sources', '-s', multiple=True, help='Source IDs cụ thể')
@click.option('--output', '-o', default='data.csv', help='Tên file đầu ra')
@click.pass_context
def data_table(ctx, notebook_id: str, description: str, language: Optional[str],
              sources: tuple, output: str):
    """Tạo bảng dữ liệu từ notebook"""
    async def _generate():
        from ..integrations import NotebookLMIntegration, ContentGenerators
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with NotebookLMIntegration() as nlm:
                content_gen = ContentGenerators(nlm.client)
                
                print_info("Đang tạo bảng dữ liệu...")
                
                source_ids = list(sources) if sources else None
                result = await content_gen.generate_data_table(
                    notebook_id, description, language, source_ids, output
                )
                
                if result['success']:
                    print_success(f"Bảng dữ liệu đã được tạo: {result['file']}")
                else:
                    print_error(f"Không thể tạo bảng dữ liệu: {result.get('error', 'Unknown error')}")
                    
        except Exception as e:
            print_error(f"Lỗi tạo bảng dữ liệu: {e}")
    
    asyncio.run(_generate())


@generate_group.command()
@click.argument('notebook_id')
@click.argument('artifact_id', help='ID của slide deck cần chỉnh sửa')
@click.argument('slide_number', type=int, help='Số thứ tự slide (bắt đầu từ 0)')
@click.argument('prompt', help='Hướng dẫn chỉnh sửa slide')
@click.option('--output', '-o', help='Tên file đầu ra (tùy chọn)')
@click.pass_context
def revise_slide(ctx, notebook_id: str, artifact_id: str, slide_number: int, 
                prompt: str, output: Optional[str]):
    """Chỉnh sửa slide cụ thể trong slide deck"""
    async def _generate():
        from ..integrations import NotebookLMIntegration, ContentGenerators
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with NotebookLMIntegration() as nlm:
                content_gen = ContentGenerators(nlm.client)
                
                print_info(f"Đang chỉnh sửa slide {slide_number}...")
                
                result = await content_gen.revise_slide(
                    notebook_id, artifact_id, slide_number, prompt, output
                )
                
                if result['success']:
                    if result.get('file'):
                        print_success(f"Slide đã được chỉnh sửa và lưu: {result['file']}")
                    else:
                        print_success(f"Slide {slide_number} đã được chỉnh sửa trong artifact {artifact_id}")
                else:
                    print_error(f"Không thể chỉnh sửa slide: {result.get('error', 'Unknown error')}")
                    
        except Exception as e:
            print_error(f"Lỗi chỉnh sửa slide: {e}")
    
    asyncio.run(_generate())