# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['shutdown_timer.py'],
    pathex=['D:\\desktop\\python program\\shijianxiansh'],
    binaries=[],
    datas=[
        ('shutdown_settings.json', '.'),
        ('help_manager.py', '.'),
        ('settings_manager.py', '.'),
        ('setting_data.py', '.')
    ],
    hiddenimports=['winotify'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='定时关机助手',
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
    entitlements_file=None
)