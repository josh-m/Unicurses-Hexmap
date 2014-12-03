from unicurses import *
from math import floor
from collections import namedtuple

from blockstrings import *
import globals as glob
from enum import Key,Platform
import sys

class Title():
    def __init__(self):
    #colors!
        init_pair(100, COLOR_WHITE, COLOR_BLACK) #Standard
        init_pair(101, COLOR_BLACK, COLOR_WHITE) #Selected
        
    
    #Create title display.
        title_rows = convert("civilization demake")
        title_win = newwin( len(title_rows), len(title_rows[0]), 0,0)
        for i in range( len(title_rows)):
            wmove(title_win,i,0)
            waddstr(title_win, title_rows[i])
        title_pnl = new_panel(title_win)
        move_panel(title_pnl, 5, glob.SCREEN_WIDTH/2 - len(title_rows[0])/2)

        start_info_str = "Press ENTER to begin."
        str_len = len(start_info_str)
        start_info_win = newwin(1, str_len, 0,0)
        waddstr(start_info_win, start_info_str)
        start_info_pnl = new_panel(start_info_win)
        move_panel(start_info_pnl, 14, glob.SCREEN_WIDTH/2 - str_len/2)
        
        
        
        world_size = Submenu(  "World Size",
                                ["Small","Average","Large"],
                                Position(int(glob.SCREEN_WIDTH*.25), 30) )
                                
        world_landmass = Submenu(  "World Landmass",
                                [   "Pangaea","Continents",
                                    "Islands"   ],
                                Position( int(glob.SCREEN_WIDTH*.5), 30)  )                   
        world_oceans = Submenu(  "Oceans Amount",
                                [   "Waterworld","Wet",
                                    "Half n' Half","Puddles"],
                                Position( int(glob.SCREEN_WIDTH*.75), 30)  )
        
        
        
        self.menu_group = MenuGroup()
        self.menu_group.add(world_size)
        self.menu_group.add(world_landmass)
        self.menu_group.add(world_oceans)
        
        showChanges()
        self.recieveInput()
        
    def recieveInput(self):
        #input loop
        while True:
            sys.stdout.flush()
            ch = getch()
            #Exit Key
            if ch == Key.ESC:
                sys.exit()
            #Movement Keys
            elif ch == Key.ENTER:
                break
            elif ch == KEY_UP or ch == KEY_DOWN:
                self.menu_group.scroll(ch)
                showChanges()
            elif ch == KEY_RIGHT or ch == KEY_LEFT:
                self.menu_group.shift(ch)
                showChanges()
        
Position = namedtuple('Position', 'x y')

"""Logical grouping of submenus"""
class MenuGroup:
    def __init__(self):
        self.menus = list()
    
    def add(self, menu):
        self.menus.append(menu)
        #first submenu
        if len(self.menus) == 1:
            self.active_menu = self.menus[0]
            menu.items[0].setActive(True)
            
    #scroll up or down through the current menu
    def scroll(self,key):
        if key == KEY_DOWN:
            self.active_menu.down()
        elif key == KEY_UP:
            self.active_menu.up()
        
        
    #move to the next menu in key dir
    def shift(self,key):
        idx = self.menus.index(self.active_menu)
        if key == KEY_RIGHT:
            if (idx != len(self.menus)-1):
                self.active_menu.activeToSelected()
                self.active_menu = self.menus[idx+1]
                self.active_menu.selected_item.setActive(True)
        elif key == KEY_LEFT:
            if idx != 0:
                self.active_menu.activeToSelected()
                self.active_menu = self.menus[idx-1]
                self.active_menu.selected_item.setActive(True)
    
    

class Submenu:
    spacing = 0
    def __init__(self, title, options, pos):
        self.items = list()
        self.width = max_len(options)+2
        self.pos = pos
        
        title_win = newwin(1,len(title),0,0)
        waddstr(title_win, title)
        self.title_pnl = new_panel(title_win)
        
        for option in options:
            item = Button(option, self.width)
            self.items.append(item)
        self.items[0].setSelected(True)
        self.selected_item = self.items[0]
        
        move_panel(self.title_pnl, pos.y, pos.x)
        
        y = pos.y
        for item in self.items:
            y += Submenu.spacing +3
            move_panel(item.panel, y, self.pos.x)
    
    def down(self):
        idx = self.items.index(self.selected_item)
        if idx != len(self.items)-1:
            self.selected_item.setActive(False)
            
            self.selected_item = self.items[idx+1]
            self.selected_item.setActive(True)
            
    def up(self):
        idx = self.items.index(self.selected_item)
        if idx != 0:
            self.selected_item.setActive(False)
            
            self.selected_item = self.items[idx-1]
            self.selected_item.setActive(True)
            
    def activeToSelected(self):
        self.selected_item.setActive(False)
        self.selected_item.setSelected(True)
        
class Button:
    def __init__(self, text, width):
        self.selected = False
        self.active = False
        
        self.text = text
        self.width = width
   
        self.window = newwin(3, width, 0,0)
        self.panel = new_panel(self.window)
        
        box(self.window)
        self.writeText()
    
    def writeText(self):
        wmove(  self.window,
                1,
                int(floor(self.width/2.0 - len(self.text)/2.0)) #tend towards the left
        )
        """
        if (self.active):
            waddstr(self.window,self.text, color_pair(1))
        else:
        """
        waddstr(self.window,self.text)
        
    
    def setActive(self, bool):
        self.active = bool
        if (bool):
            wbkgd(self.window,color_pair(101))
            box(self.window)
        else:
            wbkgd(self.window,color_pair(100))
    
    def setSelected(self, bool):
        self.selected = bool
        if (bool):
            box(self.window, color_pair(101))
        else:
            box(self.window, color_pair(100))

"""returns the length of the longest string in the list"""
def max_len(strings):
    max = 0
    for str in strings:
        n = len(str)
        if n > max:
            max = n
    return max
    
def showChanges():
    update_panels()
    doupdate()