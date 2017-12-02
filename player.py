import pygame,random

class Player(object):

	def __init__(self):
	
		self.x = 325
		self.y = 325

		self.width = 30
		self.height = 30

		self.bulletW = 10
		self.bulletH = 10

		self.xSpeed = 0
		self.ySpeed = 0

		self.centerX = 0
		self.centeY = 0

		self.direction = 'down'

		self.health = 100

		self.bulletSpeed = 10

		self.sprite = 'sprites/playerDown.png'

		self.bulletSet = []
		self.rect = pygame.Rect


		self.dead = False

		self.bulletLeft = 'sprites/bulletLeft.png'
		self.bulletRight = 'sprites/bulletRight.png'
		self.bulletUp = 'sprites/bulletUp.png'
		self.bulletDown = 'sprites/bulletDown.png'

		#self.weapon = weapon
		# self.sprite = sprite #implement sprite selection for different characters

	def move(self,dx,dy):
		#moving player based on input
		self.x += dx
		self.y += dy

		#setting player direction based on direction of movement
		if dx > 0 and dy > 0:
			self.direction = 'downRight'
			self.sprite = 'sprites/playerDownRight.png'
			return
		if dx > 0 and dy < 0:
			self.direction = 'upRight'
			self.sprite = 'sprites/playerUpRight.png'
			return
		if dx < 0 and dy > 0:
			self.direction = 'downLeft'
			self.sprite = 'sprites/playerDownLeft.png'
			return
		if dx < 0 and dy < 0:
			self.direction = 'upLeft'
			self.sprite = 'sprites/playerUpLeft.png'
			return

		if dx < 0:
			self.direction = 'left'
			self.sprite = 'sprites/playerLeft.png'
		if dx > 0:
			self.direction = 'right'
			self.sprite = 'sprites/playerRight.png'
		if dy < 0:
			self.direction = 'up'
			self.sprite = 'sprites/playerUp.png'
		if dy > 0:
			self.direction = 'down'
			self.sprite = 'sprites/playerDown.png'

	def fire(self):
		self.bulletSet.append([self.centerX,self.centerY,self.direction])

	def moveBullets(self):
		for bullet in self.bulletSet:
			if bullet[2] == 'right':
				bullet[0] += self.bulletSpeed
			if bullet[2] == 'left':
				bullet[0] -= self.bulletSpeed
			if bullet[2] == 'up':
				bullet[1] -= self.bulletSpeed
			if bullet[2] == 'down':
				bullet[1] += self.bulletSpeed
			if bullet[2] == 'downRight':
				bullet[0] += self.bulletSpeed
				bullet[1] += self.bulletSpeed
			if bullet[2] == 'downLeft':
				bullet[0] -= self.bulletSpeed
				bullet[1] += self.bulletSpeed
			if bullet[2] == 'upRight':
				bullet[0] += self.bulletSpeed
				bullet[1] -= self.bulletSpeed
			if bullet[2] == 'upLeft':
				bullet[0] -= self.bulletSpeed
				bullet[1] -= self.bulletSpeed

			if bullet[0] > 650 or bullet[0] < 0:
				self.bulletSet.remove(bullet)
			elif bullet[1] > 650 or bullet[1] < 0:
				self.bulletSet.remove(bullet)

	def drawBullets(self,screen):
		for bullet in self.bulletSet:
			center = (int(bullet[0]),int(bullet[1]))
			pygame.draw.circle(screen,(255,0,0),center,5)


	def displayHealth(self,screen):
		healthbarPos = (30,30)
		if self.health >= 0:
			pygame.draw.rect(screen,(220,0,0),(healthbarPos,(20,150*self.health/100)))
		pygame.draw.rect(screen,(0,0,0),(30,30,20,150),3)


	def draw(self,screen):
		self.drawBullets(screen)
		self.moveBullets()

		self.rect = pygame.Rect((self.x,self.y),(50,50))
		self.centerX = self.rect.centerx
		self.centerY = self.rect.centery

		sprite = pygame.image.load(self.sprite)
		# pygame.draw.rect(screen,(0,0,0),
		# 	(self.x,self.y,30,30))
		screen.blit(sprite,self.rect)
		
		



