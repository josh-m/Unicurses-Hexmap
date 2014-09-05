# coding=UTF-8

import __builtin__
from unicurses import *
from enum import Terrain, Vegetation

class Colors:
    I_WATER_BORDER = 1
    I_WATER_PLAYER = 2
    I_GRASS_BORDER = 3
    I_GRASS_PLAYER = 4
    I_GRASS_FOREST = 5
    I_GRASS_CITY = 6
    
    def __init__(self):
        start_color()
        init_pair(Colors.I_WATER_BORDER, COLOR_WHITE,COLOR_BLUE)
        init_pair(Colors.I_WATER_PLAYER, COLOR_RED, COLOR_BLUE)
        init_pair(Colors.I_GRASS_BORDER, COLOR_WHITE,COLOR_GREEN)
        init_pair(Colors.I_GRASS_PLAYER, COLOR_RED, COLOR_GREEN)
        init_pair(Colors.I_GRASS_FOREST, COLOR_GREEN, COLOR_GREEN)
        init_pair(Colors.I_GRASS_CITY, COLOR_CYAN, COLOR_GREEN)

        self.WATER_BORDER = color_pair(Colors.I_WATER_BORDER)
        self.WATER_PLAYER = color_pair(Colors.I_WATER_PLAYER) + A_BOLD
        self.GRASS_BORDER = color_pair(Colors.I_GRASS_BORDER)
        self.GRASS_PLAYER = color_pair(Colors.I_GRASS_PLAYER) + A_BOLD
        self.GRASS_FOREST = color_pair(Colors.I_GRASS_FOREST) + A_BOLD
        self.GRASS_CITY = color_pair(Colors.I_GRASS_CITY) + A_BOLD
      
class Painter():
    def __init__(self):
        start_color()
        self.colors = Colors()
        
    def drawTile(self,tile,window):
        x,y = tile.pos
        pos_x, pos_y = self.findCenterCoords(x,y)

        self.drawTileCenter(tile,window)
        self.drawTileEdges(tile,window)
        self.drawTileBorders(tile,window)

    def drawTileCenter(self,tile,window):
        x,y = tile.pos
        pos_x, pos_y = self.findCenterCoords(x,y)

        if tile.has_player:
            char = "@"
            color = self.colors.GRASS_PLAYER
        elif tile.has_worker:
            char = ";"
            color = self.colors.GRASS_CITY
        elif tile.has_city:
            char = "M"
            color = self.colors.GRASS_CITY
        else:
            if tile.vegetation == Vegetation.FOREST:
                char = "8"
                color = self.colors.GRASS_FOREST
            else:
                char = " "
                if tile.terrain == Terrain.WATER:
                    color = self.colors.WATER_BORDER
                else:
                    color = self.colors.GRASS_BORDER
        wmove(window, pos_y, pos_x)
        waddstr(window, char,color)
    
    def drawTileEdges(self,tile,window):
        if tile.vegetation == Vegetation.NONE:
            char = " "
        else: #if forest
            char = "8"
            
        if tile.terrain == Terrain.WATER:
            color = self.colors.WATER_BORDER
        else:
            color = self.colors.GRASS_FOREST
            
        pos_x, pos_y = self.findCenterCoords(tile.pos[0], tile.pos[1])
        wmove(window,pos_y-1,pos_x)
        waddstr(window, char,color)
        wmove(window,pos_y+1,pos_x)
        waddstr(window, char,color)
        wmove(window,pos_y,pos_x-1)
        waddstr(window, char,color)
        wmove(window,pos_y,pos_x+1)
        waddstr(window, char,color)        
        
    def drawTileBorders(self,tile,window):
        if tile.terrain == Terrain.WATER:
            color = self.colors.WATER_BORDER
        else:
            color = self.colors.GRASS_BORDER
        
        pos_x, pos_y = self.findCenterCoords(tile.pos[0], tile.pos[1])
        wmove(window,pos_y-1, pos_x-1)
        waddstr(window, "/", color)
        wmove(window,pos_y-1, pos_x+1)
        waddstr(window, "\\", color)
        wmove(window,pos_y, pos_x-2)
        waddstr(window, "|", color)
        wmove(window,pos_y, pos_x+2)
        waddstr(window, "|", color)
        wmove(window,pos_y+1, pos_x-1)
        waddstr(window, "\\", color)
        wmove(window,pos_y+1,pos_x+1)
        waddstr(window, "/", color)       
        
    def drawAllTiles(self, world, window):
        water = __builtin__.filter(world.isWater, world.tiles)
        grass = __builtin__.filter(world.isFlat, world.tiles)

        for tile in grass:
           self.drawTile(tile,window)
        for tile in water:
            self.drawTile(tile,window)
        
        box(window)
        
    def findCenterCoords(self,x,y):
        row = 2 + 2*y
        
        if y % 2 == 0:
            column = 5 + 4*x
        else:
            column = 3 + 4*x
            
        return [column, row]

    