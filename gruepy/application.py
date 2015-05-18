# -*- coding: utf-8 -*-

"""
The application module supplies the Application object, which provides the core
utilities for running an application with gruepy.
"""

import asyncio
from .curses_helpers import init_curses, end_curses

class Application(object):
    """
    The basic object of a gruepy application.
    """

    def __init__(self,
                 escape_delay=None,
                 use_mouse=True,
                 ):

        self.escape_delay = escape_delay
        self.use_mouse = use_mouse

        self.loop = asyncio.get_event_loop()

    def run(self):
        """
        """
        try:
            init_curses(escape_delay=self.escape_delay, use_mouse=self.use_mouse)
            self.loop.call_until_complete(self.main())
        finally:
            self.loop.close()
            end_curses()

    @asyncio.coroutine
    def main(self):
        """
        """
        pass
