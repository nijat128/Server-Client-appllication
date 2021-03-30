# CP372
# Names: Nijat Abdulkarimli, Asad Abbas
# ID: 160584230, 160498330

import socket
import threading
import sys
import json

connections = []
total_connections = 0

c = 1
official_board = []
all_pins = []

class Notes(dict):

    def __init__(self):
        self = dict()

    def add(self, key, x, y, height, width, colour, message, pins, pinned):
        self[key] = {'x': x, 'y': y, 'height': height, 'width': width, 'colour': colour, 'message': message,
                     'pins': pins, 'pinned' : pinned}


def post_note(command, note, c):
    note.add(c, int(command[1]), int(command[2]), int(command[3]), int(command[4]), command[5], command[6], [], False)
    c = c + 1
    official_board.append(note)

def get_pins():
    msg = "All pin coordinates: " + str(all_pins)
    return msg

def get_notes(refer, contains, color):
    print(refer)
    print(contains)
    print(color)
    if len(refer) == 1 and len(contains) == 1 and len(color) == 1:
        output = []
        for i in official_board:
            output.append(i[1])

        return str(output)
    elif len(refer) != 1 and len(contains) != 1 and len(color) != 1:
        reference = str(refer[1])
        x = int(contains[1].strip().split(',')[0])
        y = int(contains[1].strip().split(',')[1])
        c = str(color[1].strip())
        output = []

        for i in official_board:
            note_x = i[1]['x']
            note_y = i[1]['y']
            note_height = i[1]['height']
            note_width = i[1]['width']
            message = i[1]['message']
            note_c = i[1]['colour']

            if x >= note_x and y >= note_y and x <= note_x + note_width and y <= note_y + note_height and c == note_c and reference in message:
                output.append(i[1])

        return str(output)

    elif len(refer) != 1 and len(contains) != 1:
        reference = str(refer[1])
        x = int(contains[1].strip().split(',')[0])
        y = int(contains[1].strip().split(',')[1])
        output = []

        for i in official_board:
            note_x = i[1]['x']
            note_y = i[1]['y']
            note_height = i[1]['height']
            note_width = i[1]['width']
            message = i[1]['message']

            if x >= note_x and y >= note_y and x <= note_x + note_width and y <= note_y + note_height and reference in message:
                output.append(i[1])

        return str(output)

    elif len(refer) != 1 and len(color) != 1:
        reference = str(refer[1])
        c = str(color[1].strip())
        output = []

        for i in official_board:
            message = i[1]['message']
            note_c = i[1]['colour']

            if c == note_c and reference in message:
                print(reference)
                print(message)
                output.append(i[1])

        return str(output)
    elif len(contains) != 1 and len(color) != 1:
        x = int(contains[1].strip().split(',')[0])
        y = int(contains[1].strip().split(',')[1])
        c = str(color[1].strip())
        output = []

        for i in official_board:
            note_x = i[1]['x']
            note_y = i[1]['y']
            note_height = i[1]['height']
            note_width = i[1]['width']
            note_c = i[1]['colour']

            if x >= note_x and y >= note_y and x <= note_x + note_width and y <= note_y + note_height and c == note_c:
                output.append(i[1])

        return str(output)
    elif len(refer) != 1:
        reference = str(refer[1])
        output = []

        for i in official_board:
            message = i[1]['message']
            note_c = i[1]['colour']

            if reference in message:
                output.append(i[1])

        return str(output)
    elif len(contains) != 1:
        x = int(contains[1].strip().split(',')[0])
        y = int(contains[1].strip().split(',')[1])
        output = []

        for i in official_board:
            note_x = i[1]['x']
            note_y = i[1]['y']
            note_height = i[1]['height']
            note_width = i[1]['width']

            if x >= note_x and y >= note_y and x <= note_x + note_width and y <= note_y + note_height:
                output.append(i[1])

        return str(output)
    elif len(color) != 1:
        c = str(color[1].strip())
        output = []

        for i in official_board:
            note_c = i[1]['colour']

            if c == note_c:
                output.append(i[1])

        return str(output)


def pin_notes(cmd):
    global all_pins
    cmd = cmd.split(",")
    x = int(cmd[0])
    y = int(cmd[1])
    pin = [x, y]
    pinned = False
    already_pinned = False

    for j in all_pins:
        if pin == j:
            already_pinned = True
            break

    if already_pinned is False:
        for i in official_board:
            note_x = i[1]['x']
            note_y = i[1]['y']
            note_height = i[1]['height']
            note_width = i[1]['width']
            pins = i[1]['pins']

            if (x >= note_x and y >= note_y and x <= note_x + note_width and y <= note_y + note_height):
                i[1]['pins'].append(pin)
                print(i[1]['pins'])
                i[1]['pinned'] = True
                pinned = True

    if pinned is True:
        all_pins.append(pin)
        return "Pin is placed on board"
    elif already_pinned is True:
        return "There is already a pin at this coordinate: " + str(pin)
    else:
        return "Not pinned, there is no note at these coordinates: " + str(pin)

