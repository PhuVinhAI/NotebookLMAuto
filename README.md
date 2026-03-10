# Research CLI - YouTube Search & NotebookLM Integration

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/research-cli/research-cli)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Công cụ dòng lệnh chuyên nghiệp để tìm kiếm YouTube, phân tích video và tích hợp với NotebookLM. Được xây dựng với kiến trúc doanh nghiệp để mở rộng và bảo trì dễ dàng.

## 🚀 Tính năng chính

### Khả năng cốt lõi
- **Pipeline tự động**: Workflow hoàn chỉnh từ YouTube đến NotebookLM
- **Tìm kiếm nâng cao**: Tìm kiếm đa tiêu chí với bộ lọc thông minh
- **Phân tích video**: Trích xuất metadata chi tiết
- **Xuất dữ liệu**: Nhiều định dạng (JSON, CSV, URLs)
- **Tích hợp NotebookLM**: Tạo nội dung tự động (podcast, quiz, infographic, video)

### Tính năng chuyên nghiệp
- **Kiến trúc doanh nghiệp**: Codebase modular, có thể mở rộng
- **Bộ lọc nâng cao**: Lượt xem, thời lượng, ngày tháng, năm, kênh
- **Sắp xếp thông minh**: Nhiều thuật toán sắp xếp
- **Xử lý hàng loạt**: Xử lý dataset lớn hiệu quả
- **Xử lý lỗi**: Khôi phục lỗi mạnh mẽ và logging

## 📦 Cài đặt

### Cài đặt nhanh
```bash
pip install yt-dlp click requests notebooklm-py
```

### Cài đặt NotebookLM (tùy chọn)
```bash
# Cài đặt với hỗ trợ browser login
pip install "notebooklm-py[browser]"
playwright install chromium

# Đăng nhập NotebookLM
notebooklm login
notebooklm skill install
```

### Cài đặt development
```bash
git clone https://github.com/research-cli/research-cli.git
cd research-cli
pip install -e .
```

## 🎯 Bắt đầu nhanh

### Pipeline hoàn chỉnh (Khuyến nghị)
```bash
# Workflow như yêu cầu: YouTube → NotebookLM → Analysis → Infographic
python -m research_cli pipeline "AI tools for digital marketing content creation" \
  -n 5 --min-views 100000 -g infographic \
  -q "What are the biggest trends in AI for business and content creation?"
```

### Tìm kiếm cơ bản
```bash
python -m research_cli search "AI tools for business" -n 5 --min-views 50000
```

### Tìm video theo năm
```bash
python -m research_cli search "AI trends" --year 2024 --min-views 100000
```

### Xuất URLs cho NotebookLM
```bash
python -m research_cli export "AI trends 2026" --format urls -o ai_videos.txt
```

## 📋 Tham khảo lệnh

### Pipeline Command (Khuyến nghị sử dụng)
```bash
python -m research_cli pipeline "query" [OPTIONS]

Options:
  -t, --notebook-title TEXT     Tiêu đề notebook (tự động nếu không có)
  -n, --max-videos INTEGER      Số video tối đa (default: 5)
  -m, --min-views INTEGER       Lượt xem tối thiểu (default: 50000)
  --year INTEGER                Lọc theo năm (VD: 2024)
  -s, --sort-by [views|date|relevance]  Sắp xếp theo
  -g, --generate [podcast|quiz|infographic|video|slides|report|mindmap]
                                Tạo nội dung (có thể chọn nhiều)
  -q, --question TEXT           Câu hỏi phân tích cụ thể
  -o, --output-dir TEXT         Thư mục lưu file (default: .)
  --json                        Xuất kết quả dạng JSON
```

### Search Command
```bash
python -m research_cli search "query" [OPTIONS]

Options:
  -n, --max-results INTEGER     Số kết quả (default: 10)
  -s, --sort-by [relevance|views|date|duration|title|channel]
  -m, --min-views INTEGER       Lượt xem tối thiểu
  --max-views INTEGER           Lượt xem tối đa
  --min-duration INTEGER        Thời lượng tối thiểu (giây)
  --max-duration INTEGER        Thời lượng tối đa (giây)
  --days-ago INTEGER            Video trong N ngày qua
  --year INTEGER                Lọc theo năm (VD: 2024)
  --after-date TEXT             Video sau ngày này (YYYY-MM-DD)
  --before-date TEXT            Video trước ngày này (YYYY-MM-DD)
  --channels TEXT               Lọc theo kênh (phân cách bằng dấu phẩy)
  --json                        Xuất kết quả dạng JSON
  -v, --verbose                 Hiển thị thông tin chi tiết
```

### Export Command
```bash
python -m research_cli export "query" [OPTIONS]

Options:
  --format [urls|json|csv]      Định dạng xuất (default: urls)
  -o, --output TEXT             File đầu ra
  -n, --max-results INTEGER     Số video (default: 10)
  --sort-by [views|date|duration|relevance]
  -m, --min-views INTEGER       Lượt xem tối thiểu
  --year INTEGER                Lọc theo năm
```

### NotebookLM Commands
```bash
# Quản lý notebook
python -m research_cli notebook create "Research Title"
python -m research_cli notebook list
python -m research_cli notebook sources NOTEBOOK_ID
python -m research_cli notebook ask NOTEBOOK_ID "question"
python -m research_cli notebook delete NOTEBOOK_ID

# Tạo nội dung
python -m research_cli generate podcast NOTEBOOK_ID -o podcast.mp3
python -m research_cli generate quiz NOTEBOOK_ID -d medium -o quiz.json
python -m research_cli generate infographic NOTEBOOK_ID -o infographic.png
python -m research_cli generate video NOTEBOOK_ID -o video.mp4
python -m research_cli generate slides NOTEBOOK_ID -o slides.pdf
python -m research_cli generate report NOTEBOOK_ID -f briefing-doc -o report.md
python -m research_cli generate mindmap NOTEBOOK_ID -o mindmap.json
```

