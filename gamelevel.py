import engine # type: ignore
from engine_resources import WaveSoundResource, TextureResource # type: ignore
import engine_io # type: ignore
import engine_draw # type: ignore
from engine_math import Vector2 # type: ignore
import engine_audio # type: ignore
import levelParser
import player
import engine_save

print("start")

level = "ColourDash Test.gmd"

running = False
frame = 0
platformer = False
hitboxes = False

def gameOver():
    global running
    running = False

def levelEnd():
    return

def main_loop(camera):
    global running, frame, platformer, hitboxes

    engine_save._init_saves_dir("/Saves/ColourDash")
    engine_save.set_location("options.data")
    platformer = engine_save.load("platformer", False)
    hitboxes = engine_save.load("hitbox_visual", False)

    frame = 0
    running = True
    player.reset()
    camera.position = Vector2(0, 0)

    if level.endswith(".json"):
        scene = levelParser.parse_json_file(level)
    else:
        import gmd_parser
        scene = gmd_parser.parse_gmd_file(level)

    menuloop = WaveSoundResource("Sounds/gdmenuloop.wav")
    engine_audio.set_volume(1.0)
    loop = engine_audio.play(menuloop, 3, True)
    loop.gain = 4.0

    engine.fps_limit(60)
    background_texture = TextureResource("Images/bg.bmp")
    engine_draw.set_background(background_texture)

    if hitboxes:
        player.playerBodyRect.opacity = 0.3
        player.playerDeadlyRect.opacity = 0.3
        for i in scene:
            i.hitboxRect.opacity = 0.3
    else:
        player.playerBodyRect.opacity = 0.0
        player.playerDeadlyRect.opacity = 0.0
        for i in scene:
            i.hitboxRect.opacity = 0.0

    while running:
        if engine.tick():
            if player.rumbling:
                frame += 1
                if frame >= 12:
                    engine_io.rumble(0)
                    player.rumbling = False
                    frame = 0

            if engine_io.MENU.is_just_pressed:
                running = False
            
            if engine_io.LB.is_just_pressed:
                platformer = not platformer
                engine_save.save("platformer", int(platformer))
                print(f"Platformer is {platformer}")
            if engine_io.RB.is_just_pressed:
                hitboxes = not hitboxes
                engine_save.save("hitbox_visual", int(hitboxes))
                print(f"Hitbox visuals are {hitboxes}")
                if hitboxes:
                    player.playerBodyRect.opacity = 0.3
                    player.playerDeadlyRect.opacity = 0.3
                    for i in scene:
                        i.hitboxRect.opacity = 0.3
                else:
                    player.playerBodyRect.opacity = 0.0
                    player.playerDeadlyRect.opacity = 0.0
                    for i in scene:
                        i.hitboxRect.opacity = 0.0

            camera.position.x = player.cube.position.x
            player.movechar(scene, platformer)

