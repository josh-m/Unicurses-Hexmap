# coding=UTF-8

import __builtin__
from unicurses import *
from enum import Terrain, Vegetation
import globals

def replaceChar(str,idx,char):
    _str = str[:idx] + char + str[idx+1:]
    return _str

class Colors:
    DEFAULT = 1
    WATER_BORDER = 2
    WATER_PLAYER = 3
    GRASS_BORDER = 4
    GRASS_PLAYER = 5
    GRASS_FOREST = 6
    GRASS_CITY = 7
    
    def __init__(self):
        start_color()
        init_pair(Colors.DEFAULT, COLOR_WHITE, COLOR_BLACK)
        init_pair(Colors.WATER_BORDER, COLOR_WHITE,COLOR_BLUE)
        init_pair(Colors.WATER_PLAYER, COLOR_RED, COLOR_BLUE)
        init_pair(Colors.GRASS_BORDER, COLOR_WHITE,COLOR_GREEN)
        init_pair(Colors.GRASS_PLAYER, COLOR_RED, COLOR_GREEN)
        init_pair(Colors.GRASS_FOREST, COLOR_GREEN, COLOR_GREEN)
        init_pair(Colors.GRASS_CITY, COLOR_CYAN, COLOR_GREEN)

        self.DEFAULT = color_pair(Colors.DEFAULT)
        self.WATER_BORDER = color_pair(Colors.WATER_BORDER)
        self.WATER_PLAYER = color_pair(Colors.WATER_PLAYER) + A_BOLD
        self.GRASS_BORDER = color_pair(Colors.GRASS_BORDER)
        self.GRASS_PLAYER = color_pair(Colors.GRASS_PLAYER) + A_BOLD
        self.GRASS_FOREST = color_pair(Colors.GRASS_FOREST) + A_BOLD
        self.GRASS_CITY = color_pair(Colors.GRASS_CITY) + A_BOLD

class Symbols:
    BLANK = ' '
    V_BORDER = '|'
    R_BORDER = '/'
    L_BORDER = '\\'
    PLAYER = '@'
    TREE = '8'
    CITY = 'M'
    WORKER = ';'

class Cell():
    def __init__(self, symbol, color):
        self.symbol = symbol
        self.color = color
      
      
