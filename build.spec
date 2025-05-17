# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['shutdown_timer.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('shutdown32.png', '.'),
        ('shutdown_timer.ico', '.')
    ],
    hiddenimports=['tkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='时间与自动关机助手',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='shutdown_timer.ico'
)