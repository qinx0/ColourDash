"""
gmd_to_level.py
Desktop tool to convert a Geometry Dash .gmd file into ColourDash's level.json format.

Usage:
    pip install gmdkit
    python gmd_to_level.py mylevel.gmd level.json
"""

import json
import sys
from gmdkit import Level
from gmdkit.mappings import obj_prop

# GD_OBJECT_MAP, GD_UNIT, CD_UNIT, GD_GROUND_Y, CD_GROUND_Y,
# gd_to_cd_pos(), and gd_to_cd_rot() are all in blocklist.py
import blocklist

def convert(gmd_path, output_path):
    print(f"Loading {gmd_path}...")
    level = Level.from_file(gmd_path)
    objects = level.objects

    print(f"Found {len(objects)} objects, converting...")
    
    skipped = 0
    skippedN = []
    output = []

    for obj in objects:
        obj_id = obj.get(obj_prop.ID)
        if obj_id not in blocklist.GD_OBJECT_MAP:
            skipped += 1
            skippedN.append(str(obj_id))
            continue

        mapping = blocklist.GD_OBJECT_MAP[obj_id]

        gd_x = obj.get(obj_prop.X, 0)
        gd_y = obj.get(obj_prop.Y, 0)
        gd_rot = obj.get(obj_prop.ROTATION, 0)
        gd_flip_x = obj.get(obj_prop.FLIP_X, False)

        cd_x, cd_y = blocklist.gd_to_cd_pos(gd_x, gd_y)
        cd_rot = blocklist.gd_to_cd_rot(gd_rot)
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
    if len(skippedN) > 0:
        print(f"Skipped: {skippedN}")
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python gmd_to_level.py <input.gmd> <output.json>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
