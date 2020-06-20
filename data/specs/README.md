# Specs
This folder contains specification files for building app

## Requirements:  
* PyInstaller

Install PyInstaller using:

    pip install pyinstaller --upgrade

Or if you installed kivy using conda it is preferable to use conda installer:

    conda install pyinstaller

## Example of commands to build an app.

Creating _.spec_ file:

    python -m PyInstaller --name Tempo --onefile ../Tempo/main.py


Building an app using _.spec_ file:

    python -m PyInstaller .\Tempo.spec


## Known issues
* An error may appear while launching built application. Usually this happens if you haven't included project directory into the _.spec_ file. To fix this add Tree('projectdir') into the _.spec_ as it is decribed here:
```
        exe = EXE(pyz,
                Tree('..\\Tempo\\data'),
                Tree('..\\Tempo\\tempo'),
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
                console=False)
```