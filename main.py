from unicurses import *
import os
import sys
import __builtin__
from collections import deque
import subprocess

from map import Tile, Map
from enum import *
from painter import Painter

import globals

class Key:
    ESC = 27
    SPACE = 32
    Q = 113
    W = 119
    A = 97
    S = 115
    Z = 122
    X = 120
    E = 101
    R = 114
    D = 100
    F = 102
    G = 103

def showChanges():
    update_panels()
    doupdate()
    
def incrementTurn(world,status,painter):
    wmove(status,1,1)
    waddstr(status, "Turn " + str(world.turn))

    worker_old =world.entities[0].my_tile

    world.doTurn()
    
    worker_new = world.entities[0].my_tile
    painter.updateTileCenter(worker_old)
    painter.updateTileEdges(worker_old)
    painter.updateTileCenter(worker_new)
    
    painter.drawWindow()
    
    showChanges()
    
def movePlayer(dir, world, window, status, painter):
    for tile in world.tiles:
        if tile.has_player:
            pos_x, pos_y = tile.pos
            break
    
    _pos = world.neighborAt(pos_x, pos_y, dir)
    
    if _pos:
        _tile = world.tileAt(_pos[0], _pos[1])
    
        if _tile.terrain != Terrain.WATER:
            #increment turn
            incrementTurn(world,status,painter)
            

            tile = world.tileAt(pos_x, pos_y)
            #update position on tile map
            tile.has_player = False
            _tile.has_player = True
            #update to window
            painter.updateTileCenter(tile)
            painter.updateTileCenter(_tile)
            
            painter.drawWindow()
            
            showChanges()
                     
def main():
    platform = os.name

    #resize terminal (WINDOWS SPECIFIC)
    if platform == "nt":
        os.system("mode con cols="+str(globals.CAM_WIDTH)+" lines="+str(globals.CAM_HEIGHT+15))
    elif platform == "posix":
        #UNIX SPECIFIC
        sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=globals.CAM_HEIGHT, cols=globals.CAM_WIDTH))
    
    #init curses
    stdscr = initscr()
    noecho()
    curs_set(False)
    keypad(stdscr, True)
        
    #Get world parameters (currently hardcoded, later user-supplied)
    N_ROWS = 45
    N_COLS = 55
    
    #Create debugging display
    debug_win = newwin(15,30,0,0)
    box(debug_win)
    wmove(debug_win, 1,1)
    waddstr(debug_win, "Debug:")
    wmove(debug_win, 2,1)

    debug_pnl = new_panel(debug_win)
    move_panel(debug_pnl, globals.CAM_HEIGHT,32)

    #Generate the world
    world_map = Map(N_ROWS,N_COLS,debug_win)

    #map_height: 3 + 2*(rows-1) + 2 for border
    #map_width: 5 + 4*cols + 2 for border
    map_win = newwin(globals.CAM_HEIGHT,globals.CAM_WIDTH, 0,0)
    
       
    painter = Painter(N_ROWS,N_COLS,map_win)
    painter.updateAllTiles(world_map) 
    
    #Put world window into a panel
    map_pnl = new_panel(map_win)
    move_panel(map_pnl,1,1)
    
    top_panel(debug_pnl)
    
    status_win = newwin (10,30,0,0)
    box(status_win)
    wmove(status_win, 1,1,)
    waddstr(status_win, "Turn " + str(world_map.turn))
    
    status_pnl = new_panel(status_win)
    move_panel(status_pnl, globals.CAM_HEIGHT, 2)
    
    info_win = newwin(10,30,0,0)
    box(info_win)
    wmove(info_win, 1,1)
    waddstr(info_win, "Tile Info")
    
    info_pnl = new_panel(info_win)
    move_panel(info_pnl, globals.CAM_HEIGHT, 62)
    
    painter.drawWindow()
    showChanges()

    
    #input loop
    while True:
        sys.stdout.flush()
        ch = getch()
        #Exit Key
        if ch == Key.ESC:
            break
        #Movement Keys
        elif ch == Key.E:
            movePlayer(HexDir.UL, world_map, map_win, status_win, painter)
        elif ch == Key.R:
            movePlayer(HexDir.UR, world_map, map_win, status_win, painter)
        elif ch == Key.S:
            movePlayer(HexDir.L, world_map, map_win, status_win, painter)
        elif ch == Key.G:
            movePlayer(HexDir.R, world_map, map_win, status_win, painter)
        elif ch == Key.D:
            movePlayer(HexDir.DL, world_map, map_win, status_win, painter)
        elif ch == Key.F:
            movePlayer(HexDir.DR, world_map, map_win, status_win, painter)
        #End Turn Key
        elif ch == Key.SPACE:
            incrementTurn(world_map, status_win, painter)
        #Camera Scrolling Keys
        #TBD: Remaining order checks
        elif ch == KEY_UP:
            painter.moveCamera(0,-1*globals.CAM_SPEED)
        elif ch == KEY_DOWN:
            painter.moveCamera(0,globals.CAM_SPEED)
        elif ch == KEY_LEFT:
            painter.moveCamera(-1*globals.CAM_SPEED,0)
        elif ch == KEY_RIGHT:
            painter.moveCamera(globals.CAM_SPEED,0)
    
    endwin()
    
if __name__ == "__main__":
    main()
