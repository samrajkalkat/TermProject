#Samraj Kalkat
#15-112 Term Project

#pygame framework from 15-112 website gitbook
#server.py and server/message handling functions in client.py from 15-112 website gitbook
#sprites taken from BoxheadZombies2Play

import socket
import threading 
from queue import Queue
import os
import shelve

HOST = ''
PORT = 50003


#Connecting to server, commented out as of now for testing purposes
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.connect((HOST,PORT))
print('Connected!')


#opening the file that stores our high score
d = shelve.open('score.dat')


#server handling function from gitbook on 15-112 website
#this function will be used to handle the commands that are sent to the server
#I will use the commands in the pygame class to work the game
def handleServerMsg(server,serverMsg):
	server.setblocking(1)
	msg = ''
	command = ''
	while True:
		msg += server.recv(2048).decode('UTF-8')
		print(msg)
		command = msg.split('\n')
		while (len(command)>1):
			readyMsg = command[0]
			msg = '\n'.join(command[1:])
			serverMsg.put(readyMsg)
			command = msg.split('\n')

import pygame
from player import *
from enemy import *


#rgb colors to be used in graphics
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

#pygame framework from provided gitbook from 15-112 webstie
#slightly modified to fit needs of my game
class PygameGame(object):

	def drawStartScreen(self,screen):
		screen.fill((50,50,50))
		image = pygame.image.load("sprites/welcome.png")
		image = pygame.transform.scale(image, (500, 100))
		screen.blit(image,(30,100))

		zombie = pygame.image.load('sprites/zombie.png')
		zombie = pygame.transform.scale(zombie, (100, 100))
		screen.blit(zombie,(self.width/2-50,250))

		self.drawText(screen,"Press 'p' to start",(self.width/2,3*self.height/4),40,WHITE)
		self.drawText(screen,"Press 'i' for instructions",(self.width/2,3*self.height/4+40),40,WHITE)

	def drawInstructionScreen(self,screen):
		screen.fill((0,0,0))
		self.drawText(screen,"Instructions",(self.width/2,self.height/4),70,GREEN)
		self.drawText(screen,"Use arrow keys to move",(self.width/2,self.height/2),30,WHITE)
		self.drawText(screen,"Press space to shoot",(self.width/2,self.height/2+30),30,WHITE)
		self.drawText(screen,"Press escape to pause",(self.width/2,self.height/2+60),30,WHITE)
		self.drawText(screen,"Shoot zombies to gain points",(self.width/2,self.height/2+90),30,WHITE)
		self.drawText(screen,"Press 'i' to return to start screen",(self.width/2,self.height/2+150),30,WHITE)


	def drawMenuScreen(self,screen):
		image = pygame.image.load("sprites/menu.png")
		image = pygame.transform.scale(image, (500, 100))
		screen.blit(image,(30,100))

		single = pygame.image.load("sprites/singlePlayer.png")
		single = pygame.transform.scale(single, (200, 50))
		screen.blit(single,(30,3*self.height/4-20))
		# self.drawText(screen,'Single Player',(self.width/4,3*self.height/4),40,WHITE)
		self.drawText(screen,"(press '1')",(self.width/4,3*self.height/4+50),40,WHITE)

		multi = pygame.image.load("sprites/multiPlayer.png")
		multi = pygame.transform.scale(multi, (200, 50))
		screen.blit(multi,(self.width-230,3*self.height/4-20))
		self.drawText(screen,"(press '2')",(3*self.width/4,3*self.height/4+50),40,WHITE)

	def drawGameOverScreen(self,screen):
		screen.fill((0,0,0))
		self.drawText(screen,'Game Over!',(self.width/2,self.height/4),40,WHITE)
		self.drawText(screen,"Score: %s" % (self.player.score),(self.width/2,self.height/4 + 50),30,RED)
		self.drawText(screen,"High score: %s" % (d['Score']),(self.width/2,self.height/4 + 80),30,GREEN)
		self.drawText(screen,"(press 'r' to respawn)",(self.width/2,self.height/2+50),40,WHITE)
		self.drawText(screen,"(press 'm' to return to menu)",(self.width/2,self.height/2 + 100),40,WHITE)


	def drawGameOverScreen2Player(self,screen):
		screen.fill((0,0,0))
		self.drawText(screen,'Game Over!',(self.width/2,self.height/4),40,WHITE)
		self.drawText(screen,"Player1: %s" % (self.player.score),(self.width/2,self.height/4 + 50),30,RED)
		self.drawText(screen,"Player2: %s" % (self.player2.score),(self.width/2,self.height/4 + 80),30,RED)
		self.drawText(screen,"(press 'm' to return to menu)",(self.width/2,self.height/2 + 50),40,WHITE)


	def drawPauseScreen(self,screen):
		screen.fill((0,0,0))
		self.drawText(screen,'Game Paused!',(self.width/2,self.height/4),50,GREEN)
		self.drawText(screen,"(press 'r' to restart)",(self.width/2,self.height/2),40,WHITE)
		self.drawText(screen,"(press 'm' to return to menu)",(self.width/2,self.height/2 + 50),40,WHITE)

	def initSinglePlayerGame(self,screen):
		image = pygame.image.load("sprites/terrain.png")
		image = pygame.transform.scale(image, (550, 550))
		screen.blit(image,(0,0))
		self.drawText(screen,"Score: %s" % (self.player.score),(self.width-55,30),30,BLACK)
		

	def initMultiPlayerGame(self,screen):
		image = pygame.image.load("sprites/terrain.png")
		screen.blit(image,(0,0))
		self.drawText(screen,"Score: %s" % (self.player.score),(self.width-60,30),30,BLACK)
		self.drawText(screen,"Player2: %s" % (self.player2.score),(self.width-60,55),30,BLACK)

	def drawText(self,screen,text,center,size,color):
		#helper function to draw text on the screen
		pygame.font.init()
		font = pygame.font.Font(None,size)
		text = font.render(text,True,color)
		textBox = text.get_rect(center=center)
		screen.blit(text,textBox)


	def drawBlood(self,screen):
		image = pygame.image.load('sprites/blood.gif')
		for blood in self.blood:
			screen.blit(image,(blood[0],blood[1]))


	def readServerMsg(self):
		#taken from 15-112 sockets gitbook
		#reading and extracting messages from the server
		while self.serverMsg.qsize() > 0:
			msg = serverMsg.get(False)
			try:
				msg = msg.split()
				command = msg[0]
			except:
				print('UNABLE TO READ MESSAGE')
			serverMsg.task_done()


	def init(self):
		self.server = server
		self.enemyList = []
		self.theEnemies = []
		self.player = Player('blue')
		self.player2 = Player('red')
		x = random.randint(0,550)
		y = random.randint(0,550)
		self.enemy = Enemy(x,y)
		self.counter = 0
		self.myID = ''
		self.blood = set()


	def mousePressed(self, x, y):
		pass

	def mouseReleased(self, x, y):
		pass

	def mouseMotion(self, x, y):
		pass

	def mouseDrag(self, x, y):
		pass

	def keyPressed(self, keyCode, modifier):

		#all key input functions depending on current screen

		if self.startScreen:
			if keyCode == pygame.K_p:
				self.startScreen = False
				self.menuScreen = True

			if keyCode == pygame.K_i:
				self.instructions = not self.instructions

		if self.menuScreen:
			if keyCode == pygame.K_1:
				self.singlePlayer = True
				self.generateWalls()
			if keyCode == pygame.K_2:
				self.multiPlayer = True
				msg = 'otherPlayerReady %s\n' % (self.myID)
				self.server.send(msg.encode())

				if self.myID == 'p2':
					self.player = Player('red')
					self.player2 = Player('blue')
					self.bothPlayersReady = True


		if self.singlePlayer:

			if not self.paused:
				if keyCode == pygame.K_SPACE:
					self.player.fire()

	
			if keyCode == pygame.K_ESCAPE:
				self.paused = not self.paused

			if self.paused:
				if keyCode == pygame.K_r:
					del self.enemyList[:]
					del self.walls[:]
					self.player.respawn()
					self.generateWalls()
					self.blood.clear()
					self.paused = False

				if keyCode == pygame.K_m:
					del self.enemyList[:]
					del self.walls[:]
					self.player.respawn()
					self.blood.clear()
					self.singlePlayer = False
					self.menuScreen = True
					self.paused = False

			if self.gameOver:
				if keyCode == pygame.K_r:
					del self.enemyList[:]
					del self.walls[:]
					self.blood.clear()
					self.player.respawn()
					self.gameOver = False
					self.generateWalls()

				if keyCode == pygame.K_m:
					del self.enemyList[:]
					del self.walls[:]
					self.blood.clear()
					self.player.respawn()
					self.gameOver = False
					self.singlePlayer = False
					self.menuScreen = True

		if self.multiPlayer:

			if not self.paused:
				if keyCode == pygame.K_SPACE:
					self.player.fire()
					msg = 'fired %s\n' % (self.myID)
					self.server.send(msg.encode())

			if keyCode == pygame.K_ESCAPE:
			
				self.paused = not self.paused
				msg = 'paused %s\n' % (self.paused)
				self.server.send(msg.encode())

			if self.paused:
				if keyCode == pygame.K_r:
					msg = 'restart %s\n' % (self.myID)
					self.server.send(msg.encode())

					del self.enemyList[:]
					del self.walls[:]
					self.player.respawn()
					self.player2.respawn()
					if self.myID == 'p1':
						self.generateWalls()
					self.blood.clear()
					self.paused = False
					self.player2GameOver = False
					self.gameOver = False

				if keyCode == pygame.K_m:
					msg = 'menu %s\n' % (self.paused)
					self.server.send(msg.encode())

					del self.enemyList[:]
					del self.walls[:]
					self.player.respawn()
					self.player2.respawn()
					self.blood.clear()
					self.multiPlayer = False
					self.menuScreen = True
					self.paused = False
					self.bothPlayersReady = False

			if self.bothDead:

				if keyCode == pygame.K_m:
					del self.enemyList[:]
					del self.walls[:]
					self.player.respawn()
					self.player2.respawn()
					self.blood.clear()
					self.multiPlayer = False
					self.menuScreen = True
					self.bothDead = False
					self.gameOver = False
					self.player2GameOver = False
					self.paused = False

	def keyReleased(self, keyCode, modifier):
		pass


	def didBulletHitEnemy(self,enemy,player,player2):
		#checking if any of the bullets hit the players
		if player2 == None:
			for bullet in player.bulletSet:
				for enemy in self.enemyList:
					bulletRect = pygame.Rect(bullet[0],bullet[1],player.bulletW,player.bulletH)
					enemyRect = pygame.Rect(enemy.x,enemy.y,enemy.width,enemy.height)
					if bulletRect.colliderect(enemyRect):
						try:
							if bullet[2] == 'downRight':
								enemy.x += 6
								enemy.y += 6
							if bullet[2] == 'upRight':
								enemy.x += 6
								enemy.y -= 6
							if bullet[2] == 'downLeft':
								enemy.x -= 6
								enemy.y += 6
							if bullet[2] == 'upLeft':
								enemy.x -= 6
								enemy.y -= 6
							if bullet[2] == 'left':
								enemy.x -= 6
							if bullet[2] == 'right':
								enemy.x += 6
							if bullet[2] == 'up':
								enemy.y -= 6
							if bullet[2] == 'down':
								enemy.y += 6
							player.bulletSet.remove(bullet)
							enemy.health -= 1
						except:
							print('')
						if enemy.health == 0:
							try:
								self.blood.add((enemy.x,enemy.y))
								self.enemyList.remove(enemy)
								player.score += 1
								break
							except:
								print('')
		else:
			#checking for 2 players
			for bullet in player.bulletSet:
				for enemy in self.enemyList:
					bulletRect = pygame.Rect(bullet[0],bullet[1],player.bulletW,player.bulletH)
					enemyRect = pygame.Rect(enemy.x,enemy.y,enemy.width,enemy.height)
					if bulletRect.colliderect(enemyRect):
						try:
							if bullet[2] == 'downRight':
								enemy.x += 6
								enemy.y += 6
							if bullet[2] == 'upRight':
								enemy.x += 6
								enemy.y -= 6
							if bullet[2] == 'downLeft':
								enemy.x -= 6
								enemy.y += 6
							if bullet[2] == 'upLeft':
								enemy.x -= 6
								enemy.y -= 6
							if bullet[2] == 'left':
								enemy.x -= 6
							if bullet[2] == 'right':
								enemy.x += 6
							if bullet[2] == 'up':
								enemy.y -= 6
							if bullet[2] == 'down':
								enemy.y += 6
							player.bulletSet.remove(bullet)
							enemy.health -= 1
						except:
							print('no bullet to remove')
						if enemy.health == 0:
							try:
								self.blood.add((enemy.x,enemy.y))
								self.enemyList.remove(enemy)
								player.score += 1

								msg = 'myScore %s\n' % (player.score)
								self.server.send(msg.encode())

								break
							except:
								print('no enemy to delete')

			for bullet in player2.bulletSet:
				for enemy in self.enemyList:
					bulletRect = pygame.Rect(bullet[0],bullet[1],player2.bulletW,player2.bulletH)
					enemyRect = pygame.Rect(enemy.x,enemy.y,enemy.width,enemy.height)
					if bulletRect.colliderect(enemyRect):
						try:
							if bullet[2] == 'downRight':
								enemy.x += 6
								enemy.y += 6
							if bullet[2] == 'upRight':
								enemy.x += 6
								enemy.y -= 6
							if bullet[2] == 'downLeft':
								enemy.x -= 6
								enemy.y += 6
							if bullet[2] == 'upLeft':
								enemy.x -= 6
								enemy.y -= 6
							if bullet[2] == 'left':
								enemy.x -= 6
							if bullet[2] == 'right':
								enemy.x += 6
							if bullet[2] == 'up':
								enemy.y -= 6
							if bullet[2] == 'down':
								enemy.y += 6
							player2.bulletSet.remove(bullet)
							enemy.health -= 1
						except:
							print('no bullet to remove')
						if enemy.health == 0:
							try:
								self.blood.add((enemy.x,enemy.y))
								self.enemyList.remove(enemy)
								playe2.score += 1
								break
							except:
								print('no enemy to delete')


	def didEnemyHitPlayer(self):
		#checking if any of the enemies are colliding with our player
		try:
			for enemy in self.enemyList:
				enemyRect = pygame.Rect(enemy.x,enemy.y,enemy.width,enemy.height)
				if self.player.rect.colliderect(enemyRect):
					self.player.health -= 1
		except:
			print('')


	def generateWalls(self):
		#generating random walls on the map
		for x in range(5):
			x = random.randint(50,500)
			y = random.randint(50,500)
			wallRect = pygame.Rect((x,y),(80,80))
			playerRect = pygame.Rect((275,275),(50,50))

			if len(self.walls) > 0:
				if wallRect.collidelist(self.walls) == -1:
					if not wallRect.colliderect(playerRect):
						self.walls.append(wallRect)
						message = 'newWall %s %s\n' % (x,y)
						self.server.send(message.encode())
			else:
				if not wallRect.colliderect(playerRect):
					self.walls.append(wallRect)
					message = 'newWall %s %s\n' % (x,y)
					self.server.send(message.encode())

	def drawWalls(self,screen):
		#drawing all the walls from the wall list created in generateWalls
		for wallRect in self.walls:
			sprite = pygame.image.load('sprites/wall.png')
			sprite = pygame.transform.scale(sprite,(74,74))
			screen.blit(sprite,wallRect)


	def timerFired(self,dt):
		
		while self.serverMsg.qsize() > 0:
			#checking all the server messages
			msg = self.serverMsg.get(False)
			if type(msg) == dict:
				print("got it")
			else:
				msg = msg.split()
				cmd = msg[0]

				if cmd == 'newPlayer':
					print(msg[1])

				if cmd == 'playerMoved':
					dx = int(msg[2])
					dy = int(msg[3])
					self.player2.move(dx,dy)
				if cmd == 'enemyList':
					self.enemyList = msg[1]
				if cmd == 'myIDis':
					self.myID = msg[1]

				if cmd == 'otherPlayerReady':

					self.otherPlayerReady = True

					if self.myID == 'p1':
						self.bothPlayersReady = True
					if self.multiPlayer:
						self.bothPlayersReady = True
						self.generateWalls()

				if self.multiPlayer:
					if cmd == 'newEnemy':
						x = int(msg[2])
						y = int(msg[3])
						self.enemyList.append(Enemy(x,y))

					if cmd == 'fired':
						self.player2.fire()

					if cmd == 'paused':
						self.paused = not self.paused

					if cmd == 'restart':
						if self.paused:
							del self.enemyList[:]
							del self.walls[:]
							self.player.respawn()
							self.player2.respawn()
							if self.myID == 'p1':
								self.generateWalls()
							self.blood.clear()
							self.paused = False
							self.player2GameOver = False
							self.gameOver = False

					if cmd == 'menu':
						if self.paused:
							del self.enemyList[:]
							del self.walls[:]
							self.player.respawn()
							self.player2.respawn()
							self.blood.clear()
							self.multiPlayer = False
							self.menuScreen = True
							self.paused = False

					if cmd == 'myScore':
						self.player2.score = int(msg[2])

					if cmd == 'gameOver':
						self.player2GameOver = True

					if cmd == 'newWall':
						print('received')
						x = int(msg[2])
						y = int(msg[3])
						print(x,y)
						wallRect = pygame.Rect((x,y),(74,74))
						self.walls.append(wallRect)
						
		if self.singlePlayer:
			if not self.paused:
				self.moveEnemies()
				self.didBulletHitEnemy(self.enemy, self.player,None)
				self.didEnemyHitPlayer()

				try:
					#checking if any of the bullets hit the walls
					for bullet in self.player.bulletSet:
						bulletRect = pygame.Rect(bullet[0],bullet[1],self.player.bulletW,self.player.bulletH)
						if bulletRect.collidelist(self.walls) != -1:
							self.player.bulletSet.remove(bullet)
				except:
					print('')
			

				if not self.gameOver:
					self.createEnemies()
				if self.player.health <= 0:
					self.gameOver = True

					try:
						#storing our high sccore as persistent data
						if self.player.score > (d['Score']):
							d['Score'] = self.player.score
					except:
						d['Score'] = self.player.score
						
					self.blood.clear()

		if self.multiPlayer:
			if not self.paused:
				if self.myID == 'p1':
					if self.bothPlayersReady:
						self.createEnemies()
				try:
					#checking if bullets hit any walls for both players
					for bullet in self.player.bulletSet:
						bulletRect = pygame.Rect(bullet[0],bullet[1],self.player.bulletW,self.player.bulletH)
						if bulletRect.collidelist(self.walls) != -1:
							self.player.bulletSet.remove(bullet)

					for bullet in self.player2.bulletSet:
						bulletRect = pygame.Rect(bullet[0],bullet[1],self.player2.bulletW,self.player2.bulletH)
						if bulletRect.collidelist(self.walls) != -1:
							self.player2.bulletSet.remove(bullet)
				except:
					print('')

				self.moveEnemies()
				self.didBulletHitEnemy(self.enemy,self.player,self.player2)
				self.didEnemyHitPlayer()

				if self.player.health <= 0:
					self.gameOver = True
					msg = 'gameOver %s\n' % (self.myID)
					self.server.send(msg.encode())

			if self.gameOver and self.player2GameOver:
				print('Over')
				self.bothDead = True			

	def moveEnemies(self):

		#moving all of the enemies in the enemy list

		if self.singlePlayer:
			for enemy in self.enemyList:
				enemy.move(self.player,None,self.walls)
			

		elif self.multiPlayer:

			#moving enemies depending on who is dead and who is alive

			try:
				for enemy in self.enemyList:

						if self.gameOver:
							enemy.move(self.player2,None,self.walls)

						elif not self.player2GameOver and self.gameOver == False:
							enemy.move(self.player,self.player2,self.walls)

						elif self.player2GameOver and self.gameOver == False:
							enemy.move(self.player,None,self.walls)

						else:
							enemy.move(self.player,self.player2,self.walls)

			except:
				print('fail')

   
	def createEnemies(self):
		#randomly generating enemies

		self.counter += 1

		try:	
			if self.multiPlayer:
				if self.counter % 30 == 0:
					x = random.randint(135,412)
					y = random.choice([-5,555])
					enemy = Enemy(x,y)
					self.enemyList.append(enemy)
					message = 'newEnemy %s %s\n' % (x,y)
					self.server.send(message.encode())

			elif self.singlePlayer:
				if self.counter % 60 == 0:
					x = random.randint(135,412)
					y = random.choice([-5,555])
					enemy = Enemy(x,y)
					self.enemyList.append(enemy)
					message = 'newEnemy %s %s\n' % (x,y)
					self.server.send(message.encode())

					if self.counter % 120 == 0:
						x = random.randint(135,412)
						y = random.choice([-5,555])
						enemy = Boss(x,y)
						self.enemyList.append(enemy)
		except:
			print('')

	def redrawAll(self, screen):

		#drawing different screens based on what screen we are looking at

		if self.startScreen:
			self.drawStartScreen(screen)

			if self.instructions:
				self.drawInstructionScreen(screen)

		if self.menuScreen:
			self.drawMenuScreen(screen)
		if self.singlePlayer:
			self.menuScreen = False
			self.startScreen = False
			self.initSinglePlayerGame(screen)
			self.drawBlood(screen)
			self.drawWalls(screen)
			self.player.draw(screen)
			for enemy in self.enemyList:
				enemy.draw(screen)

			self.player.displayHealth(screen)  

			if self.paused:
				self.drawPauseScreen(screen)

		if self.gameOver:
			self.drawGameOverScreen(screen)

		if self.multiPlayer:

			self.initMultiPlayerGame(screen)
			self.drawBlood(screen)	

			self.drawWalls(screen)

			self.player.draw(screen)
			self.player2.draw(screen)
			for enemy in self.enemyList:
				enemy.draw(screen)
			self.player.displayHealth(screen)  

			if not self.bothPlayersReady:
				self.drawText(screen,'Waiting for Player 2...',(self.width/2,self.height/4),35,RED)

			if self.gameOver:
					self.drawText(screen,'You died!',(self.width/2,self.height/4),40,RED)

			if self.paused:
				self.drawPauseScreen(screen)

			if self.bothDead:
				self.drawGameOverScreen2Player(screen)
				self.bothPlayersReady = False
				self.otherPlayerReady = False


	def isKeyPressed(self, key):
		''' return whether a specific key is being held '''
		return self._keys.get(key, False)

	def __init__(self, width=550, height=550, fps=50, title="Term Project"):
		self.width = width
		self.height = height
		self.fps = fps
		self.title = title
		self.bgColor = BLACK

		#screens
		self.startScreen = True
		self.menuScreen = False
		self.singlePlayer = False
		self.multiPlayer = False
		self.gameOver = False
		self.bothPlayersReady = False
		self.otherPlayerReady = False
		self.paused = False
		self.player2GameOver = False
		self.bothDead = False

		self.walls = []
		self.instructions = False

		pygame.init()

	def run(self,serverMsg=None,server=None):
		self.server = server
		self.serverMsg = serverMsg
		clock = pygame.time.Clock()
		screen = pygame.display.set_mode((self.width, self.height))
		# set the title of    the window
		pygame.display.set_caption(self.title)

		# stores all the keys currently being held down
		self._keys = dict()

		# call game-specific initialization
		self.init()
		playing = True
		while playing:
			time = clock.tick(self.fps)
			self.timerFired(time)

			if self.singlePlayer:

				#key input to control single player

				keys = pygame.key.get_pressed()
				dx = 0
				dy = 0
				if keys[pygame.K_UP]:
					dy = -3
				if keys[pygame.K_DOWN]:
					dy = 3
				if keys[pygame.K_LEFT]:
					dx = -3
				if keys[pygame.K_RIGHT]:
					dx = 3  

				playerRect = pygame.Rect((self.player.x+2*dx,self.player.y+2*dy),(self.player.spriteWidth//2, self.player.spriteHeight//2))
				
				#checking wall collision
				if playerRect.collidelist(self.walls) == -1:
					if not self.paused:
						self.player.move(dx,dy)


			if self.multiPlayer:

				#key control for multiplayer

				if self.bothPlayersReady:

					keys = pygame.key.get_pressed()
					dx = 0
					dy = 0
					if keys[pygame.K_UP]:
						dy = -3
					if keys[pygame.K_DOWN]:
						dy = 3
					if keys[pygame.K_LEFT]:
						dx = -3
					if keys[pygame.K_RIGHT]:
						dx = 3  

					playerRect = pygame.Rect((self.player.x+dx,self.player.y+dy),(self.player.spriteWidth//2, self.player.spriteHeight//2))
					
					try:
						if not self.gameOver:
							if playerRect.collidelist(self.walls) == -1:
								self.player.move(dx,dy)
								message = 'playerMoved %d %d\n' %(dx,dy)
								self.server.send(message.encode())
					except:
						print('fail')


			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					self.mousePressed(*(event.pos))
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					self.mouseReleased(*(event.pos))
				elif (event.type == pygame.MOUSEMOTION and
					  event.buttons == (0, 0, 0)):
					self.mouseMotion(*(event.pos))
				elif (event.type == pygame.MOUSEMOTION and
					  event.buttons[0] == 1):
					self.mouseDrag(*(event.pos))
				elif event.type == pygame.KEYDOWN:
					self._keys[event.key] = True
					self.keyPressed(event.key, event.mod)
				elif event.type == pygame.KEYUP:
					self._keys[event.key] = False
					self.keyReleased(event.key, event.mod)
				elif event.type == pygame.QUIT:
					playing = False
			screen.fill(self.bgColor)
			self.redrawAll(screen)
			pygame.display.flip()

		pygame.quit()
		d.close()
		self.server.close()

def main():
	try:
		game = PygameGame()
		serverMsg = Queue(1000)
		threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
		game.run(serverMsg,server)
	except:
		print('fail')

if __name__ == '__main__':
	main()