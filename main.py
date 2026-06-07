import sys
import os  
import engine_main
import engine_save
import engine
import engine_io
import engine_draw
import engine_resources
import math
from time import ticks_ms
from engine_nodes import Sprite2DNode, CameraNode, Rectangle2DNode
from engine_math import Vector2
from outlinedText import OutlinedTextNode

if sys.platform != "rp2":
    sys.path.append("Games/ColourDash")
    os.chdir("Games/ColourDash")
# engine_save._init_saves_dir("/Saves/ColourDash")

import gamelevel

engine_save._init_saves_dir("/Saves/ColourDash")
engine_save.set_location("options.data")
h = engine_save.load("hitbox_visual", False) # Hitboxes
p = engine_save.load("platformer", False) # Platformer

def RGB888to565(c):
    return ((c[0]>>3)<<11) | ((c[1]>>2)<<5) | c[2]>>3

bg = Sprite2DNode(texture = engine_resources.TextureResource("Images/bg.bmp"), layer = 0)
bgcolour = Rectangle2DNode(color = engine_draw.Color(0.0,0.0,0.0), opacity = 0.5, width = 128, height = 128, layer = 1)
Font = engine_resources.FontResource("Font/pixelatedPusab.bmp")
# title = Text2DNode(Vector2(0,-16),Font,"ColourDash",0.0,Vector2(0.55,0.55),1.0,0.0,0.0,engine_draw.Color(1.0,1.0,1.0), layer = 2)
title = OutlinedTextNode(
    Vector2(0,-16),
    Font,
    "ColourDash",
    Vector2(0.55,0.55),
    engine_draw.Color(1.0,1.0,1.0),
    engine_draw.Color(0.0,0.0,0.0),
    layer = 2
)
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
            p = not p
            engine_save.save("platformer", int(p))
            print(f"Platformer is {p}")
        if engine_io.RB.is_just_pressed:
            h = not h
            engine_save.save("hitbox_visual", int(h))
            print(f"Hitbox visuals are {h}")
        if engine_io.A.is_just_pressed:
            bg.opacity = 0.0
            bgcolour.opacity = 0.0
            title.opacity = 0.0
            Button.opacity = 0.0
            gamelevel.main_loop(camera)
            camera.position = Vector2(0, 0)
            bg.opacity = 1.0
            bgcolour.opacity = 0.5
            title.opacity = 1.0
            Button.opacity = 1.0
