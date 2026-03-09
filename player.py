from engine_nodes import Sprite2DNode # type: ignore
from engine_resources import TextureResource # type: ignore
import engine_io # type: ignore
from engine_math import Vector2 # type: ignore
import engine_audio # type: ignore

moveSpeed = 3.5
velocityY = 0
isJumping = False
rumbling = False
gravity = 1
jumpForce = -10
groundLevel = 37

cubeTex = TextureResource("Images/cube.bmp")
cube = Sprite2DNode(texture=cubeTex, position=Vector2(-64+8, 0))

def getAABB(pos, half_x=8, half_y=8):
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

    aL, aR, aT, aB = getAABB(cube.position)

    for obj in scene:
        h = getattr(obj, 'hitbox_half', 8)
        if isinstance(h, Vector2):
            bL, bR, bT, bB = getAABB(obj.pos, h.x, h.y)
        else:
            bL, bR, bT, bB = getAABB(obj.pos, h, h)

        if not overlaps(aL, aR, aT, aB, bL, bR, bT, bB):
            continue

        if obj.deadly:
            on_death()
            return

        overlapTop    = aB - bT
        overlapBottom = bB - aT
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

def restartLevel():
    global velocityY, isJumping, rumbling
    cube.position = Vector2(-64+8, 0)
    velocityY = 0
    isJumping = False
    rumbling = False

def movechar(scene, platformer):
    global rumbling, velocityY, isJumping

    velocityY += gravity
    cube.position.y += velocityY

    checkCollision(scene, on_death=restartLevel)

    if not platformer:
        cube.position.x += 2.2

    if cube.position.y >= groundLevel:
        cube.position.y = groundLevel
        velocityY = 0
        isJumping = False

    if engine_io.A.is_just_pressed and not isJumping:
        velocityY = jumpForce
        isJumping = True
        engine_io.rumble(0.35)
        rumbling = True

    if engine_io.LEFT.is_pressed and platformer:
        cube.position.x -= moveSpeed
    if engine_io.RIGHT.is_pressed and platformer:
        cube.position.x += moveSpeed
