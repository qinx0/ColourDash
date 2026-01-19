import engine_main # type: ignore
import engine # type: ignore
from engine_nodes import Sprite2DNode # type: ignore
from engine_resources import TextureResource # type: ignore
from engine_math import Vector2 # type: ignore
import math
import engine_draw # type: ignore
from engine_draw import Color # type: ignore

rotDeg = [-90,-180,-270,90,180,270]
# exactRotRad = [-1.57079633,-3.14159265,-4.71238898,1.57079633,3.14159265,4.71238898]
#exactRotRad = [(math.pi)/2,(math.pi),(math.pi)/2,(math.pi)/2,(math.pi),(math.pi)/2]
exactRotRad = [(3*math.pi)/2,(3*math.pi),(3*math.pi)/2,(3*math.pi)/2,(3*math.pi),(3*math.pi)/2]
offsetRot = [Vector2(0,-1),Vector2(-1,-1),Vector2(0,-1),Vector2(-1,0),Vector2(-1,-1),Vector2(0,-1)]
#Offsets for rotation:
#-90: y -1 pixel
#-180: x -1 pixel y -1 pixel
#-270: y -1 pixel
#90: x -1 pixel
#180: y -1 pixel x -1 pixel
#270: y -1 pixel
radRotrounding = 1
#rouding radian rotation check:
#1 decimal: nope
portals = [Vector2(1,2),Vector2(2,2),Vector2(3,2),Vector2(4,2)]

blocks = TextureResource("Images/blocks.bmp")
portalsimg = TextureResource("Images/portals.bmp")

def centredTextPrintout(Text, width):
    padding = (width - len(Text)) // 2
    line = "-" * padding + Text + "-" * padding
    return line

# blocks
class block:
    def __init__(self, cord, pos, deadly, portal, tag, rot):
        if not isinstance(cord, Vector2) or not isinstance(pos, Vector2) or not isinstance(tag, str):
            raise TypeError("'cord' and 'pos' must be of type 'Vector2'")
        self.cord = cord
        self.pos = pos
        self.deadly = deadly
        self.tag = tag
        self.rot = rot
        self.scale = Vector2(1,1)
        self.portal = portal

        self.pos.x = self.pos.x * 16# - 8
        self.pos.y = self.pos.y * 16 + 5

        # Cool little printout
        print(centredTextPrintout("Block Info", 75))

        # Correct rotation and position offset to be accurate
        if self.rot in rotDeg:
            if self.rot > 0:
                print(f'Changed rot from: {rot} to {exactRotRad[rotDeg.index(rot)]}, Math.radians would return: {math.radians(self.rot)}')
                if self.rot == 270:
                    self.scale.y = -1
                    self.scale.x = -1
                    print("Rotation is 270; flipped the y and x")
            else:
                print(f'Changed rot from: {rot} to {exactRotRad[rotDeg.index(rot)]}, Math.radians would return: {math.radians(self.rot)}')
                if self.rot == -90: self.scale.x = -1; self.scale.y = -1
            self.rot = exactRotRad[rotDeg.index(rot)]
            self.pos.x += offsetRot[rotDeg.index(rot)].x
            self.pos.y += offsetRot[rotDeg.index(rot)].y
        else: print("Rotation is 0, not offsetting")

            # Check if portal and change sprite accordingly
        if self.cord in portals and self.tag == "Portal":
            self.portal = True
            if portals.index(cord) - 1 > 1:
                self.cord.x = portals.index(cord) - 2
                self.cord.y = 1
            else:
                self.cord.x = portals.index(cord) - 1
                self.cord.y = 0
            # else: self.portal = False
                
            # print(f'Changed rot from: {rot} to {round(exactRotRad[rotDeg.index(rot)],radRotrounding)} rounded to {radRotrounding}, Math.radians would return: {math.radians(self.rot)}')
            # self.rot = round(exactRotRad[rotDeg.index(rot)],radRotrounding)
            
            # pos -= offsetRot[i-1]

        # self.rot = math.radians(rot)
         
                
        self.Block = getBlock(self.cord, self.portal)
        self.Block.position = self.pos
        self.Block.rotation = self.rot
        self.Block.scale = self.scale
        print("---------------------------------------------------------------------------")
        print(f'Block rotation is {self.Block.rotation}')
        print(f'Block scale is (x{self.Block.scale.x}, y{self.Block.scale.y})')
        print(f'Portal: {self.portal}')
        print(f'Block texture Coords: (x{self.cord.x}, y{self.cord.y})')
        print("---------------------------------------------------------------------------\n")
        
        def __repr__(self):
            return f"block(cord={self.cord}, pos={self.pos})"
        
def getBlock(cord, portal):
    if portal == True:
        b = Sprite2DNode(texture=portalsimg, frame_count_x=2, frame_count_y=2, transparent_color = Color(1,0,1), playing=False)
    else:
        b = Sprite2DNode(texture=blocks, frame_count_x=6, frame_count_y=6, transparent_color = Color(1,0,1), playing=False)
    b.frame_current_x = int(cord.x)
    b.frame_current_y = int(cord.y)
    return b