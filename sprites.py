import pygame, math, random
from config import *

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 0

        self.image = self.game.character_spritesheet.get_sprite(32,0,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()
        self.collide_grass()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def collide_grass(self):
        hits = pygame.sprite.spritecollide(self, self.game.grass, False)
        if hits:
            encounter = random.randint(0,100)
            if encounter == 0:
                self.game.playing = False

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(32, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(64, 0, self.width, self.height)]
        
        up_animations = [self.game.character_spritesheet.get_sprite(96, 0, self.width, self.height),
                        self.game.character_spritesheet.get_sprite(128, 0, self.width, self.height),
                        self.game.character_spritesheet.get_sprite(160, 0, self.width, self.height)]
        
        left_animations = [self.game.character_spritesheet.get_sprite(192, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(224, 0, self.width, self.height)]
        
        right_animations = [self.game.character_spritesheet.get_sprite(256, 0, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(288, 0, self.width, self.height)]
        
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(32, 0, self.width, self.height)
            else:
                if self.animation_loop >= 3:
                    self.animation_loop = 0
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(32, 0, self.width, self.height)
            else:
                if self.animation_loop >= 3:
                    self.animation_loop = 0
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(32, 0, self.width, self.height)
            else:
                if self.animation_loop >= 2:
                    self.animation_loop = 0
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(32, 0, self.width, self.height)
            else:
                if self.animation_loop >= 2:
                    self.animation_loop = 0
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1

class EnemyBulbasaur(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.width = 56
        self.height= 56
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.name = 'BULBASAUR'
        self.hp = 45
        self.maxhp = 45
        self.attack = 49
        self.defense = 49
        self.speed = 45

        self.weakness = ['fire']
        self.resistant = ['water', 'grass', 'electric']

        self.x = 400
        self.y = -50

        self.image = self.game.pokemon_front.get_sprite(0,0,self.width,self.height)
        self.image = pygame.transform.scale(self.image, (224,224))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.game.draw_text(self.name, FONT, BLACK, 70, 15)

    def attackPlayer(self, opponent):
        attackOption = random.randint(0,3)
        if attackOption == 1:
            self.tackle(opponent)
        elif attackOption == 2:
            self.growl(opponent)
        else:
            self.vine_whip(opponent)

    def tackle(self, opponent):
        power = 40

        effectiveness = 1
        if 'normal' in opponent.weakness:
            effectiveness *= 2
        if 'normal' in opponent.resistant:
            effectiveness /= 2

        damage = math.floor((((4 * power) / power + 2)) * effectiveness)
        opponent.hp -= damage

    def growl(self, opponent):
        opponent.attack -= (opponent.attack / 0.1)

    def vine_whip(self, opponent):
        power = 35
        
        effectiveness = 1
        if 'grass' in opponent.weakness:
            effectiveness *= 2
        if 'grass' in opponent.resistant:
            effectiveness /= 2

        damage = math.floor((((4 * power) / power + 2)) * effectiveness)
        opponent.hp -= damage

class EnemyCharmander(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.width = 56
        self.height= 56
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.name = 'CHARMANDER'
        self.hp = 39
        self.maxhp = 39
        self.attack = 52
        self.defense = 43
        self.speed = 65

        self.weakness = ['water']
        self.resistant = ['fire', 'grass']

        self.x = 400
        self.y = -50

        self.image = self.game.pokemon_front.get_sprite(56,0,self.width,self.height)
        self.image = pygame.transform.scale(self.image, (224,224))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.game.draw_text(self.name, FONT, BLACK, 70, 15)

    def attackPlayer(self, opponent):
        attackOption = random.randint(0,3)
        if attackOption == 1:
            self.scratch(opponent)
        elif attackOption == 2:
            self.growl(opponent)
        else:
            self.ember(opponent)

    def scratch(self, opponent):
        power = 35
        
        effectiveness = 1
        if 'normal' in opponent.weakness:
            effectiveness *= 2
        if 'normal' in opponent.resistant:
            effectiveness /= 2

        damage = math.floor((((4 * power) / power + 2)) * effectiveness)
        opponent.hp -= damage

    def growl(self, opponent):
        opponent.attack -= (opponent.attack / 0.1)

    def ember(self, opponent):
        power = 40
        
        effectiveness = 1
        if 'fire' in opponent.weakness:
            effectiveness *= 2
        if 'fire' in opponent.resistant:
            effectiveness /= 2

        damage = math.floor((((4 * power) / power + 2)) * effectiveness)
        opponent.hp -= damage

class EnemySquirtle(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.width = 56
        self.height= 56
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.name = 'SQUIRTLE'
        self.hp = 44
        self.maxhp = 44
        self.attack = 48
        self.defense = 65
        self.speed = 43

        self.weakness = ['grass', 'electric']
        self.resistant = ['fire', 'water']

        self.x = 400
        self.y = -50

        self.image = self.game.pokemon_front.get_sprite(112,0,self.width,self.height)
        self.image = pygame.transform.scale(self.image, (224,224))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.game.draw_text(self.name, FONT, BLACK, 70, 15)

    def attackPlayer(self, opponent):
        attackOption = random.randint(0,3)
        if attackOption == 1:
            self.scratch(opponent)
        elif attackOption == 2:
            self.tail_whip(opponent)
        else:
            self.water_gun(opponent)

    def scratch(self, opponent):
        power = 40
        
        effectiveness = 1
        if 'normal' in opponent.weakness:
            effectiveness *= 2
        if 'normal' in opponent.resistant:
            effectiveness /= 2

        damage = math.floor((((4 * power) / power + 2)) * effectiveness)
        opponent.hp -= damage

    def tail_whip(self, opponent):
        opponent.defense -= (opponent.defense / 0.1)

    def water_gun(self, opponent):
        power = 40
        
        effectiveness = 1
        if 'water' in opponent.weakness:
            effectiveness *= 2
        if 'water' in opponent.resistant:
            effectiveness /= 2

        damage = math.floor((((4 * power) / power + 2)) * effectiveness)
        opponent.hp -= damage

class PlayerBulbasaur(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.width = 32
        self.height= 32
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.name = 'BULBASAUR'
        self.hp = 45
        self.maxhp = 45
        self.attack = 49
        self.defense = 49
        self.speed = 45

        self.weakness = ['fire']
        self.resistant = ['water', 'grass', 'electric']

        self.x = 50
        self.y = 160

        self.image = self.game.pokemon_back.get_sprite(0,0,self.width,self.height)
        self.image = pygame.transform.scale(self.image, (160,160))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        

    def update(self):
        self.game.draw_text(self.name, FONT, BLACK, 360, 220)
        self.hp_text = FONT.render(f"{self.hp} / {self.maxhp}", 0, BLACK)
        self.game.screen.blit(self.hp_text, (360,250))

    def tackle(self, opponent):
        power = 40

        effectiveness = 1
        if 'normal' in opponent.weakness:
            effectiveness *= 2
        if 'normal' in opponent.resistant:
            effectiveness /= 2

        damage = math.floor((((4 * power) / power + 2)) * effectiveness)
        opponent.hp -= damage
        print('tackle')

    def growl(self, opponent):
        opponent.attack -= (opponent.attack / 0.1)
        print('growl')

    def vine_whip(self, opponent):
        power = 35
        
        effectiveness = 1
        if 'grass' in opponent.weakness:
            effectiveness *= 2
        if 'grass' in opponent.resistant:
            effectiveness /= 2

        damage = math.floor((((4 * power) / power + 2)) * effectiveness)
        opponent.hp -= damage
        print('tackle')

class PlayerCharmander(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.width = 32
        self.height= 32
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.name = 'CHARMANDER'
        self.hp = 39
        self.maxhp = 39
        self.attack = 52
        self.defense = 43
        self.speed = 65

        self.weakness = ['water']
        self.resistant = ['fire', 'grass']

        self.x = 50
        self.y = 160

        self.image = self.game.pokemon_back.get_sprite(32,0,self.width,self.height)
        self.image = pygame.transform.scale(self.image, (160,160))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        

    def update(self):
        self.game.draw_text(self.name, FONT, BLACK, 360, 220)
        self.hp_text = FONT.render(f"{self.hp} / {self.maxhp}", 0, BLACK)
        self.game.screen.blit(self.hp_text, (360,250))

    def scratch(self, opponent):
        power = 35
        
        effectiveness = 1
        if 'normal' in opponent.weakness:
            effectiveness *= 2
        if 'normal' in opponent.resistant:
            effectiveness /= 2

        damage = math.floor((((4 * power) / power + 2)) * effectiveness)
        opponent.hp -= damage

    def growl(self, opponent):
        opponent.attack -= (opponent.attack / 0.1)

    def ember(self, opponent):
        power = 40
        
        effectiveness = 1
        if 'fire' in opponent.weakness:
            effectiveness *= 2
        if 'fire' in opponent.resistant:
            effectiveness /= 2

        damage = math.floor((((4 * power) / power + 2)) * effectiveness)
        opponent.hp -= damage

class HealthBar():
    def __init__(self, game, x, y, hp, max_hp):
        self.game = game
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        self.hp = hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(self.game.screen, RED, (self.x, self.y, 200, 10))
        pygame.draw.rect(self.game.screen, GREEN, (self.x, self.y, 200 * ratio, 10))
                

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(32,0,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Grass(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GRASS_LAYER
        self.groups = self.game.all_sprites, self.game.grass
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y