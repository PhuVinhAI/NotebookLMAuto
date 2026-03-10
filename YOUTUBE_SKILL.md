# YouTube Search Tool CLI

Complete programmatic access to YouTube search and video information using yt-dlp. Search videos, get detailed information, download subtitles, and export URLs for integration with other tools like NotebookLM.

## Installation

```bash
pip install yt-dlp click requests
```

## Prerequisites

**IMPORTANT:** The tool requires yt-dlp to be installed and updated:

```bash
pip install --upgrade yt-dlp
```

If commands fail with API errors, update yt-dlp to the latest version.

## When This Skill Activates

**Explicit:** User says "youtube search", "search youtube", "find youtube videos", or mentions the tool by name

**Intent detection:** Recognize requests like:
- "Find YouTube videos about [topic]"
- "Search for tutorials on [subject]"
- "Get video information from this URL"
- "Download subtitles from YouTube video"
- "Find top videos about [topic] for research"
- "Export YouTube URLs for NotebookLM"
- "Get video details and metadata"

## Autonomy Rules

**Run automatically (no confirmation):**
- `python youtube_search_tool.py search` - search videos
- `python youtube_search_tool.py info` - get video information
- `python youtube_search_tool.py urls` - export URLs list
- `python youtube_search_tool.py --help` - show help

**Ask before running:**
- `python youtube_search_tool.py subtitles` - downloads files to filesystem

## Quick Reference

| Task | Command |
|------|---------|
| Search videos | `python youtube_search_tool.py search "query"` |
| Search with limit | `python youtube_search_tool.py search "query" -n 5` |
| Search JSON output | `python youtube_search_tool.py search "query" --json` |
| Get video info | `python youtube_search_tool.py info "VIDEO_URL"` |
| Get video info JSON | `python youtube_search_tool.py info "VIDEO_URL" --json` |
| Download subtitles | `python youtube_search_tool.py subtitles "VIDEO_URL"` |
| Download specific languages | `python youtube_search_tool.py subtitles "VIDEO_URL" -l "en,vi"` |
| Export URLs only | `python youtube_search_tool.py urls "query"` |
| Export URLs to file | `python youtube_search_tool.py urls "query" -o urls.txt` |
| Show help | `python youtube_search_tool.py --help` |

## Command Output Formats

Commands with `--json` return structured data for parsing:

**Search videos:**
```bash
python youtube_search_tool.py search "AI tools" --json
```
Returns:
```json
[
  {
    "title": "Video Title",
    "uploader": "Channel Name", 
    "view_count": 1000000,
    "duration": 600,
    "url": "https://www.youtube.com/watch?v=...",
    "video_id": "...",
    "upload_date": "20240101",
    "description": "Video description..."
  }
]
```

**Video information:**
```bash
python youtube_search_tool.py info "https://youtube.com/watch?v=..." --json
```
Returns:
```json
{
  "title": "Video Title",
  "uploader": "Channel Name",
  "view_count": 1000000,
  "like_count": 50000,
  "duration": 600,
  "upload_date": "20240101",
  "description": "Full description",
  "tags": ["tag1", "tag2"],
  "categories": ["Education"],
  "subtitles": ["en", "es"],
  "automatic_captions": ["en", "es", "fr"]
}
```

**URLs export:**
```bash
python youtube_search_tool.py urls "AI business" -n 5
```
Returns plain text URLs, one per line.

## Integration with NotebookLM

**Common workflow:** Search YouTube → Export URLs → Add to NotebookLM

```bash
# 1. Search and export URLs
python youtube_search_tool.py urls "AI tools for business" -n 5 -o ai_videos.txt

# 2. Add URLs to NotebookLM
notebooklm create "AI Business Research"
while read url; do notebooklm source add "$url"; done < ai_videos.txt
```

**Automated integration example:**
```bash
# Search for videos and add directly to NotebookLM
python youtube_search_tool.py urls "digital marketing AI" -n 3 | while read url; do
  notebooklm source add "$url"
done
```

## Common Workflows

### Research Video Discovery
**Time:** 1-2 minutes

1. `python youtube_search_tool.py search "topic" -n 10` — *search for relevant videos*
2. Review results and select interesting videos
3. `python youtube_search_tool.py info "VIDEO_URL"` — *get detailed information*
4. `python youtube_search_tool.py urls "topic" -o research_urls.txt` — *export for other tools*

### Content Analysis Pipeline
**Time:** 2-5 minutes

1. `python youtube_search_tool.py search "topic" --json` — *get structured data*
2. Parse JSON to extract URLs and metadata
3. `python youtube_search_tool.py subtitles "URL" -l "en"` — *download transcripts*
4. Use subtitles for content analysis

### NotebookLM Integration
**Time:** 3-5 minutes

1. `python youtube_search_tool.py urls "research topic" -n 5 -o videos.txt`
2. `notebooklm create "Research: [topic]"`
3. Add each URL: `while read url; do notebooklm source add "$url"; done < videos.txt`
4. Wait for processing: `notebooklm source list`
5. Analyze: `notebooklm ask "What are the main themes?"`

## Output Style

**Progress updates:** Brief status for each step
- "Searching for 'AI tools'..."
- "Found 5 videos"
- "Getting video information..."
- "Downloading subtitles..."

**Structured output:** Use `--json` flag for machine-readable output
**Plain text:** Default human-readable format with formatted numbers and durations

## Error Handling

**On failure, offer the user a choice:**
1. Retry with updated yt-dlp
2. Try different search terms
3. Skip problematic videos and continue

**Error decision tree:**

| Error | Cause | Action |
|-------|-------|--------|
| "No module named yt_dlp" | Not installed | Run `pip install yt-dlp` |
| API/extraction errors | Outdated yt-dlp | Run `pip install --upgrade yt-dlp` |
| "No results found" | Bad search query | Try different keywords |
| Subtitle download fails | No subtitles available | Check video has captions |
| Rate limiting | Too many requests | Wait and retry |

## Known Limitations

**Rate limiting:** YouTube may throttle requests if too many are made quickly
**Geo-restrictions:** Some videos may not be available in all regions  
**Private/deleted videos:** Cannot access private or removed content
**Subtitle availability:** Not all videos have subtitles or captions

**Workarounds:**
- Use smaller batch sizes for bulk operations
- Add delays between requests for large datasets
- Check video accessibility before processing
- Verify subtitle availability with `info` command first

## Features

| Feature | Command | Description |
|---------|---------|-------------|
| **Video search** | `search "query"` | Find videos by keywords with view counts, duration |
| **Detailed info** | `info "URL"` | Get comprehensive video metadata |
| **Subtitle download** | `subtitles "URL"` | Download captions in multiple languages |
| **URL export** | `urls "query"` | Export video URLs for other tools |
| **JSON output** | `--json` flag | Machine-readable structured data |
| **Batch processing** | Multiple commands | Process multiple videos efficiently |

## Troubleshooting

```bash
python youtube_search_tool.py --help     # Show all commands
pip install --upgrade yt-dlp             # Update extractor
python -c "import yt_dlp; print(yt_dlp.version.__version__)"  # Check version
```

**Common issues:**
- **Import errors:** Install missing packages with pip
- **Extraction failures:** Update yt-dlp to latest version  
- **No results:** Try broader or different search terms
- **Subtitle errors:** Check if video has captions available