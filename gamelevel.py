import engine # type: ignore
from engine_nodes import CameraNode # type: ignore
from engine_resources import WaveSoundResource # type: ignore
import engine_io # type: ignore
import engine_draw # type: ignore
from engine_math import Vector2 # type: ignore
import engine_audio # type: ignore
import levelParser
import player

print("start")

frame = 0
platformer = True
running = True

scene = levelParser.parse_json_file("level.json")
for i in scene:
    print(i.tag + str(i.portal))

menuloop = WaveSoundResource("Sounds/gdmenuloop.wav")
engine_audio.set_volume(1.0)
loop = engine_audio.play(menuloop, 3, True)
loop.gain = 4.0

camera = CameraNode()

engine.fps_limit(60)
background_texture = engine_draw.TextureResource("Images/bg.bmp") if hasattr(engine_draw, 'TextureResource') else None
from engine_resources import TextureResource # type: ignore
background_texture = TextureResource("Images/bg.bmp")
engine_draw.set_background(background_texture)

def gameOver():
    global running
    running = False

def levelEnd():
    return

while running:
    if engine.tick():
        if player.rumbling:
            frame += 1
            if frame >= 12:
                engine_io.rumble(0)
                player.rumbling = False
                frame = 0

        if engine_io.MENU.is_just_pressed:
            break

        camera.position.x = player.cube.position.x
        player.movechar(scene, platformer)