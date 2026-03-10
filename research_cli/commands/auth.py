"""
Authentication commands - Xử lý đăng nhập NotebookLM
"""

import click
import asyncio
from pathlib import Path


@click.command()
def login():
    """Đăng nhập tài khoản Google để sử dụng NotebookLM"""
    async def _login_process():
        from playwright.async_api import async_playwright
        from ..utils.output import print_success, print_error, print_info
        
        # Đường dẫn mặc định mà thư viện notebooklm-py sử dụng
        storage_dir = Path.home() / '.notebooklm'
        storage_dir.mkdir(parents=True, exist_ok=True)
        storage_path = storage_dir / 'storage_state.json'
        
        print_info("🌐 Đang mở trình duyệt. Vui lòng đăng nhập tài khoản Google của bạn...")
        print_info("⚠️  Lưu ý: Không đóng terminal trong quá trình này.")
        
        try:
            async with async_playwright() as p:
                # Khởi chạy trình duyệt có giao diện (headless=False)
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()
                
                # Đi tới trang NotebookLM
                await page.goto("https://notebooklm.google.com/")
                
                # Chờ người dùng đăng nhập và trang tải xong
                click.echo("\n👉 Khi bạn đã thấy màn hình chính của NotebookLM, hãy quay lại đây.")
                click.pause(info="Nhấn phím BẤT KỲ để lưu phiên đăng nhập và đóng trình duyệt...")
                
                # Lưu cookie và state lại cho thư viện notebooklm-py sử dụng
                await context.storage_state(path=str(storage_path))
                await browser.close()
                
                print_success(f"✅ Đăng nhập thành công! Phiên đã được lưu tại: {storage_path}")
                print_success("Bây giờ bạn có thể sử dụng các lệnh: research-cli pipeline ...")
                
        except Exception as e:
            print_error(f"Lỗi trong quá trình đăng nhập: {e}")
            print_info("💡 Hãy đảm bảo bạn đã cài đặt: pip install playwright && playwright install chromium")
    
    asyncio.run(_login_process())


@click.command()
def logout():
    """Đăng xuất và xóa phiên đăng nhập"""
    from ..utils.output import print_success, print_error, print_info
    
    storage_dir = Path.home() / '.notebooklm'
    storage_path = storage_dir / 'storage_state.json'
    
    try:
        if storage_path.exists():
            storage_path.unlink()
            print_success("✅ Đã đăng xuất và xóa phiên đăng nhập")
        else:
            print_info("ℹ️  Chưa có phiên đăng nhập nào để xóa")
    except Exception as e:
        print_error(f"Lỗi khi đăng xuất: {e}")


@click.command()
def status():
    """Kiểm tra trạng thái đăng nhập"""
    from ..utils.output import print_success, print_error, print_info
    
    storage_dir = Path.home() / '.notebooklm'
    storage_path = storage_dir / 'storage_state.json'
    
    if storage_path.exists():
        try:
            import json
            with open(storage_path, 'r') as f:
                data = json.load(f)
            
            # Kiểm tra xem có cookies không
            cookies = data.get('cookies', [])
            if cookies:
                print_success("✅ Đã đăng nhập NotebookLM")
                print_info(f"📁 File phiên: {storage_path}")
                print_info(f"🍪 Số cookies: {len(cookies)}")
            else:
                print_error("❌ File phiên tồn tại nhưng không có cookies hợp lệ")
                print_info("💡 Hãy chạy: research-cli login")
        except Exception as e:
            print_error(f"❌ File phiên bị lỗi: {e}")
            print_info("💡 Hãy chạy: research-cli login")
    else:
        print_error("❌ Chưa đăng nhập")
        print_info("💡 Hãy chạy: research-cli login")