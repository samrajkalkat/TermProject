###
#Server code from provided gitBook on 15-112 webiste
###


import socket
import threading
from queue import Queue
from enemy import *


HOST = '' # put your IP address here if playing on multiple computers
PORT = 50003
BACKLOG = 4

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("Waiting for connection...")

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

clientele = dict()
playerNum = 0
names = ["p1","p2"]

while True:
	serverChannel = Queue(100)
	threading.Thread(target = serverThread, args = (clientele, serverChannel)).start()
	client, address = server.accept()
	# myID is the key to the client in the clientele dictionary
	myID = names[playerNum]
	print(myID, playerNum)
	for cID in clientele:
		print (repr(cID), repr(playerNum))
		clientele[cID].send(("newPlayer %s\n" % myID).encode())
		client.send(("newPlayer %s\n" % cID).encode())
	clientele[myID] = client
	client.send(("myIDis %s \n" % myID).encode())
	print("connection recieved from %s" % myID)
	threading.Thread(target = handleClient, args = (client ,serverChannel, myID, clientele)).start()
	playerNum += 1
	print('PlayerNum: ' + str(playerNum))




