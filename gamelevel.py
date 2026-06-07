import engine # type: ignore
from engine_resources import WaveSoundResource, TextureResource, FontResource # type: ignore
from engine_nodes import Sprite2DNode, Rectangle2DNode # type: ignore
import engine_io # type: ignore
import engine_draw # type: ignore
from engine_math import Vector2 # type: ignore
from engine_draw import Color # type: ignore
import engine_audio # type: ignore
import engine_animation # type: ignore
import levelParser
import gmd_parser
import player
import engine_save
from outlinedText import OutlinedTextNode

print("start")

level = "ColourDash Test.gmd"

running = False
frame = 0
platformer = False
hitboxes = False

_sound_loaded = False
_menuloop = None

attempts = 1
jumps = 0
endXPos = 0
endScreenX = 0
gameState = 0  # 0=playing, 1=endAnimation, 2=results

def onDeath():
    global attempts, jumps
    attempts += 1
    jumps = 0
    player.restartLevel()

def gameOver():
    global running
    running = False

def main_loop(camera):
    global running, frame, platformer, hitboxes, _sound_loaded, _menuloop, attempts, jumps, endXPos, endScreenX, gameState

    engine_save._init_saves_dir("/Saves/ColourDash")
    engine_save.set_location("options.data")
    platformer = engine_save.load("platformer", False)
    hitboxes = engine_save.load("hitbox_visual", False)

    frame = 0
    attempts = 1
    jumps = 0
    gameState = 0
    running = True
    player.reset()
    player.cube.opacity = 1.0
    camera.position = Vector2(0, 0)

    if level.endswith(".json"):
        scene = levelParser.parse_json_file(level)
    else:
        try:
            scene = gmd_parser.parse_gmd_file(level)
        except Exception as e:
            print(e)
            print("falling back to level.json")
            scene = levelParser.parse_json_file("level.json")

    endXPos = max(b.pos.x for b in scene) + 120
    endScreenX = max(b.pos.x for b in scene) + 256

    if not _sound_loaded:
        _menuloop = WaveSoundResource("Sounds/gdmenuloop.wav")
        _sound_loaded = True

    engine_audio.set_volume(1.0)
    loop = engine_audio.play(_menuloop, 3, True)
    loop.gain = 4.0

    engine.fps_limit(60)
    background_texture = TextureResource("Images/bg.bmp")
    engine_draw.set_background(background_texture)

    resultFont = FontResource("Font/pixelatedPusab.bmp")
    tableTop = Sprite2DNode(position=Vector2(0, -50),
        texture=TextureResource("Images/table_top.bmp"),
        transparent_color=Color(1,0,1), opacity=0.0, layer=1)
    levelComplete = Sprite2DNode(position=Vector2(0, -32),
        texture=TextureResource("Images/level_complete.bmp"),
        transparent_color=Color(1,0,1), opacity=0.0, layer=1)
    tableBottom = Sprite2DNode(position=Vector2(0, 50),
        texture=TextureResource("Images/table_bottom.bmp"),
        transparent_color=Color(1,0,1), opacity=0.0, layer=1)
    attemptsText = OutlinedTextNode(position=Vector2(0,-5), font=resultFont,
        text="", scale=Vector2(0.5,0.5), color=Color(1,1,1),
        outline_color=Color(0,0,0), layer=1, offset=1)
    jumpsText = OutlinedTextNode(position=Vector2(0,15), font=resultFont,
        text="", scale=Vector2(0.5,0.5), color=Color(1,1,1),
        outline_color=Color(0,0,0), layer=1, offset=1)
    resultBackground = Rectangle2DNode(
        Vector2(0,0),
        105,
        100,
        Color(0.0,0.0,0.0),
        0.0,
        layer=0)
    resultNodes = [tableTop, levelComplete, tableBottom, attemptsText, jumpsText, resultBackground]

    def applyHitboxVis(v):
        if player.playerBodyRect:
            player.playerBodyRect.opacity = 0.3 if v else 0.0
        if player.playerDeadlyRect:
            player.playerDeadlyRect.opacity = 0.3 if v else 0.0
        for i in scene:
            i.hitboxRect.opacity = 0.3 if v else 0.0
    applyHitboxVis(hitboxes)

    class FlyState:
        pass
    fly = FlyState()
    flyTween = None
    midX = 0

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
                if flyTween:
                    flyTween.pause()

            if gameState == 0:
                if engine_io.LB.is_just_pressed:
                    platformer = not platformer
                    engine_save.save("platformer", int(platformer))
                    print(f"Platformer is {platformer}")
                if engine_io.RB.is_just_pressed:
                    hitboxes = not hitboxes
                    engine_save.save("hitbox_visual", int(hitboxes))
                    print(f"Hitbox visuals are {hitboxes}")
                    applyHitboxVis(hitboxes)

                jumped = player.movechar(scene, platformer, on_death=onDeath)
                if jumped:
                    jumps += 1
                camera.position = Vector2(player.cube.position.x, 0)

                if player.cube.position.x >= endXPos:
                    gameState = 1
                    engine_audio.stop(3)
                    jingle = WaveSoundResource("Sounds/endjingle.wav")
                    engine_audio.play(jingle, 3, False)

                    fly.start_x = player.cube.position.x
                    fly.start_y = player.cube.position.y
                    fly.t = 0.0
                    midX = (fly.start_x + endScreenX) / 2

                    flyTween = engine_animation.Tween(fly, "t", 1.0, 3000,
                        engine_animation.ONE_SHOT, engine_animation.EASE_QUART_OUT, 500)

                    def fly_update(*_):
                        t = fly.t
                        x = fly.start_x + (endScreenX - fly.start_x) * t
                        y = -40 * 4 * t * (1 - t)
                        player.cube.position = Vector2(x, y)
                        cam = camera.position
                        tableTop.position = Vector2(cam.x, cam.y - 50)
                        levelComplete.position = Vector2(cam.x, cam.y - 32)
                        tableBottom.position = Vector2(cam.x, cam.y + 50)
                        attemptsText.position = Vector2(cam.x, cam.y - 5)
                        jumpsText.position = Vector2(cam.x, cam.y + 15)
                        resultBackground.position = Vector2(cam.x, cam.y + 0)
                        fade = min(t / 0.666, 1.0)
                        # resultBackgroundFade = min(t / 0.666, 0.4)
                        # resultBackground.opacity = resultBackgroundFade
                        for n in resultNodes:
                            n.opacity = fade
                        resultBackgroundFade = min(t / 0.666, 0.4)
                        resultBackground.opacity = resultBackgroundFade

                    def fly_done(*_):
                        attemptsText.text = "Attempts: " + str(attempts)
                        jumpsText.text = "Jumps: " + str(jumps)

                    flyTween.during = fly_update
                    flyTween.after = fly_done
                    flyTween.start(fly, "t", 0.0, 1.0, 3000, 1.0,
                        engine_animation.ONE_SHOT, engine_animation.EASE_QUART_OUT)

            elif gameState == 1:
                camera.position = Vector2(min(player.cube.position.x, midX), 0)
                if flyTween and flyTween.finished:
                    gameState = 2
                    player.cube.opacity = 0.0

            elif gameState == 2:
                if engine_io.A.is_just_pressed:
                    player.cube.opacity = 1.0
                    for n in resultNodes:
                        n.opacity = 0.0
                    attempts = 1
                    jumps = 0
                    gameState = 0
                    player.reset()
                    camera.position = Vector2(0, 0)
                    if flyTween:
                        flyTween.pause()
                    flyTween = None
                    endXPos = max(b.pos.x for b in scene) + 120
                    engine_audio.set_volume(1.0)
                    loop = engine_audio.play(_menuloop, 3, True)
                    loop.gain = 4.0
                elif engine_io.B.is_just_pressed:
                    running = False

    if flyTween:
        flyTween.pause()
    player.cube.opacity = 0.0
    engine_audio.stop(3)
    for n in resultNodes:
        n.opacity = 0.0

