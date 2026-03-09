import engine # type: ignore
from engine_nodes import CameraNode, Sprite2DNode # type: ignore
from engine_resources import TextureResource, WaveSoundResource # type: ignore
import engine_io # type: ignore
import engine_draw # type: ignore
from engine_draw import Color # type: ignore
from engine_math import Vector2 # type: ignore
import engine_audio # type: ignore
import levelParser
print("start")

def colour(r, g, b):
    rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    return rgb565

frame = 0
rumbling = False
platformer = True

moveSpeed = 3.5
velocityY = 0
isJumping = False
gravity = 1
jumpForce = -10
groundLevel = 37
scene = levelParser.parse_json_file("level.json")
for i in scene:
    print(i.tag + str(i.portal))
    
gameover = False
running = True

oldcubepos = Vector2()

cubeTex = TextureResource("Images/cube.bmp")
cube = Sprite2DNode(texture=cubeTex, position=Vector2(-64+8, 0))
menuloop = WaveSoundResource("Sounds/gdmenuloop.wav")
engine_audio.set_volume(1.0)
loop = engine_audio.play(menuloop, 3, True)
loop.gain = 4.0

camera = CameraNode()

engine.fps_limit(60)
background_texture = TextureResource("Images/bg.bmp")
engine_draw.set_background(background_texture )

def getAABB(pos, half=8):
    return (
        pos.x - half,  # left
        pos.x + half,  # right
        pos.y - half,  # top
        pos.y + half   # bottom
    )

def overlaps(aL, aR, aT, aB, bL, bR, bT, bB):
    return aR > bL and aL < bR and aB > bT and aT < bB

def checkCollision():
    global velocityY, isJumping

    aL, aR, aT, aB = getAABB(cube.position)

    for obj in scene:
        half = getattr(obj, 'hitbox_half', 8)
        bL, bR, bT, bB = getAABB(obj.pos, half)

        if not overlaps(aL, aR, aT, aB, bL, bR, bT, bB):
            continue  # No collision at all, skip

        if obj.deadly:
            restartLevel()
            return  # No point checking more

        # Figure out overlap depth on each axis
        overlapTop    = aB - bT  # how far A has gone into B from the top
        overlapBottom = bB - aT  # how far A has gone into B from the bottom
        overlapLeft   = aR - bL
        overlapRight  = bR - aL

        minOverlap = min(overlapTop, overlapBottom, overlapLeft, overlapRight)

        if minOverlap == overlapTop:
            cube.position.y = bT - 8
            velocityY = 0
            isJumping = False
        elif minOverlap == overlapBottom:
            cube.position.y = bB + 8
            velocityY = 0
        elif minOverlap == overlapLeft:
            cube.position.x = bL - 8
        elif minOverlap == overlapRight:
            cube.position.x = bR + 8

def gameOver():
    global running
    running = False

def restartLevel():
    cube.position = Vector2(-64+8, 0)
    velocityY = 0
    isJumping = False
    rumbling = False
    frame = 0
    isCollidingVertically = False
    isJumping = False

def levelEnd():
    return

def movechar():
    global rumbling
    global velocityY
    global gravity
    global isJumping 
    velocityY += gravity
    cube.position.y += velocityY
    
    checkCollision()
    
    if not platformer:
        cube.position.x += 2.2
    
    if cube.position.y >= groundLevel:
      cube.position.y = groundLevel
      velocityY = 0
      isJumping = False
    
    if engine_io.A.is_just_pressed and isJumping != True:
        velocityY = jumpForce
        isJumping = True
        engine_io.rumble(0.35)
        rumbling = True
    
    # if cube.position.x < -64+8:
    #     cube.position.x = -64+8
#     if cube.position.x > 64-8:
#         cube.position.x = 64-8
    
    if engine_io.LEFT.is_pressed and platformer:
        cube.position.x -= moveSpeed
    if engine_io.RIGHT.is_pressed and platformer:
        cube.position.x += moveSpeed

while running:
    if engine.tick():
        if rumbling:
            frame += 1
            if frame >= 12:
                engine_io.rumble(0)
                rumbling = False
                frame = 0
        
        if engine_io.MENU.is_just_pressed:
            break
        camera.position.x = cube.position.x
        movechar()
        
 