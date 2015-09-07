#encoding: utf-8

"""
The application module supplies the Application object, which provides the core
utilities for running an application with gruepy.
"""

import asyncio
import logging
import os
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

    def run(self):
        """
        """
        os.environ['PYTHONASYNCIODEBUG'] = 1
        logging.basicConfig(level=logging.DEBUG)
        try:
            stdscr = init_curses(escape_delay=self.escape_delay,
                                 use_mouse=self.use_mouse)
            self.loop.call_until_complete(self.main())
        finally:
            self.loop.close()
            end_curses(stdscr)

    def add_workspace(self, workspace_class, workspace_id, *args, **kwargs):
        """
        Create a workspace of the given class. workspace_id should be a string
        which will uniquely identify the workspace. *args and **kwargs will be
        passed to the workspace constructor.
        """
        workspace = workspace_class(parent_app=self,
                                    #keypress_timeout=self.keypress_timeout_default,
                                    *args,
                                    **kwargs)
        self.workspaces[workspace_id] = workspace_id
        return weakref.proxy(workspace)

    def remove_workspace(self, workspace_id):
        del self.workspaces[workspace_id].parent_app
        del self.workspaces[workspace_id]

    def get_workspace(self, workspace_id):
        workspace = self.workspaces[workspace_id]
        try:
            return weakref.proxy(workspace)
        except:
            return workspace

    def set_next_workspace(self, workspace_id):
        """
        Set the workspace that will be selected when the current one exits.
        """
        self.next_active_workspace = workspace_id

    #def switch_workspace(self, workspace_id):
        #"""
        #Immediately switch to the workspace specified by workspace_id.
        #"""
        #self._THISFORM.editing = False
        #self.set_next_form(workspace_id)
        #self.switch_form_now()

    @asyncio.coroutine
    def main(self):
        """
        This function starts the application. It is usually called indirectly
        through the `run` method.
        You should not override this function, but override the
        `on_in_main_loop`, `on_start` and `on_clean_exit` methods instead, if
        you need to modify the application's behaviour.
        """

        self.on_start()
        while self.next_active_workspace is not None:
            self.active_workspace = self.workspaces[self.next_active_workspace]
            self.active_workspace._resize()

            self.on_in_main_loop()
        self.on_clean_exit()

    def on_in_main_loop(self):
        """
        Called between each screen while the application is running. Not called
        before the first screen. Override at will.
        """
        pass

    def on_start(self):
        """
        Override this method to perform any initialisation.
        """
        pass

    def on_clean_exit(self):
        """
        Override this method to perform any cleanup when application is exiting
        without error.
        """
        pass