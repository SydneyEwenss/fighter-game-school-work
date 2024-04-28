import pygame, sys
from sprites import *
from config import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        # self.font = pygame.font.Font('Arial', 32)
        self.running = True

        self.character_spritesheet = Spritesheet('imgs/player.png')
        self.terrain_spritesheet = Spritesheet('imgs/terrain.png')
        self.pokemon_back = Spritesheet('imgs/pokemon_back.png')
        self.pokemon_front = Spritesheet('imgs/pokemon_front.png')
        self.fight_background = pygame.image.load('./imgs/fight_background.png')

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

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.blit(self.fight_background, (0,0))
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