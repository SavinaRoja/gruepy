#encoding: utf-8

"""
The application module supplies the Application object, which provides the core
utilities for running an application with gruepy.
"""

import asyncio
from concurrent.futures import CancelledError
import curses
from functools import partial
import logging
import os
import datetime
import weakref

from .curses_helpers import init_curses, end_curses


class Application(object):
    """
    The basic object of a gruepy application.
    """

    STARTING_WORKSPACE = "MAIN"

    def __init__(self,
                 escape_delay=None,
                 use_mouse=True,
                 *args,
                 **kwargs):

        self.escape_delay = escape_delay
        self.use_mouse = use_mouse

        self.workspaces = {}

        self.loop = asyncio.get_event_loop()

        self.main_future = None

    def run(self):
        """
        """
        os.environ['PYTHONASYNCIODEBUG'] = '1'
        try:
            stdscr = init_curses(escape_delay=self.escape_delay,
                                 use_mouse=self.use_mouse)
            main_task = asyncio.async(self.main())

            user_input_task = asyncio.async(self.user_input())
            tasks = [main_task,
                     user_input_task]

            self.main_future = main_task

            done, pending = self.loop.run_until_complete(
                    asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))

            #Clean up the pending coroutine tasks
            try:
                self.loop.run_until_complete(asyncio.gather(*pending))
            except CancelledError:
                pass
            self.loop.stop()
        finally:
            self.loop.close()
            end_curses(stdscr)

    @asyncio.coroutine
    def main(self):
        self.curses_pad = curses.newpad(24, 80)
        self.addstr(0, 0, 'Press keys and mouse to test. Esc to quit.')
        self.loop.call_soon(self.show_time)
        while not self.main_future.cancelled():
            yield from asyncio.sleep(0.1)

    def addstr(self, row, col, string, refresh=True):
        self.curses_pad.addstr(row, col, string)
        if refresh:
            self.curses_pad.refresh(0, 0, 0, 0, 23, 79)

    def show_time(self):
        self.addstr(1, 0, str(datetime.datetime.now()))
        self.loop.call_soon(self.show_time)

    def print_ch(self, message):
        self.addstr(2, 0, ' ' * 80, refresh=False)
        self.addstr(2, 0, 'Character received: ' + repr(message))

    @asyncio.coroutine
    def get_wch(self):
        curses.raw()
        curses.cbreak()
        self.curses_pad.timeout(10)
        self.curses_pad.keypad(1)
        try:
            ch = self.curses_pad.get_wch()
        except curses.error:
            pass
        else:
            return ch

    @asyncio.coroutine
    def user_input(self):
        while not self.main_future.cancelled():
            curses.raw()
            curses.cbreak()
            curses.meta(1)
            event = yield from asyncio.async(self.get_wch())
            if event is None:
                continue
            if event == curses.KEY_MOUSE:
                self.loop.call_soon(partial(self.mouse_event_handler,
                                            *curses.getmouse()))
            else:
                self.loop.call_soon(partial(self.key_event_handler, event))

    def quit(self):
        self.main_future.cancel()

    def key_event_handler(self, event):
        handlers = {'\x1b': self.quit}
        if event in handlers:
            handlers[event]()
        else:
            self.print_ch(event)

    def mouse_event_handler(self, short_id, x, y, z, bstate):
        self.addstr(2, 0, ' ' * 80, refresh=False)
        self.addstr(2, 0, 'Mouse: ' + repr((short_id, x, y, z, bstate)))
