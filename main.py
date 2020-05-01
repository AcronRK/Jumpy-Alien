from sprites import *
import sys


class Game:
    def __init__(self):
        # initialize game window
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.dir = os.path.dirname(__file__)
        img_dir = os.path.join(self.dir, "img")
        sheet = os.path.join(img_dir, "spritesheet")
        self.spritesheet = Spritesheet(os.path.join(sheet, SPRITESHEET))
        self.player_spritesheet = Spritesheet(os.path.join(sheet, PLAYER_SPRITESHEET))

    def new(self):
        # Start a new game
        # init score
        self.score = 0
        # create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        # create player
        self.player = Player(self)
        self.all_sprites.add(self.player)

        # create platform
        for platform in PLATFORM_LIST:
            p = Platform(self, *platform)
            self.all_sprites.add(p)
            self.platforms.add(p)

        # create projectiles
        p = Projectile(100)
        self.all_sprites.add(p)
        self.projectiles.add(p)

        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game loop - Update
        self.platforms.update()

        # move camera when player goes to 1/3 of the screen
        if self.player.rect.top <= HEIGHT / 3:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    # if platform moves off the screen delete it
                    plat.kill()
                    self.score += 1
        else:
            for plat in self.platforms:
                plat.rect.y += MOVING_SCREEN

        # check if player bumps head with a platform
        if self.player.vel.y < 0 and self.player.can_collide:
            platform_hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if platform_hits:
                # find the lowest platform hit by the player
                lowest = platform_hits[0]
                for hit in platform_hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                # if player's feet hit platform move player to the platform
                if self.player.pos.y < lowest.rect.bottom:
                    self.player.pos.y = lowest.rect.bottom
                    self.player.vel.y = 0
                    self.player.jumping = False


        # check collision between player and platform
        # check if player hits platform only when falling ( y > 0 )
        if self.player.vel.y > 0:
            # platform_hits returns all the platforms which collided with the player
            platform_hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if platform_hits:
                # find the lowest platform hit by the player
                lowest = platform_hits[0]
                for hit in platform_hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                # if player's feet hit platform move player to the platform
                if self.player.pos.y < lowest.rect.centery:
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0
                    self.player.jumping = False



        self.player.update()
        self.projectiles.update()

        # when player dies
        if self.player.rect.bottom > HEIGHT:
            self.playing = False

        # check if player collides with projectile
        projectile_hits = platform_hits = pygame.sprite.spritecollide(self.player, self.projectiles, False)
        if projectile_hits:
            self.playing = False

        # removing projectiles
        for projectile in self.projectiles:
            if projectile.rect.top >= HEIGHT:
                projectile.kill()

        # spawning projectiles
        percentage = random.randrange(0, 100)
        projectile_nr = random.randint(1, 3)
        if percentage > 95 and len(self.projectiles) < projectile_nr:
            x = random.randrange(0, WIDTH - PROJECTILE_WIDTH)
            projectile = Projectile(x)
            self.all_sprites.add(projectile)
            self.projectiles.add(projectile)

        # spawn new platforms as game progresses
        # we want atleast 6 platforms on the screen
        while len(self.platforms) < 7:
            width = random.randrange(30, 100)
            p = Platform(self,
                         random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30))
            self.all_sprites.add(p)
            self.platforms.add(p)

    def events(self):
        # Game loop - Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_UP:
                    self.player.jump()

    def draw(self):
        # Game loop - Draw
        # background = pygame.image.load(os.path.join("img", "black.png"))
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        # show score
        self.draw_text("Score: " + str(self.score), 25, WHITE, 35, 0)

        # flip display after drawing
        pygame.display.flip()

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 50, WHITE, WIDTH / 2, 4)
        self.draw_text("Move with arrows, Space to jump", 30, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 30, WHITE, WIDTH / 2, HEIGHT * 0.75)
        pygame.display.flip()
        self.waitKey()

    def show_gameover_screen(self):
        # check if player wants to quit
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 50, WHITE, WIDTH / 2, 4)
        self.draw_text("Score: " + str(self.score), 30, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press key to play again", 30, WHITE, WIDTH / 2, HEIGHT * 0.75)
        pygame.display.flip()
        self.waitKey()

    def waitKey(self):
        # function used in starting and ending game to wait for a key to be pressed
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_gameover_screen()

pygame.quit()
