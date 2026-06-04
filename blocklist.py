# Texture coordinates (x, y) in blocks.bmp spritesheet (6x6 grid)

BLOCK_DEFAULT = (0, 0)
GRIDBLOCK_1   = (1, 0)
GRIDBLOCK_2   = (2, 0)
GRIDBLOCK_3   = (3, 0)
GRIDBLOCK_4   = (4, 0)
GRIDBLOCK_5   = (5, 0)
GRIDBLOCK_6   = (0, 1)
BLOCK_HALF    = (4, 1)

SPIKE_NORMAL  = (1, 1)
SPIKE_FLAT    = (2, 1)
SPIKE_GROUND  = (3, 1)

JUMP_PAD      = (5, 1)
JUMP_ORB      = (0, 2)

PORTAL_GRAVITY_DOWN = (1, 2)
PORTAL_GRAVITY_UP   = (2, 2)
PORTAL_SHIP         = (4, 2)
PORTAL_CUBE         = (3, 2)

PORTAL_COORDS = [
    ("PORTAL_GRAVITY_DOWN", PORTAL_GRAVITY_DOWN),
    ("PORTAL_GRAVITY_UP",   PORTAL_GRAVITY_UP),
    ("PORTAL_SHIP",         PORTAL_SHIP),
    ("PORTAL_CUBE",         PORTAL_CUBE),
]

# --- GD object mapping ---
# Maps GD object ID -> ColourDash block data
# cord: (x, y) index into blocks.bmp spritesheet
# deadly: whether this object kills the player
# tag: block type tag

GD_OBJECT_MAP = {
    1:    {"cord": BLOCK_DEFAULT,       "deadly": False, "tag": "Block"},
    2:    {"cord": GRIDBLOCK_1,         "deadly": False, "tag": "Block"},
    3:    {"cord": GRIDBLOCK_2,         "deadly": False, "tag": "Block"},
    4:    {"cord": GRIDBLOCK_3,         "deadly": False, "tag": "Block"},
    5:    {"cord": GRIDBLOCK_4,         "deadly": False, "tag": "Block"},
    6:    {"cord": GRIDBLOCK_5,         "deadly": False, "tag": "Block"},
    7:    {"cord": GRIDBLOCK_6,         "deadly": False, "tag": "Block"},
    40:   {"cord": BLOCK_HALF,          "deadly": False, "tag": "Block"},
    8:    {"cord": SPIKE_NORMAL,        "deadly": True,  "tag": "Deadly"},
    1716: {"cord": SPIKE_GROUND,        "deadly": True,  "tag": "Deadly"},
    39:   {"cord": SPIKE_FLAT,          "deadly": True,  "tag": "Deadly"},
    10:   {"cord": PORTAL_GRAVITY_DOWN, "deadly": False, "tag": "Portal"},
    11:   {"cord": PORTAL_GRAVITY_UP,   "deadly": False, "tag": "Portal"},
    13:   {"cord": PORTAL_CUBE,         "deadly": False, "tag": "Portal"},
    12:   {"cord": PORTAL_SHIP,         "deadly": False, "tag": "Portal"},
}

# GD coordinate conversion constants
GD_UNIT = 30
CD_UNIT = 16
GD_GROUND_Y = 0
CD_GROUND_Y = 2

def gd_to_cd_pos(gd_x, gd_y):
    cd_x = int(gd_x / GD_UNIT + 0.5)
    cd_y = CD_GROUND_Y - round(gd_y / GD_UNIT)
    return cd_x, cd_y

def gd_to_cd_rot(gd_rot):
    if gd_rot is None or gd_rot == 0:
        return 0
    r = int(gd_rot) % 360
    if r > 180:
        r -= 360
    return r
