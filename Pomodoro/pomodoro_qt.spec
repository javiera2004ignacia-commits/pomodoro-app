# -*- mode: python ; coding: utf-8 -*-

# pomodoro_qt.spec
# Compila Pomodoro con PyQt5/Tkinter y recursos en un solo archivo .exe portable
from PyInstaller.utils.hooks import collect_submodules
hiddenimports = collect_submodules('plyer')

block_cipher = None

a = Analysis(
    ['pomodoro_qt.py'],
    pathex=['C:\\Users\\javie\\OneDrive\\Documentos\\Codigo\\Pomodoro'],
    binaries=[],
    datas=[
        ('tomato.png', '.'),
        ('tomato.ico', '.'),
        ('trabajo.mp3', '.'),
        ('descanso.mp3', '.'),
        ('button_icons/*', 'button_icons'),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Pomodoro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='tomato.ico'
)
