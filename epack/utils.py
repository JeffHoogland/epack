#!/usr/bin/env python
# encoding: utf-8
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import absolute_import, print_function, unicode_literals

import os
import magic
from efl.ecore import Exe

VERSION = '0.1.0'

GITHUB = 'https://github.com/wfx/epack'

AUTHORS = """
<br>
<align=center>
<hilight>Wolfgang Morawetz (wfx)</hilight><br>
wolfgang.morawetz@gmail.com<br><br>

<hilight>Davide Andreoli (davemds)</hilight><br>
dave@gurumeditation.it<br><br>
</align>
"""

LICENSE = """
<align=center>
<hilight>
GNU GENERAL PUBLIC LICENSE<br>
Version 3, 29 June 2007<br><br>
</hilight>

This program is free software: you can redistribute it and/or modify 
it under the terms of the GNU General Public License as published by 
the Free Software Foundation, either version 3 of the License, or 
(at your option) any later version.<br><br>

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
GNU General Public License for more details.<br><br>

You should have received a copy of the GNU General Public License 
along with this program. If not, see<br>
<link><a href=http://www.gnu.org/licenses>http://www.gnu.org/licenses/</a></link>
</align>
"""

INFO = """
<align=center>
<hilight>Epack</hilight> is an archive manager for the Enlightenment desktop.<br> 
<br>
With <hilight>Epack</hilight> you can:<br>
View the content of an archive.<br>
Extract files from the archive.<br>
Extract into a different folder.<br>
Create archive folder.<br>
Delete archive after extraction.<br>
feed youre kitty.<br>
<br>
</align>
"""

SUPPORTED_MIME = [
    'application/gzip', 'application/x-gzip',
    'application/bzip2', 'application/x-bzip2',
    'application/bz2', 'application/x-bz2',
    'application/rar', 'application/x-rar',
    'application/gz', 'application/x-gz',
    'application/tar', 'application/x-tar',
    'application/tbz2', 'application/x-tbz2',
    'application/tar.gz', 'application/x-tar.gz',
    'application/tar.bz2', 'application/x-tar.bz2',
    'application/tgz', 'application/x-tgz',
    'application/zip', 'application/x-zip',
    'application/Z', 'application/x-Z',
    'application/xz', 'application/x-xz',
    'application/iso9660-image', 'application/x-iso9660-image'
]


def mime_type_query(fname):
    m = magic.open(magic.MAGIC_MIME_TYPE)
    m.load()
    return m.file(fname)

def pkg_resource_get(fname):
    return os.path.join(os.path.dirname(__file__), 'data', fname)

def xdg_open(url_or_file):
    Exe('xdg-open %s' % url_or_file)