class Painter():

    def __init__(self,rows,cols,window):
        start_color()
        self.colors = Colors()
        self.window = window
        box(self.window)
        
        self.cam_size = [globals.CAM_WIDTH, globals.CAM_HEIGHT]
        self.cam_pos = [0,0]
        
        #map_height: 3 + 2*(rows-1) + 2 for border
        #map_width: 5 + 4*cols + 2 for border        
        self.world_size = [5+4*cols, 3+2*(rows-1)]
        
        x = self.findCenterCoords(cols, 0)[0]+1
        y = self.findCenterCoords(0, rows)[1]

        self.cell_matrix = list()
        
        for k in range(y):
            _ls = list()
            for j in range(x):
               cell = Cell(Symbols.BLANK, Colors.DEFAULT)
               _ls.append(cell)
            self.cell_matrix.append(_ls)
        
    def updateTile(self,tile):
        self.updateTileCenter(tile)
        self.updateTileEdges(tile)
        self.updateTileBorders(tile)

    def updateTileCenter(self,tile):
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
        
        #update
        self.cell_matrix[pos_y][pos_x].symbol = char
        self.cell_matrix[pos_y][pos_x].color = color
        
        #draw
        #wmove(self.window, pos_y+1, pos_x+1)
        #waddstr(self.window, char,color)
        
    def updateTileEdges(self,tile):
        if tile.vegetation == Vegetation.NONE:
            char = " "
        else: #if forest
            char = "8"
            
        if tile.terrain == Terrain.WATER:
            color = self.colors.WATER_BORDER
        else:
            color = self.colors.GRASS_FOREST
            
        pos_x, pos_y = self.findCenterCoords(tile.pos[0], tile.pos[1])

        #update
        self.cell_matrix[pos_y-1][pos_x].symbol = char
        self.cell_matrix[pos_y-1][pos_x].color = color
        self.cell_matrix[pos_y+1][pos_x].symbol = char
        self.cell_matrix[pos_y+1][pos_x].color = color
        self.cell_matrix[pos_y][pos_x-1].symbol = char
        self.cell_matrix[pos_y][pos_x-1].color = color
        self.cell_matrix[pos_y][pos_x+1].symbol = char
        self.cell_matrix[pos_y][pos_x+1].color = color

        #draw
        """
        wmove(self.window,pos_y-1+1,pos_x+1)
        waddstr(self.window, char,color)
        wmove(self.window,pos_y+1+1,pos_x+1)
        waddstr(self.window, char,color)
        wmove(self.window,pos_y+1,pos_x-1+1)
        waddstr(self.window, char,color)
        wmove(self.window,pos_y+1,pos_x+1+1)
        waddstr(self.window, char,color)
        """
        
    def updateTileBorders(self,tile):
        if tile.terrain == Terrain.WATER:
            color = self.colors.WATER_BORDER
        else:
            color = self.colors.GRASS_BORDER
        
        pos_x, pos_y = self.findCenterCoords(tile.pos[0], tile.pos[1])

        #char cells
        self.cell_matrix[pos_y-1][pos_x-1].symbol = Symbols.R_BORDER
        self.cell_matrix[pos_y-1][pos_x-1].color = color
        self.cell_matrix[pos_y-1][pos_x+1].symbol = Symbols.L_BORDER
        self.cell_matrix[pos_y-1][pos_x+1].color = color
        self.cell_matrix[pos_y][pos_x-2].symbol = Symbols.V_BORDER
        self.cell_matrix[pos_y][pos_x-2].color = color
        self.cell_matrix[pos_y][pos_x+2].symbol = Symbols.V_BORDER
        self.cell_matrix[pos_y][pos_x+2].color = color
        self.cell_matrix[pos_y+1][pos_x-1].symbol = Symbols.L_BORDER
        self.cell_matrix[pos_y+1][pos_x-1].color = color
        self.cell_matrix[pos_y+1][pos_x+1].symbol = Symbols.R_BORDER
        self.cell_matrix[pos_y+1][pos_x+1].color = color
        
    def updateAllTiles(self, world):      
        water = __builtin__.filter(world.isWater, world.tiles)
        grass = __builtin__.filter(world.isFlat, world.tiles)

        for tile in grass:
           self.updateTile(tile)
        for tile in water:
            self.updateTile(tile)

    #returns char cell coordinate
    def findCenterCoords(self,x,y):
        row = (1 + 2*y)
        
        column = 4*x
        if y % 2 == 0:
            column += 4
        else:
            column += 2
            
        return [column, row]

    def moveCamera(self,x,y):
        if x > 0:
            #can full shift be made?
            if self.cam_pos[0] + globals.CAM_WIDTH -2 + x <= self.world_size[0]:
                self.cam_pos[0] += x
                self.drawWindow()
            #is the camera already at the border?
            elif not self.cam_pos[0] == self.world_size[0] - self.cam_size[0] + 2:
                self.cam_pos[0] = self.world_size[0] - self.cam_size[0] + 2
                self.drawWindow()
        elif x < 0:
            if self.cam_pos[0]+x >= 0:
                self.cam_pos[0] += x
                self.drawWindow()
            elif not self.cam_pos[0] == 0:
                self.cam_pos[0] = 0
                self.drawWindow()
            
        if y > 0:
            if self.cam_pos[1] + globals.CAM_HEIGHT -2 + y <= self.world_size[1]:
                self.cam_pos[1] += y
                self.drawWindow()
            elif not self.cam_pos[1] == self.world_size[1] - self.cam_size[1] + 2:
                self.cam_pos[1] = self.world_size[1] - self.cam_size[1] + 2
                self.drawWindow()
        elif y < 0:
            if self.cam_pos[1] + y >= 0:
                self.cam_pos[1] += y
                self.drawWindow()
            elif not self.cam_pos[1] == 0:
                self.cam_pos[1] = 0
                self.drawWindow()

    #redraws all tiles within camera
    def drawWindow(self):
        for x in range(self.cam_pos[0], self.cam_pos[0]+self.cam_size[0] -2):
            for y in range(self.cam_pos[1], self.cam_pos[1] + self.cam_size[1]-2):
                wmove(self.window,y-self.cam_pos[1]+1, x-self.cam_pos[0]+1)
                waddstr(self.window, self.cell_matrix[y][x].symbol, self.cell_matrix[y][x].color)
        
        self.showChanges()

    def showChanges(self):
        update_panels()
        doupdate()
        
        