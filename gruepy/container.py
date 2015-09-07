#encoding: utf-8

import curses
import weakref

from .widget import Widget


class Container(Widget):
    """
    """
    def __init__(self,
                 workspace,
                 parent,
                 *args,
                 **kwargs):
        super(Container, self).__init__(workspace,
                                        parent,
                                        *args,
                                        **kwargs)
        self.contained = []
        self.contained_map = {}
        self._default_widget = 0

    def add_widget(self,
                   widget_class,
                   widget_id=None,
                   rely=None,
                   relx=None,
                   max_width=None,
                   max_height=None,
                   *args,
                   **kwargs):
        """
        """
        y, x = self.next_rely_relx()
        if rely is None:
            rely = y
        if relx is None:
            relx = x
        if max_height is None:
            max_height = self.max_height
        if max_width is None:
            max_width = self.max_width

        widget = widget_class(self.workspace,
                              self,
                              relx=relx,
                              rely=rely,
                              max_height=max_height,
                              max_width=max_width,
                              *args,
                              **kwargs)

        self.contained.append(widget)

        widget_proxy = weakref.proxy(widget)
        if widget_id is not None:
            self.contained[widget_id] = widget_proxy
        else:
            self.contained_map[self._default_widget_id] = widget_proxy
            self._default_widget_id += 1

        return widget_proxy

    add = add_widget

    def remove_widget(self, widget=None, widget_id=None):
        """
        """
        if widget is None and widget_id is None:
            raise TypeError('remove_widget requires at least one argument')

        #By ID
        if widget_id is not None:
            if widget_id not in self.contained_map:
                return False
            widget = self.contained_map[widget_id]
            self.contained.remove(widget)
            del self.contained_map[widget_id]
            #self.resize()
            return True

        #By widget reference
        try:
            self.contained.remove(widget)
        except ValueError:
            return False
        else:
            #Looking for values in a dict is weird, but seems necessary
            map_key = None
            for key, val in self.contained_map.items()
                if val == widget:
                    map_key = key
                    break
            if map_key is not None:
                del self.contained_map[map_key]
            #self.resize()
            return True

    def next_rely_relx(self):
        """
        """
        rely = self.rely #+ self.top_margin
        relx = self.relx #+ self.left_margin
        return rely, relx

