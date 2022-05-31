import ctypes, math, random, pygame
from .graphics import *
v2 = pygame.Vector2
atkdur = 0
curlvl = None
class Character(Spritesheet):
    def __init__(self, pos, surf, characterName, cells:dict={"stand": (0,0,64,64)}):
        super().__init__( f"Art/Characters/{characterName}/sheet.png", cells)
        self.surf = surf
        self.gsp = 0
        self.up = -90 # this is in degrees
        self.x = self.y = 20
        self.width = 7*2+1
        self.height = 9*2+1
        self.vec = v2((self.x, self.y))
        self.xvel = self.yvel = 0
        self.frc = self.acc = 0.046875
        self.dec = 0.03125
        self.layer = 0
        self.rect = pygame.Rect(self.vec, (self.width, self.height))
        self.ang = 0
        self.top = 6
        self.position = v2(pos)
        self._facing = v2(1,0)
        self.floor_under = False

    @property
    def facing(self):
        return self._facing
    @property.setter
    def facing(self):
        self._facing = v2(1,0).rotate(self.ang)
    def update(self, drc: str):
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
                    gsp = -0.5
            elif self.gsp < 0:
                self.gsp -= self.acc
                if abs(self.gsp) > self.top:
                    self.gsp = -self.top
        else:
            self.gsp = min(abs(self.gsp), self.frc) * math.sin(self.gsp)
        self.vec.from_polar((self.gsp, self.ang))
        self.rect = pygame.Rect(*self.vec, self.width, self.height)
        self.floor_under_right_a = curlvl["colA"][self.rect.bottom][self.rect.right][3] > 0
        self.floor_under_right_b = curlvl["colB"][self.rect.bottom][self.rect.right][3] > 0
        if self.layer == 0:
            self.floor_under = self.floor_under_a or self.floor_under_b
        if self.layer == 1:
            self.floor_under = self.floor_under_a
        if self.layer == 2:
            self.floor_under = self.floor_under_b
        self.rect = pygame.Rect(self.vec, self.width, self.height)
        # rotate direction vector to that of the current rotation cell of the level.]
        

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
                    distance = self.vec.distance_to(pygame.Vector2(-150,self.y))
                elif atk['name'] == "moveright":
                    distance = self.vec.distance_to(pygame.Vector2(self.surf.width + 150, self.y))
                elif atk['name'] == "movedown":
                    self.targetPos = self.x, self.surf.height+150
                    distance = self.vec.distance_to(pygame.Vector2(self.x, self.surf.height+150))
                elif atk['name'] == "moveup":
                    distance = self.vec.distance_to(pygame.Vector2(self.x, -150))
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
    # def fire(self, ang):