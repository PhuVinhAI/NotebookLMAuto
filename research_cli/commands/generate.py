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
@click.option('--output', '-o', default='podcast.mp3', help='Tên file đầu ra')
@click.pass_context
def podcast(ctx, notebook_id: str, instructions: Optional[str], output: str):
    """Tạo podcast từ notebook"""
    async def _generate():
        from ..integrations import NotebookLMIntegration, ContentGenerators
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with NotebookLMIntegration() as nlm:
                content_gen = ContentGenerators(nlm.client)
                
                print_info("Đang tạo podcast... (có thể mất 10-20 phút)")
                success = await content_gen.generate_podcast(notebook_id, instructions, output)
                
                if success:
                    print_success(f"Podcast đã được tạo: {output}")
                else:
                    print_error("Không thể tạo podcast")
                    
        except Exception as e:
            print_error(f"Lỗi tạo podcast: {e}")
    
    asyncio.run(_generate())


@generate_group.command()
@click.argument('notebook_id')
@click.option('--difficulty', '-d', default='medium', 
              type=click.Choice(['easy', 'medium', 'hard']), help='Độ khó quiz')
@click.option('--output', '-o', default='quiz.json', help='Tên file đầu ra')
@click.pass_context
def quiz(ctx, notebook_id: str, difficulty: str, output: str):
    """Tạo quiz từ notebook"""
    async def _generate():
        from ..integrations import NotebookLMIntegration, ContentGenerators
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with NotebookLMIntegration() as nlm:
                content_gen = ContentGenerators(nlm.client)
                
                print_info("Đang tạo quiz...")
                success = await content_gen.generate_quiz(notebook_id, difficulty, output)
                
                if success:
                    print_success(f"Quiz đã được tạo: {output}")
                else:
                    print_error("Không thể tạo quiz")
                    
        except Exception as e:
            print_error(f"Lỗi tạo quiz: {e}")
    
    asyncio.run(_generate())


@generate_group.command()
@click.argument('notebook_id')
@click.option('--instructions', '-i', help='Hướng dẫn tùy chỉnh cho infographic')
@click.option('--output', '-o', default='infographic.png', help='Tên file đầu ra')
@click.pass_context
def infographic(ctx, notebook_id: str, instructions: Optional[str], output: str):
    """Tạo infographic từ notebook"""
    async def _generate():
        from ..integrations import NotebookLMIntegration, ContentGenerators
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with NotebookLMIntegration() as nlm:
                content_gen = ContentGenerators(nlm.client)
                
                print_info("Đang tạo infographic...")
                success = await content_gen.generate_infographic(notebook_id, instructions, output)
                
                if success:
                    print_success(f"Infographic đã được tạo: {output}")
                else:
                    print_error("Không thể tạo infographic")
                    
        except Exception as e:
            print_error(f"Lỗi tạo infographic: {e}")
    
    asyncio.run(_generate())


@generate_group.command()
@click.argument('notebook_id')
@click.option('--output', '-o', default='mindmap.json', help='Tên file đầu ra')
@click.pass_context
def mindmap(ctx, notebook_id: str, output: str):
    """Tạo mind map từ notebook"""
    async def _generate():
        from ..integrations import NotebookLMIntegration, ContentGenerators
        from ..utils.output import print_success, print_error, print_info
        
        try:
            async with NotebookLMIntegration() as nlm:
                content_gen = ContentGenerators(nlm.client)
                
                print_info("Đang tạo mind map...")
                success = await content_gen.generate_mind_map(notebook_id, output)
                
                if success:
                    print_success(f"Mind map đã được tạo: {output}")
                else:
                    print_error("Không thể tạo mind map")
                    
        except Exception as e:
            print_error(f"Lỗi tạo mind map: {e}")
    
    asyncio.run(_generate())