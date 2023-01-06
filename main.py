import pyhog

DEBUG = True
pyhog.ON()
WIN = pyhog.gui.Window(600, 600, bgcolor="cyan")#, fullscreen=True)
WIN.display()
# creation of variables
Sonic = pyhog.dynamics.Character(WIN.surf, "sonic", {"stand": [(8,17,27,39)]}, (20,20))
EHZ = pyhog.dynamics.Level(WIN.surf, "Art/Zones/EHZ/FG.png", ["Art/Zones/EHZ/colliders/colA.png", "Art/Zones/EHZ/colliders/colB.png"], "Emerald Hill", 1, bg="Art/Zones/EHZ/BG.png", y=-560)
dbgtxt = pyhog.gui.Box(WIN.surf, [10,10], text="Debug", hover=True, function=lambda: print("This should work"))
to_EHZ = pyhog.gui.Box(WIN.surf, [165,10], text="Emerald Hill Zone 1", hover=True, function=EHZ.load)
debugMNU = pyhog.gui.Menu("Debug", 0, buttons=[[dbgtxt, to_EHZ]])
time = ""
boss = False
sunset = pyhog.graphics.sky_mod(WIN.surf, "Art/Zones/Shared/Sunset.png")
ang = 0
gRun = True
drc = None

if DEBUG:
    pyhog.gui.openMenu(0)
while gRun:
    WIN.clear()
    state = pyhog.files.get_state()
    print(f"{state=}")
    """The game loop"""
    if pyhog.key_pressed("esc"):
        gRun = False
    if not state is None:
        if state[0] == "menu":
            for btnlst in pyhog.gui.menus['current'].btns:
                for btn in btnlst:
                    btn.draw()
        else:
            try:
                s = pyhog.dynamics.curlvl.started
            except AttributeError as e:
                _ = e
                del _
            except Exception as e:
                print(e)
            else:
                if pyhog.dynamics.curlvl.started:
                    if pyhog.key_pressed("right"):
                        drc = 1
                    elif pyhog.key_pressed("left"):
                        drc = -1
                    else:
                        drc = 0
                    if pyhog.key_pressed("rotate_left"):
                        Sonic.ang -= 4
                    elif pyhog.key_pressed("rotate_right"):
                        Sonic.ang += 4
                    if time == "sunset":
                        if not sunset.loaded:
                            sunset.load()
                    if Sonic.layer == 2:
                        Sonic.update(drc)
                        pyhog.dynamics.curlvl.draw()
                    else:
                        colliding = pyhog.gui.Box(WIN.surf, text=f"Sonic is grounded:{Sonic.grounded}")
                        located = pyhog.gui.Box(WIN.surf, text=f"Sonic is located at:{Sonic.location}")
                        pyhog.dynamics.curlvl.draw()
                        Sonic.update(drc)
                        colliding.draw()
                        located.draw()
                else:
                    pyhog.dynamics.curlvl.load({1:[Sonic]})
                    pyhog.dynamics.curlvl.start()
            
    if boss == False:
        if pyhog.key_pressed("dbg"):
            boss = 'pre'
    elif boss == "pre":
        pyhog.load_Music("music/bossB1.wav")
        pyhog.music_volume(0.25)
        boss = "activate"
    elif boss == 'activate':
        pyhog.play_music(-1)
        boss = True
    c = pyhog.clock()
    WIN.update()
    c.tick(30)
pyhog.OFF()
