#encoding: utf-8

import curses
import curses.panel
import struct
import sys
import termios
import weakref

#For more complex method of getting the size of screen
try:
    import fcntl
except ImportError:
    # Win32 platforms do not have fcntl
    pass

from .container import Container


class Workspace(Container):
    """
    """
    def __init__(self,
                 name=None,
                 parent_app=None,
                 min_height=24,
                 min_width=80,
                 max_height=None,
                 max_width=None,
                 #color='FORMDEFAULT',
                 #keypress_timeout=None,
                 #widget_list=None,
                 #cycle_widgets=False,
                 *args,
                 **kwargs):

        if max_height is None:
            self.auto_max_height = True
            max_height = self.max_physical()[0]
        else:
            self.auto_max_height = False

        if max_width is None:
            self.auto_max_width = True
            max_width = self.max_physical()[1]
        else:
            self.auto_max_width = False

        #Attention! Widgets sets self.form and self.parent as weakrefs of their
        #first instantiation arguments. Since Forms inherit from Widgets this
        #means that Form.form and Form.parent will be weakrefs to self; as a
        #consequence, inherited methods from Widget and Container that refer to
        #self.form or self.parent should still work
        super(Workspace, self).__init__(self,  # self.workspace -> self
                                        self,  # self.parent -> self
                                        #rely=0,
                                        #relx=0,
                                        max_height=max_height,
                                        max_width=max_width,
                                        *args,
                                        **kwargs)

        self.name = name
        self.parent_app = weakref.proxy(parent_app)
        self.min_height = min_height
        self.min_width = min_width

        #global APPLICATION_THEME_MANAGER
        #if APPLICATION_THEME_MANAGER is None:
            #self.theme_manager = theme_managers.ThemeManager()
        #else:
            #self.theme_manager = APPLICATION_THEME_MANAGER

        #self.keypress_timeout = keypress_timeout

        self.show_from_y = 0
        self.show_from_x = 0
        self.show_aty = 0
        self.show_atx = 0

        self.create_pad()

    def create_pad(self):
        #Safety margin by adding 1; avoids issues, like putting a character in
        #the bottom right corner which causes an error as scrolling is not set
        pad_height = self.max_height + 1
        pad_width = self.max_width + 1

        if self.min_height > self.max_height:
            pad_height = self.min_height
        if self.min_width > self.max_width:
            pad_width = self.min_width

        self.pad_height = pad_height
        self.pad_width = pad_width

        self.curses_pad = curses.newpad(pad_height, pad_width)

    def max_physical(self):
        """
        Returns the height and width of the physical screen.
        """
        #On OS X newwin does not correctly get the size of the screen.
        #let's see how big we could be: create a temp screen
        #and see the size curses makes it.  No good to keep, though
        try:
            max_y, max_x = struct.unpack('hh',
                                         fcntl.ioctl(sys.stderr.fileno(),
                                                     termios.TIOCGWINSZ,
                                                     'xxxx'))
            if (max_y, max_x) == (0, 0):
                raise ValueError
        except (ValueError, NameError):
            max_y, max_x = curses.newwin(0, 0).getmaxyx()
        return (max_y, max_x)

    def resize(self):
        pass

    def _resize(self, inpt=None):
        #This logic is arranged to ensure at most one call to max_physical
        if self.auto_max_height and self.auto_max_width:
            self.max_height, self.max_width = self.max_physical()
        elif self.auto_max_height:
            self.max_height = self.max_physical()[0]
        elif self.auto_max_width:
            self.max_width = self.max_physical()[1]

        self.height = self.max_height
        self.width = self.max_width

        self.create_pad()
        self.resize()
        for containee in self.contained:
            containee._resize()
        #self._after_resizing_contained()
        self.DISPLAY()

    @asyncio.coroutine
    def main(self):
        pass