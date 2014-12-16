import unicurses as uc
import sys
from map import Tile, Map
from enum import HexDir, Terrain, Key
from painter import Painter
from tilewindow import TileWindow
import globals as glob


class Game(object):
    def __init__(self):
        self.turn =1
        
        #Create debugging display
        debug_win = uc.newwin(15, 30, 0, 0)
        uc.box(debug_win)
        uc.wmove(debug_win, 1, 1)
        uc.waddstr(debug_win, "Debug:")
        uc.wmove(debug_win, 2, 1)

        debug_pnl = uc.new_panel(debug_win)
        uc.move_panel(debug_pnl, glob.CAM_HEIGHT, 32)

        #Generate the world
        self.world = Map(glob.N_HEX_ROWS, glob.N_HEX_COLS, debug_win)

        #map_height: 3 + 2*(rows-1) + 2 for border
        #map_width: 5 + 4*cols + 2 for border
        map_win = uc.newwin(glob.CAM_HEIGHT, glob.CAM_WIDTH, 0, 0)


        self.painter = Painter(glob.N_HEX_ROWS, glob.N_HEX_COLS, map_win)
        self.painter.updateAllTiles(self.world)

        #Put world window into a panel
        map_pnl = uc.new_panel(map_win)
        uc.move_panel(map_pnl, 1, 1)

        uc.top_panel(debug_pnl)

        self.status_win = uc.newwin(10, 30, 0, 0)
        uc.box(self.status_win)
        uc.wmove(self.status_win, 1, 1)
        uc.waddstr(self.status_win, "Turn " + str(self.turn))

        status_pnl = uc.new_panel(self.status_win)
        uc.move_panel(status_pnl, glob.CAM_HEIGHT, 2)

        self.tile_window = TileWindow()

        self.painter.drawWindow()
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
                self.movePlayer(HexDir.UL)
            elif ch == Key.R:
                self.movePlayer(HexDir.UR)
            elif ch == Key.S:
                self.movePlayer(HexDir.L)
            elif ch == Key.G:
                self.movePlayer(HexDir.R)
            elif ch == Key.D:
                self.movePlayer(HexDir.DL)
            elif ch == Key.F:
                self.movePlayer(HexDir.DR)
            #End Turn Key
            elif ch == Key.SPACE:
                self.incrementTurn()
            #Camera Scrolling Keys
            #TBD: Remaining order checks
            elif ch == uc.KEY_UP:
                self.painter.moveCamera(0, -1*glob.CAM_SPEED)
            elif ch == uc.KEY_DOWN:
                self.painter.moveCamera(0, glob.CAM_SPEED)
            elif ch == uc.KEY_LEFT:
                self.painter.moveCamera(-1*glob.CAM_SPEED, 0)
            elif ch == uc.KEY_RIGHT:
                self.painter.moveCamera(glob.CAM_SPEED, 0)
            #Toggle drawing borders
            elif ch == Key.B:
                self.painter.draw_borders = not self.painter.draw_borders
                self.painter.updateAllTileBorders(self.world)
                self.painter.drawWindow()
                
    #TODO: This needs to become moveCursor
    def movePlayer(self, dir):
        for tile in self.world.tiles:
            if tile.has_player:
                pos_x, pos_y = tile.pos
                break

        _pos = self.world.neighborAt(pos_x, pos_y, dir)

        if _pos:
            _tile = self.world.tileAt(_pos[0], _pos[1])

            if _tile.terrain != Terrain.WATER:
                tile = self.world.tileAt(pos_x, pos_y)
                #update position on tile map
                tile.has_player = False
                _tile.has_player = True
                #update to window
                self.painter.updateTileCenter(tile)
                self.painter.updateTileCenter(_tile)

                self.painter.drawWindow()

                #update Tile Info Panel
                tile_list = _tile.getInfo()
                self.tile_window.write(tile_list)
                
                #increment turn
                self.incrementTurn()
                
    def incrementTurn(self):
        self.turn +=1
        
        uc.wmove(self.status_win, 1, 6) #6 is pos after string "Turn "
        uc.waddstr(self.status_win, str(self.turn))

        worker_old = self.world.entities[0].my_tile

        self.world.moveEntities()

        worker_new = self.world.entities[0].my_tile
        self.painter.updateTileCenter(worker_old)
        self.painter.updateTileEdges(worker_old)
        self.painter.updateTileCenter(worker_new)

        self.painter.drawWindow()

        showChanges()
                
def showChanges():
    uc.update_panels()
    uc.doupdate()


