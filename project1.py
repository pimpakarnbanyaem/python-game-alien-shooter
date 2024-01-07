import pygame
import math
import random
from pygame import mixer
from csv import*

pygame.font.init()
pygame.init()

red = (255,0,0)
WHITE = (255,255,255)
WIDTH,HEIGHT = 800,600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

#icon & caption
pygame.display.set_caption("เกมยิงเอเลี่ยน")
icon=pygame.image.load('spaceship.png')

pygame.display.set_icon(icon)

#image & bg
BG = pygame.transform.scale((pygame.image.load('background-black.png')), (WIDTH,HEIGHT))

#player(spaceship)
SPACESHIP_IMAGE = pygame.image.load('spaceship.png')
SPACESHIP = pygame.transform.scale(SPACESHIP_IMAGE, (64,64))
playerX = 370 #ตำแหน่งX ของ spaceship
playerY = 480 #ตำแหน่งY ของ spaceship
playerX_change = 0 #การเคลื่อนที่ของ spaceship ในแกน X

#enemy(alien)
ALIEN = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    ALIEN_IMAGE = pygame.image.load('alien.png')
    
    ALIEN.append(pygame.transform.scale(ALIEN_IMAGE,(70,70)))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(7)
    enemyY_change.append(50)

#bomb
BOMB_IMAGE = pygame.image.load('bomb.png')
BOMB = pygame.transform.scale(BOMB_IMAGE,(64,64))
bombX = random.randint(0,735)
bombY = 0
bombY_change = 2

#bullet
BULLET = pygame.image.load('bullet555.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#score
font = pygame.font.Font('freesansbold.ttf',32)
score_value = 0
textX = 10
textY = 10

#game over
over_font = pygame.font.Font('freesansbold.ttf',64)

#lives
lives_value = 3
lives = font.render("lives :" + str(lives_value),True, (WHITE))

def show_lives(x,y):
    lives = font.render("lives :" + str(lives_value),True, (WHITE))
    WIN.blit(lives, (x, y))

def show_score(x,y):
    score = font.render("score :" + str(score_value),True, (WHITE))
    WIN.blit (score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (WHITE))
    WIN.blit (over_text, (200, 250))

def player (x, y):
    WIN.blit (SPACESHIP, (x, y))

def enemy (x, y, i):
    WIN.blit (ALIEN[i], (x, y))

def bomb (x, y):
    WIN.blit (BOMB, (x, y))

def fire_bullet (x, y):
    global bullet_state
    bullet_state = "fire"
    WIN.blit(BULLET , (x+16,y+10))

def isCollision (enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 35:
        return True
    else:
        return False

def bombCollision (bombX,bombY,bulletX,bulletY):
    b_distance = math.sqrt((math.pow(bombX-bulletX,2)) + (math.pow(bombY-bulletY,2)))
    if b_distance <  30:
        return True
    else:
        return False

def getHighscore ():
    with open("Highest Score.csv","r",encoding='utf-8') as f:
       return f.read()

try:
    highScore = int(getHighscore())
except:
    highScore = 0

#game main loop
run = True
while run:
    WIN.fill((0,0,0))
    WIN.blit(BG ,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:    #ทำให้ spaceship เคลื่อนที่ได้ตามการกดแป้นพิมพ์ไปทางซ้าย
            if event.key == pygame.K_LEFT:
                playerX_change = -7
            if event.key == pygame.K_RIGHT: #ทำให้ spaceship เคลื่อนที่ได้ตามการกดแป้นพิมพ์ไปทางขวา
                playerX_change = 7
            if event.key == pygame.K_SPACE: #กด spacebar = ยิ่งปืน
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('sounds_fire.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0          #การไม่กดปุ่มซ้ายขวา = หยุด
    
    playerX += playerX_change
    if playerX <= 0 :
        playerX = 0
    elif playerX >= 736 :
        playerX = 736
    
    bombY += bombY_change
    if bombY >= 900 :
        bombY = 0
        bombX = random.randint(0,735)
    
  
    enemyX += enemyX_change
    if playerX <= 0 :
        playerX = 0
    elif playerX >= 736 :
        playerX = 736

    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range (num_of_enemies):
                enemyY[j] =2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 :
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736 :
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            point_sound = mixer.Sound('sounds_point.wav')
            point_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,100)

        enemy(enemyX[i],enemyY[i],i)  

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
 
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    collision_bb = bombCollision (bombX,bombY,bulletX,bulletY)
    if collision_bb:
        explosion_sound = mixer.Sound('expl6.wav')
        explosion_sound.play()
        bulletY = 480
        bullet_state = "ready"
        lives_value -= 1
        print(lives_value)
        bombX = random.randint(0,735)
        bombY = 0
    if lives_value <= 0:
        WIN.fill((0,0,0))
        game_over_text()

    if highScore < score_value :
        highScore = score_value
    with open("Highest Score.csv","w",encoding='utf-8') as f:
        f.write(str(highScore))
    highscore_text = font.render("highscore :" + str(highScore),True, (red))
    WIN.blit (highscore_text, (10,40))

        
    player(playerX,playerY)
    bomb(bombX, bombY)
    show_score(textX, textY)
    show_lives(WIDTH - lives.get_width()-10,10)
    getHighscore()
    pygame.display.update()      




                              
