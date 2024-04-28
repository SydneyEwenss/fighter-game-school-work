import pygame

pygame.font.init()

WIN_WIDTH = 640
WIN_HEIGHT = 480
TILE_SIZE = 32
FPS = 60

FONT = pygame.font.Font("Minecraft.ttf", 30)

PLAYER_LAYER = 4
GRASS_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 3

RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
BLUE = (0,0,255)

tilemap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BGGGGGG.B.....................B',
    'BGGGGGG.B.....................B',
    'BGGGGG..B................G....B',
    'BGGGG...B.....................B',
    'BGG.....B.....................B',
    'B..BBBBBB.....................B',
    'B..............P..............B',
    'B.............................B',
    'B.............................B',
    'B...........GGG...............B',
    'B.........GGGGGG..............B',
    'B........GGGGGGGG.............B',
    'B.........GGGGGG..............B',
    'B...........GGGG..............B',
    'B............G................B',
    'B.............................B',
    'B.............................B',
    'B.............................B',
    'BBBB...BB...BBB.........G.....B',
    'BB.B..B..B...B.........GGG....B',
    'BBBB.BBBBBB..B..........G.....B',
    'BB...B....B..B................B',
    'BB...B....B..B................B',
    'B.............................B',
    'BBBB.B...B.BBBB.B....B....BBBB.',
    'BB...BB.BB.B....B....B....B..B.',
    'BBBB.B.B.B.BBB..B....B....BBBB.',
    'B..B.B...B.B....B....B......BB.',
    'BBBB.B...B.BBBB.BBBB.BBBB.BBBB.',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]