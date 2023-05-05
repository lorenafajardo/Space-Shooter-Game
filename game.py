import pygame
import random
import math

# Initialize Pygame
pygame.init()
pygame.font.init()

# Game's Screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# Background
background = pygame.image.load("resources/images/background.jpg")

# Sound
background_sound = pygame.mixer.music.load(
    "resources/audios/background_music.mp3")
pygame.mixer.music.play(-1)

# Icon's Game
icon = pygame.image.load("resources/images/icon.png")
pygame.display.set_icon(icon)

# Game's Name
pygame.display.set_caption("Space Shooter")

# Explosion Sound
explosion_sound = pygame.mixer.Sound("resources/audios/explosion.wav")

# Player Variables
player_img = pygame.image.load("resources/images/player.png")
playerX = 350
playerY = 480
player_positionX = 0

# Bullet Variables
bullet_img = pygame.image.load("resources/images/bullet.png")
bulletX = 0
bulletY = 480
bullet_state = 'loaded'
bullet_positionY = 4

# Enemy Variables
enemy_img = []
enemyX = []
enemyY = []
enemy_positionX = []
enemies_number = 4

for i in range(enemies_number):
	enemy_img.append(pygame.image.load("resources/images/enemy.png"))
	enemyX.append(random.randint(0, 736))
	enemyY.append(random.randint(0, 150))
	enemy_positionX.append(2)

# Player Function
def player(playerX, playerY):
	screen.blit(player_img, (playerX, playerY))

# Shot Function
def shot(bulletX, bulletY):
	global bullet_state
	bullet_state = "fired"
	screen.blit(bullet_img, (bulletX, bulletY))

# Enemy Function
def enemy(enemyX, enemyY, i):
	screen.blit(enemy_img[i], (enemyX, enemyY))

# Collison Fuction
def isCollided(bulletX, bulletY, enemyX, enemyY):
	distance = math.sqrt(math.pow(bulletX-enemyX, 2)+math.pow(bulletY-enemyY, 2))

	if distance <= 30:
		return True
	else:
		return False

# Display Score
score = 0
font = pygame.font.Font("freesansbold.ttf",32)
def showPunctuation():
	score_value = font.render("SCORE: " + str(score), True, "grey")
	screen.blit(score_value, (10, 10))

# Execution loop
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

			if event.key == pygame.K_LEFT:
				player_positionX = -2

			if event.key == pygame.K_RIGHT:
				player_positionX = 2

			if event.key == pygame.K_SPACE:
				if bullet_state == "loaded":
					bulletX = playerX
					shot(bulletX, bulletY)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				player_positionX = 0

	screen.blit(background, (0, 0))
	playerX += player_positionX
  	
	#Boundaries

	if playerX < 0:
		playerX = 0
	elif playerX > 709:
		playerX = 709

	if bulletY <= 0:
		bulletY = 480
		bullet_state = "loaded"

	if bullet_state == "fired":
		shot(bulletX, bulletY)
		bulletY -= bullet_positionY

	for i in range(enemies_number):
		enemyX[i] += enemy_positionX[i]

		if enemyX[i] < 0:
			enemy_positionX[i] = 1.5
			enemyY[i] += random.randint(0, 68)
		elif enemyX[i] > 736:
			enemy_positionX[i] = -1.5
			enemyY[i] += random.randint(0, 68)
		
		if enemyY[i] > 430:
			screen.blit(background, (0, 0))
			font2 = pygame.font.Font("freesansbold.ttf",60)
			game_over = font2.render("Game Over ", True, "white")
			screen.blit(game_over, (220, 250))
			break

		if isCollided(bulletX,bulletY,enemyX[i],enemyY[i]):
			explosion_sound.play()
			bulletY=480
			bullet_state ='loaded'
			score+=10

			enemyX[i] = random.randint(0,736)
			enemyY[i] = random.randint(0,150)


		enemy(enemyX[i],enemyY[i],i)

	player(playerX, playerY)
	showPunctuation()
	pygame.display.update()

pygame.quit()
