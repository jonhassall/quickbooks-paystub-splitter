# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from dotenv import load_dotenv
from PIL import Image

# Load environment variables if .env exists, otherwise load .env.example
env_path = '.env' if os.path.exists('.env') else '.env.example'
load_dotenv(env_path)

base_prefix = getattr(sys, 'base_prefix', sys.prefix)
tcl_dir = os.path.join(base_prefix, 'tcl', 'tcl8.6')
tk_dir = os.path.join(base_prefix, 'tcl', 'tk8.6')

if os.path.exists(tcl_dir) and 'TCL_LIBRARY' not in os.environ:
    os.environ['TCL_LIBRARY'] = tcl_dir
if os.path.exists(tk_dir) and 'TK_LIBRARY' not in os.environ:
    os.environ['TK_LIBRARY'] = tk_dir

app_name = os.getenv('APP_NAME', 'Paystub Splitter')
logo_path = os.getenv('LOGO_PATH', '').strip()

datas = []
if os.path.exists('.env'):
    datas.append(('.env', '.'))
elif os.path.exists('.env.example'):
    datas.append(('.env.example', '.'))

if logo_path and os.path.isfile(logo_path):
    datas.append((logo_path, '.'))

# Convert PNG to ICO for EXE icon if logo exists
icon_file = None
if logo_path and os.path.isfile(logo_path):
    try:
        ico_path = 'app_icon.ico'
        img = Image.open(logo_path)
        img.save(ico_path, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
        icon_file = ico_path
    except Exception as e:
        print(f"Warning: Could not create icon from {logo_path}: {e}")

version_file = 'version_info.txt' if os.path.exists('version_info.txt') else None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox', 'dotenv', 'PIL', 'PIL.ImageTk'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
    version=version_file,
)
