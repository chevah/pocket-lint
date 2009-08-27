# Copyright (C) 2009 - Curtis Hovey <sinzui.is at verizon.net>
"""Bazaar integration."""

import mimetypes
import os

from bzrlib import workingtree
from bzrlib.errors import NotBranchError
from bzrlib.revisionspec import RevisionSpec


__all__  = [
    'open_changed_files_to_push',
    'open_uncommitted_files',
    ]


class BzrProject:
    """View and manage a bazaar branch."""

    def __init__(self, gedit, window, working_tree=None):
        self.gedit = gedit
        self.window = window
        self.utf8_encoding = gedit.encoding_get_from_charset('UTF-8')
        mimetypes.init()
        self.working_tree = working_tree

    def set_working_tree(self):
        """Return the working tree for the working directory or document"""
        doc = self.window.get_active_document()
        if doc is None:
            self.working_tree = None
            return
        file_path = doc.get_uri_for_display()
        if file_path is None:
            cwd = os.getcwd()
        else:
            cwd = os.path.dirname(file_path)
        try:
            working_tree, relpath_ = workingtree.WorkingTree.open_containing(
                cwd)
            self.working_tree = working_tree
        except NotBranchError:
            self.working_tree = None

    def is_doc_open(self, uri):
        """Return True if the window already has a document opened for uri."""
        for doc in self.window.get_documents():
            if doc.get_uri() == uri:
                return True
        return False

    def open_doc(self, uri):
        """Open document at uri if it can be, and is not already, opened."""
        if self.is_doc_open(uri):
            return
        mime_type, charset_ = mimetypes.guess_type(uri)
        if mime_type is None or 'text/' in mime_type:
            # This appears to be a file that gedit can open.
            encoding = self.utf8_encoding
            self.window.create_tab_from_uri(uri, encoding, 0, False, False)

    def open_changed_files(self, other_tree):
        """Open files in the bzr branch."""
        try:
            self.working_tree.lock_read()
            other_tree.lock_read()
            changes = self.working_tree.iter_changes(
                other_tree, False, None,
                require_versioned=False, want_unversioned=False)
            for change in changes:
                # change is: (file_id, paths, content_change, versioned,
                #             parent_id, name, kind, executable)
                # paths is (previous_path, current_path)
                tree_file_path = change[1][1]
                base_dir = self.working_tree.basedir
                uri = 'file://%s' % os.path.join(base_dir, tree_file_path)
                self.open_doc(uri)
        finally:
            self.working_tree.unlock()
            other_tree.unlock()
    def open_uncommitted_files(self, data):
        """Open modified and added files in the bzr branch."""
        self.open_changed_files(self.working_tree.basis_tree())

    def open_changed_files_to_push(self, data):
        """Open the changed files in the branch that not been pushed."""
        push_uri = self.working_tree.branch.get_push_location()
        if push_uri is None:
            return
        revision = RevisionSpec.from_string('branch:%s' % push_uri)
        self.open_changed_files(revision.as_tree(self.working_tree.branch))


