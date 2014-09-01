import __builtin__
import random
from enum import Dir, Terrain, Vegetation


class Tile():
    def __init__(self,x,y,terrain=Terrain.WATER,veg=Vegetation.NONE):
        self.pos = (x,y)
        
        self.terrain = terrain
        self.vegetation = veg
        
        self.has_player = False
        
        #used in various pathfinding/gen algorithms
        self.visited = False
        
class Map():
    def __init__(self, rows, cols):
        self.width = cols
        self.height = rows
        self.turn = 1
        
        self.tiles = list()
        num_tiles = rows*cols + rows/2
        
        for row in range(rows):
            for col in range(cols):
                self.tiles.append(Tile(col, row))
            #odd rows have an extra column
            if row % 2 != 0:
                self.tiles.append(Tile(cols, row))
                
        #choose a random tile to place player
        #more likely to be towards center
        player_x = int( random.triangular(0,cols))
        player_y = int( random.triangular(0,rows))
        player_tile = self.tileAt(player_x, player_y)
        player_tile.has_player = True
        
        #Player location is flatland
        player_tile.terrain = Terrain.FLAT
        self.generateSnakyLandmassAround(player_tile.pos[0],player_tile.pos[1])
        self.resetVisited()
        self.generateForests()
    
    #returns tile at position on hex map
    def tileAt(self, x,y):
        idx = y*self.width + y/2 + x
        return self.tiles[idx]
    
    #returns a list of all neighboring tiles
    def neighborsOf(self, x,y):
        ls = list()
        for dir in range(Dir.FIRST, Dir.LAST):
            pos = self.neighborAt(x,y, dir)
            if pos:
                ls.append(self.tileAt(pos[0],pos[1]))
            
        return ls
    
    #returns tile coordinates if neighbor exists, else None
    def neighborAt(self, x,y, dir):
        pos_x, pos_y = self.tileAt(x,y).pos
        
        _x = -1
        _y = -1
        
        if (dir == Dir.UL):
            if (pos_y != 0):
                if (pos_x > 0 or (pos_y % 2 == 0)):
                    if pos_y % 2 == 0:
                        _x = pos_x
                    else:
                        _x = pos_x-1
                    _y = pos_y-1
        elif (dir == Dir.UR):
            if (pos_y > 0):
                if(pos_x < self.width):
                    if pos_y % 2 == 0:
                        _x = pos_x + 1
                    else:
                        _x = pos_x
                    _y = pos_y-1              
        elif (dir == Dir.L):
            if (pos_x > 0):
                _x = pos_x-1
                _y = pos_y
        elif (dir == Dir.R):
            if (pos_y % 2 == 0):
                bound = self.width-1
            else:
                bound = self.width
            if (pos_x < bound):
                _x = pos_x+1
                _y = pos_y
        elif (dir == Dir.DL):
            if (pos_y < self.height-1):
                if(pos_x >0 or pos_y %2 == 0):
                    if pos_y %2 == 0:
                        _x = pos_x
                    else:
                        _x = pos_x-1
                    _y = pos_y + 1
        elif (dir == Dir.DR):
            if (pos_y < self.height-1):
                if (pos_x < self.width):
                    if (pos_y %2 == 0):
                        _x = pos_x +1
                    else:
                        _x = pos_x
                    _y = pos_y +1
        
        if (_x>-1 and _y>-1):
            return [_x,_y]
        else:
            return None
    
    def notVisited(self,tile):
        return not tile.visited
        
    def resetVisited(self):
        for tile in self.tiles:
            tile.visited = False
       
    #currently acting as a DFS, resulting in snaky continents
    # try switching to BFS for more bulky continents
    def generateSnakyLandmassAround(self, x,y, gen_chance=100.0):
        this_tile = self.tileAt(x,y)
        this_tile.visited = True
        
        if random.uniform(0,99.9) < gen_chance:
            this_tile.terrain = Terrain.FLAT
            gen_chance -= 0.5
            neighbors = self.neighborsOf(x,y)
                            
            for tile in neighbors:
                if not tile.visited:
                    self.generateLandmassAround(tile.pos[0],tile.pos[1],gen_chance)
    
    
    #iterative iteration that produces more bulky landmasses
    def generateLandmassAround(self, x,y, gen_chance= 100.0):
        this_tile = self.tileAt(x,y)
        this_tile.visited = True
        
        gen_list = self.neighborsOf(x,y)
        temp_list = list()
        
        while gen_list:
            #set all these tiles to visited
            #and give them a chance to be added to landmass
            for tile in gen_list:
                tile.visited = True
                
                if random.uniform(0, 99.9) < gen_chance:
                    tile.terrain = Terrain.FLAT
                    temp_list += self.neighborsOf(tile.pos[0], tile.pos[1])
            
            gen_list += temp_list
            #prune visited from list
            gen_list = filter(self.notVisited, gen_list)
            
            gen_chance -= 7.0
            
    def generateForests(self):
        gen_chance = 5.0
        land = __builtin__.filter(self.isFlat, self.tiles)
        
        
        for tile in land:
            if random.uniform(0, 100.0) < gen_chance:
                tile.vegetation = Vegetation.FOREST
            
            
    def isWater(self,tile):
        return tile.terrain == Terrain.WATER
    
    def isFlat(self,tile):
        return tile.terrain == Terrain.FLAT
            
    
    
                    
        
        