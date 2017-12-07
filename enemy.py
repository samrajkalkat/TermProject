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
		self.direction = ''
		self.speed = 0.6
		self.health = 3

		self.name = 'reg'

		self.rect = pygame.Rect
		self.sprite = 'sprites/zdown.gif'

		self.spriteHeight = 0
		self.spriteWidth = 0

		self.centerX = 0
		self.centerY = 0


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

		

		enemyRect = pygame.Rect((self.x+self.xSpeed*10,self.y+self.ySpeed*10),(self.spriteHeight+5,self.spriteWidth+5))
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



		self.updateSprite()
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
			self.centerX = self.rect.centerx
			self.centerY = self.rect.centery


			# pygame.draw.rect(screen,self.color,
			# 	(self.x,self.y,self.width,self.height))



class Boss(Enemy):
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
		self.speed = 0.3
		self.health = 5

		self.name = 'boss'

		self.rect = pygame.Rect
		self.sprite = 'sprites/zdown.gif'

		self.spriteHeight = 0
		self.spriteWidth = 0

		self.bulletSet = []
		self.bulletSpeed = 0

		self.centerX = 0
		self.centerY = 0

		print('New enemy created')
	
		#self.weapon = weapon
		# self.sprite = sprite #implement sprite selection for different characters

	def __repr__(self):
		
		return("Boss()")

	def updateSprite(self):
		if self.xSpeed > 0 and self.ySpeed > 0:
			self.sprite = 'sprites/dDownRight.gif'
			self.direction = 'downRight'
		if self.xSpeed > 0 and self.ySpeed < 0:
			self.sprite = 'sprites/dUpRight.gif'
			self.direction = 'upRight'	
		if self.xSpeed < 0 and self.ySpeed > 0:
			self.sprite = 'sprites/dDownLeft.gif'
			self.direction = 'downLeft'	
		if self.xSpeed < 0 and self.ySpeed < 0:
			self.sprite = 'sprites/dUpLeft.gif'
			self.direction = 'upLeft'

		if self.xSpeed < 0 and self.ySpeed == 0:
			self.sprite = 'sprites/dLeft.gif'
			self.direction = 'left'
		if self.xSpeed > 0 and self.ySpeed == 0:
			self.sprite = 'sprites/dRight.gif'
			self.direction = 'right'
		if self.ySpeed < 0 and self.xSpeed == 0:
			self.sprite = 'sprites/dUp.gif'
			self.direction = 'up'
		if self.ySpeed > 0 and self.xSpeed == 0:
			self.sprite = 'sprites/dDown.gif'
			self.direction = 'down'	

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

	def fire(self):
		self.bulletSet.append([self.centerX,self.centerY,self.direction])

