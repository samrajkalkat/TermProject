###
#Server code from provided gitBook on 15-112 webiste, slightly modified at this point for my game
###


#TO BE ADDED:
#Create enemies in server
#Added complexity feature

import pygame
import socket
import threading
from queue import Queue
from enemy import *


HOST = "" # put your IP address here if playing on multiple computers
PORT = 50003
BACKLOG = 4

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("looking for connection")

def handleClient(client, serverChannel, cID, clientele):
  client.setblocking(1)
  msg = ""
  while True:
    try:
      msg += client.recv(10).decode("UTF-8")
      command = msg.split("\n")
      while (len(command) > 1):
        readyMsg = command[0]
        msg = "\n".join(command[1:])
        serverChannel.put(str(cID) + " " + readyMsg)
        command = msg.split("\n")
        print()
    except:
      # we failed
      return

def serverThread(clientele, serverChannel):
  while True:
    msg = serverChannel.get(True, None)
    print("msg recv: ", msg)
    msgList = msg.split(" ")
    senderID = msgList[0]
    instruction = msgList[1]
    details = " ".join(msgList[2:])
    if (details != ""):
      for cID in clientele:
        if cID != senderID:
          sendMsg = instruction + " " + senderID + " " + details + "\n"
          clientele[cID].send(sendMsg.encode())
          print("> sent to %s:" % cID, sendMsg[:-1])
    print()
    serverChannel.task_done()



# while True:
#   client, address = server.accept()
#   # myID is the key to the client in the clientele dictionary
#   myID = names[playerNum]
#   print(myID, playerNum)
#   for cID in clientele:
#     print (repr(cID), repr(playerNum))
#     clientele[cID].send(("newPlayer %s\n" % myID).encode())
#     client.send(("newPlayer %s\n" % cID).encode())
#   clientele[myID] = client
#   client.send(("myIDis %s \n" % myID).encode())
#   print("connection recieved from %s" % myID)
#   threading.Thread(target = handleClient, args = 
#                         (client ,serverChannel, myID, clientele)).start()

class PygameGame(object):

    def init(self):
        self.clientele = dict()
        self.playerNum = 0
        self.names = ["p1","p2"]

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        # clientele = dict()
        # playerNum = 0

        while True:
            serverChannel = Queue(100)
            threading.Thread(target = serverThread, args = (self.clientele, serverChannel)).start()

            # names = ["p1", "p2"]
            client, address = server.accept()
            # myID is the key to the client in the clientele dictionary
            myID = self.names[self.playerNum]
            print(myID, self.playerNum)
            for cID in self.clientele:
                print (repr(cID), repr(self.playerNum))
                self.clientele[cID].send(("newPlayer %s\n" % myID).encode())
                client.send(("newPlayer %s\n" % cID).encode())
            self.clientele[myID] = client
            client.send(("myIDis %s \n" % myID).encode())
            print("connection recieved from %s" % myID)
            threading.Thread(target = handleClient, args = (client ,serverChannel, myID, self.clientele)).start()
            self.playerNum += 1

            print('PlayerNum: ' + str(self.playerNum))



    def createEnemies(self):
        
        self.counter += 1
        if self.counter % 30 == 0:
            self.enemyList.append(Enemy())
            # if self.counter % 45 == 0:
            #     self.enemyList.append(Boss())


    

    def getData(self):
        data = dict()
        data['enemyList'] = self.enemyList
        return data


    def redrawAll(self, screen):
        pass

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=600, height=400, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)


        self.enemyList = []
        self.counter = 0

        
        pygame.init()

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
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
            # screen.fill(self.bgColor)
            # self.redrawAll(screen)
            # pygame.display.flip()

        pygame.quit()




def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()



