# Zombies Online

CMU 15-112 Term Project. Created with Pygame and Web Sockets.\

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.\

## Prerequisites

Install pygame. Open the terminal and enter the following:\
\
```\
pip3 install pygame\
```\
\
## Running\
\
* Find IP address of one player\
	* Replace HOST string value on server.py and client.py files\
	* For single player leave the HOST value as an empty string (\'91\'92)\
\
* Run server.py from one computer\
	* The console should print \'91waiting for connection\'92\
\
* Run client.py from each computer\
\
## Closing\
\
* Close the client.py windows first\
* Close server by pressing \'93control \'91c\'92\'94 on the server.py file so the console prints [Cancelled]\
	* Note that it may take a few seconds for the socket to re-open after server.py is closed\
\
\pard\pardeftab720\partightenfactor0

\f1\fs24 \cf0 \kerning1\expnd0\expndtw0 \
}
