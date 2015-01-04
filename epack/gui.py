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

from efl import ecore
from efl import elementary
from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL
from efl.elementary.background import Background
from efl.elementary.window import StandardWindow, DialogWindow
from efl.elementary.box import Box
from efl.elementary.ctxpopup import Ctxpopup
from efl.elementary.entry import Entry
from efl.elementary.icon import Icon
from efl.elementary.label import Label
from efl.elementary.frame import Frame
from efl.elementary.genlist import Genlist, GenlistItemClass, \
    ELM_GENLIST_ITEM_TREE
from efl.elementary.button import Button
from efl.elementary.table import Table
from efl.elementary.check import Check
from efl.elementary.fileselector_button import FileselectorButton
from efl.elementary.fileselector import Fileselector
from efl.elementary.popup import Popup
from efl.elementary.progressbar import Progressbar
from efl.elementary.separator import Separator

import epack.utils as utils


EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
EXPAND_HORIZ = EVAS_HINT_EXPAND, 0.0
EXPAND_VERT = 0.0, EVAS_HINT_EXPAND
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL
FILL_HORIZ = EVAS_HINT_FILL, 0.0
FILL_VERT = 0.0, EVAS_HINT_FILL


def gl_fold_text_get(obj, part, item_data):
    return item_data[:-1].split('/')[-1]

def gl_fold_icon_get(obj, part, item_data):
    return Icon(obj, standard='folder')

def gl_file_text_get(obj, part, item_data):
    return item_data.split('/')[-1]


