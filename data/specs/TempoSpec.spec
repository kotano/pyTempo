# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import plyer
from plyer import notification, vibrator
from plyer.utils import platform



a = Analysis(['..\\Tempo\\main.py'],
             pathex=['S:\\Users\\ahuda\\Code\\demos'],
             binaries=[],
             datas=[],
             hiddenimports=['plyer', 'plyer.utils', 'notification', 'vibrator', 'platform'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          Tree('..\\Tempo'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Tempo',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