def unpin_notes(cmd):
    global all_pins
    cmd = cmd.split(",")
    x = int(cmd[0])
    y = int(cmd[1])
    pin = [x, y]
    unpinned = False
    no_pin = True

    pin_index = 0
    for j in all_pins:
        if pin == j:
            no_pin = False
            break
        pin_index += 1

    if no_pin is False:
        for i in official_board:
            count = 0
            for k in i[1]['pins']:
                if k == pin:
                    i[1]['pins'].pop(count)
                    unpinned = True
                    break
                count += 1

            if len(i[1]['pins']) == 0:
                i[1]['pinned'] = False

    if unpinned is True:
        all_pins.pop(pin_index)
        return "Unpinned at coordinate: " + str(pin)
    elif no_pin is True:
        return "There is no pin at this coordinate: " + str(pin)
    else:
        return "Not pinned, there is no note at these coordinates: " + str(pin)

def clear_notes():
    note_indexs = []
    idx = 0

    for i in official_board:
        pinned = i[1]['pinned']
        if pinned is False:
            note_indexs.append(idx)
        idx += 1

    sub = 0
    for t in note_indexs:
        official_board.pop(t-sub)
        sub += 1

    return "Cleared " + str(len(note_indexs)) + " notes from the board!"

class Client(threading.Thread):

    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal

    def __str__(self):
        return str(self.id) + " " + str(self.address)

    # Attempt to get data from client
    # If unable to, assume client has disconnected and remove him from server data
    # If able to and we get data back, print it in the server and send it back to every
    # client aside from the client that has sent it
    # .decode is used to convert the byte data into a printable string
    def run(self):
        board_data = json.dumps({"data": board_details})
        self.socket.send(board_data.encode())

        while self.signal:
            try:
                data = self.socket.recv(1024)
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections.remove(self)
                break
            if data == b'':
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections.remove(self)
                break
            elif data != "":
                print(data)
                print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                if str(data.decode("utf-8")).split()[0] == 'POST':
                    cmd = str(data.decode("utf-8")).split(' ', 6)
                elif str(data.decode("utf-8")).split()[0] == 'PIN' or str(data.decode("utf-8")).split()[0] == 'UNPIN':
                    cmd = str(data.decode("utf-8")).split(' ', 1)
                elif str(data.decode("utf-8")).split()[0] == 'CLEAR':
                    cmd = str(data.decode("utf-8")).split()
                elif str(data.decode("utf-8")).split()[0] == 'GET':
                    cmd = str(data.decode("utf-8")).split()
                    if (len(cmd) > 1 and cmd[1] != 'PINS') or len(cmd) == 1:
                        refer = str(data.decode("utf-8")).split("refersTo=")
                        contains = str(refer[0]).split("contains=")
                        color = str(contains[0]).split("color=")

                if (cmd[0] == 'POST'):
                    note = Notes()
                    msg = "Post was successful!"
                    try:
                        post_note(cmd, note, c)
                        self.socket.send(msg.encode())
                    except:
                        msg = "An error occurred while posting. Please check your input and try again."
                        self.socket.send(msg.encode())

                    # self.socket.send(bytes("Message POSTED","UTF-8"))
                elif (cmd[0] == 'PIN'):
                    msg = pin_notes(cmd[1])
                    try:
                        self.socket.send(msg.encode())
                    except:
                        msg = "An error occurred while posting. Please check your input and try again."
                        self.socket.send(msg.encode())
                elif (cmd[0] == 'UNPIN'):
                    msg = unpin_notes(cmd[1])
                    try:
                        self.socket.send(msg.encode())
                    except:
                        msg = "An error occurred while posting. Please check your input and try again."
                        self.socket.send(msg.encode())
                elif (cmd[0] == 'CLEAR'):
                    msg = clear_notes()
                    try:
                        self.socket.send(msg.encode())
                    except:
                        msg = "An error occurred while posting. Please check your input and try again."
                        self.socket.send(msg.encode())
                elif (cmd[0] == 'GET'):
                    if len(cmd) > 1 and cmd[1] == 'PINS':
                        msg = get_pins()
                        try:
                            self.socket.send(msg.encode())
                        except:
                            msg = "An error occurred while posting. Please check your input and try again."
                            self.socket.send(msg.encode())
                    else:
                        msg = get_notes(refer, contains, color)
                        try:
                            self.socket.send(msg.encode())
                        except:
                            msg = "An error occurred while posting. Please check your input and try again."
                            self.socket.send(msg.encode())

                print(official_board)

                # for client in connections:
                #    if client.id == self.id:
                #        client.socket.sendall(data)


# Wait for new connections
def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1


def Main():
    # Get host and port
    host = 'localhost'
    port = serverPort

    # Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    print("socket binded to port " + str(port))
    sock.listen(5)
    print("socket is listening")

    # Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target=newConnections, args=(sock,))
    newConnectionsThread.start()


num_argv = len(sys.argv)
if num_argv < 5:
    print("You must run the program with atleast 5 arguments \n Ex. python server.py 4554 200 100 red")
    sys.exit()

# Assign a port number
try:
    serverPort = int(sys.argv[1])
    board_width = int(sys.argv[2])
    board_height = int(sys.argv[3])
except:
    print("Port, width, and height must be integers. \n Ex. python server.py 4554 200 100 red")
    sys.exit()

if board_width < 1 or board_height < 1 or serverPort < 1:
    print("Board width and height must be positive integers")
    sys.exit()

board_details = []
board_details.append(board_width)
board_details.append(board_height)

for arg in sys.argv[4:]:
    board_details.append(arg)

Main()
