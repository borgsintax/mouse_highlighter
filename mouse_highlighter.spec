# mouse_highlighter.spec
# PyInstaller build specification for Mouse Highlighter
# Run with: pyinstaller mouse_highlighter.spec

from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
import os

BASE = os.path.dirname(os.path.abspath(SPEC))  # noqa: F821  (SPEC is injected by PyInstaller)

a = Analysis(
    ['mouse_highlighter.py'],
    pathex=[BASE],
    binaries=[],
    datas=[
        # Bundle the default config so it's available inside the exe
        ('config.default.json', '.'),
    ],
    hiddenimports=[
        'pystray._win32',           # Windows tray backend
        'PIL._tkinter_finder',      # Pillow / tkinter bridge
        'pkg_resources.py2_compat', # sometimes needed by pystray
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MouseHighlighter',        # output exe name
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                       # compress with UPX if available (smaller file)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                  # no black console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icon.ico',              # ← uncomment and add icon.ico to use a custom icon
)
