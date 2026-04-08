# AI Image Studio

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![UI](https://img.shields.io/badge/UI-CustomTkinter-black.svg)

A professional-grade desktop application for AI-powered background removal and multi-format image conversion. Designed with a modern "Zinc" aesthetic inspired by shadcn/ui.

## Features
- **AI Background Removal**: High-precision extraction using U2-Net.
- **Instant Preview**: Real-time image rendering before processing.
- **Multi-Format Export**: Support for PNG, JPEG, WEBP, BMP, TIFF, and PDF.
- **Privacy Focused**: Processes everything locally. No cloud, no data tracking.

## Getting Started
1. Clone the repo: `git clone https://github.com/naawish/AI-Image-Studio.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python src/main.py`

## Building the Executable
Run the following command to generate a standalone Windows EXE:
```bash
pyinstaller --noconfirm --onefile --windowed --collect-all rembg --collect-all onnxruntime --name "AI_Image_Studio" src/main.py