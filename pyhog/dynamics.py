import ctypes, math, random, functools, pygame
from . import graphics
from . import audio
from . import files
from . import math as phgMath

curlvl = None
atkdur = 0

grv = 0.25

class Character(graphics.Spritesheet):
    def __init__(self, surf, characterName, cells:dict={"stand": [0,0,64,64]}, pos=()):
        super().__init__(f"Art/Characters/{characterName}/sheet.png", cells)
        self.surf = surf
        self.gsp = 0
        self.up = -90 # this is in degrees
        self.pos = pygame.Vector2(20)
        self.xvel = self.yvel = 0
        self.frc = self.acc = 0.046875
        self.layer = 0
        self.rect = pygame.Rect(self.pos, (7, 9))
        self.coll_anchor = pygame.Vector2(self.rect.center)
        self.ang = 0
        self.top = 6
        self.height_radius = 19
        self.width_radius = 9
        self.loaded = False
        self.grounded = False
        self.is_ball = False
        self.active_sensors = [True for _ in range(6)]
    def activate_sensors(self):
        self.active_sensors = [True for _ in range(6)]
        if self.gsp > 0:
            self.active_sensors[4] = False
        elif self.gsp < 0:
            self.active_sensors[5] = False
        if self.grounded:
            self.active_sensors[2:2] = [False, False]
        else:
            if self.yvel > 0:
                self.active_sensors[2:2] = [False, False]
            else:
                self.active_sensors[0:2] = [False, False]

        
    def update(self, drc: int):
        self.up = self.ang - 90
        if drc > 0:
            if self.gsp < 0:
                self.gsp += self.dec
                if self.gsp >= 0:
                    self.gsp = 0.5
            elif self.gsp > 0:
                self.gsp += self.acc
                if self.gsp > self.top:
                    self.gsp = self.top
        elif drc < 0:
            if self.gsp > 0:
                self.gsp -= self.dec
                if self.gsp <= 0:
                    self.gsp = -0.5
            elif self.gsp < 0:
                self.gsp -= self.acc
                if abs(self.gsp) > self.top:
                    self.gsp = -self.top
        else:
            self.gsp = min(abs(self.gsp), self.frc) * math.sin(self.gsp)
        """Change Radii depending if we are in a ball or not"""
        if self.is_ball:
            self.height_radius = 7
            self.width_radius = 14
        else:
            self.height_radius = 19
            self.width_radius = 9
        #
        self.activate_sensors()
        self.pos += pygame.Vector2(self.gsp, 0).rotate(self.ang) 
        self.up = self.ang - 90
        self.rect = pygame.Rect(*self.pos, 10, 10)
        if not self.loaded:
            self.load()
        if not self.grounded:
            self.yvel += grv
            if self.yvel > self.top:
                self.yvel = self.top
            self.pos += pygame.Vector2(0, self.yvel)
        print(self.grounded)
        curlvl.collide(self)
        self.render()
class Boss(Character):
    def __init__(self, surf, name, cells, hits, spawn, behaviors=()):
        super().__init__(surf, name, cells)
        self.spawn = spawn
        self.htis = hits
        self.behaviors = behaviors
        self.atkdur = 256
        
    def update(self):
        global atkdur
        if len(self.behaviors) >= 2:            
            if self.atkdur == 0:
                targetPos = None
                atk = random.choice(self.behaviors).lower()
                if atk['name'] == "moveleft":
                    distance = self.pos.distance_to(pygame.Vector2(-150,self.y))
                elif atk['name'] == "moveright":
                    distance = self.pos.distance_to(pygame.Vector2(self.surf.width + 150, self.y))
                elif atk['name'] == "movedown":
                    self.targetPos = self.x, self.surf.height+150
                    distance = self.pos.distance_to(pygame.Vector2(self.x, self.surf.height+150))
                elif atk['name'] == "moveup":
                    distance = self.pos.distance_to(pygame.Vector2(self.x, -150))
                elif atk['name'] == "hover":
                    atkdur = 120
                elif atk['name'] == "fireleft":
                    self.fire(180)
                    atkdur = 180
                elif atk['name'] == "fireright":
                    self.fire()
                    atkdur = 180
                elif atk['name'] == "firedown":
                    self.fire(90)
                    atkdur = 180
                elif atk['name'] == "fireup":
                    self.fire(-90)
                    atkdur = 180
                elif atk['name'] == "fireto":
                    self.fire(pygame)
                if not targetPos == None:
                    atkdur = self.distance_to(pygame.Vector2(*targetPos)/6)

    
class Level:
    def __init__(self, surf, fg, colliders, name, lvl_id=1, bgm=None, bg=None, x=0, y=0):
        self.surf, self.fg, self.colFiles, self.name, self.lvl_id, self.bgm, self.bg, self.x, self.y = surf, fg, colliders, name, ctypes.c_int8(lvl_id).value, bgm, bg, x, y
    def load(self):
        self.collision = {}
        if not len(self.colFiles) > 2:
            for num, file in enumerate(self.colFiles):
                
                self.collision[num] = graphics.load_image(file)
        else:
            raise NotImplementedError("I have yet to code in support for more than 2 layers.")
        if self.bg:
            self.bgIMG = graphics.load_image(self.bg)
        else:
            self.bgIMG = None
        if self.bgm:
            audio.load_music(self.bgm)
        self.fgIMG = graphics.load_image(self.fg)
        self.start()
    def start(self):
        global curlvl
        files.set_state(1, self.lvl_id)
        if audio.get_busy():
            audio.stop_music()
        if self.bgm:
            audio.play_music(-1)
        self.started = True
        curlvl = self
    def unload(self):
        pygame.mixer.music.unload()
    def collide(self, caller):
        if not caller.layer == 0:
            collision_layer = self.collision[caller.layer]
        caller_pos = int(caller.pos.x), int(caller.pos.y)
        pixel = collision_layer.get_at(*caller_pos)
        is_colliding = not pixel == (0,0,0,0)
        if is_colliding:
            return True, pixel[3]
    def draw(self):
        if self.bgIMG:
            self.surf.blit(self.bgIMG, (self.x, 0))
        self.surf.blit(self.fgIMG, (self.x, self.y))