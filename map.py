import __builtin__
import random
from enum import HexDir, Terrain, Vegetation, Behavior

import unicurses


class Worker():
    def __init__(self,tile,world):
        self.world = world
        self.my_tile = tile
        self.behavior = Behavior.TRAVEL
        self.path = self.world.findPath(tile, world.hasForest)
        
    def doTurn(self):
        if self.behavior == Behavior.TRAVEL:
            if len(self.path) > 0:
                self.world.tileAt(self.my_tile.pos[0],self.my_tile.pos[1]).has_worker = False
                new_tile = self.path.pop()
                self.world.tileAt(new_tile.pos[0],new_tile.pos[1]).has_worker = True
                self.my_tile = new_tile
            else:
                if self.my_tile.has_city:#travel to a forest
                    self.path = self.world.findPath(self.my_tile, self.world.hasForest)
                else:#cut forest, travel to the city
                    self.my_tile.vegetation = Vegetation.NONE
                    self.path = self.world.findPath(self.my_tile, self.world.hasCity)
                
                #idle if no path was found
                if len(self.path) == 0:
                    self.behavior = Behavior.IDLE
                       
class Tile():
    def __init__(self,x,y,terrain=Terrain.WATER,veg=Vegetation.NONE):
        self.pos = (x,y)
        
        self.terrain = terrain
        self.vegetation = veg
        
        self.has_player = False
        self.has_worker = False
        
        self.has_city = False
        
        #used in various pathfinding/gen algorithms
        self.visited = False
        self.depth = -1
 
