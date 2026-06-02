@echo off
if "%~1"=="" (
    echo Usage: run_analyzer.bat ^<path_to_image^>
    exit /b 1
)
uv run --with Pillow --with matplotlib --with numpy python "%~dp0color_analyzer.py" "%~1"
