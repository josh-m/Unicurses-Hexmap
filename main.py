from unicurses import *
from map import Tile, Map
from enum import *
from painter import Painter

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

def drawChanges():
    update_panels()
    doupdate()
    
def incrementTurn(world,status):
    world.turn += 1
    wmove(status,1,1)
    waddstr(status, "Turn " + str(world.turn))
    
    drawChanges()
    
def movePlayer(dir, world, window, status, painter):
    searching = True
    for tile in world.tiles:
        if tile.has_player:
            pos_x, pos_y = tile.pos 
            searching = False
        if not searching:
            break
    
    _pos = world.neighborAt(pos_x, pos_y, dir)
    
    if _pos:
        _tile = world.tileAt(_pos[0], _pos[1])
    
        if _tile.terrain != Terrain.WATER:
            #increment turn
            incrementTurn(world,status)
            
            tile = world.tileAt(pos_x, pos_y)
            #update position on tile map
            tile.has_player = False
            _tile.has_player = True
            #draw to window
            painter.drawCharOnTile(tile, " ", window)
            painter.drawCharOnTile(_tile, "@", window)
            

                          
def main():
    stdscr = initscr()

    noecho()
    curs_set(False)
    keypad(stdscr, True)
        
    #Get world parameters (currently hardcoded, later user-supplied)
    N_ROWS = 25
    N_COLS = 30
    
    #Generate the world
    world_map = Map(N_ROWS,N_COLS)

    #map_height: 3 + 2*(rows-1) + 2 for border
    #map_width: 5 + 4*cols + 2 for border
    map_win = newwin(5+2*(N_ROWS-1), 7+4*N_COLS, 0,0)
    
    painter = Painter()

    painter.drawTiles(world_map, map_win) 
    
    #Put world window into a panel
    map_pnl = new_panel(map_win)
    move_panel(map_pnl,1,1)
    
    top_panel(map_pnl)
    
    status_win = newwin (10,30,0,0)
    box(status_win)
    wmove(status_win, 1,1,)
    waddstr(status_win, "Turn " + str(world_map.turn))
    
    status_pnl = new_panel(status_win)
    move_panel(status_pnl, 5+2*(N_ROWS-1) -1 , 2)
    
    drawChanges()
    
    
    #input loop
    running = True
    while running:
        ch = getch()
        if ch == Key.ESC:
            running = False
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
            incrementTurn(world_map, status_win)
        
    
    endwin()
    
if __name__ == "__main__":
    main()

    
