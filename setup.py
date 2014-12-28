#!/usr/bin/env python

from distutils.core import setup

setup(
    name = 'epack',
    version = '0.1.0',
    description = 'A simple tool to extract any archive file',
    license="GNU General Public License v3 (GPLv3)",
    author = 'Wolfgang Morawetz (wfx) & Davide Andreoli (davemds)',
    author_email = 'wolfgang.morawetz@gmail.com',
    url="https://github.com/wfx/epack",
    requires = ['efl', 'magic'],
    provides = ['epack'],
    packages = ['epack', 'epack.libarchive'],
    scripts = ['bin/epack'],
    data_files = [
        ('share/applications', ['data/epack.desktop']),
        ('share/icons', ['data/epack.png']),
        ('share/icons/hicolor/24x24/apps', ['data/icons/24x24/epack.png']),
        ('share/icons/hicolor/32x32/apps', ['data/icons/32x32/epack.png']),
        ('share/icons/hicolor/64x64/apps', ['data/icons/64x64/epack.png']),
        ('share/icons/hicolor/128x128/apps', ['data/icons/128x128/epack.png']),
        ('share/icons/hicolor/256x256/apps', ['data/icons/256x256/epack.png']),
    ]
)
