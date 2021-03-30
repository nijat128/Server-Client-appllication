# Server-Client-application

1. Introduction

1.1	 Assignment Description 

The Server-Client application is intended to support clients’ ability to store “notes” on a server, and to request “notes” that have certain properties. 

Client should be able to make the following requests:
1.	Setup a connection with the server
2.	Send different types of request messages through established connection:
a.	POST <note>
b.	GET <params>
c.	PIN/UNPIN <coord>
d.	CLEAR
e.	DISCONNECT

Server should be able to do the following:
•	Accept multiple requests for connections
•	Maintain an appropriate data structure (“notes” dictionary or board) that holds data received from clients
•	Process messages received from client:
o	If message is POST <note>, server will have to store the note described in <note> part of the message.
o	If message is GET <params>, server has to send to client all notes stored in the dictionary that satisfy properties described in <params>.
o	If message is PIN <coord>, server must pin all notes relevant to <coord>.
o	If message is UNPIN <coord>, server must unpin all notes relevant to <coord>.
o	If message is CLEAR, server must forget all notes which are not pinned.
o	If message is DISCONNECT, server will disconnect the connection with the client


1.2 Definitions

<note> is similar to post-it note (colored rectangular piece of paper containing a string): If a client would like to POST a note, it must completely defined by the coordinates of lower-left corner, width, height, color, message and status (pinned/unpinned)

Example:
   POST 2 3 10 20 white Meeting next Wednesday from 2 to 3
   POST 6 6 5 5 red Pick up Fred from home at 5

<coord> is a pair of integers, describing x and y coordinates of a point on the board. When notes are originally posted, they are not pinned. To change the status of a note, a client can use PIN or UNPIN command. For example,

	PIN 4,4
will pin all notes that contain the given “pin coordinates”. In the example above the first note will be pinned

PIN 7,7
Will change the status of both notes to pinned

The meaning of UNPIN is obvious. However, remember that a note can be pinned by more than one pin. So, UNPIN command does not necessarily change the status of a note.

<params> field in GET request may take two values 

1.	PIN 
Example: 
GET PINS 
The above message forces the server to supply a client with coordinates of all pins. 

2.	It could have the following general format: 
color=<color>
contains<coord>
referesTo=<string> 

Such a parameter will force the server to supply the client with information of all notes of the particular color that contain point and has substring in the content. If one of the criteria is missing – the semantics of request is ALL (for example, no color in GET means ALL colors)

1.3	Implementation requirements

Server is a multi-process python console application that has multiple command line arguments and starts with empty “notes” dictionary. The arguments are in order: 

<port number>, <board width>, <board height>, <default color>,
<color 2>,...,<color n>.

For example, if implementation of server is in file SBoard.py, then to start server in command line one can execute 

>python SBoard.py 4554 200 100 red white green yellow 

which starts the server ready to accept connections on port 4554, supporting the board 200 units wide and 100 units tall, accepting notes of the colors red, white, green or yellow (with red being default color). 

Every new client connected to the server will receive a list of available colors, and the dimension of the board upon successful connection. Server’s response to GET type of message is obvious. Server’s response to POST type of messages has to confirm the receipt of the note (or send back an ERROR message). Error handling responsibilities naturally split between server and client and must be described in your document. Also note that the board exists only between server start and shutdown, and does not need to be stored.

Client has to provide a text menu to the user for different functionalities supported 
1-connect 
2-disconnect 
3-POST 
4-GET 
5-PIN 
6-UNPIN 
7-CLEAR 

Client should show the result of each request to the user. Upon choosing any of the options by the user, the client program should ask the user for more information. For example, If the user chooses 1, the program should ask the user to provide server address and port numbers. If the user chooses 3, the program should ask the user to enter the message to be posted to the server.

2	Protocol Description

This client server application follows a protocol format of COMMAND, parameter, parameter, ...

The formatting for this is described as below:
POST <x> <y> <width> <height> <color> <message>
GET color=<colour> contains=<x>,<y> refersTo=<text>
GET PINS
PIN <x>,<y>
UNPIN, <x>,<y>
CLEAR
DISCONNECT

2.1 Server Message Format

 As for the Server File connection. The formatting is as described below:

Python server.py <port> <width> <height> <colour1> <colour2> …<ColourN>

Successful server Startup message:
Socket binded to port <port>
Socket is listening

On Client Connection:
New connection at id 0 
(‘121.0.0.1’, 50078)

On Client Disconnection:
Client (‘121.0.0.1’, 50078)has disconnected

2.2 Client-Server Message Format

On a successful connection between server-client:
Available colour include: red, blue and green
Dimensions of Board: 200, 100

User Options GUI
1-connect button
2-disconnect button
3-POST button
POST has fields x, y, width, height, message before sending request to server
Server response format to POST:
Note posted

4-GET
Pins option and Notes option for GET button
Colour, contains, and refers to fields for GET Notes request
Response format to GET:
Array of pins [[5,9]]
Array of Notes information [{‘x’: 5, ‘y’: 9, etc..}]

5-PIN
X and Y fields for PIN and UNPIN button
PIN Request Message sent by Client: 5
Response format to PIN:
Note pinned to board

6-UNPIN
X and Y fields for PIN and UNPIN button
Response format to UNPIN:
Unpinned at coordinate:

7-CLEAR
Response format to CLEAR:
n notes cleared

2.3 Synchronization Policies

The synchronization mechanism enabled in the application is multithreading. This way multiple clients are connected and commuting with the server at the same time. Multiple threads within the process share the same data space with the main thread. This allows for overall efficient communication and sharing of information.


3. Error Handling Mechanism 

Some of the error catching is done on the client side. This is essentially where the program tells the user what to change before sending. Further some of the error handling is done on the server side. The server will send a message back to the client telling it that it didn’t do the request and the reason behind it.
Ex. Errors involving coordinates will be handled on client side and an error where the user tries to unpin where a pin doesn’t exist will be handled by the server who will send back an appropriate message to the client

4. GUI Based Application

The client side of the application is done through a GUI. This includes the following:

● Text field to provide IP address of the server
● Text field to provide port number
● Connect/Disconnect button
● Text area to type in text to be sent to server and POST button
● GET button with dialogue to enter required properties
● PIN and UNPIN buttons with dialogue to enter coordinates



