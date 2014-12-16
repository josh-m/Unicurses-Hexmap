import unicurses as uc
import os
import sys
import atexit
import time

import term_size

import globals as glob
from enum import Platform
from title import Title
from game import Game


def main():
    determineOS()
    if glob.platform == Platform.UNDEFINED:
        print "Your operating system is not supported.\n"
        return -1

    glob.orig_shell_x, glob.orig_shell_y = term_size.getTerminalSize()

    #atexit.register(clean_screen)

    resizeTerminal(True)

    initCurses()

    #Run the title screen
    title_screen = Title()

    #Get world parameters
    #Breaks when world is smaller than screen (min size: 34x34)
    world_size = title_screen.getWorldSize()
    if world_size == "Small":
        glob.N_HEX_ROWS = 34
        glob.N_HEX_COLS = 34
    elif world_size == "Average":
        glob.N_HEX_ROWS = 50
        glob.N_HEX_COLS = 50
    elif world_size == "Large":
        glob.N_HEX_ROWS = 120
        glob.N_HEX_COLS = 100
    else:
        print "Error getting world size."
        sys.exit()

    #Run the game.
    Game()

    #Close unicurses
    uc.endwin()

"""
determineOS()
Determines the current operating system.
Sets a global OS code, as defined in enum.Platform.
"""
def determineOS():
    os_name = os.name

    if os_name == "nt":
        glob.platform = Platform.WINDOWS
    elif os_name == "posix":
        glob.platform = Platform.UNIX
    else:
        glob.platform = Platform.UNDEFINED

"""
resizeTerminal(os_code)
Resizes the terminal using the appropriate method for the current platform.
Expects os_code to be valid and supported.

entering is a bool to decided whether to resize to the game's required
dimensions or to return to the dimensions before the application started
"""
def resizeTerminal(entering):
    os_code = glob.platform

    if entering:
        x,y = glob.SCREEN_WIDTH, glob.SCREEN_HEIGHT
    else:
        x,y = glob.orig_shell_x, glob.orig_shell_y


    if os_code == Platform.WINDOWS:
        os.system("mode con cols="+str(x) +
                    " lines="+str(y))
    elif os_code == Platform.UNIX:
        sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=y,
                                                        cols=x))
    else:
        print "resizeTerminal: Called with invalid os_code!\n"



"""
initCurses():
Initializes the curses library.
"""
def initCurses():
    stdscr = uc.initscr()
    uc.noecho()
    uc.curs_set(False)
    uc.keypad(stdscr, True)
    uc.start_color()

def clean_screen():
    if (glob.BAD_EXIT):
        time.sleep(5)
    resizeTerminal(False)
    os.system('clear' if glob.platform == Platform.UNIX else 'cls')



if __name__ == "__main__":
    #try:
    main()
    """except SystemExit as e:
        #Normal Exit
        None
    except:
        glob.BAD_EXIT=True"""