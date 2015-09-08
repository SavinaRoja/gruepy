#encoding: utf-8

import copy
import sys
import curses
import time
import weakref
from functools import wraps
import locale


class Widget(object):

    def __init__(self,
                 workspace,
                 parent,
                 relx=0,
                 rely=0,
                 width=None,
                 height=None,
                 max_width=None,
                 max_height=None,
                 editable=True,
                 hidden=False,
                 keep_starting_dimensions=True,
                 **kwargs):

        try:
            self.workspace = weakref.proxy(workspace)
        except TypeError:
            self.workspace = workspace

        try:
            self.parent = weakref.proxy(parent)
        except TypeError:
            self.parent = parent

        self.keep_starting_dimensions = keep_starting_dimensions

        self.max_width, self.max_height = max_width, max_height

        self.requested_width, self.requested_height = width, height
        self.width, self.height = width, height

        self.relx, self.rely = relx, rely

        self.editable = editable
        self.hidden = hidden

## Some Aspects of Size Management
# Recall that Containers inherit from Widgets, so this applies to them also
#
# 1: As a rule, a Widget will not modify its own rely/relx attributes. This
#    job belongs to its Parent.
#
# 2: As a rule, a Widget will not modify its own max_height/max_width
#    attributes. This job belongs to its Parent.
#
# 3: A Widget is free to modify its own height/width attributes. The Parent
#    should not do this, as it will instead manage the max_height/max_width
#    dimension constraints.
#
# 4. The dimensions passed in during instantiation are stored in
#    requested_height/requested_width attributes and these are not to be
#    modified by either the Widget or Parent.
#
# 5. A Widget's height/width attributes may not report a value greater than
#    its max_height/max_width.
#
# 6. By default, the keep_starting_dimensions attribute will cause the Widget
#    to use its requested_height/requested_width values as its height/width.
#    This behavior may be altered for custom Widgets as needed.

    @property
    def max_width(self):
        return self._max_width

    @max_width.setter
    def max_width(self, value):
        #Care should be taken that this does not extend past available screen
        if value is None:
            value = 0
        self._max_width = value

    @property
    def max_height(self):
        return self._max_height

    @max_height.setter
    def max_height(self, value):
        #Care should be taken that this does not extend past available screen
        if value is None:
            value = 0
        self._max_height = value

    @property
    def width(self):
        if self.keep_starting_dimensions and self.requested_width is not None:
            w = self.requested_width
        else:
            w = self._width
        if w > self.max_width:
            w = self.max_width
        return w

    @width.setter
    def width(self, value):
        if value is None:
            value = 0
        self._width = value

    @property
    def height(self):
        if self.keep_starting_dimensions and self.requested_height is not None:
            h = self.requested_height
        else:
            h = self._height
        if h > self.max_height:
            h = self.max_height
        return h

    @height.setter
    def height(self, value):
        if value is None:
            value = 0
        self._height = value

