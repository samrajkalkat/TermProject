import pygame,random

class Enemy(object):

	def __init__(self):
		self.x = random.randint(550,650)
		self.y = random.randint(550,650)

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

	def draw(self,screen):
		pygame.draw.rect(screen,(0,255,0),
			(self.x,self.y,30,30))



#subclass Enemy to create differet types of enemies
