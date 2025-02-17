import engine_main # type: ignore
import engine # type: ignore
from engine_nodes import Sprite2DNode # type: ignore
from engine_resources import TextureResource # type: ignore
from engine_math import Vector2 # type: ignore
import math
import engine_draw # type: ignore
from engine_draw import Color # type: ignore

offRot = [-90,-180,-270,90,180,270]
portals = [Vector2(2,1),Vector2(2,2),Vector2(2,3),Vector2(2,4)]

blocks = TextureResource("Images/blocks.bmp")
portalsimg = TextureResource("Images/portals.bmp")

# blocks
class block:
    def __init__(self, cord, pos, deadly, tag, rot):
        if not isinstance(cord, Vector2) or not isinstance(pos, Vector2) or not isinstance(tag, str):
            raise TypeError("'cord' and 'pos' must be of type 'Vector2'")
        self.cord = cord
        self.pos = pos
        self.deadly = deadly
        self.tag = tag
        self.rot = math.radians(rot)
                
        self.pos.x = self.pos.x * 16# - 8
        self.pos.y = self.pos.y * 16 + 5
        
        if self.cord in portals:
            print("PORTALLLL")
            self.portal = True
        elif self.cord not in portals:
            print("Not portal")
            self.portal = False
        
        self.Block = getBlock(cord, self.portal)
        self.Block.position = self.pos
        self.Block.rotation = self.rot
        
        def __repr__(self):
            return f"block(cord={self.cord}, pos={self.pos})"
        
def getBlock(cord, portal):
    if portal == True:
        b = Sprite2DNode(texture=portalsimg, frame_count_x=6, frame_count_y=6, transparent_color = Color(1,0,1), playing=False)
    else:
        b = Sprite2DNode(texture=blocks, frame_count_x=6, frame_count_y=6, transparent_color = Color(1,0,1), playing=False)
    b.frame_current_x = int(cord.x)
    b.frame_current_y = int(cord.y)
    return b