## 🔧 Ví dụ sử dụng

### Workflow nghiên cứu hoàn chỉnh
```bash
# Nghiên cứu AI tools với nhiều nội dung
python -m research_cli pipeline "AI business tools 2024" \
  --year 2024 \
  --min-views 100000 \
  -n 5 \
  -g podcast -g quiz -g infographic \
  -q "What are the most practical AI tools for small businesses?"
```

### Tìm kiếm nâng cao
```bash
# Tìm tutorial chất lượng cao gần đây
python -m research_cli search "Python machine learning" \
  --min-views 50000 \
  --min-duration 600 \
  --year 2024 \
  --sort-by views \
  -n 10
```

### Xuất dữ liệu cho phân tích
```bash
# Xuất CSV để phân tích
python -m research_cli export "digital marketing trends 2024" \
  --format csv \
  --min-views 100000 \
  --year 2024 \
  -o marketing_analysis.csv
```

### Workflow thủ công (linh hoạt)
```bash
# 1. Tìm và xuất URLs
python -m research_cli export "AI content creation" \
  --format urls --min-views 50000 -n 5 -o videos.txt

# 2. Tạo notebook
python -m research_cli notebook create "AI Content Research"

# 3. Thêm sources (cần notebook ID từ bước 2)
python -m research_cli notebook add-sources NOTEBOOK_ID $(cat videos.txt)

# 4. Phân tích
python -m research_cli notebook ask NOTEBOOK_ID "What are the main trends?"

# 5. Tạo nội dung
python -m research_cli generate infographic NOTEBOOK_ID -o trends.png
```

## 🏗️ Kiến trúc dự án

### Cấu trúc thư mục
```
research_cli/
├── __init__.py              # Package initialization
├── main.py                  # CLI entry point
├── commands/                # CLI commands
│   ├── __init__.py
│   ├── search.py           # Tìm kiếm YouTube
│   ├── info.py             # Thông tin video
│   ├── export.py           # Xuất dữ liệu
│   ├── notebook.py         # Quản lý NotebookLM
│   ├── generate.py         # Tạo nội dung
│   └── pipeline.py         # Workflow tự động
├── core/                    # Core functionality
│   ├── __init__.py
│   ├── youtube_client.py   # YouTube client
│   ├── filters.py          # Bộ lọc video
│   └── sorters.py          # Thuật toán sắp xếp
├── integrations/           # Tích hợp bên ngoài
│   ├── __init__.py
│   ├── notebooklm_client.py    # NotebookLM client
│   └── content_generators.py   # Tạo nội dung
└── utils/                  # Tiện ích
    ├── __init__.py
    └── output.py           # Định dạng output
```

## 📊 Định dạng output

### JSON Output
```json
{
  "title": "AI Tools That Will Change Business in 2026",
  "uploader": "Tech Insights",
  "view_count": 1250000,
  "duration": 1820,
  "upload_date": "20241215",
  "url": "https://youtube.com/watch?v=...",
  "description": "Comprehensive guide to AI tools...",
  "tags": ["AI", "business", "automation"]
}
```

### Pipeline Results
```json
{
  "query": "AI tools for business",
  "notebook_id": "abc123...",
  "videos_found": 5,
  "videos_added": 5,
  "analysis_answer": "Key trends include...",
  "generated_content": {
    "infographic": "./AI_tools_infographic.png",
    "podcast": "./AI_tools_podcast.mp3"
  }
}
```

## 🚨 Xử lý lỗi

### Lỗi thường gặp

**Import Errors**
```bash
pip install --upgrade yt-dlp click requests notebooklm-py
```

**NotebookLM Authentication**
```bash
notebooklm login
notebooklm auth check
```

**API Extraction Failures**
```bash
pip install --upgrade yt-dlp
```

**Không tìm thấy kết quả**
- Thử từ khóa rộng hơn
- Giảm tiêu chí lọc
- Kiểm tra kết nối internet

### Debug Mode
```bash
python -m research_cli search "query" --verbose
```

## 🎯 Use Cases

### 1. Nghiên cứu thị trường
```bash
python -m research_cli pipeline "fintech trends 2024" \
  --year 2024 -n 10 -g report -g mindmap \
  -q "What are the emerging fintech trends?"
```

### 2. Tạo nội dung giáo dục
```bash
python -m research_cli pipeline "machine learning basics" \
  -n 5 -g quiz -g slides \
  -q "Create educational content for beginners"
```

### 3. Phân tích đối thủ
```bash
python -m research_cli pipeline "competitor marketing strategies" \
  --min-views 100000 -g infographic \
  -q "Analyze competitor marketing approaches"
```

## 🤝 Đóng góp

Chúng tôi hoan nghênh đóng góp! Vui lòng xem [Contributing Guide](CONTRIBUTING.md).

### Development Setup
```bash
git clone https://github.com/research-cli/research-cli.git
cd research-cli
pip install -e ".[dev]"
pytest tests/
```

## 📄 License

Dự án này được cấp phép theo MIT License - xem file [LICENSE](LICENSE).

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube data extraction
- [Click](https://click.palletsprojects.com/) - CLI framework
- [NotebookLM](https://notebooklm.google.com/) - AI research platform
- [notebooklm-py](https://github.com/teng-lin/notebooklm-py) - Python API

---

**Được tạo với ❤️ cho các nhà nghiên cứu, marketer và content creator**