#coding = UTF-8

from unicurses import *
from map import Tile, Map
from enum import *
from painter import Painter

import os
import __builtin__
from collections import deque



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
    

    
def incrementTurn(world,status,painter,window):
    wmove(status,1,1)
    waddstr(status, "Turn " + str(world.turn))

    worker_old =world.entities[0].my_tile

    world.doTurn()
    
    worker_new = world.entities[0].my_tile
    painter.drawTileCenter(worker_old, window)
    painter.drawTileEdges(worker_old, window)
    painter.drawTileCenter(worker_new, window)
    
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
            incrementTurn(world,status,painter,window)
            

            tile = world.tileAt(pos_x, pos_y)
            #update position on tile map
            tile.has_player = False
            _tile.has_player = True
            #draw to window
            painter.drawTileCenter(tile, window)
            painter.drawTileCenter(_tile, window)
            
            showChanges()
            
             
def main():
    #resize terminal (WINDOWS SPECIFIC)
    os.system("mode con cols=140 lines=80")
    
    stdscr = initscr()

    noecho()
    curs_set(False)
    keypad(stdscr, True)
        
    #Get world parameters (currently hardcoded, later user-supplied)
    N_ROWS = 25
    N_COLS = 30
    
    debug_win = newwin(15,30,0,0)
    box(debug_win)
    wmove(debug_win, 1,1)
    waddstr(debug_win, "Debug:")
    wmove(debug_win, 2,1)

    debug_pnl = new_panel(debug_win)
    move_panel(debug_pnl, 5+2*(N_ROWS-1) -1, 32)

    #Generate the world
    world_map = Map(N_ROWS,N_COLS,debug_win)

    #map_height: 3 + 2*(rows-1) + 2 for border
    #map_width: 5 + 4*cols + 2 for border
    map_win = newwin(5+2*(N_ROWS-1), 7+4*N_COLS, 0,0)
    
    painter = Painter()

    painter.drawTiles(world_map, map_win) 
    
    #Put world window into a panel
    map_pnl = new_panel(map_win)
    move_panel(map_pnl,1,1)
    
    top_panel(debug_pnl)
    
    status_win = newwin (10,30,0,0)
    box(status_win)
    wmove(status_win, 1,1,)
    waddstr(status_win, "Turn " + str(world_map.turn))
    
    status_pnl = new_panel(status_win)
    move_panel(status_pnl, 5+2*(N_ROWS-1) -1 , 2)


    
    showChanges()
    
    
    #input loop
    while True:
        ch = getch()
        if ch == Key.ESC:
            break
        elif ch == Key.E:
            movePlayer(Dir.UL, world_map, map_win, status_win, painter)
        elif ch == Key.R:
            movePlayer(Dir.UR, world_map, map_win, status_win, painter)
        elif ch == Key.S:
            movePlayer(Dir.L, world_map, map_win, status_win, painter)
        elif ch == Key.G:
            movePlayer(Dir.R, world_map, map_win, status_win, painter)
        elif ch == Key.D:
            movePlayer(Dir.DL, world_map, map_win, status_win, painter)
        elif ch == Key.F:
            movePlayer(Dir.DR, world_map, map_win, status_win, painter)
        elif ch == Key.SPACE:
            incrementTurn(world_map, status_win, painter, map_win)
        
    
    endwin()
    
if __name__ == "__main__":
    main()
