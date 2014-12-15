import unicurses as uc
import sys
from map import Tile, Map
from enum import HexDir, Terrain, Key
from painter import Painter
import globals as glob


class Game(object):
    def __init__(self):            
        #Create debugging display
        debug_win = uc.newwin(15, 30, 0, 0)
        uc.box(debug_win)
        uc.wmove(debug_win, 1, 1)
        uc.waddstr(debug_win, "Debug:")
        uc.wmove(debug_win, 2, 1)

        debug_pnl = uc.new_panel(debug_win)
        uc.move_panel(debug_pnl, glob.CAM_HEIGHT, 32)

        #Generate the world
        world_map = Map(glob.N_HEX_ROWS, glob.N_HEX_COLS, debug_win)

        #map_height: 3 + 2*(rows-1) + 2 for border
        #map_width: 5 + 4*cols + 2 for border
        map_win = uc.newwin(glob.CAM_HEIGHT, glob.CAM_WIDTH, 0, 0)


        painter = Painter(glob.N_HEX_ROWS, glob.N_HEX_COLS, map_win)
        painter.updateAllTiles(world_map)

        #Put world window into a panel
        map_pnl = uc.new_panel(map_win)
        uc.move_panel(map_pnl, 1, 1)

        uc.top_panel(debug_pnl)

        status_win = uc.newwin(10, 30, 0, 0)
        uc.box(status_win)
        uc.wmove(status_win, 1, 1)
        uc.waddstr(status_win, "Turn " + str(world_map.turn))

        status_pnl = uc.new_panel(status_win)
        uc.move_panel(status_pnl, glob.CAM_HEIGHT, 2)

        info_win = uc.newwin(10, 30, 0, 0)
        uc.box(info_win)
        uc.wmove(info_win, 1, 1)
        uc.waddstr(info_win, "Tile Info")

        info_pnl = uc.new_panel(info_win)
        uc.move_panel(info_pnl, glob.CAM_HEIGHT, 62)

        painter.drawWindow()
        showChanges()


        #input loop
        while True:
            sys.stdout.flush()
            ch = uc.getch()
            uc.waddstr(debug_win, str(ch))
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
            elif ch == uc.KEY_UP:
                painter.moveCamera(0, -1*glob.CAM_SPEED)
            elif ch == uc.KEY_DOWN:
                painter.moveCamera(0, glob.CAM_SPEED)
            elif ch == uc.KEY_LEFT:
                painter.moveCamera(-1*glob.CAM_SPEED, 0)
            elif ch == uc.KEY_RIGHT:
                painter.moveCamera(glob.CAM_SPEED, 0)
                
                
                
def showChanges():
    uc.update_panels()
    uc.doupdate()

def incrementTurn(world, status, painter):
    uc.wmove(status, 1, 1)
    uc.waddstr(status, "Turn " + str(world.turn))

    worker_old = world.entities[0].my_tile

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
            incrementTurn(world, status, painter)


            tile = world.tileAt(pos_x, pos_y)
            #update position on tile map
            tile.has_player = False
            _tile.has_player = True
            #update to window
            painter.updateTileCenter(tile)
            painter.updateTileCenter(_tile)

            painter.drawWindow()

            showChanges()
