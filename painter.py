import __builtin__
from unicurses import *
from enum import Terrain

class ColorPair:
    WATER = 5
    GRASS = 6
    WATER_BORDER = 1
    GRASS_BORDER = 2
    GRASS_PLAYER = 3
    GRASS_FOREST = 4
    
class Painter():
    def __init__(self):
        start_color()
        init_pair(ColorPair.WATER, COLOR_WHITE,COLOR_BLUE)
        init_pair(ColorPair.GRASS, COLOR_WHITE,COLOR_GREEN)
        
    def firstDrawCharOnTile(self,tile,char,window, attr=A_NORMAL):
        x,y = tile.pos
        pos_x, pos_y = self.findCenter(x,y)
     
        if tile.terrain == Terrain.WATER:
            this_color = ColorPair.WATER
        elif tile.terrain == Terrain.FLAT:
            this_color = ColorPair.GRASS
            
        wmove(window, pos_y, pos_x)
        waddstr(window, char, color_pair(this_color) + attr)
        
        wmove(window,pos_y-1,pos_x)
        waddstr(window, " ", color_pair(this_color) + attr)
        wmove(window,pos_y+1,pos_x)
        waddstr(window, " ", color_pair(this_color) + attr)
        wmove(window,pos_y,pos_x-1)
        waddstr(window, " ", color_pair(this_color) + attr)
        wmove(window,pos_y,pos_x+1)
        waddstr(window, " ", color_pair(this_color) + attr)
        
        wmove(window,pos_y +1,pos_x+1)
        waddstr(window, "/", color_pair(this_color) + attr)
        wmove(window,pos_y-1, pos_x+1)
        waddstr(window, "\\", color_pair(this_color) + attr)
        wmove(window,pos_y, pos_x+2)
        waddstr(window, "|", color_pair(this_color) + attr)
        wmove(window,pos_y, pos_x-2)
        waddstr(window, "|", color_pair(this_color) + attr)
        wmove(window,pos_y+1, pos_x-1)
        waddstr(window, "\\", color_pair(this_color) + attr)
        wmove(window,pos_y-1, pos_x-1)
        waddstr(window, "/", color_pair(this_color) + attr)
        
    #incomplete
    def drawTileBorders(self,tile,window,attr=A_NORMAL):
        pos_x, pos_y = tile.pos
        
    
    def drawCharOnTile(self,tile,char,window,attr = A_NORMAL):
        x,y = tile.pos
        pos_x, pos_y = self.findCenter(x,y)
     
        if tile.terrain == Terrain.WATER:
            this_color = ColorPair.WATER
        elif tile.terrain == Terrain.FLAT:
            this_color = ColorPair.GRASS
        wmove(window, pos_y, pos_x)
        waddstr(window, char, color_pair(this_color) + attr)
        
        update_panels()
        doupdate()
        
    def findCenter(self,x,y):
        row = 2 + 2*y
        
        if y % 2 == 0:
            column = 5 + 4*x
        else:
            column = 3 + 4*x
            
        return [column, row]

    
    def drawTiles(self, world, window):
 
        water = __builtin__.filter(world.isWater, world.tiles)
        grass = __builtin__.filter(world.isFlat, world.tiles)

        for tile in grass:
            #Draw tile contents
            if tile.has_player:
                self.firstDrawCharOnTile(tile,"@",window)
                pos = self.findCenter(tile.pos[0],tile.pos[1])
                move(pos[1]+1,pos[0]+1)
            else:
                self.firstDrawCharOnTile(tile," ",window)
        
        for tile in water:
            #Draw tile contents
            if tile.has_player:
                self.firstDrawCharOnTile(tile,"@",window)
                pos = findCenter(tile.pos[0],tile.pos[1])
                move(pos[1]+1,pos[0]+1)
            else:
                self.firstDrawCharOnTile(tile," ",window)
        
        box(window)
        update_panels()
        doupdate()