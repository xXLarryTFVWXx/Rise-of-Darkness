import ctypes, math, random, functools, pygame
from . import graphics
from . import audio
from . import files

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
        self.c_angles = [
            64.6538240580533,
            115.34617594194671,
            -64.6538240580533,
            -115.34617594194671
        ]
        self.coll_delta = 21.02379604162864
        
        """The following might be inefficient, but it's the best I've got for right now."""
        self.coll_pos = {_: pygame.Vector2(self.coll_anchor).from_polar((self.coll_delta, ang)) for _, ang in enumerate(self.c_angles)}
        self.coll_pos[4], self.coll_pos[5] = [self.ang, 10], [self.ang, -10]
        self.loaded = False
        self.grounded = False
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
        self.pos.from_polar((self.gsp, self.ang))
        self.pos = pygame.Vector2(self.pos)
        self.up = self.ang - 90
        self.rect = pygame.Rect(*self.pos, 10, 10)
        self.coll_anchor = pygame.Vector2(self.rect.center)
        for k, v in self.coll_pos.items():
            _ = self.coll_anchor
            if not k > 3:
                self.coll_pos = {_: pygame.Vector2(self.coll_anchor).from_polar((self.coll_delta, ang)) for _, ang in enumerate(self.c_angles)}
                self.coll_pos[4], self.coll_pos[5] = [self.ang, 10], [self.ang, -10] 
        if not self.loaded:
            self.load()
        if not self.grounded:
            self.yvel += grv
            if self.yvel > self.top:
                self.yvel = self.top
            self.pos.from_polar((self.yvel, 90))
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
                if num == 0:
                    self.collision["colA"] = graphics.load_image(file)
                else:
                    self.collision["colB"] = graphics.load_image(file)
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
            if caller.layer == 1:
                layer = "colA"
            else:
                layer = "colB"
            while self.collision[caller.layer].get_at(caller.pos)[3] == 255:
                 caller.pos.from_polar(1, caller.up)
        else:
            caller_pos = int(caller.pos.x), int(caller.pos.y)
            print(caller_pos)
            while self.collision["colA"].get_at(caller_pos)[3] == 255 or self.collision["colB"].get_at(caller_pos)[3] == 255:
                caller.pos.vec.from_polar((1, caller.up))
    def draw(self):
        if self.bgIMG:
            self.surf.blit(self.bgIMG, (self.x, 0))
        self.surf.blit(self.fgIMG, (self.x, self.y))