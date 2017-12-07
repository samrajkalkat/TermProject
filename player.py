import pygame,random

class Player(object):

	def __init__(self,color):
		self.color = color
	
		self.x = 275
		self.y = 275

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

		if self.color == 'red':
			self.sprite = 'sprites/pDown.png'
		if self.color == 'blue':
			self.sprite = 'sprites/p2Down.png'
		else:
			self.sprite = 'sprites/p2Down.png'

		self.bulletSet = []
		self.rect = pygame.Rect

		self.spriteHeight = 0
		self.spriteWidth = 0
		

		self.dead = False


		self.score = 0

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
		if self.color == 'red':
			if dx > 0 and dy > 0:
				self.direction = 'downRight'
				self.sprite = 'sprites/pDownRight.png'
				return
			if dx > 0 and dy < 0:
				self.direction = 'upRight'
				self.sprite = 'sprites/pUpRight.png'
				return
			if dx < 0 and dy > 0:
				self.direction = 'downLeft'
				self.sprite = 'sprites/pDownLeft.png'
				return
			if dx < 0 and dy < 0:
				self.direction = 'upLeft'
				self.sprite = 'sprites/pUpLeft.png'
				return
			if dx < 0:
				self.direction = 'left'
				self.sprite = 'sprites/pLeft.png'
			if dx > 0:
				self.direction = 'right'
				self.sprite = 'sprites/pRight.png'
			if dy < 0:
				self.direction = 'up'
				self.sprite = 'sprites/pUp.png'
			if dy > 0:
				self.direction = 'down'
				self.sprite = 'sprites/pDown.png'

		if self.color == 'blue':
			if dx > 0 and dy > 0:
				self.direction = 'downRight'
				self.sprite = 'sprites/p2DownRight.png'
				return
			if dx > 0 and dy < 0:
				self.direction = 'upRight'
				self.sprite = 'sprites/p2UpRight.png'
				return
			if dx < 0 and dy > 0:
				self.direction = 'downLeft'
				self.sprite = 'sprites/p2DownLeft.png'
				return
			if dx < 0 and dy < 0:
				self.direction = 'upLeft'
				self.sprite = 'sprites/p2UpLeft.png'
				return

			if dx < 0:
				self.direction = 'left'
				self.sprite = 'sprites/p2Left.png'
			if dx > 0:
				self.direction = 'right'
				self.sprite = 'sprites/p2Right.png'
			if dy < 0:
				self.direction = 'up'
				self.sprite = 'sprites/p2Up.png'
			if dy > 0:
				self.direction = 'down'
				self.sprite = 'sprites/p2Down.png'

	def fire(self):
		xOffset = 0
		yOffset = 0

		if self.direction == 'left':
			yOffset = -10
		if self.direction == 'right':
			yOffset = 7
		if self.direction == 'up':
			xOffset = 10
		if self.direction == 'down':
			xOffset = -10

		self.bulletSet.append([self.centerX+xOffset,self.centerY+yOffset,self.direction])


	def respawn(self):
		self.health = 100
		self.x = 275
		self.y = 275
		self.direction = 'down'
		self.sprite = 'sprites/p2Down.png'
		self.score = 0

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
			pygame.draw.circle(screen,(0,0,0),center,2)


	def displayHealth(self,screen):
		healthbarPos = (30,30)
		if self.health >= 0:
			pygame.draw.rect(screen,(220,0,0),(healthbarPos,(20,150*self.health/100)))
		pygame.draw.rect(screen,(0,0,0),(30,30,20,150),3)


	def draw(self,screen):
		self.drawBullets(screen)
		self.moveBullets()

		sprite = pygame.image.load(self.sprite)
		self.spriteWidth = sprite.get_rect().size[0]
		self.spriteHeight = sprite.get_rect().size[1]
		sprite = pygame.transform.scale(sprite, (self.spriteWidth//2, self.spriteHeight//2))

		self.rect = pygame.Rect((self.x,self.y),(self.spriteWidth//2,self.spriteHeight//2))
		self.centerX = self.rect.centerx
		self.centerY = self.rect.centery

		
		# pygame.draw.rect(screen,(0,0,0),
		# 	(self.x,self.y,30,30))
		screen.blit(sprite,self.rect)
		
		