class MainWin(StandardWindow):
    def __init__(self, app):
        self.app = app
        self.post_extract_action = 'close' # or 'fm' or 'term'

        # the window
        StandardWindow.__init__(self, 'epack.py', 'Epack')
        self.autodel_set(True)
        self.callback_delete_request_add(lambda o: self.app.exit())

        # main vertical box
        vbox = Box(self, size_hint_weight=EXPAND_BOTH)
        self.resize_object_add(vbox)
        vbox.show()

        ### header horiz box (inside a padding frame)
        frame = Frame(self, style='pad_medium',
                      size_hint_weight=EXPAND_HORIZ,
                      size_hint_align=FILL_HORIZ)
        vbox.pack_end(frame)
        frame.show()

        self.header_box = Box(self, horizontal=True,
                              size_hint_weight=EXPAND_HORIZ,
                              size_hint_align=FILL_HORIZ)
        frame.content = self.header_box
        self.header_box.show()

        # genlist with archive content
        self.file_itc = GenlistItemClass(item_style="no_icon",
                                         text_get_func=gl_file_text_get)
        self.fold_itc = GenlistItemClass(item_style="one_icon",
                                         text_get_func=gl_fold_text_get,
                                         content_get_func=gl_fold_icon_get)
        self.file_list = Genlist(self, homogeneous=True,
                                 size_hint_weight=EXPAND_BOTH,
                                 size_hint_align=FILL_BOTH)
        self.file_list.callback_expand_request_add(self._gl_expand_req_cb)
        self.file_list.callback_contract_request_add(self._gl_contract_req_cb)
        self.file_list.callback_expanded_add(self._gl_expanded_cb)
        self.file_list.callback_contracted_add(self._gl_contracted_cb)
        vbox.pack_end(self.file_list)
        self.file_list.show()

        ### footer table (inside a padding frame)
        frame = Frame(self, style='pad_medium',
                      size_hint_weight=EXPAND_HORIZ,
                      size_hint_align=FILL_HORIZ)
        vbox.pack_end(frame)
        frame.show()

        table = Table(frame)
        frame.content = table
        table.show()

        # FileSelectorButton
        self.fsb = DestinationButton(self)
        self.fsb.callback_file_chosen_add(self.chosen_folder_cb)
        table.pack(self.fsb, 0, 0, 3, 1)
        self.fsb.show()

        sep = Separator(table, horizontal=True,
                        size_hint_weight=EXPAND_HORIZ)
        table.pack(sep, 0, 1, 3, 1)
        sep.show()

        # extract button
        self.extract_btn = Button(table, text=_('Extract'))
        self.extract_btn.callback_clicked_add(self.extract_btn_cb)
        table.pack(self.extract_btn, 0, 2, 1, 2)
        self.extract_btn.show()

        sep = Separator(table, horizontal=False)
        table.pack(sep, 1, 2, 1, 2)
        sep.show()

        # delete-archive checkbox
        self.del_chk = Check(table, text=_('Delete archive after extraction'),
                             size_hint_weight=EXPAND_HORIZ,
                             size_hint_align=(0.0, 1.0))
        self.del_chk.callback_changed_add(self.del_check_cb)
        table.pack(self.del_chk, 2, 2, 1, 1)
        self.del_chk.show()

        # create-archive-folder checkbox
        self.create_folder_chk = Check(table, text=_('Create archive folder'),
                                       size_hint_weight=EXPAND_HORIZ,
                                       size_hint_align=(0.0, 1.0))
        table.pack(self.create_folder_chk, 2, 3, 1, 1)
        self.create_folder_chk.callback_changed_add(
                               lambda c: self.update_fsb_label())
        self.create_folder_chk.show()

        # set the correct ui state
        self.update_ui()

        # show the window
        self.resize(300, 300)
        self.show()

    def del_check_cb(self, check):
        self.app.delete_after_extract = check.state

    def update_ui(self, listing_in_progress=False):
        box = self.header_box
        box.clear()
        ui_disabled = True

        # file listing in progress
        if listing_in_progress:
            spin = Progressbar(box, style='wheel', pulse_mode=True)
            spin.pulse(True)
            spin.show()
            box.pack_end(spin)

            lb = Label(box, text=_('Reading archive, please wait...'),
                       size_hint_weight=EXPAND_HORIZ,
                       size_hint_align=(0.0, 0.5))
            lb.show()
            box.pack_end(lb)

        # no archive loaded
        elif self.app.file_name is None:
            bt = Button(box, text=_('No archive loaded, click to choose a file'),
                        size_hint_weight=EXPAND_HORIZ)
            bt.callback_clicked_add(lambda b: FileChooserWin(self.app, self))
            box.pack_end(bt)
            bt.show()

        # normal operation (archive loaded and listed)
        else:
            txt = _('<b>Archive:</b> %s') % (os.path.basename(self.app.file_name))
            lb = Label(box, text=txt, size_hint_weight=EXPAND_HORIZ,
                       size_hint_align=(0.0, 0.5))
            box.pack_end(lb)
            lb.show()
            ui_disabled = False

        # always show the about button
        sep = Separator(box)
        box.pack_end(sep)
        sep.show()

        ic = Icon(box, standard='dialog-info', size_hint_min=(24,24))
        ic.callback_clicked_add(lambda i: InfoWin(self))
        box.pack_end(ic)
        ic.show()

        for widget in (self.extract_btn, self.fsb,
                       self.create_folder_chk, self.del_chk):
            widget.disabled = ui_disabled

        self.update_fsb_label()

    def update_fsb_label(self):
        if self.create_folder_chk.state is True:
            name = os.path.splitext(os.path.basename(self.app.file_name))[0]
            self.fsb.text = os.path.join(self.app.dest_folder, name)
        else:
            self.fsb.text = self.app.dest_folder or ''

    def show_error_msg(self, msg):
        pop = Popup(self, text=msg)
        pop.part_text_set('title,text', _('Error'))

        btn = Button(self, text=_('Continue'))
        btn.callback_clicked_add(lambda b: pop.delete())
        pop.part_content_set('button1', btn)

        btn = Button(self, text=_('Exit'))
        btn.callback_clicked_add(lambda b: self.app.exit())
        pop.part_content_set('button2', btn)

        pop.show()

    def chosen_folder_cb(self, fsb, folder):
        if folder:
            self.app.dest_folder = folder
            self.update_fsb_label()

    def tree_populate(self, file_list=None, parent=None):
        if file_list is not None:
            self._file_list = file_list

        if parent is None:
            prefix = None # items must match this prefix to be listed
            fscount = 0   # folder must have this number of slashes
            dscount = 1   # files must have this number of slashes
        else:
            prefix = parent.data[:-1]
            fscount = prefix.count('/') + 1
            dscount = fscount + 1

        files = []
        for path in self._file_list:
            if prefix and not path.startswith(prefix):
                continue

            if path.endswith('/'):
                if path.count('/') == dscount:
                    self.file_list.item_append(self.fold_itc, path, parent,
                                               flags=ELM_GENLIST_ITEM_TREE)
            else:
                if path.count('/') == fscount:
                    files.append(path)

        for path in files:
            self.file_list.item_append(self.file_itc, path, parent)

    def _gl_expand_req_cb(self, gl, item):
        item.expanded = True

    def _gl_expanded_cb(self, gl, item):
        self.tree_populate(None, item)

    def _gl_contract_req_cb(self, gl, item):
        item.expanded = False

    def _gl_contracted_cb(self, gl, item):
        item.subitems_clear()

    def extract_btn_cb(self, btn):
        self.prog_popup = None
        self.app.dest_folder = self.fsb.text
        self.app.extract_archive()

    def build_prog_popup(self):
        pp = Popup(self)
        pp.part_text_set('title,text', _('Extracting files, please wait...'))
        pp.show()

        vbox = Box(self)
        pp.part_content_set('default', vbox)
        vbox.show()

        lb = Label(self, ellipsis=True, size_hint_weight=EXPAND_HORIZ,
                   size_hint_align=FILL_HORIZ)
        vbox.pack_end(lb)
        lb.show()

        pb = Progressbar(pp, size_hint_weight=EXPAND_HORIZ,
                         size_hint_align=FILL_HORIZ)
        vbox.pack_end(pb)
        pb.show()

        bt = Button(pp, text=_('Cancel'), disabled=True)
        # TODO make the button actually work
        pp.part_content_set('button1', bt)

        self.prog_pbar = pb
        self.prog_label = lb
        self.prog_popup = pp

    def extract_progress(self, progress, cur_name):
        if self.prog_popup is None:
            self.build_prog_popup()

        self.prog_pbar.value = progress
        self.prog_label.text = cur_name

    def extract_finished(self):
        if self.prog_popup:
            self.prog_popup.delete()
            self.prog_popup = None

    def _open_fm_and_exit_cb(self, bt):
        utils.xdg_open(self.app.dest_folder)
        self.app.exit()

    def _open_term_and_exit_cb(self, bt):
        utils.open_in_terminal(self.app.dest_folder)
        self.app.exit()

    def ask_what_to_do_next(self):
        pop = Popup(self)
        pop.part_text_set('title,text', _('Extract completed'))

        box = Box(pop)
        pop.content = box
        box.show()

        lb = Label(pop, text=_('What to do next?'),
                   size_hint_align=FILL_HORIZ)
        box.pack_end(lb)
        lb.show()

        btn = Button(pop, text=_('Open Filemanager'),
                     size_hint_align=FILL_HORIZ)
        btn.callback_clicked_add(self._open_fm_and_exit_cb)
        box.pack_end(btn)
        btn.show()

        btn = Button(pop, text=_('Open Terminal'),
                     size_hint_align=FILL_HORIZ)
        btn.callback_clicked_add(self._open_term_and_exit_cb)
        box.pack_end(btn)
        btn.show()

        btn = Button(pop, text=_('Close this popup'),
                     size_hint_align=FILL_HORIZ)
        btn.callback_clicked_add(lambda b: pop.delete())
        box.pack_end(btn)
        btn.show()

        btn = Button(pop, text=_('Exit'),
                     size_hint_align=FILL_HORIZ)
        btn.callback_clicked_add(lambda b: self.app.exit())
        box.pack_end(btn)
        btn.show()

        pop.show()


