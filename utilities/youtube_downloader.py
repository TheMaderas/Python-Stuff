import os
import time
import ssl
from yt_dlp import YoutubeDL

ssl._create_default_https_context = ssl._create_unverified_context

def download_from_youtube(url, download_type='video', resolution='best', output_dir='downloads'):
    """Download video or audio from YouTube using yt-dlp"""
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'bestaudio/best' if download_type == 'audio' else resolution,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if download_type == 'audio' else []
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        filename = ydl.prepare_filename(info)
    return filename

def main():
    print("YouTube Downloader - choose type:")
    choice = ''
    while choice not in ['1', '2']:
        print("1: Video\n2: Audio")
        choice = input("Enter your choice (1 or 2): ")
    download_type = 'audio' if choice == '2' else 'video'
    resolution = 'best'
    if download_type == 'video':
        print("Select resolution (e.g. 1080, 720) or leave blank for best:")
        res = input("Resolution: ").strip()
        resolution = res if res else 'best'
    url = input("Enter YouTube URL: ")
    print(f"Downloading {download_type}...")
    try:
        path = download_from_youtube(url, download_type, resolution)
        print(f"Download completed: {path}")
    except Exception as e:
        print(f"Error downloading: {e}")

if __name__ == '__main__':
    main()
