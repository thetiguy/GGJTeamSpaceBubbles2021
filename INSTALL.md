# Installation Procedure

## Windows

-   Install [Python][python]

-   Install [Build Tools for Visual Studio][build-tools].
    Note that it's hidden in the "Tools for Visual Studio" part of the website.
    During installation, select the "Build Tools for C++" option.

-   Restart your computer

-   Open PowerShell, navigate to the directory containing this file and run:
    `pip install -r requirements.txt`

-   In the same PowerShell, run `python run.py`

## Linux

-  Install dependancies for pyglet and arcade
  - sudo dnf install libtiff-devel libjpeg-devel openjpeg2-devel zlib-devel freetype-devel lcms2-devel libwebp-devel tcl-devel tk-devel harfbuzz-devel fribidi-devel libraqm-devel libxcb-devel python3-devel python-devel freeglut-devel

-  pip install requirements.txt
-  pip uninstall pillow
-  pip install git+https://github.com/nulano/Pillow.git@fribidi-link

[build-tools]: https://visualstudio.microsoft.com/downloads/
[python]: https://www.python.org/
