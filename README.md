# Python-Stuff
A handpicked collection of Python scripts to simplify everyday tasks.

## Contents

- **utilities/**: handy scripts (passwords, IP info, downloads, compression, monitoring, automation, text analysis)
- **generators/**: creative tools (e.g., QR code generator)
- **requirements.txt**: dependencies

## Prerequisites

1. [VS Code](https://code.visualstudio.com/) + Python extension (ms-python.python)
2. Python 3.9+ ([python.org](https://python.org/))
3. (Optional) For YouTube utility: `yt-dlp` and `ffmpeg`:
   ```bash
   pip3 install yt-dlp
   brew install ffmpeg   # macOS
   ```
4. (Optional) For QR Code generator: `pip3 install qrcode pillow`

## Installation

Install core dependencies:
```bash
pip3 install -r requirements.txt
```

## What’s Inside

### Generators
- `QRCode.py`: generate QR codes for URLs or text

### Utilities
- `passwords.py`: create secure passwords
- `ip_address.py`: local & public IP info
- `ip_websites.py`: lookup website IPs & ping
- `youtube_downloader.py`: video/audio downloads
- `image_compressor.py`: resize & compress images
- `system_monitor.py`: check CPU, memory, disk, network
- `task_automator.py`: backup, clean & organise files
- `text_analyzer.py`: word counts, sentiment, summaries

## Usage

Invoke any utility via the command line:
```bash
python3 utilities/*.py
```

Or for generators:
```bash
python3 generators/*.py
```

Examples:
```bash
python3 utilities/passwords.py
python3 utilities/youtube_downloader.py
python3 generators/QRCode.py
```

*Note*: macOS users may need `python3` and `pip3`.
