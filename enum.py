class Terrain():
    WATER = 0
    FLAT = 1
    MOUNTAIN = 2
    
class Vegetation():
    NONE = 0
    FOREST = 1
      
class HexDir:
    FIRST = 0
    UL = 0
    UR = 1
    L = 2
    R = 3
    DL = 4
    DR = 5
    LAST = 6
    
class Behavior:
    IDLE = 0
    WANDER = 1
    TRAVEL = 2