class InfoWin(DialogWindow):
    def __init__(self, parent):
        DialogWindow.__init__(self, parent, 'epack-info', 'Epack', autodel=True)

        fr = Frame(self, style='pad_large', size_hint_weight=EXPAND_BOTH,
                   size_hint_align=FILL_BOTH)
        self.resize_object_add(fr)
        fr.show()

        hbox = Box(self, horizontal=True, padding=(12,12))
        fr.content = hbox
        hbox.show()

        vbox = Box(self, align=(0.0,0.0), padding=(6,6),
                   size_hint_weight=EXPAND_VERT, size_hint_align=FILL_VERT)
        hbox.pack_end(vbox)
        vbox.show()

        # icon + version
        ic = Icon(self, standard='epack', size_hint_min=(64,64))
        vbox.pack_end(ic)
        ic.show()

        lb = Label(self, text=_('Version: %s') % utils.VERSION)
        vbox.pack_end(lb)
        lb.show()

        sep = Separator(self, horizontal=True)
        vbox.pack_end(sep)
        sep.show()

        # buttons
        bt = Button(self, text=_('Epack'), size_hint_align=FILL_HORIZ)
        bt.callback_clicked_add(lambda b: self.entry.text_set(utils.INFO))
        vbox.pack_end(bt)
        bt.show()

        bt = Button(self, text=_('Website'),size_hint_align=FILL_HORIZ)
        bt.callback_clicked_add(lambda b: utils.xdg_open(utils.GITHUB))
        vbox.pack_end(bt)
        bt.show()

        bt = Button(self, text=_('Authors'), size_hint_align=FILL_HORIZ)
        bt.callback_clicked_add(lambda b: self.entry.text_set(utils.AUTHORS))
        vbox.pack_end(bt)
        bt.show()

        bt = Button(self, text=_('License'), size_hint_align=FILL_HORIZ)
        bt.callback_clicked_add(lambda b: self.entry.text_set(utils.LICENSE))
        vbox.pack_end(bt)
        bt.show()

        # main text
        self.entry = Entry(self, editable=False, scrollable=True, text=utils.INFO,
                        size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        self.entry.callback_anchor_clicked_add(lambda e,i: utils.xdg_open(i.name))
        hbox.pack_end(self.entry)
        self.entry.show()

        self.resize(400, 200)
        self.show()


class DestinationButton(FileselectorButton):
    def __init__(self, parent):
        FileselectorButton.__init__(self, parent,
                    inwin_mode=False, folder_only=True,
                    size_hint_weight=EXPAND_HORIZ, size_hint_align=FILL_HORIZ)
        self._text = ''

        box = Box(self, horizontal=True, padding=(3,0))
        self.content = box
        box.show()

        icon = Icon(box, standard='folder', size_hint_min=(16,16))
        box.pack_end(icon)
        icon.show()

        self.label = Label(box, ellipsis=True,
                           size_hint_weight=EXPAND_BOTH,
                           size_hint_align=FILL_HORIZ)
        box.pack_end(self.label)
        self.label.show()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.label.text = '<align=left>%s</align>' % text


class FileChooserWin(DialogWindow):
    def __init__(self, app, parent):
        self.app = app
        DialogWindow.__init__(self, parent, 'epack.py', _('Choose an archive'))
        self.callback_delete_request_add(lambda o: self.delete())

        fs = Fileselector(self, expandable=False,
                          path=os.path.expanduser('~'),
                          size_hint_weight=EXPAND_BOTH,
                          size_hint_align=FILL_BOTH)
        fs.callback_done_add(self.done_cb)
        fs.callback_activated_add(self.done_cb)
        # TODO this filter seems not to work well...need fixing
        # fs.mime_types_filter_append(list(EXTRACT_MAP.keys()), 'Archive files')
        # fs.mime_types_filter_append(['*'], 'All files')
        fs.show()

        self.resize_object_add(fs)
        self.resize(300, 400)
        self.show()

    def done_cb(self, fs, path):
        if path is None:
            self.delete()
        elif os.path.isfile(path):
            self.app.load_file(path)
            self.delete()


