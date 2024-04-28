import pygame, sys
from sprites import *
from config import *
from button import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.fight_state = 'main'

        self.character_spritesheet = Spritesheet('imgs/player.png')
        self.terrain_spritesheet = Spritesheet('imgs/terrain.png')
        self.pokemon_back = Spritesheet('imgs/pokemon_back.png')
        self.pokemon_front = Spritesheet('imgs/pokemon_front.png')
        self.fight_background = pygame.image.load('./imgs/fight_background.png')

        self.fight_btn_img = pygame.image.load('./imgs/buttons/fight_button.png').convert_alpha()
        self.pkmn_btn_img = pygame.image.load('./imgs/buttons/pkmn_button.png').convert_alpha()
        self.item_btn_img = pygame.image.load('./imgs/buttons/item_button.png').convert_alpha()
        self.run_btn_img = pygame.image.load('./imgs/buttons/run_button.png').convert_alpha()

        self.scratch_btn_img = pygame.image.load('./imgs/buttons/run_button.png').convert_alpha()
        self.tackle_btn_img = pygame.image.load('./imgs/buttons/run_button.png').convert_alpha()
        self.growl_btn_img = pygame.image.load('./imgs/buttons/run_button.png').convert_alpha()
        self.tail_whip_btn_img = pygame.image.load('./imgs/buttons/run_button.png').convert_alpha()
        self.ember_btn_img = pygame.image.load('./imgs/buttons/run_button.png').convert_alpha()
        self.water_gun_btn_img = pygame.image.load('./imgs/buttons/run_button.png').convert_alpha()
        self.vine_whip_btn_img = pygame.image.load('./imgs/buttons/run_button.png').convert_alpha()

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                j += (((WIN_WIDTH /32) / 2) - (len(row) / 2))
                i += (((WIN_HEIGHT /32) / 2) - 7.5)
                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i)
                if column == 'P':
                    Player(self, j, i)
                if column == 'G':
                    Grass(self, j, i)

    def draw_text(self, text, font, colour, x, y):
        img = font.render(text, True, colour)
        self.screen.blit(img, (x,y))

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.grass = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
    
    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def fight(self):
        for sprite in self.all_sprites:
            sprite.kill()

        enemy = EnemyBulbasaur(self)
        player = PlayerCharmander(self)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.blit(self.fight_background, (0,0))

            fight_button = Button(25, 350, self.fight_btn_img, 5)
            pkmn_button = Button(345, 350, self.pkmn_btn_img, 5)
            item_button = Button(25, 415, self.item_btn_img, 5)
            run_button = Button(345, 415, self.run_btn_img, 5)

            if self.fight_state == 'main':
                if fight_button.draw(self.screen):
                    self.fight_state = 'fight'
                    player.hp -= 8
                if pkmn_button.draw(self.screen):
                    pass
                if item_button.draw(self.screen):
                    pass
                if run_button.draw(self.screen):
                    self.running = False

            if self.fight_state == 'fight':
                pass

            self.all_sprites.draw(self.screen)
            self.clock.tick(FPS)
            self.update()
            pygame.display.update()
            

    def intro_screen(self):
        pass

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.fight()

pygame.quit()
sys.exit()