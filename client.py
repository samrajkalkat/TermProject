import socket
import threading 
from queue import Queue
import os

HOST = ''
PORT = 50003


#Connecting to server, commented out as of now for testing purposes
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.connect((HOST,PORT))
print('Connected!')


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


#pygame framework from provided gitbook
#slightly modified to fit needs of my game
class PygameGame(object):

	def drawStartScreen(self,screen):
		self.drawText(screen,'Welcome!',(self.width/2,self.height/4),80,WHITE)
		self.drawText(screen,"Press 'p' to start",(self.width/2,3*self.height/4),40,WHITE)

	def drawMenuScreen(self,screen):
		self.drawText(screen,'Select game mode',(self.width/2,self.height/4),50,WHITE)

		self.drawText(screen,'Single Player',(self.width/4,3*self.height/4),40,WHITE)
		self.drawText(screen,"(press '1')",(self.width/4,3*self.height/4+50),40,WHITE)

		self.drawText(screen,'Multi Player',(3*self.width/4,3*self.height/4),40,WHITE)
		self.drawText(screen,"(press '2')",(3*self.width/4,3*self.height/4+50),40,WHITE)

	def drawGameOverScreen(self,screen):
		self.drawText(screen,'You Died!',(3*self.width/4,3*self.height/4),40,WHITE)
		self.drawText(screen,"(press 'r' to respawn)",(3*self.width/4,3*self.height/4+50),40,WHITE)

	def initSinglePlayerGame(self,screen):
		image = pygame.image.load("terrain.png")
		screen.blit(image,(0,0))

	def initMultiPlayerGame(self,screen):
		image = pygame.image.load("terrain.png")
		screen.blit(image,(0,0))
		# screen.fill((225,225,225))

	def drawText(self,screen,text,center,size,color):
		#helper function to draw text on the screen
		pygame.font.init()
		font = pygame.font.Font(None,size)
		text = font.render(text,True,color)
		textBox = text.get_rect(center=center)
		screen.blit(text,textBox)


	def readServerMsg(self):
		#reading and extracting messages from the server
		while self.serverMsg.qsize() > 0:
			msg = serverMsg.get(False)
			try:
				msg = msg.split()
				command = msg[0]
			except:
				print('UNABLE TO READ MESSAGE')
			serverMsg.task_done()

		#do stuff to interpret the messages

	def init(self):
		self.server = server
		self.enemyList = []
		self.theEnemies = []
		self.player = Player()
		self.player2 = Player()
		x = random.randint(0,650)
		y = random.randint(0,650)
		self.enemy = Enemy(x,y)
		self.counter = 0

		self.myID = ''

	def mousePressed(self, x, y):
		pass

	def mouseReleased(self, x, y):
		pass

	def mouseMotion(self, x, y):
		pass

	def mouseDrag(self, x, y):
		pass

	def keyPressed(self, keyCode, modifier):

		if self.startScreen:
			if keyCode == pygame.K_p:
				self.startScreen = False
				self.menuScreen = True
		if self.menuScreen:
			if keyCode == pygame.K_1:
				self.singlePlayer = True
			if keyCode == pygame.K_2:
				self.multiPlayer = True
				msg = 'otherPlayerReady %s\n' % (self.myID)
				self.server.send(msg.encode())
				if self.myID == 'p2':
					self.bothPlayersReady = True

		if self.singlePlayer:
			if keyCode == pygame.K_SPACE:
				self.player.fire()
			if self.player.health <= 0:
				print('respawn player here\nto be implemented')
				# if keyCode == pygmae.K_r:
				# 	self.player.health = 100
		if self.multiPlayer:
			if keyCode == pygame.K_SPACE:
				self.player.fire()
				msg = 'fired %s\n' % (self.myID)
				self.server.send(msg.encode())

	def keyReleased(self, keyCode, modifier):
		pass


	def didBulletHitEnemy(self,enemy,player,player2):
		if player2 == None:
			for bullet in player.bulletSet:
				for enemy in self.enemyList:
					bulletRect = pygame.Rect(bullet[0],bullet[1],player.bulletW,player.bulletH)
					enemyRect = pygame.Rect(enemy.x,enemy.y,enemy.width,enemy.height)
					if bulletRect.colliderect(enemyRect):
						player.bulletSet.remove(bullet)
						enemy.health -= 1
						if enemy.health == 0:
							self.enemyList.remove(enemy)
							break
		else:
			for bullet in player.bulletSet:
				for enemy in self.enemyList:
					bulletRect = pygame.Rect(bullet[0],bullet[1],player.bulletW,player.bulletH)
					enemyRect = pygame.Rect(enemy.x,enemy.y,enemy.width,enemy.height)
					if bulletRect.colliderect(enemyRect):
						player.bulletSet.remove(bullet)
						enemy.health -= 1
						if enemy.health == 0:
							self.enemyList.remove(enemy)
							break

			for bullet in player2.bulletSet:
				for enemy in self.enemyList:
					bulletRect = pygame.Rect(bullet[0],bullet[1],player2.bulletW,player2.bulletH)
					enemyRect = pygame.Rect(enemy.x,enemy.y,enemy.width,enemy.height)
					if bulletRect.colliderect(enemyRect):
						player2.bulletSet.remove(bullet)
						enemy.health -= 1
						if enemy.health == 0:
							self.enemyList.remove(enemy)
							break


	def didEnemyHitPlayer(self):
		for enemy in self.enemyList:
			enemyRect = pygame.Rect(enemy.x,enemy.y,enemy.width,enemy.height)
			if self.player.rect.colliderect(enemyRect):
				self.player.health -= 1



	def timerFired(self,dt):
		

		while self.serverMsg.qsize() > 0:
			msg = self.serverMsg.get(False)
			if type(msg) == dict:
				print("GOT IT")
			else:
				print(msg)
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
					print('ready')
					print('kasjdkfljasdkfajldfkjasdlfkajsldfkajdklfajlfk')
					if self.multiPlayer:
						self.bothPlayersReady = True

				if self.multiPlayer:
					if cmd == 'newEnemy':
						print('YUHHH!!!')
						x = int(msg[2])
						y = int(msg[3])
						self.enemyList.append(Enemy(x,y))

					if cmd == 'fired':
						self.player2.fire()
						


		if self.singlePlayer:
			self.moveEnemies()
			self.didBulletHitEnemy(self.enemy, self.player,None)
			self.didEnemyHitPlayer()
			if self.player.health > 0:
				self.createEnemies()
			else:
				del self.enemyList[:]

		if self.multiPlayer:
			if self.myID == 'p1':
				if self.bothPlayersReady:
					self.createEnemies()

			self.moveEnemies()
			self.didBulletHitEnemy(self.enemy, self.player,self.player2)
			self.didEnemyHitPlayer()

		



	def moveEnemies(self):
		if self.singlePlayer:
			for enemy in self.enemyList:
				enemy.move(self.player,None)
		elif self.multiPlayer:
			for enemy in self.enemyList:
				enemy.move(self.player,self.player2)


		
   
	def createEnemies(self):
		self.counter += 1
		if self.counter % 30 == 0:
			x = random.randint(0,650)
			y = random.randint(0,650)
			enemy = Enemy(x,y)
			self.enemyList.append(enemy)
			message = 'newEnemy %s %s\n' % (x,y)
			self.server.send(message.encode())



	def redrawAll(self, screen):
		if self.startScreen:
			self.drawStartScreen(screen)
		if self.menuScreen:
			self.drawMenuScreen(screen)
		if self.singlePlayer:
			self.menuScreen = False
			self.startScreen = False
			if self.player.health > 0:
				self.initSinglePlayerGame(screen)
				self.player.draw(screen)
				for enemy in self.enemyList:
					enemy.draw(screen)
			if self.player.health <=0:
				self.drawGameOverScreen(screen)
			self.player.displayHealth(screen)  
		if self.multiPlayer:
			self.initMultiPlayerGame(screen)
			self.player.draw(screen)
			self.player2.draw(screen)
			for enemy in self.enemyList:
				enemy.draw(screen)
			self.player.displayHealth(screen)  

	def isKeyPressed(self, key):
		''' return whether a specific key is being held '''
		return self._keys.get(key, False)

	def __init__(self, width=650, height=650, fps=50, title="Term Project"):
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

		self.bothPlayersReady = False

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

				self.player.move(dx,dy)

			if self.multiPlayer:

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

					self.player.move(dx,dy)
					message = 'playerMoved %d %d\n' %(dx,dy)
					self.server.send(message.encode())


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

def main():
	game = PygameGame()
	serverMsg = Queue(1000)
	threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
	game.run(serverMsg,server)

if __name__ == '__main__':
	main()