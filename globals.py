from enum import Platform

CAM_HEIGHT = 70
CAM_WIDTH = 140
CAM_SPEED = 13

SCREEN_HEIGHT = CAM_HEIGHT+15
SCREEN_WIDTH = CAM_WIDTH

platform = Platform.UNDEFINED

orig_shell_x, orig_shell_y = None, None

N_HEX_ROWS, N_HEX_COLS = 0,0

BAD_EXIT = False