"""
Main CLI entry point for Research CLI Tool
"""

import click
import logging

from .commands.search import search_command
from .commands.info import info_command
from .commands.notebook import notebook_group
from .commands.generate import generate_group
from .commands.export import export_command
from .commands.pipeline import pipeline
from .commands.auth import login, logout, status
from .__init__ import __version__


def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


@click.group()
@click.version_option(version=__version__, prog_name="research-cli")
@click.option('--verbose', '-v', is_flag=True, help='Bật chế độ verbose')
@click.pass_context
def cli(ctx, verbose: bool):
    """Research CLI Tool - YouTube Search & NotebookLM Integration
    
    Công cụ nghiên cứu chuyên nghiệp kết hợp YouTube và NotebookLM
    
    🚀 Bắt đầu nhanh:
      research-cli login                    # Đăng nhập Google/NotebookLM
      research-cli status                   # Kiểm tra trạng thái đăng nhập
      research-cli pipeline "AI tools"      # Chạy pipeline nghiên cứu tự động
    
    📚 Các lệnh chính:
      research-cli search "AI tools" --min-views 100000
      research-cli notebook create "My Research"
      research-cli notebook share <id> --public
      research-cli generate podcast <notebook-id>
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    setup_logging(verbose)


# Register all command groups
cli.add_command(login, name='login')
cli.add_command(logout, name='logout') 
cli.add_command(status, name='status')
cli.add_command(search_command, name='search')
cli.add_command(info_command, name='info')
cli.add_command(notebook_group, name='notebook')
cli.add_command(generate_group, name='generate')
cli.add_command(export_command, name='export')
cli.add_command(pipeline, name='pipeline')


if __name__ == '__main__':
    cli()