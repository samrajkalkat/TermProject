import pygame,random


class Enemy(object):

	def __init__(self):
		self.id = ''
		self.x = random.randint(550,650)
		self.y = random.randint(550,650)

		self.dead = False

		self.width = 30
		self.height = 30

		self.xSpeed = 0
		self.ySpeed = 0

		self.health = 100
		# self.direction = down
		self.speed = 0.3

	
		#self.weapon = weapon
		# self.sprite = sprite #implement sprite selection for different characters

	def move(self,player):
		if self.x < player.x:
			self.xSpeed = self.speed
		if self.x > player.x:
			self.xSpeed = -self.speed
		if self.x == player.x:
			self.xSpeed = 0
		if self.y < player.y:
			self.ySpeed = self.speed
		if self.y > player.y:
			self.ySpeed = -self.speed
		if self.y == player.y:
			self.ySpeed = 0

		self.x += self.xSpeed
		self.y += self.ySpeed

	def kill(self):
		self.dead = True
	

	def draw(self,screen):
		if not self.dead:
			pygame.draw.rect(screen,(0,255,0),
				(self.x,self.y,self.width,self.height))



#subclass Enemy to create differet types of enemies
