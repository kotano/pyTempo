import PyInstaller.__main__
import os
package_name = 'Tempo'

from pathlib import  Path

PyInstaller.__main__.run([
    '--name=%s' % package_name,
    '--onefile',
    '--windowed',
    '--hidden-import=plyer'
    # '--add-binary=%s' % os.path.join('resource', 'path', '*.png'),
    '--add-data=%s' % os.path.join('resource', 'path', '*.txt'),
    # '--icon=%s' % os.path.join('resource', 'path', 'icon.ico'),
    os.path.join('my_package', '__main__.py'),
])