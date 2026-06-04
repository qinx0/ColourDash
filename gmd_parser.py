import ubinascii, deflate, uio, ure
import blocklist
from blocks import block
from engine_math import Vector2

def parse_gmd_file(path):
    with open(path) as f:
        content = f.read()

    m = ure.search("<k>k4</k><s>([^<]+)</s>", content)
    if not m:
        raise ValueError("Could not find k4 data in .gmd file")
    raw = m.group(1)
    raw = raw.replace("-", "+").replace("_", "/")

    decoded = ubinascii.a2b_base64(raw)
    buf = uio.BytesIO(decoded)
    d = deflate.DeflateIO(buf, deflate.GZIP)
    text = d.read().decode("utf-8")
    d.close()
    buf.close()

    semi = text.find(";")
    if semi < 0:
        raise ValueError("No game data found (missing ; separator)")
    game_data = text[semi + 1:]

    objs = game_data.split(";")
    result = []
    for obj_str in objs:
        obj_str = obj_str.strip()
        if not obj_str:
            continue

        parts = obj_str.split(",")
        gd_id = None
        gd_x = 0
        gd_y = 0
        gd_rot = 0
        for i in range(0, len(parts) - 1, 2):
            key = parts[i]
            val = parts[i + 1]
            if key == "1":
                gd_id = int(float(val))
            elif key == "2":
                gd_x = float(val)
            elif key == "3":
                gd_y = float(val)
            elif key == "6":
                gd_rot = float(val)

        if gd_id is None or gd_id not in blocklist.GD_OBJECT_MAP:
            continue

        mapping = blocklist.GD_OBJECT_MAP[gd_id]
        cd_x, cd_y = blocklist.gd_to_cd_pos(gd_x, gd_y)
        cd_rot = blocklist.gd_to_cd_rot(gd_rot)

        b = block(
            Vector2(mapping["cord"][0], mapping["cord"][1]),
            Vector2(cd_x, cd_y),
            mapping["deadly"],
            mapping["tag"] == "Portal",
            mapping["tag"],
            cd_rot
        )
        result.append(b)

    return result
