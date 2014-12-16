
import globals as glob
import unicurses as uc

class TileWindow(object):
    def __init__(self):
        self.win = uc.newwin(10, 30, 0, 0)
        uc.box(self.win)
        uc.wmove(self.win, 1, 1)
        uc.waddstr(self.win, "Tile Info")

        panel = uc.new_panel(self.win)
        uc.move_panel(panel, glob.CAM_HEIGHT, 62)
        
    #writes a list of strings to the window
    def write(self, strings):
        row = 2
        for s in strings:
            s +=(" " * (28-len(s))) #fill extra with spaces
            uc.wmove(self.win, row, 1)
            uc.waddstr(self.win, s)
            row +=1
        #clear the remaining rows
        filler_str = " "*28
        for i in range(row, 10):
            uc.wmove(self.win, row, 1)
            uc.waddstr(self.win, filler_str) 