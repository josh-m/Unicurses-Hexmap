from enum import Behavior, Vegetation

class Worker(object):
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