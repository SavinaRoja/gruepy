#encoding: utf-8

"""

"""

import curses
import locale
import os


def init_curses(escape_delay=None, use_mouse=True):
    """
    """
    #The ESCDELAY environment variable controls how long curses waits in getch
    #to see if the Esc Key is being used for an escape sequence. If ESCDELAY is
    #not set then it will wait 1s, this is commonly an annoyance.
    if escape_delay is None:
        if 'ESCDELAY' not in os.environ:
            os.environ['ESCDELAY'] = '10'  # A 10ms delay as default
    else:
        os.environ['ESCDELAY'] = str(escape_delay)

    #Initialize our curses environment
    #return_code = None
    locale.setlocale(locale.LC_ALL, '')
    stdscr = curses.initscr()
    try:
        curses.start_color()
    except:
        pass
    #These lines might be redundant after curses.initscr()?
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)

    if use_mouse:
        curses.mousemask(curses.ALL_MOUSE_EVENTS)

    return stdscr


def end_curses(stdscr):
    """
    """
    stdscr.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()

