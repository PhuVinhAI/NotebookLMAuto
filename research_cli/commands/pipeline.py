"""
Research pipeline command - Workflow tự động từ YouTube đến NotebookLM
"""

import click
import asyncio
from typing import Optional, List


@click.command()
@click.argument('query')
@click.option('--notebook-title', '-t', help='Tiêu đề notebook (tự động nếu không có)')
@click.option('--max-videos', '-n', default=5, help='Số video tối đa')
@click.option('--min-views', '-m', default=50000, help='Lượt xem tối thiểu')
@click.option('--year', type=int, help='Lọc theo năm (VD: 2024)')
@click.option('--sort-by', '-s', default='views', 
              type=click.Choice(['views', 'date', 'relevance']), help='Sắp xếp theo')
@click.option('--generate', '-g', multiple=True,
              type=click.Choice(['podcast', 'quiz', 'infographic', 'video', 'slides', 'report', 'mindmap']),
              help='Tạo nội dung (có thể chọn nhiều)')
@click.option('--question', '-q', help='Câu hỏi phân tích cụ thể')
@click.option('--output-dir', '-o', default='.', help='Thư mục lưu file')
@click.option('--json', 'output_json', is_flag=True, help='Xuất kết quả dạng JSON')
@click.pass_context
def pipeline(ctx, query: str, notebook_title: Optional[str], max_videos: int, 
            min_views: int, year: Optional[int], sort_by: str, generate: tuple,
            question: Optional[str], output_dir: str, output_json: bool):
    """Pipeline nghiên cứu hoàn chỉnh: YouTube → NotebookLM → Analysis → Content
    
    Examples:
      # Nghiên cứu cơ bản
      research-cli pipeline "AI tools for business" -n 5 -g infographic
      
      # Nghiên cứu chi tiết với nhiều content
      research-cli pipeline "digital marketing AI 2024" --year 2024 \\
        -g podcast -g quiz -g infographic -q "What are the main trends?"
      
      # Workflow như yêu cầu
      research-cli pipeline "AI tools for digital marketing content creation" \\
        -n 5 --min-views 100000 -g infographic \\
        -q "What are the biggest trends in AI for business and content creation?"
    """
    async def _pipeline():
        from ..core import YouTubeClient, VideoFilter, VideoSorter
        from ..integrations import NotebookLMIntegration, ContentGenerators
        from ..utils.output import print_success, print_error, print_info
        import json
        import os
        
        results = {
            "query": query,
            "notebook_id": None,
            "videos_found": 0,
            "videos_added": 0,
            "analysis_answer": None,
            "generated_content": {}
        }
        
        try:
            # Step 1: Search YouTube videos
            print_info(f"🔍 Tìm kiếm YouTube: {query}")
            client = YouTubeClient()
            videos = client.search_videos(query, max_results=max_videos * 2)
            
            if not videos:
                print_error("Không tìm thấy video nào")
                return
            
            # Apply filters
            if min_views > 0:
                videos = VideoFilter.by_view_count(videos, min_views=min_views)
            
            if year:
                after_date = f"{year}-01-01"
                before_date = f"{year}-12-31"
                videos = VideoFilter.by_upload_date(videos, after_date=after_date, before_date=before_date)
            
            # Sort and limit
            videos = VideoSorter.sort_videos(videos, sort_by, reverse=True)
            videos = videos[:max_videos]
            
            if not videos:
                print_error("Không có video nào sau khi lọc")
                return
            
            results["videos_found"] = len(videos)
            video_urls = [v['url'] for v in videos]
            
            print_success(f"✅ Tìm thấy {len(videos)} video chất lượng cao")
            for i, video in enumerate(videos, 1):
                views = video['view_count']
                formatted_views = f"{views/1000000:.1f}M" if views >= 1000000 else f"{views/1000:.1f}K"
                print(f"  {i}. {video['title']} - {formatted_views} views")
            
            # Step 2: Create NotebookLM notebook
            print_info("📓 Tạo notebook NotebookLM...")
            if not notebook_title:
                notebook_title = f"Research: {query}"
            
            async with NotebookLMIntegration() as nlm:
                notebook_id = await nlm.create_research_notebook(notebook_title)
                results["notebook_id"] = notebook_id
                print_success(f"Đã tạo notebook: {notebook_title}")
                
                # Step 3: Add YouTube sources
                print_info("📹 Thêm video làm nguồn...")
                source_ids = await nlm.add_youtube_sources(notebook_id, video_urls, wait_for_processing=True)
                results["videos_added"] = len(source_ids)
                print_success(f"Đã thêm {len(source_ids)} video vào notebook")
                
                # Step 4: Analysis question
                analysis_question = question or f"Phân tích các xu hướng chính về {query}. Tóm tắt những insight quan trọng nhất."
                print_info(f"🤔 Phân tích: {analysis_question}")
                
                answer = await nlm.research_query(notebook_id, analysis_question)
                results["analysis_answer"] = answer
                
                if not output_json:
                    print_success("💡 KẾT QUẢ PHÂN TÍCH:")
                    print("=" * 60)
                    print(answer)
                    print("=" * 60)
                
                # Step 5: Generate content
                if generate:
                    content_gen = ContentGenerators(nlm.client)
                    print_info(f"🎨 Tạo nội dung: {', '.join(generate)}")
                    
                    for content_type in generate:
                        try:
                            filename = os.path.join(output_dir, f"{query.replace(' ', '_')}_{content_type}")
                            
                            if content_type == 'podcast':
                                filename += '.mp3'
                                instructions = f"Tạo podcast thú vị về {query}, tập trung vào các xu hướng chính"
                                success = await content_gen.generate_podcast(notebook_id, instructions, filename)
                            
                            elif content_type == 'quiz':
                                filename += '.json'
                                success = await content_gen.generate_quiz(notebook_id, 'medium', filename)
                            
                            elif content_type == 'infographic':
                                filename += '.png'
                                instructions = f"Tạo infographic blueprint-style về các xu hướng {query}"
                                success = await content_gen.generate_infographic(notebook_id, instructions, filename)
                            
                            elif content_type == 'video':
                                filename += '.mp4'
                                instructions = f"Tạo video giải thích về {query} và các xu hướng chính"
                                success = await content_gen.generate_video(notebook_id, instructions, filename)
                            
                            elif content_type == 'slides':
                                filename += '.pdf'
                                instructions = f"Tạo slide deck tổng hợp về {query}"
                                success = await content_gen.generate_slide_deck(notebook_id, instructions, filename)
                            
                            elif content_type == 'report':
                                filename += '.md'
                                success = await content_gen.generate_report(notebook_id, 'briefing-doc', filename)
                            
                            elif content_type == 'mindmap':
                                filename += '.json'
                                success = await content_gen.generate_mind_map(notebook_id, filename)
                            
                            if success:
                                results["generated_content"][content_type] = filename
                                print_success(f"  ✅ {content_type}: {filename}")
                            else:
                                print_error(f"  ❌ Không thể tạo {content_type}")
                                
                        except Exception as e:
                            print_error(f"  ❌ Lỗi tạo {content_type}: {e}")
            
            # Final output
            if output_json:
                print(json.dumps(results, indent=2, ensure_ascii=False))
            else:
                print_success("\n🎉 HOÀN THÀNH PIPELINE!")
                print(f"📓 Notebook ID: {results['notebook_id']}")
                print(f"📹 Videos analyzed: {results['videos_added']}")
                if results['generated_content']:
                    print("🎨 Nội dung đã tạo:")
                    for content_type, filename in results['generated_content'].items():
                        print(f"  • {content_type}: {filename}")
                        
        except Exception as e:
            print_error(f"Pipeline thất bại: {e}")
            if output_json:
                results["error"] = str(e)
                print(json.dumps(results, indent=2, ensure_ascii=False))
    
    asyncio.run(_pipeline())