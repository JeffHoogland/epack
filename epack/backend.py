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

from __future__ import absolute_import, print_function

from epack.backend_libarchive import LibarchiveBackend
from epack.backend_shell import ShellBackend


def load_backend(fname):
    for backend in LibarchiveBackend, ShellBackend:
        try:
            instance = backend(fname)
            break
        except Exception as e:
            print(e)
            instance = None

    return instance
