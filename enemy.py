import pygame,random,math
import time

#class code for the enemies and bosses
#AI movement and draw functions for the enemies

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

		#moving to the closest player

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
			
			#checking which palyer is closer and moving towards that player

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

		try:

			#creating the enemy rect for a few steps ahead of current posistion
			enemyRect = pygame.Rect((self.x+self.xSpeed*10,self.y+self.ySpeed*10),(self.spriteHeight+5,self.spriteWidth+5))
			self.updateSprite()

			# if self.ySpeed > 0:

			count = 0

			#checking wall collision and moving around the walls based on posistion
			while enemyRect.collidelist(walls) != -1 and count < 30:
				print('moving')
				if self.x <= walls[enemyRect.collidelist(walls)].left:
					self.x -= .4
					self.y += 0
					count += 1
					enemyRect = pygame.Rect((self.x,self.y),(self.spriteHeight,self.spriteWidth))
				elif self.x >= walls[enemyRect.collidelist(walls)].right:
					self.x += .4
					self.y += 0
					count += 1
					enemyRect = pygame.Rect((self.x,self.y),(self.spriteHeight,self.spriteWidth))
				else:
					self.x += 2
					self.y += 0
					count += 1
					enemyRect = pygame.Rect((self.x,self.y),(self.spriteHeight,self.spriteWidth))

			self.updateSprite()
			self.x += self.xSpeed
			self.y += self.ySpeed

		except:
			print('')
				

	def updateSprite(self):
		#updating sprite depending on speed vectors
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

		#drawing the enemy in posistion

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
		self.health = 8

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
		#updating sprite for boss
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
