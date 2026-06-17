import pygame
import random

class Player:
    def __init__(self, screenWidth, screenHeight):
        self.shipImage = pygame.image.load('./images/player/ship.png')
        self.laserImage = pygame.image.load('./images/player/laser.png')
        # self.explosionImage = pygame.image.load(f'./images/player/explosion.png')
        # # self.explosionImage = pygame.transform.scale(self.explosionImage, (height, width))
        self.rect = self.shipImage.get_rect(center = (screenWidth // 2, screenHeight - 35))
        self.laserRects = []

    def checkCollision(self, laserRect):
        if laserRect.colliderect(self.rect):
            return True
        return False

class Enemy:
    def __init__(self, enemyType, game, x, y, height=45, width=45):
        frame1Image = pygame.image.load(f'./images/enemy/{enemyType}/frame_1.png')
        frame2Image = pygame.image.load(f'./images/enemy/{enemyType}/frame_2.png')
        explosionImage = pygame.image.load(f'./images/enemy/{enemyType}/explosion.png')
        enemyTypePoints = { 'enemy1': 10, 'enemy2': 20, 'enemy3': 30 }
        self.height = height
        self.width = width
        self.frame1Image = pygame.transform.scale(frame1Image, (height, width))
        self.frame2Image = pygame.transform.scale(frame2Image, (height, width))
        self.explosionImage = pygame.transform.scale(explosionImage, (height, width))
        self.laserImage = pygame.image.load('./images/enemy/laser.png')
        self.rect = self.frame1Image.get_rect(topleft = (x, y))
        self.points = enemyTypePoints[enemyType]
        self.currentFrame = 'frame_1'
        self.laserRects = []
        self.cooldowns = {}
        self.cooldowns['explosion'] = 0.25 * game.fps

    def checkCollision(self, laserRect):
        if laserRect.left >= self.rect.left and laserRect.right <= self.rect.right and laserRect.top >= self.rect.top and laserRect.bottom <= self.rect.bottom:
            return True
        return False

    def explode(self):
        self.currentFrame = 'explosion'

class Game:
    def __init__(self, screenWidth=850, screenHeight=650):
        pygame.init()
        pygame.display.set_caption('Space Invaders')
        backgroundImage = pygame.image.load('./images/background.jpg')
        self.backgroundImage = pygame.transform.scale(backgroundImage, (screenWidth, screenHeight))
        self.backgroundImageRect = self.backgroundImage.get_rect(topleft = (0, 0))
        self.laserImage = pygame.image.load('./images/enemy/laser.png')
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.enemyHeight = 45
        self.enemyWidth = 45
        self.tileWidth = screenWidth // 20
        self.tileHeight = screenHeight // 20
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        self.fps = 60   
        self.scoreFont = pygame.font.SysFont('Arial', 35)
        self.livesFont = pygame.font.SysFont('Arial', 35)
        self.startingMessageFont = pygame.font.SysFont('Arial', 50)
        self.gameOverMessageFont = pygame.font.SysFont('Arial', 40)
        self.laserRects = { 'player': [], 'enemy': [] }
        self.cooldowns = {}
        self.score = 0
        self.lives = 3
        self.gameRunning = True
        self.gameStarted = False
        self.player = Player(screenWidth, screenHeight)
        self.enemies = []
        self.enemyDirection = 'right'
        self.setupEnemies()

    def checkEnemyDistance(self):
        for index, enemy in enumerate(self.enemies):
            if self.enemies[index].rect.bottom >= self.player.rect.top:
                return True
        return False

    def setupEnemies(self):
        marginLeft = 5
        marginTop = 100
        inBetweenSpacing = 50

        for x in range(9):
            enemy = Enemy('enemy1', self, marginLeft + (x * inBetweenSpacing), marginTop)
            self.enemies.append(enemy)

        for x in range(9):
            for y in range(2):
                enemy = Enemy('enemy2', self, marginLeft + (x * inBetweenSpacing), (inBetweenSpacing * y) + marginTop + 55)
                self.enemies.append(enemy)

        for x in range(9):
            for y in range(2):
                enemy = Enemy('enemy3', self, marginLeft + (x * inBetweenSpacing), (inBetweenSpacing * y) + marginTop + (55 * 3))
                self.enemies.append(enemy)

    def gameOver(self):
        print('game over')

    def win(self):
        print('You win!')

    def moveAllEnemies(self, direction, amount):
        for index, enemies in enumerate(self.enemies):
            if direction.lower() == 'left':
                    self.enemies[index].rect.move_ip(-amount, 0)
            elif direction.lower() == 'right':
                    self.enemies[index].rect.move_ip(amount, 0)
            elif direction.lower() == 'up':
                self.enemies[index].rect.move_ip(0, -amount)
            elif direction.lower() == 'down':
                self.enemies[index].rect.move_ip(0, amount)

    def execute(self):
        while self.gameRunning:
            event = pygame.event.poll()
            keys = pygame.key.get_pressed()
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.backgroundImage, self.backgroundImageRect)
            scoreText = self.scoreFont.render('SCORE {:02}'.format(self.score), False, (255, 255, 255))
            livesText = self.livesFont.render('LIVES {:02}'.format(self.lives), False, (255, 255, 255))
            startingMessageText = self.startingMessageFont.render('Press any key to begin!', False, (255, 255, 255))
            gameOverText = self.gameOverMessageFont.render('Game Over!', False, (255, 255, 255))
            scoreRect = scoreText.get_rect(topleft=(5, 5))
            livesRect = livesText.get_rect(topright=(self.screenWidth - 5, 5))
            startingMessageRect = startingMessageText.get_rect(center=(self.screenWidth // 2, self.screenHeight // 2))
            gameOverTextRect = gameOverText.get_rect(center=(self.screenWidth // 2, self.screenHeight // 2))
            self.screen.blit(self.player.shipImage, self.player.rect)

            if not self.cooldowns.get('enemyAnimation') or self.cooldowns['enemyAnimation'] == 0:
                seconds = 0.5
                self.cooldowns['enemyAnimation'] = self.fps * seconds
                for index, enemy in enumerate(self.enemies):
                    if not self.enemies[index].currentFrame == 'explosion':
                        if self.enemies[index].currentFrame == 'frame_1':
                            self.enemies[index].currentFrame = 'frame_2'
                        elif self.enemies[index].currentFrame == 'frame_2':
                            self.enemies[index].currentFrame = 'frame_1'

            enemies = []
            for index, enemy in enumerate(self.enemies):
                enemies.append(enemy)
                if self.enemies[index].currentFrame == 'explosion':
                    self.screen.blit(enemy.explosionImage, enemy.rect)
                    self.enemies[index].cooldowns['explosion'] -= 1
                    if self.enemies[index].cooldowns['explosion'] <= 0:
                        enemies.pop()
                elif self.enemies[index].currentFrame == 'frame_1':
                    self.screen.blit(enemy.frame1Image, enemy.rect) 
                elif self.enemies[index].currentFrame == 'frame_2':
                    self.screen.blit(enemy.frame2Image, enemy.rect)
            self.enemies = enemies

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
                        self.player.laserRects.append(laserRect)

                if not self.cooldowns.get('enemyLaser'):
                    seconds = 5
                    self.cooldowns['enemyLaser'] = self.fps * seconds
                    randomEnemy = random.choice(self.enemies)
                    laserRect = randomEnemy.laserImage.get_rect()
                    laserRect.center = randomEnemy.rect.center
                    laserRect.top = randomEnemy.rect.bottom
                    self.screen.blit(randomEnemy.laserImage, laserRect)
                    randomEnemy.laserRects.append(laserRect)

                if not self.cooldowns.get('alienMovement'):
                    seconds = 0.75
                    amount = 25
                    margin = 5
                    self.cooldowns['alienMovement'] = seconds * self.fps
                    if self.enemyDirection == 'left':
                        self.moveAllEnemies('left', amount)
                    elif self.enemyDirection == 'right':
                        self.moveAllEnemies('right', amount)

                    for index, enemy in enumerate(self.enemies):
                        if self.enemies[index].rect.left <= margin:
                            self.moveAllEnemies('down', amount)
                            self.enemyDirection = 'right'
                            break
                        elif self.enemies[index].rect.right >= self.screenWidth - margin:
                            self.moveAllEnemies('down', amount)
                            self.enemyDirection = 'left'
                            break

                for cooldownName, cooldown in self.cooldowns.items():
                    if cooldown > 0:
                        self.cooldowns[cooldownName] -= 1

                playerLaserRects = []
                for laserRect in self.player.laserRects:
                    if laserRect.bottom >= 0:
                        laserRect.move_ip(0, -5)
                        self.screen.blit(self.player.laserImage, laserRect)
                        playerLaserRects.append(laserRect)
                        for enemy in self.enemies:
                            if enemy.checkCollision(laserRect):
                                playerLaserRects.pop()
                                self.score += enemy.points
                                enemy.explode()
                                break
                self.player.laserRects = playerLaserRects
                for index, enemy in enumerate(self.enemies):
                    enemyLaserRects = []
                    for laserRect in enemy.laserRects:
                        if laserRect.top <= self.screenHeight:
                            laserRect.move_ip(0, 5)
                            self.screen.blit(self.enemies[index].laserImage, laserRect)
                            enemyLaserRects.append(laserRect)
                            if self.player.checkCollision(laserRect):
                                enemyLaserRects.pop()
                                self.lives -= 1
                    self.enemies[index].laserRects = enemyLaserRects 

                if len(self.enemies) == 0:
                    self.win()

                if self.lives <= 0 or self.checkEnemyDistance():
                    self.gameOver()
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.execute()