class Map():
    def __init__(self, rows, cols, debug):
        self.db = debug
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
        
        #Place player
        #choose a random tile to place player
        #more likely to be towards center
        player_x = int( random.triangular(0,cols))
        player_y = int( random.triangular(0,rows))
        player_tile = self.tileAt(player_x, player_y)
        player_tile.has_player = True
        
        #Player location is flatland
        player_tile.terrain = Terrain.FLAT
        self.generateLandmassAround(player_tile.pos[0],player_tile.pos[1])
        self.resetVisited()
        
        self.generateForests()
        
        #Place City
        land = __builtin__.filter(self.isClear, self.tiles)
        idx = random.randint(0,len(land)-1)
        city_tile = land[idx]
        city_tile.has_city = True
        worker = Worker(city_tile,self)
        city_tile.has_worker=True

        self.entities = [worker]
    
    def doTurn(self):
        self.turn += 1
        for entity in self.entities:
            entity.doTurn()
        
        #unicurses.waddstr(self.db, str(entity.my_tile.pos[0]) +',' +str(entity.my_tile.pos[1])+'\n')
        
    #returns tile at position on hex map
    def tileAt(self, x,y):
        idx = y*self.width + y/2 + x
        return self.tiles[idx]
    
    #returns a list of all neighboring tiles
    def neighborsOfPos(self, x,y):
        ls = list()
        for dir in range(HexDir.FIRST, HexDir.LAST):
            pos = self.neighborAt(x,y, dir)
            if pos:
                ls.append(self.tileAt(pos[0],pos[1]))
            
        return ls
    
    def neighborsOf(self, tile):        
        return self.neighborsOfPos(tile.pos[0], tile.pos[1])
    
    #returns tile coordinates if neighbor exists, else None
    def neighborAt(self, x,y, dir):
        pos_x, pos_y = self.tileAt(x,y).pos
        
        _x = -1
        _y = -1
        
        if (dir == HexDir.UL):
            if (pos_y != 0):
                if (pos_x > 0 or (pos_y % 2 == 0)):
                    if pos_y % 2 == 0:
                        _x = pos_x
                    else:
                        _x = pos_x-1
                    _y = pos_y-1
        elif (dir == HexDir.UR):
            if (pos_y > 0):
                if(pos_x < self.width):
                    if pos_y % 2 == 0:
                        _x = pos_x + 1
                    else:
                        _x = pos_x
                    _y = pos_y-1              
        elif (dir == HexDir.L):
            if (pos_x > 0):
                _x = pos_x-1
                _y = pos_y
        elif (dir == HexDir.R):
            if (pos_y % 2 == 0):
                bound = self.width-1
            else:
                bound = self.width
            if (pos_x < bound):
                _x = pos_x+1
                _y = pos_y
        elif (dir == HexDir.DL):
            if (pos_y < self.height-1):
                if(pos_x >0 or pos_y %2 == 0):
                    if pos_y %2 == 0:
                        _x = pos_x
                    else:
                        _x = pos_x-1
                    _y = pos_y + 1
        elif (dir == HexDir.DR):
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
        if (not tile.visited) and tile.depth == -1:
            return True
        else:
            return False
        
    def resetVisited(self):
        for tile in self.tiles:
            tile.visited = False
       
    def resetDepth(self):
        for tile in self.tiles:
            tile.depth = -1
       
    #currently acting as a DFS, resulting in snaky continents
    # try switching to BFS for more bulky continents
    def generateSnakyLandmassAround(self, x,y, gen_chance=100.0):
        this_tile = self.tileAt(x,y)
        this_tile.visited = True
        
        if random.uniform(0,99.9) < gen_chance:
            this_tile.terrain = Terrain.FLAT
            gen_chance -= 0.5
            neighbors = self.neighborsOf(this_tile)
                            
            for tile in neighbors:
                if not tile.visited:
                    self.generateSnakyLandmassAround(tile.pos[0],tile.pos[1],gen_chance)
    
    
    #iterative iteration that produces more bulky landmasses
    def generateLandmassAround(self, x,y, gen_chance= 100.0):
        this_tile = self.tileAt(x,y)
        this_tile.visited = True
        
        gen_list = self.neighborsOf(this_tile)
        temp_list = list()
        
        while gen_list:
            #set all these tiles to visited
            #and give them a chance to be added to landmass
            for tile in gen_list:
                tile.visited = True
                
                if random.uniform(0, 99.9) < gen_chance:
                    tile.terrain = Terrain.FLAT
                    temp_list += self.neighborsOf(tile)
            
            gen_list += temp_list
            #prune visited from list
            gen_list = filter(self.notVisited, gen_list)
            
            gen_chance -= 7.0
            
    def generateForests(self):
        gen_chance = 3.0
        land = __builtin__.filter(self.isFlat, self.tiles)
              
        for tile in land:
            if (random.uniform(0, 100.0) < gen_chance) and (tile.vegetation == Vegetation.NONE):
                tile.vegetation = Vegetation.FOREST
                self.spreadForest(tile)
                self.resetVisited()
    
    def spreadForest(self, tile, gen_chance=90.0):
        tile.visited = True
        
        if (random.uniform(0,100.0) < gen_chance):
            tile.vegetation = Vegetation.FOREST
        
            neighbors = self.neighborsOf(tile)
            neighbors = __builtin__.filter(self.isFlat, neighbors)
            neighbors = __builtin__.filter(self.notVisited, neighbors)
            
            for tile in neighbors:
                self.spreadForest(tile, gen_chance-20.0)
        
    def isWater(self,tile):
        return tile.terrain == Terrain.WATER
    
    def isFlat(self,tile):
        return tile.terrain == Terrain.FLAT
            
    def isClear(self,tile):
        if tile.terrain == Terrain.FLAT:
            if tile.vegetation == Vegetation.NONE:
                if not tile.has_player:
                    return True
        return False
        
    def hasWorker(self,tile):
        return tile.has_worker
        
    def hasForest(self,tile):
        return tile.vegetation == Vegetation.FOREST
        
    def hasCity(self,tile):
        return tile.has_city
        
    #returns a tile that fits property,
    #modifies depth properties of tiles
    #part 1 of shortest path algo
    def findTile(self, src, has_property):
        depth = 0
        src.depth = depth
        found = False
        ls = [src]
        
        while not found:
            depth += 1
            _ls = []
            
            for tile in ls: 
                children = self.neighborsOf(tile)
                children = __builtin__.filter(self.isFlat, children)
                children = __builtin__.filter(self.notVisited, children)
                for child in children:
                    child.depth = depth
                    if has_property(child):
                        found = True
                        return child
                        
                _ls += children
        
            ls = _ls
            
            if len(ls) == 0:    
                return None
    
    
    def findPath(self, src, has_property):
        curr = self.findTile(src, has_property)
        if curr == None:
            return list()
            
        path = [curr]
        
        f = lambda t:  t.depth == (curr.depth-1)
        
        #find neighbor of dst with appropriate depth
        while True:
            neighbors = self.neighborsOf(curr)
            neighbors = __builtin__.filter(f, neighbors)
            
            i = random.randint(0,len(neighbors)-1)
            curr = neighbors[i]
            path.append(curr)
            
            if curr.depth == 0:
                path.pop()
                self.resetDepth()
                return path

