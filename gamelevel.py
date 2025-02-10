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
groundLevel = 37;
scene = levelParser.parse_json_file("level.json")
for i in scene:
    print(i.tag)
gameover = False
running = True

#use COLLAR somewhere

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

def checkCollision():
    for obj in scene:
        global running
        global velocityY
        global isJumping
        
        leftA = cube.position.x - 8
        rightA = cube.position.x + 8
        topA = cube.position.y - 8
        bottomA = cube.position.y + 8

        leftB = obj.pos.x -8
        rightB = obj.pos.x + 8
        topB = obj.pos.y - 8
        bottomB = obj.pos.y + 8
        
        isCollidingVertically = False
        if not obj.deadly:
            
            if bottomA > topB and topA < topB:
                if rightA > leftB and leftA < rightB:  # Ensure horizontal overlap
                # if bottomA > topB and topA < topB:  # Hitting the top of the block
                    cube.position.y = topB - 8
                    isJumping = False
                    isCollidingVertically = True
                    velocityY = 0
                elif topA < bottomB and bottomA > bottomB:  # Hitting the bottom of the block
                    cube.position.y = bottomB + 8
                    velocityY = 0
                    isCollidingVertically = True
            
            if not isCollidingVertically:
                # if not cube.position.x < -64-8 and cube.position.x > 64+8:
                if rightA > leftB and leftA < leftB and bottomA > topB and topA < bottomB:
                    cube.position.x = leftB - 8
                    # cube.position = Vector2(-32, groundLevel+8)
                elif leftA < rightB and rightA > rightB and bottomA > topB and topA < bottomB:
                    cube.position.x = rightB + 8
                    # cube.position = Vector2(-32, groundLevel+8)
        else:
            leftB = obj.pos.x - 7
            rightB = obj.pos.x + 7
            topB = obj.pos.y - 7
            bottomB = obj.pos.y + 7
            if bottomA > topB and topA < topB:
                if rightA > leftB and leftA < rightB:  # Ensure horizontal overlap
                # if bottomA > topB and topA < topB:  # Hitting the top of the block
                    isJumping = False
                    isCollidingVertically = True
                    velocityY = 0
                    running = False
                    print("colliDED")
                elif topA < bottomB and bottomA > bottomB:  # Hitting the bottom of the block
                    velocityY = 0
                    isCollidingVertically = True
                    running = False
                    print("colliDED")
            
            if not isCollidingVertically:
                # if not cube.position.x < -64-8 and cube.position.x > 64+8:
                if rightA > leftB and leftA < leftB and bottomA > topB and topA < bottomB:
                    running = False
                    print("colliDED")
                    # cube.position = Vector2(-32, groundLevel+8)
                elif leftA < rightB and rightA > rightB and bottomA > topB and topA < bottomB:
                    running = False
                    print("colliDED")
                    # cube.position = Vector2(-32, groundLevel+8)

def gameOver():
    global running
    running = False

def moveScene(movespeed):
    for x in scene:
        x.pos.x -= movespeed.x
        if x.pos.x < -64 - 8:
            x.pos.x = 64 + 8

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
        
 