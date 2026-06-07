from engine_nodes import Sprite2DNode, Rectangle2DNode # type: ignore
from engine_resources import TextureResource # type: ignore
import engine_io # type: ignore
from engine_math import Vector2 # type: ignore
import engine_audio # type: ignore
import engine_draw
from engine_draw import Color
PLAYER_HALF_X = 8
PLAYER_HALF_Y = 8
DEADLY_HALF_X = 3
DEADLY_HALF_Y = 3
moveSpeed = 11.540004 * (16 / 60)
velocityY = 0
isJumping = False
rumbling = False
gravity = 1

jumpBlocks = 2.15
target_px = jumpBlocks * 16

jumpForce = -((-1 + (1 + 8 * target_px) ** 0.5) / 2)

groundLevel = 37
portalsTouching = set()

cubeTex = TextureResource("Images/cube.bmp")
cube = Sprite2DNode(texture=cubeTex, position=Vector2(-64+8, 0), frame_count_x=1, frame_count_y=1, transparent_color=Color(1,0,1), playing=False)
playerBodyRect = Rectangle2DNode(position=cube.position, width=PLAYER_HALF_X*2, height=PLAYER_HALF_Y*2, color=Color(0,0,1.0), opacity=0.0)
playerDeadlyRect = Rectangle2DNode(position=cube.position, width=DEADLY_HALF_X*2, height=DEADLY_HALF_Y*2, color=Color(1.0,0,0), opacity=0.0)

def flipGravity(object):
    global gravity, jumpForce
    if (object.cord.x == 0 and gravity == -1) or (object.cord.x == 1 and gravity == 1):
        if gravity == 1: gravity = -1
        else: gravity = 1
        jumpForce = jumpForce *-1
        # print(f' Flipped, gravity: {gravity}, jumpforce: {jumpForce}')

def getAABB(pos, half_x=PLAYER_HALF_X, half_y=PLAYER_HALF_Y):
    half_x = float(half_x)
    half_y = float(half_y)
    return (
        pos.x - half_x,
        pos.x + half_x,
        pos.y - half_y,
        pos.y + half_y
    )

def overlaps(aL, aR, aT, aB, bL, bR, bT, bB):
    return aR > bL and aL < bR and aB > bT and aT < bB

def checkCollision(scene, on_death):
    global velocityY, isJumping

    bodyL, bodyR, bodyT, bodyB = getAABB(cube.position, PLAYER_HALF_X, PLAYER_HALF_Y)
    deadlyL, deadlyR, deadlyT, deadlyB = getAABB(cube.position, DEADLY_HALF_X, DEADLY_HALF_Y)

    for obj in scene:
        h = getattr(obj, 'hitbox_half', Vector2(8, 8))
        bL, bR, bT, bB = getAABB(obj.pos, h.x, h.y)

        if obj.deadly:
            aL, aR, aT, aB = deadlyL, deadlyR, deadlyT, deadlyB
            if not overlaps(aL, aR, aT, aB, bL, bR, bT, bB):
                continue
            on_death()
            return
        elif obj.portal:
            aL, aR, aT, aB = bodyL, bodyR, bodyT, bodyB
            if not overlaps(aL, aR, aT, aB, bL, bR, bT, bB):
                portalsTouching.discard(id(obj))
                continue
            if id(obj) not in portalsTouching:
                portalsTouching.add(id(obj))
                if obj.cord.y == 0:
                    # if (obj.cord.x == 0 and gravity == -1) or (obj.cord.x == 1 and gravity == 1):
                    flipGravity(obj)
            continue
        else:
            aL, aR, aT, aB = bodyL, bodyR, bodyT, bodyB
            if not overlaps(aL, aR, aT, aB, bL, bR, bT, bB):
                continue

        overlapTop    = aB - bT
        overlapBottom = bB - aT
        overlapLeft   = aR - bL
        overlapRight  = bR - aL

        minOverlap = min(overlapTop, overlapBottom, overlapLeft, overlapRight)

        if minOverlap == overlapTop:
            cube.position.y = bT - PLAYER_HALF_Y
            velocityY = 0
            isJumping = False
        elif minOverlap == overlapBottom:
            cube.position.y = bB + PLAYER_HALF_Y
            velocityY = 0
            isJumping = False 
        elif minOverlap == overlapLeft:
            cube.position.x = bL - PLAYER_HALF_X
        elif minOverlap == overlapRight:
            cube.position.x = bR + PLAYER_HALF_X

def reset():
    global cube, playerBodyRect, playerDeadlyRect, velocityY, isJumping, rumbling, gravity
    cube.position = Vector2(-64 + PLAYER_HALF_X, 0)
    velocityY = 0
    isJumping = False
    rumbling = False
    gravity = 1

def restartLevel():
    global velocityY, isJumping, rumbling, gravity, cube, playerBodyRect, playerDeadlyRect
    cube.position = Vector2(-64 + PLAYER_HALF_X, 0)
    velocityY = 0
    isJumping = False
    rumbling = False
    gravity = 1

def movechar(scene, platformer, on_death=None):
    global rumbling, velocityY, isJumping

    velocityY += gravity
    cube.position.y += velocityY
    # print("y:", cube.position.y, "vy:", velocityY)

    checkCollision(scene, on_death=on_death if on_death else restartLevel)

    if not platformer:
        cube.position.x += 2.2

    if cube.position.y >= groundLevel and gravity > 0:
        cube.position.y = groundLevel
        velocityY = 0
        isJumping = False

    if engine_io.A.is_just_pressed and not isJumping:
        velocityY = jumpForce
        isJumping = True
        engine_io.rumble(0.35)
        rumbling = True
        return True

    if engine_io.LEFT.is_pressed and platformer:
        cube.position.x -= moveSpeed
    if engine_io.RIGHT.is_pressed and platformer:
        cube.position.x += moveSpeed
    
    if playerBodyRect: playerBodyRect.position = cube.position
    if playerDeadlyRect: playerDeadlyRect.position = cube.position
    return False
