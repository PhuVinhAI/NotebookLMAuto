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
                # CÁC THAM SỐ ANTI-BOT ĐỂ QUA MẶT GOOGLE
                browser = await p.chromium.launch(
                    headless=False,
                    args=[
                        "--disable-blink-features=AutomationControlled",  # Tắt cờ báo hiệu bot
                        "--start-maximized"
                    ],
                    ignore_default_args=["--enable-automation"]  # Ẩn dòng chữ "Chrome is being controlled..."
                )
                
                # Cấu hình User-Agent giống hệt người dùng thật
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                    viewport={"width": 1280, "height": 720}
                )
                
                # Chặn thuộc tính webdriver bằng script khởi tạo
                await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                page = await context.new_page()
                
                # Đi tới trang NotebookLM
                await page.goto("https://notebooklm.google.com/")
                
                # Chờ người dùng đăng nhập
                click.echo("\n👉 Khi bạn đã đăng nhập thành công và thấy màn hình chính của NotebookLM...")
                click.pause(info="Nhấn phím ENTER tại đây để lưu phiên và đóng trình duyệt...")
                
                # Kiểm tra xem có lấy được cookie cần thiết chưa (tuỳ chọn)
                cookies = await context.cookies()
                has_auth = any(c['name'] == 'SID' or c['name'] == 'HSID' for c in cookies)
                if not has_auth:
                    print_info("⚠️ Có vẻ bạn chưa đăng nhập thành công (hoặc chưa lưu đủ cookie). Vẫn tiếp tục lưu file...")
                
                # Lưu cookie và state lại cho thư viện notebooklm-py sử dụng
                await context.storage_state(path=str(storage_path))
                await browser.close()
                
                print_success(f"✅ Đã lưu phiên đăng nhập tại: {storage_path}")
                print_success("Bây giờ bạn có thể sử dụng các lệnh của CLI.")
                
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