import sys
import os  
import engine_main # type: ignore
import engine # type: ignore
import engine_io # type: ignore
import engine_draw # type: ignore
import engine_resources # type: ignore
import math
from time import ticks_ms
from engine_nodes import Sprite2DNode, CameraNode, Text2DNode, Rectangle2DNode # type: ignore
from engine_math import Vector2 # type: ignore

sys.path.append("Games/ColourDash")
os.chdir("Games/ColourDash")

# engine_draw.set_background_color(engine_draw.Color(0.0,0.0,1.0))
r = False
def RGB888to565(c):
    return ((c[0]>>3)<<11) | ((c[1]>>2)<<5) | c[2]>>3

bg = Sprite2DNode(texture = engine_resources.TextureResource("Images/bg.bmp"), layer = 0)
bgcolour = Rectangle2DNode(color = engine_draw.Color(0.0,0.0,0.0), opacity = 0.5, width = 128, height = 128, layer = 1)
Font = engine_resources.FontResource("Font/pixelatedPusab.bmp")
title = Text2DNode(Vector2(0,-16),Font,"ColourDash",0.0,Vector2(0.55,0.55),1.0,0.0,0.0,engine_draw.Color(1.0,1.0,1.0), layer = 2)
Button = Sprite2DNode(Vector2(0,29), engine_resources.TextureResource("Images/startButton.bmp"), engine_draw.Color(1.0,0.0,1.0), layer = 2)
camera = CameraNode()

while True:
    if engine.tick():
        t = ticks_ms()/5
        colour = RGB888to565([
        int(math.sin(math.radians(t*1.2+50)/5)*100+127),
        int(math.sin(math.radians(t+150)/5)*100+127),
        int(math.sin(math.radians(t*1.1)/5)*100+127)])
        bgcolour.color = colour
        if engine_io.LB.is_just_pressed:
            import gamelevel
            gamelevel.platformer = True
            r = True
        if engine_io.A.is_just_pressed:
            import gamelevel
            r = True
        if r and not gamelevel.running:
            break