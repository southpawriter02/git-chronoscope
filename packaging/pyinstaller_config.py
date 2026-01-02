# PyInstaller Configuration for git-chronoscope
# 
# Build with:
#   cd git-chronoscope
#   pip install pyinstaller
#   pyinstaller packaging/pyinstaller_config.py
#
# Or use the helper script:
#   python packaging/build_executable.py

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Collect all Pygments submodules for syntax highlighting
hiddenimports = collect_submodules('pygments.lexers') + collect_submodules('pygments.styles')

a = Analysis(
    [os.path.join('..', 'src', 'main.py')],
    pathex=[os.path.dirname(os.path.dirname(os.path.abspath(__file__)))],
    binaries=[],
    datas=[
        (os.path.join('..', 'README.md'), '.'),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib', 
        'scipy',
        'numpy.testing',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='git-chronoscope',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
