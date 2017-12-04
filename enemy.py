import pygame,random,math

class Enemy(object):

	def __init__(self,x,y):
		self.id = ''

		self.x = x
		self.y = y

		self.dead = False
		self.width = 30
		self.height = 30
		self.xSpeed = 0
		self.ySpeed = 0
		self.color = (255,200,0)
		self.health = 100
		# self.direction = down
		self.speed = 0.6
		self.health = 3

		self.rect = pygame.Rect
		self.sprite = 'sprites/zdown.gif'


		print('New enemy created')
	
		#self.weapon = weapon
		# self.sprite = sprite #implement sprite selection for different characters

	def __repr__(self):
		
		return("Enemy()")

	def move(self,player1,player2):
		if player2 == None:
			if self.x < player1.x:
				self.xSpeed = self.speed
			if self.x > player1.x:
				self.xSpeed = -self.speed
			if self.y < player1.y:
				self.ySpeed = self.speed
			if self.y > player1.y:
				self.ySpeed = -self.speed
			if abs(self.x - player1.x) <= 5:
				self.xSpeed = 0
			if abs(self.y - player1.y) <= 5:
				self.ySpeed = 0

		else:
			distance = lambda x1,y1,x2,y2: math.sqrt((x2-x1)**2 + (y2-y1)**2)
			if distance(self.x,self.y,player2.x,player2.y) <= distance(self.x,self.y,player1.x,player1.y):
				if self.x < player2.x:
					self.xSpeed = self.speed
				if self.x > player2.x:
					self.xSpeed = -self.speed
				if self.y < player2.y:
					self.ySpeed = self.speed
				if self.y > player2.y:
					self.ySpeed = -self.speed
				if abs(self.x - player2.x) <= 5:
					self.xSpeed = 0
				if abs(self.y - player2.y) <= 5:
					self.ySpeed = 0
			elif distance(self.x,self.y,player1.x,player1.y) < distance(self.x,self.y,player2.x,player2.y):
				if self.x < player1.x:
					self.xSpeed = self.speed
				if self.x > player1.x:
					self.xSpeed = -self.speed
				if self.y < player1.y:
					self.ySpeed = self.speed
				if self.y > player1.y:
					self.ySpeed = -self.speed
				if abs(self.x - player1.x) <= 5:
					self.xSpeed = 0
				if abs(self.y - player1.y) <= 5:
					self.ySpeed = 0


		if self.xSpeed > 0 and self.ySpeed > 0:
			self.sprite = 'sprites/zrightdown.gif'
		if self.xSpeed > 0 and self.ySpeed < 0:
			self.sprite = 'sprites/zrightup.gif'	
		if self.xSpeed < 0 and self.ySpeed > 0:
			self.sprite = 'sprites/zleftdown.gif'	
		if self.xSpeed < 0 and self.ySpeed < 0:
			self.sprite = 'sprites/zleftup.gif'

		if self.xSpeed < 0 and self.ySpeed == 0:
			self.sprite = 'sprites/zleft.gif'
		if self.xSpeed > 0 and self.ySpeed == 0:
			self.sprite = 'sprites/zright.gif'
		if self.ySpeed < 0 and self.xSpeed == 0:
			self.sprite = 'sprites/zup.gif'
		if self.ySpeed > 0 and self.xSpeed == 0:
			self.sprite = 'sprites/zdown.gif'	

		self.x += self.xSpeed
		self.y += self.ySpeed


	def kill(self):
		self.dead = True
	
	def draw(self,screen):
		if not self.dead:

			self.rect = pygame.Rect((self.x,self.y),(0,0))
			sprite = pygame.image.load(self.sprite)
			screen.blit(sprite,self.rect)


			# pygame.draw.rect(screen,self.color,
			# 	(self.x,self.y,self.width,self.height))



class Boss(Enemy):
	def __init__(self):	
		self.x = random.randint(0,650)
		self.y = random.randint(0,650)
		self.dead = False
		self.width = 30
		self.height = 30
		self.xSpeed = 0
		self.ySpeed = 0
		self.color = (255,0,0)
		self.health = 100
		# self.direction = down
		self.speed = 1
		self.health = 5

