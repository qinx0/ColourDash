"""
gmd_to_level.py
Desktop tool to convert a Geometry Dash .gmd file into ColourDash's level.json format.

Usage:
    pip install gmdkit
    python gmd_to_level.py mylevel.gmd level.json

GD coordinates use 30px units. ColourDash uses a 16px grid.
GD Y axis is inverted (positive = up), ColourDash Y is positive = down.
The ground in ColourDash is at y=2 (after 16px scaling + offset).
"""

import json
import sys
from gmdkit import Level
from gmdkit.mappings import obj_prop

# --- Sprite mapping ---
# Maps GD object ID -> ColourDash block data
# cord: [x, y] index into blocks.bmp spritesheet (6x6 grid)
# deadly: whether this object kills the player
# tag: block type tag
#
# To add more objects, find the GD object ID and map it here.
# GD 1.0 common IDs:
#   1   = basic block
#   2   = dirt block  
#   3   = stone block
#   6   = short spike (up)
#   7   = medium spike
#   8   = tall spike
#   9   = small cube decoration
#   10  = medium cube decoration
#   35  = gravity portal (up)
#   36  = gravity portal (down)
#   12  = ship portal
#   13  = ball portal

GD_OBJECT_MAP = {
    1:  {"cord": [1, 0], "deadly": False, "tag": "Block"},
    2:  {"cord": [2, 0], "deadly": False, "tag": "Block"},
    3:  {"cord": [3, 0], "deadly": False, "tag": "Block"},
    6:  {"cord": [1, 1], "deadly": True,  "tag": "Deadly"},
    7:  {"cord": [1, 1], "deadly": True,  "tag": "Deadly"},
    8:  {"cord": [1, 1], "deadly": True,  "tag": "Deadly"},
    35: {"cord": [1, 2], "deadly": False, "tag": "Portal"},
    36: {"cord": [2, 2], "deadly": False, "tag": "Portal"},
    12: {"cord": [3, 2], "deadly": False, "tag": "Portal"},
    13: {"cord": [4, 2], "deadly": False, "tag": "Portal"},
}

# GD ground baseline in GD units (objects at y=0 sit on the ground floor)
GD_UNIT = 30        # GD uses 30px per grid unit
CD_UNIT = 16        # ColourDash uses 16px per grid unit
GD_GROUND_Y = 0     # GD ground level in GD units
CD_GROUND_Y = 2     # ColourDash ground row in grid units

def gd_to_cd_pos(gd_x, gd_y):
    """
    Convert GD absolute pixel coords to ColourDash grid units.
    GD Y is positive=up, ColourDash Y is positive=down.
    GD starts levels at x=0, ColourDash at x=-4 (roughly).
    """
    cd_x = round(gd_x / GD_UNIT) - 4
    cd_y = CD_GROUND_Y - round(gd_y / GD_UNIT)
    return cd_x, cd_y

def gd_to_cd_rot(gd_rot):
    """Convert GD rotation degrees to ColourDash rotation value."""
    if gd_rot is None or gd_rot == 0:
        return 0
    # GD and ColourDash both use degrees, just pass through
    # ColourDash handles: -90, -180, -270, 90, 180, 270
    r = int(gd_rot) % 360
    if r > 180:
        r -= 360
    return r

def convert(gmd_path, output_path):
    print(f"Loading {gmd_path}...")
    level = Level.from_file(gmd_path)
    objects = level.objects

    print(f"Found {len(objects)} objects, converting...")
    
    skipped = 0
    output = []

    for obj in objects:
        obj_id = obj.get(obj_prop.ID)
        if obj_id not in GD_OBJECT_MAP:
            skipped += 1
            continue

        mapping = GD_OBJECT_MAP[obj_id]

        gd_x = obj.get(obj_prop.X, 0)
        gd_y = obj.get(obj_prop.Y, 0)
        gd_rot = obj.get(obj_prop.ROTATION, 0)
        gd_flip_x = obj.get(obj_prop.FLIP_X, False)

        cd_x, cd_y = gd_to_cd_pos(gd_x, gd_y)
        cd_rot = gd_to_cd_rot(gd_rot)
        if gd_flip_x:
            cd_rot = -cd_rot  # mirror rotation for flipped objects

        entry = [
            f"Vector2({mapping['cord'][0]},{mapping['cord'][1]})",
            f"Vector2({cd_x},{cd_y})",
            mapping["deadly"],
            mapping["tag"] == "Portal",
            mapping["tag"],
            cd_rot
        ]
        output.append(entry)

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=4)

    print(f"Done! Converted {len(output)} objects, skipped {skipped} unsupported objects.")
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python gmd_to_level.py <input.gmd> <output.json>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
