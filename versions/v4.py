import pygame

class Player:
    def __init__(self, screenWidth, screenHeight):
        self.shipImage = pygame.image.load('./images/player/ship.png')
        self.laserImage = pygame.image.load('./images/player/laser.png')
        self.rect = self.shipImage.get_rect(center = (screenWidth // 2, screenHeight - 35))
        self.laserRects = []

class Enemy:
    def __init__(self, enemyType, x, y, height=45, width=45):
        frame1Image = pygame.image.load(f'./images/enemy/{enemyType}/frame_1.png')
        frame2Image = pygame.image.load(f'./images/enemy/{enemyType}/frame_2.png')
        self.height = height
        self.width = width
        self.frame1Image = pygame.transform.scale(frame1Image, (height, width))
        self.frame2Image = pygame.transform.scale(frame2Image, (height, width))
        self.laserImage = pygame.image.load('./images/enemy/laser.png')
        self.rect = self.frame1Image.get_rect(topleft = (x, y))
        self.laserRects = []

class Game:
    def __init__(self, screenWidth=500, screenHeight=350):
        pygame.init()
        pygame.display.set_caption('Space Invaders')
        self.laserImage = pygame.image.load('./images/enemy/laser.png')
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.tileWidth = screenWidth // 20
        self.tileHeight = screenHeight // 20
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        self.fps = 60   
        self.scoreFont = pygame.font.SysFont('Arial', 20)
        self.livesFont = pygame.font.SysFont('Arial', 20)
        self.startingMessageFont = pygame.font.SysFont('Arial', 20)
        self.gameOverMessageFont = pygame.font.SysFont('Arial', 40)
        self.laserRects = { 'player': [], 'enemy': [] }
        self.cooldowns = {}
        self.score = 0
        self.lives = 3
        self.gameRunning = True
        self.gameStarted = False
        self.player = Player(screenWidth, screenHeight)
        self.enemies = []
        self.setupEnemies()
    
    def setupEnemies(self):
        for x in range(9):
            enemy = Enemy('enemy1', 10 + (x * 55), 100)
            self.enemies.append(enemy)

        for x in range(9):
            for y in range(2):
                enemy = Enemy('enemy2', 10 + (x * 55), (55 * y) + 155)
                self.enemies.append(enemy)

        for x in range(9):
            for y in range(2):
                enemy = Enemy('enemy3', 10 + (x * 55), (55 * y) + 265)
                self.enemies.append(enemy)
    
    def execute(self):
        while self.gameRunning:
            event = pygame.event.poll()
            keys = pygame.key.get_pressed()
            self.screen.fill((0, 0, 0))
            scoreText = self.scoreFont.render('SCORE {:02}'.format(self.score), False, (255, 255, 255))
            livesText = self.livesFont.render('LIVES {:02}'.format(self.lives), False, (255, 255, 255))
            startingMessageText = self.startingMessageFont.render('Press any key to begin!', False, (255, 255, 255))
            gameOverText = self.gameOverMessageFont.render('Game Over!', False, (255, 255, 255))
            scoreRect = scoreText.get_rect(topleft=(5, 5))
            livesRect = livesText.get_rect(topright=(self.screenWidth - 5, 5))
            startingMessageRect = startingMessageText.get_rect(center=(self.screenWidth // 2, self.screenHeight // 2))
            gameOverTextRect = gameOverText.get_rect(center=(self.screenWidth // 2, self.screenHeight // 2))
            self.screen.blit(self.player.shipImage, self.player.rect)

            for enemy in self.enemies:
                self.screen.blit(enemy.frame2Image, enemy.rect)
                
            self.screen.blit(scoreText, scoreRect)
            self.screen.blit(livesText, livesRect)

            if event.type == pygame.QUIT:
                self.gameRunning = False
            if not self.gameStarted:
                self.screen.blit(startingMessageText, startingMessageRect)
                if True in keys:
                    self.gameStarted = True
            else:
                if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.player.rect.left > 0:
                    self.player.rect.move_ip(-5, 0)
                elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.player.rect.right < self.screenWidth:
                    self.player.rect.move_ip(5, 0)
                if keys[pygame.K_SPACE]:
                    if not self.cooldowns.get('playerLaser'):
                        seconds = 1
                        self.cooldowns['playerLaser'] = self.fps * seconds
                        laserRect = self.player.laserImage.get_rect()
                        laserRect.center = self.player.rect.center
                        laserRect.bottom = self.player.rect.top
                        self.screen.blit(self.player.laserImage, laserRect)
                        self.laserRects['player'].append(laserRect)

                for cooldownName, cooldown in self.cooldowns.items():
                    if cooldown > 0:
                        self.cooldowns[cooldownName] -= 1

                for laserCategory in self.laserRects:
                    for laserRect in self.laserRects[laserCategory]:
                        if laserCategory == 'player' and laserRect.bottom >= 0:
                            laserRect.move_ip(0, -5)
                            self.screen.blit(self.player.laserImage, laserRect)
                        elif laserCategory == 'enemy' and laserRect.top <= self.screenHeight:
                            laserRect.move_ip(0, 5)
                            self.screen.blit(self.enemy.laserImage, laserRect)
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.execute()
