import pygame

class Game:
    def __init__(self, screenWidth=500, screenHeight=350):
        pygame.init()
        pygame.display.set_caption('Space Invaders')
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
        self.playerShipImage = pygame.image.load('./images/player/ship.png')
        self.playerLaserImage = pygame.image.load('./images/player/laser.png')
        self.enemyLaserImage = pygame.image.load('./images/enemies/laser.png')
        self.playerRect = self.playerShipImage.get_rect()
        self.playerRect.center = (screenWidth // 2, screenHeight - 35)
        self.laserRects = { 'player': [], 'enemy': [] }
        self.cooldowns = {}
        self.score = 0
        self.lives = 3
        self.gameRunning = True
        self.gameStarted = False

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
            self.screen.blit(scoreText, scoreRect)
            self.screen.blit(livesText, livesRect)
            self.screen.blit(self.playerShipImage, self.playerRect)

            if event.type == pygame.QUIT:
                self.gameRunning = False
            if not self.gameStarted:
                self.screen.blit(startingMessageText, startingMessageRect)
                if True in keys:
                    self.gameStarted = True
            else:
                if event.type == pygame.QUIT:
                    self.gameRunning = False
                if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.playerRect.left > 0:
                    self.playerRect.move_ip(-5, 0)
                elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.playerRect.right < self.screenWidth:
                    self.playerRect.move_ip(5, 0)
                if keys[pygame.K_SPACE]:
                    if not self.cooldowns.get('playerLaser'):
                        seconds = 1
                        self.cooldowns['playerLaser'] = self.fps * seconds
                        laserRect = self.playerLaserImage.get_rect()
                        laserRect.center = self.playerRect.center
                        laserRect.bottom = self.playerRect.top
                        self.screen.blit(self.playerLaserImage, laserRect)
                        self.laserRects['player'].append(laserRect)

                for cooldownName, cooldown in self.cooldowns.items():
                    if cooldown > 0:
                        self.cooldowns[cooldownName] -= 1

                for laserCategory in self.laserRects:
                    for laserRect in self.laserRects[laserCategory]:
                        if laserCategory == 'player' and laserRect.bottom >= 0:
                            laserRect.move_ip(0, -5)
                            self.screen.blit(self.playerLaserImage, laserRect)
                        elif laserCategory == 'enemy' and laserRect.bottom <= self.screenHeight:
                            laserRect.move_ip(0, 5)
                            self.screen.blit(self.playerLaserImage, laserRect)

            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.execute()
