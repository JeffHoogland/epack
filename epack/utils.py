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


def pkg_resource_get(fname):
    return os.path.join(os.path.dirname(__file__), 'data', fname)

def xdg_open(url_or_file):
    Exe('xdg-open %s' % url_or_file)


