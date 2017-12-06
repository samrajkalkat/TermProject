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

		self.spriteHeight = 0
		self.spriteWidth = 0


		print('New enemy created')
	
		#self.weapon = weapon
		# self.sprite = sprite #implement sprite selection for different characters

	def __repr__(self):
		
		return("Enemy()")

	def move(self,player1,player2,walls):
		distance = lambda x1,y1,x2,y2: math.sqrt((x2-x1)**2 + (y2-y1)**2)

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

		

		enemyRect = pygame.Rect((self.x+self.xSpeed*10,self.y+self.ySpeed*10),(self.spriteHeight+4,self.spriteWidth))
		self.updateSprite()

		# if self.ySpeed > 0:
		while enemyRect.collidelist(walls) != -1:
			if self.x <= walls[enemyRect.collidelist(walls)].left:
				self.x -= .4
				self.y += 0
				enemyRect = pygame.Rect((self.x,self.y),(self.spriteHeight,self.spriteWidth))
			elif self.x >= walls[enemyRect.collidelist(walls)].right:
				self.x += .4
				self.y += 0
				enemyRect = pygame.Rect((self.x,self.y),(self.spriteHeight,self.spriteWidth))
			else:
				self.x += .4
				self.y += 0
				enemyRect = pygame.Rect((self.x,self.y),(self.spriteHeight,self.spriteWidth))

	
		self.x += self.xSpeed
		self.y += self.ySpeed
			

	def updateSprite(self):
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

	def kill(self):
		self.dead = True
	
	def draw(self,screen):
		if not self.dead:

			
			sprite = pygame.image.load(self.sprite)
			self.spriteWidth = sprite.get_rect().size[0]
			self.spriteHeight = sprite.get_rect().size[1]
			self.rect = pygame.Rect((self.x,self.y),(self.spriteHeight//2,self.spriteWidth//2))
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

