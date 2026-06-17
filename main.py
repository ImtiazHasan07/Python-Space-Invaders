import random
import pygame
from pygame.mixer_music import play

class Player:
    def __init__(self, game, height=45, width=45):
        shipImage = pygame.image.load('./images/player/ship.png')
        self.shootingSound = pygame.mixer.Sound('./sounds/player/shoot.wav')
        self.explosionSound = pygame.mixer.Sound('./sounds/player/explosion.wav')
        self.shipImage = pygame.transform.scale(shipImage, (height, width))
        self.laserImage = pygame.image.load('./images/player/laser.png')
        self.rect = self.shipImage.get_rect(center = (game.screenWidth // 2, game.screenHeight - 35))
        self.laserRects = []

    def checkCollision(self, laserRect):
        if laserRect.colliderect(self.rect):
            return True
        return False

class Enemy:
    def __init__(self, enemyType, game, x, y):
        enemyTypePoints = { 'enemy1': 10, 'enemy2': 20, 'enemy3': 30, 'special': 300 }
        self.enemyType = enemyType
        self.points = enemyTypePoints[enemyType]
        self.laserImage = pygame.image.load('./images/enemy/laser.png')
        self.shootingSound = pygame.mixer.Sound('./sounds/enemy/shoot.wav')
        self.explosionSound = pygame.mixer.Sound('./sounds/enemy/explosion.wav')
        self.laserRects = []
        self.cooldowns = {}
        self.cooldowns['explosion'] = 0.25 * game.fps
        if enemyType.lower() == 'special':
            self.width = 90
            self.height = 45
            shipImage = pygame.image.load(f'./images/enemy/{enemyType}/ship.png')
            explosionImage = pygame.image.load(f'./images/enemy/{enemyType}/ship.png')
            self.shipImage = pygame.transform.scale(shipImage, (self.width, self.height))
            self.explosionImage = pygame.transform.scale(explosionImage, (self.width, self.height))
            self.rect = self.shipImage.get_rect(topleft = (x, y))
            self.currentFrame = 'ship'
        else:
            self.width = 45
            self.height = 45
            frame1Image = pygame.image.load(f'./images/enemy/{enemyType}/frame_1.png')
            frame2Image = pygame.image.load(f'./images/enemy/{enemyType}/frame_2.png')
            explosionImage = pygame.image.load(f'./images/enemy/{enemyType}/explosion.png')
            self.frame1Image = pygame.transform.scale(frame1Image, (self.width, self.height))
            self.frame2Image = pygame.transform.scale(frame2Image, (self.width, self.height))
            self.explosionImage = pygame.transform.scale(explosionImage, (self.width, self.height))
            self.rect = self.frame1Image.get_rect(topleft = (x, y))
            self.currentFrame = 'frame_1'

    def checkCollision(self, laserRect):
        if laserRect.left >= self.rect.left and laserRect.right <= self.rect.right and laserRect.top >= self.rect.top and laserRect.bottom <= self.rect.bottom:
            return True
        return False

    def explode(self):
        self.currentFrame = 'explosion'
        self.explosionSound.play()

class Game:
    def __init__(self, screenWidth=850, screenHeight=650):
        pygame.init()
        pygame.display.set_caption('Space Invaders')
        self.backgroundMusic = pygame.mixer.Sound('./sounds/backgroundMusic.mp3')
        self.backgroundMusic.play(-1)
        backgroundImage = pygame.image.load('./images/background.jpg')
        self.backgroundImage = pygame.transform.scale(backgroundImage, (screenWidth, screenHeight))
        self.backgroundImageRect = self.backgroundImage.get_rect(topleft = (0, 0))
        self.laserImage = pygame.image.load('./images/enemy/laser.png')
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.tileWidth = screenWidth // 20
        self.tileHeight = screenHeight // 20
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        self.fps = 60   
        self.scoreFont = pygame.font.SysFont('Arial', 35)
        self.livesFont = pygame.font.SysFont('Arial', 35)
        self.startingMessageFont = pygame.font.SysFont('Arial', 50)
        self.gameOverMessageFont = pygame.font.SysFont('Arial', 40)
        self.youWinMessageFont = pygame.font.SysFont('Arial', 75)
        self.laserRects = { 'player': [], 'enemy': [] }
        self.cooldowns = {}
        self.score = 0
        self.lives = 3
        self.gameStarted = False
        self.gameRunning = True
        self.gameEnded = False
        self.player = Player(self)
        self.enemies = []
        self.walls = []
        self.enemyDirection = 'right'
        self.outcome = None
        self.setupEnemies()
        self.createWalls()

    def resetGame(self):
        self.laserRects = { 'player': [], 'enemy': [] }
        self.cooldowns = {}
        self.score = 0
        self.lives = 3
        self.gameStarted = False
        self.gameRunning = True
        self.gameEnded = False
        self.player = Player(self)
        self.enemies = []
        self.walls = []
        self.enemyDirection = 'right'
        self.outcome = None
        self.setupEnemies()
        self.createWalls()

    def checkEnemyDistance(self):
        for index, enemy in enumerate(self.enemies):
            if self.enemies[index].rect.bottom >= self.player.rect.top:
                return True
        return False

    def setupEnemies(self):
        marginLeft = 5
        marginTop = 100
        inBetweenSpacing = 50

        # enemy = Enemy('special', self, 0, marginTop - 50)
        # enemy.rect.center=(self.screenWidth // 2, enemy.rect.top)
        # self.enemies.append(enemy)
        
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
    
    def moveAllEnemies(self, direction, amount):
        for index, enemies in enumerate(self.enemies):
            if self.enemies[index].enemyType != 'special':
                if direction.lower() == 'left':
                        self.enemies[index].rect.move_ip(-amount, 0)
                elif direction.lower() == 'right':
                        self.enemies[index].rect.move_ip(amount, 0)
                elif direction.lower() == 'up':
                    self.enemies[index].rect.move_ip(0, -amount)
                elif direction.lower() == 'down':
                    self.enemies[index].rect.move_ip(0, amount)

    def createWalls(self):
        marginLeft = 50
        marginBottom = 150
        width = 12
        height = 12
        for x in range(9):
            for y in range(4):
                for z in range(4):
                    brick = pygame.Rect(marginLeft + (210 * z) + (width * x), self.screenHeight - marginBottom + (height * y), width, height)
                    self.walls.append(brick)
    
    def execute(self):
        while self.gameRunning:
            event = pygame.event.poll()
            keys = pygame.key.get_pressed()
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.backgroundImage, self.backgroundImageRect)
            scoreText = self.scoreFont.render('SCORE {:02}'.format(self.score), False, (255, 255, 255))
            livesText = self.livesFont.render('LIVES {:02}'.format(self.lives), False, (255, 255, 255))
            startingMessageText = self.startingMessageFont.render('Press any key to begin!', False, (255, 255, 255))
            gameOverMessageText = self.gameOverMessageFont.render('Game Over!', False, (255, 255, 255))
            youWinMessageText = self.youWinMessageFont.render('You Win!', False, (255, 255, 255))
            scoreRect = scoreText.get_rect(topleft=(5, 5))
            livesRect = livesText.get_rect(topright=(self.screenWidth - 5, 5))
            startingMessageRect = startingMessageText.get_rect(center=(self.screenWidth // 2, self.screenHeight // 2))
            gameOverMessageTextRect = gameOverMessageText.get_rect(center=(self.screenWidth // 2, self.screenHeight // 2))
            youWinMessageTextRect = youWinMessageText.get_rect(center=(self.screenWidth // 2, self.screenHeight // 2))
            self.screen.blit(self.player.shipImage, self.player.rect)
            self.screen.blit(scoreText, scoreRect)
            self.screen.blit(livesText, livesRect)

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
                if self.enemies[index].currentFrame == 'ship':
                    self.screen.blit(enemy.shipImage, enemy.rect)
                elif self.enemies[index].currentFrame == 'frame_1':
                    self.screen.blit(enemy.frame1Image, enemy.rect) 
                elif self.enemies[index].currentFrame == 'frame_2':
                    self.screen.blit(enemy.frame2Image, enemy.rect)
                elif self.enemies[index].currentFrame == 'explosion':
                    self.screen.blit(enemy.explosionImage, enemy.rect)
                    self.enemies[index].cooldowns['explosion'] -= 1
                    if self.enemies[index].cooldowns['explosion'] <= 0:
                        enemies.pop()
            self.enemies = enemies

            for index, brick in enumerate(self.walls):
                pygame.draw.rect(self.screen, (75, 250, 75), brick)

            if event.type == pygame.QUIT:
                self.gameRunning = False
            if not self.gameStarted:
                self.screen.blit(startingMessageText, startingMessageRect)
                if True in keys:
                    self.gameStarted = True
            elif self.gameEnded:
                self.cooldowns['gameEnded'] -= 1
                if self.outcome == 'win':
                    self.screen.blit(youWinMessageText, youWinMessageTextRect)
                elif self.outcome == 'lose':
                    self.screen.blit(gameOverMessageText, gameOverMessageTextRect)
                if self.cooldowns['gameEnded'] <= 0:
                    self.resetGame()
            elif not self.cooldowns.get('pause') or self.cooldowns['pause'] <= 0:
                if keys[pygame.K_SPACE] and not self.cooldowns.get('playerLaser'):
                    seconds = 1
                    self.cooldowns['playerLaser'] = self.fps * seconds
                    laserRect = self.player.laserImage.get_rect()
                    laserRect.center = self.player.rect.center
                    laserRect.bottom = self.player.rect.top
                    self.screen.blit(self.player.laserImage, laserRect)
                    self.player.laserRects.append(laserRect)
                    self.player.shootingSound.play()
                if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.player.rect.left > 0:
                    self.player.rect.move_ip(-5, 0)
                elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.player.rect.right < self.screenWidth:
                    self.player.rect.move_ip(5, 0)
                        
                if not self.cooldowns.get('enemyLaser'):
                    seconds = 3
                    self.cooldowns['enemyLaser'] = self.fps * seconds
                    randomEnemy = random.choice(self.enemies)
                    laserRect = randomEnemy.laserImage.get_rect()
                    laserRect.center = randomEnemy.rect.center
                    laserRect.top = randomEnemy.rect.bottom
                    self.screen.blit(randomEnemy.laserImage, laserRect)
                    randomEnemy.laserRects.append(laserRect)
                    randomEnemy.shootingSound.play()

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
                        for index, wall in enumerate(self.walls):
                            if wall.colliderect(laserRect):
                                playerLaserRects.pop()
                                self.walls.pop(index)
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
                                self.player.explosionSound.play()
                            else:
                                for i, wall in enumerate(self.walls):
                                    if wall.colliderect(laserRect):
                                        enemyLaserRects.pop()
                                        self.walls.pop(i)
                                        break
                    self.enemies[index].laserRects = enemyLaserRects 

                if len(self.enemies) == 0 or self.lives <= 0 or self.checkEnemyDistance():
                    seconds = 5
                    self.cooldowns['gameEnded'] = seconds * self.fps
                    self.gameEnded = True
                    if len(self.enemies) == 0:
                        self.outcome = 'win'
                    else:
                        self.outcome = 'lose'
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.execute()