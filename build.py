"""
打包脚本 - 编译为EXE/DMG/AppImage
"""
import os
import sys
import subprocess
from pathlib import Path


def build_exe():
    """
    编译为Windows EXE
    
    要求: pip install pyinstaller
    """
    print("Building Windows EXE...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=QuickFileSharing",
        "--icon=assets/icon.ico",
        "--add-data=ui:ui",
        "--add-data=config.py:.",
        "--collect-all=PySide6",
        "--hidden-import=zeroconf",
        "--hidden-import=psutil",
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✓ EXE build completed")
        print(f"Output: dist/QuickFileSharing.exe")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        sys.exit(1)


def build_macos():
    """
    编译为macOS DMG
    """
    print("Building macOS DMG...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=QuickFileSharing",
        "--icon=assets/icon.icns",
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✓ macOS build completed")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        sys.exit(1)


def build_linux():
    """
    编译为Linux AppImage
    """
    print("Building Linux AppImage...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=QuickFileSharing",
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✓ Linux build completed")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build.py [windows|macos|linux|all]")
        sys.exit(1)
    
    platform_type = sys.argv[1].lower()
    
    if platform_type == "windows":
        build_exe()
    elif platform_type == "macos":
        build_macos()
    elif platform_type == "linux":
        build_linux()
    elif platform_type == "all":
        build_exe()
        build_macos()
        build_linux()
    else:
        print("Unknown platform")
        sys.exit(1)
