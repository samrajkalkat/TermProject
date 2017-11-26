import pygame,random

class Player(object):

	def __init__(self):
	
		self.x = 0
		self.y = 0

		self.xSpeed = 0
		self.ySpeed = 0

		self.direction = 'down'

		self.health = 100

		self.sprite = 'sprites/playerDown.png'

		self.bullets = dict()

		#self.weapon = weapon
		# self.sprite = sprite #implement sprite selection for different characters

	def move(self,dx,dy):
		#moving player based on input
		self.x += dx
		self.y += dy

		#setting player direction based on direction of movement
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

		

	def fire(self,screen):
		pass

	def draw(self,screen):
		spriteRect = pygame.Rect((self.x,self.y),(500,500))
		sprite = pygame.image.load(self.sprite)

		screen.blit(sprite,spriteRect)



