#!/usr/bin/env python3
"""
Build script for creating standalone executables.
Usage: python packaging/build_executable.py
"""
import os
import sys
import subprocess
import platform
import shutil


def get_platform_suffix():
    """Get platform-specific suffix for executable."""
    system = platform.system().lower()
    if system == 'windows':
        return 'windows.exe'
    elif system == 'darwin':
        return 'macos'
    else:
        return 'linux'


def build_executable():
    """Build the standalone executable using PyInstaller."""
    # Get project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    print(f"Building git-chronoscope executable for {platform.system()}...")
    
    # Install PyInstaller if needed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    # Change to project root
    os.chdir(project_root)
    
    # Build command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--name', 'git-chronoscope',
        '--console',
        '--clean',
        '--noconfirm',
        # Hidden imports for Pygments
        '--collect-submodules', 'pygments.lexers',
        '--collect-submodules', 'pygments.styles',
        # Exclude unnecessary modules
        '--exclude-module', 'tkinter',
        '--exclude-module', 'matplotlib',
        '--exclude-module', 'scipy',
        '--exclude-module', 'pytest',
        # Entry point
        'src/main.py',
    ]
    
    print(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)
    
    # Rename output with platform suffix
    dist_dir = os.path.join(project_root, 'dist')
    suffix = get_platform_suffix()
    
    if platform.system() == 'Windows':
        src = os.path.join(dist_dir, 'git-chronoscope.exe')
        dst = os.path.join(dist_dir, f'git-chronoscope-{suffix}')
    else:
        src = os.path.join(dist_dir, 'git-chronoscope')
        dst = os.path.join(dist_dir, f'git-chronoscope-{suffix}')
    
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"Created: {dst}")
    
    print("Build complete!")
    return dst


if __name__ == '__main__':
    build_executable()
