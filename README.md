# Python Media & File Downloader

A command-line Python tool that downloads media files (videos, audio) using `yt-dlp` **and** regular files via HTTP requests.  
Supports downloading single URLs or batch downloading from a queue file, with file type validation and size checks.

---

## Features

- Download media URLs (YouTube, TikTok, etc.) using yt-dlp with quality control (minimum 720p video + 128 kbps audio)  
- Download regular files (images, PDFs, text, etc.) using HTTP requests  
- Validate file type and size before adding URLs to queue  
- Batch download URLs listed in a queue text file  
- Option to clear the queue file after batch download  
- Restricts filenames for safe cross-platform use  
- Configurable output folder  

---

## Requirements

- Python 3.7 or higher  
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)  
- [ffmpeg](https://ffmpeg.org/) installed and added to your system PATH (for merging video + audio streams)  
- `requests` Python library (`pip install requests`)  

---

## Setup

1. Clone or download the repo  
2. Install Python dependencies:  
   ```bash
   pip install yt-dlp requests

## Commands

1. Add URL(s) to the queue:
   ```bash
   python text.py -a <URL>
   python text.py -add <URL>
2. Remove URL(s) from the queue:
   ```bash
   python text.py -r <URL>
   python text.py -remove <URL>
3. Download a single URL:
   ```bash
   python main.py <URL>
4. Download all URLs from the queue:
   ```bash
   python main.py --batch
   python main.py -b
5. Choose output folder for the downloads (default = "web-downloads"):
   ```bash
   python main.py -b --out <OUTPUT_FOLDER>
6. If you downloaded using batch, choose to clear queue or not:
   ```bash
   python main.py -b -c
   python main.py --batch --clear
   
