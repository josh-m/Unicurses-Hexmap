"""
enum.py

Defines various enumerated types used throughout the application.
100% Pylint compliant. Gee-whiz!
"""

def enum(**enums):
    """Usage: Foo = enum(KEY1=VAL1, ...)"""
    return type('Enum', (), enums)

Key = enum(
    ENTER=10, #This value may not work on all platforms.
    ESC=27,
    SPACE=32,
    Q=113,
    W=119,
    A=97,
    S=115,
    Z=122,
    X=120,
    E=101,
    R=114,
    D=100,
    F=102,
    G=103)

Terrain = enum(
    WATER=0,
    FLAT=1,
    MOUNTAIN=2)

Vegetation = enum(
    NONE=0,
    FOREST=1)

HexDir = enum(
    FIRST=0,
    UL=0,
    UR=1,
    L=2,
    R=3,
    DL=4,
    DR=5,
    LAST=6)

Behavior = enum(
    IDLE=0,
    WANDER=1,
    TRAVEL=2)

Platform = enum(
    UNDEFINED=-1,
    UNIX=0,
    WINDOWS=1)
