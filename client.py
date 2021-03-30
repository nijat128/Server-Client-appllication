# CP372
# Names: Nijat Abdulkarimli, Asad Abbas
# ID: 160584230, 160498330

# Import
from socket import *
import json
import sys
import tkinter
import time

connection_status = False
board_width = 0
board_height = 0
colors = [""]
clientSocket = socket(AF_INET, SOCK_STREAM)

def connect():
    global connection_status
    global board_width
    global board_height
    global colors
    if serverName.get().strip() == "" or serverPort.get().strip() == "":
        error.configure(text="Couldn't establish connection. Server IP and Server Port must both be filled.", fg='red')
    elif connection_status is False:
        # Bind the socket to server address and server port
        print(int(serverPort.get().strip()))
        print(serverName.get().strip())
        server_name = str(serverName.get().strip())
        server_port = int(serverPort.get().strip())

        try:
            clientSocket.connect((server_name, server_port))
            status.configure(text="Connected!", fg='green')
            error.configure(text="", fg='green')
            connection_status = True
            # catch error here for bad server name
            # sentence = input('Input lower case sentence: ')
            # clientSocket.send(sentence.encode())
            # print('From server: ', modifiedSentence.decode())
            board_data = clientSocket.recv(2048)
            data = json.loads(board_data.decode())
            board_details = data.get("data")
            # print(str(board_details))
            board_width = board_details[0]
            board_height = board_details[1]
            board_w.configure(text="Board Width: " + str(board_width))
            board_h.configure(text="Board Height: " + str(board_height))
            colors.pop()
            for x in board_details[2:]:
                colors.append(x)
            variable.set('')
            variable2.set('')
            post_colors['menu'].delete(0, "end")
            # get_color['menu'].delete(0, "end")
            for string in colors:
                post_colors['menu'].add_command(label=string, command=lambda value=string: variable.set(value))
                get_color['menu'].add_command(label=string, command=lambda value=string: variable2.set(value))
            variable.set(colors[0])
            variable2.set(colors[0])
        except:
            error.configure(text="Couldn't establish connection. Try a different Server name.")


def disconnect():
    global connection_status
    if connection_status is True:
        connection_status = False
        clientSocket.close()
        sys.exit()
    # you will need to end the process from server side and close client application

def post():
    if x_coor.get().strip() == "" or y_coor.get().strip() == "" or note_width.get().strip() == "" or note_height.get().strip() == "" or note.get().strip() == "":
        error.configure(text="All fields must be filled before pressing Post!", fg="red")
    elif connection_status is False:
        error.configure(text="A connection must be established first!", fg="red")
    else:
        values = [x_coor.get().strip(), y_coor.get().strip(), note_width.get().strip(), note_height.get().strip()]
        try:
            int_values = [int(x) for x in values]
            x = int_values[0]
            y = int_values[1]
            width = int_values[2]
            height = int_values[3]
            message = note.get().strip()
            post_color = variable.get().strip()
            print(height)
            if (x+width) > board_width or (y+height) > board_height:
                error.configure(text="Coordinates of post are not defined within the board!", fg="red")
                return
            elif x < 0 or y < 0 or width < 1 or height < 1:
                error.configure(text="Note dimensions must be positive integers!", fg="red")
                return
            sentence = "POST " + str(x) + " " + str(y) + " " + str(width) + " " + str(height) + " " + str(post_color) + " " + str(message)
            clientSocket.send(sentence.encode())
            message = ""
            while message == "":
                response = clientSocket.recv(1024)
                decoded = response.decode()
                if str(decoded) != "":
                    message = str(decoded)
            results.configure(text=message)
            error.configure(text="")

        except:
            error.configure(text="Note dimensions must be positive integers!", fg="red")

def get_results():

    if connection_status is False:
        error.configure(text="A connection must be established first!", fg="red")
    elif v.get() == 1:
        try:
            sentence = "GET PINS"
            clientSocket.send(sentence.encode())
            message = ""
            while message == "":
                response = clientSocket.recv(1024)
                decoded = response.decode()
                if str(decoded) != "":
                    message = str(decoded)
            results.configure(text=message)
            error.configure(text="")
        except:
            error.configure(text="An error occurred, check you input and try again!", fg="red")

    elif v.get() == 2:
        if (get_x.get().strip() == "" and get_y.get().strip() != "") or (get_x.get().strip() != "" and get_y.get().strip() == ""):
            error.configure(text="Both coordinates need to be provided or neither!", fg="red")
            return
        else:
            sentence = "GET"
            if variable2.get().strip() != "":
                sentence = sentence + " color=" + str(variable2.get().strip())
            if get_x.get().strip() != "" and get_y.get().strip() != "":
                values = [get_x.get().strip(), get_y.get().strip()]
                try:
                    int_values = [int(x) for x in values]
                    x = int_values[0]
                    y = int_values[1]
                    if x > board_width or y > board_height or x < 0 or y < 0:
                        error.configure(text="Coordinates are not on board!", fg="red")
                        return
                    sentence = sentence + " contains=" + str(x) + "," + str(y)
                except:
                    error.configure(text="Coordinates must be integers!", fg="red")
                    return
            if refersTo.get().strip() != "":
                sentence = sentence + " refersTo=" + str(refersTo.get().strip())

            try:
                clientSocket.send(sentence.encode())
                message = ""
                while message == "":
                    response = clientSocket.recv(1024)
                    decoded = response.decode()
                    if str(decoded) != "":
                        message = str(decoded)
                results.configure(text=message)
                error.configure(text="")
            except:
                error.configure(text="An error occurred, check you input and try again!", fg="red")

        # send message to server to get what we need
    else:
        error.configure(text="Select one of the radio options before continuing!", fg="red")

def pin():
    if connection_status is False:
        error.configure(text="A connection must be established first!", fg="red")
    elif pin_x.get().strip() == "" or pin_y.get().strip() == "":
        error.configure(text="Please give coordinates of pin!", fg="red")
    else:
        values = [pin_x.get().strip(), pin_y.get().strip()]
        try:
            int_values = [int(x) for x in values]
            x = int_values[0]
            y = int_values[1]
            if x > board_width or y > board_height or x < 0 or y <0:
                error.configure(text="Pin coordinates are not on board!", fg="red")
                return
            sentence = "PIN " + str(x) + "," + str(y)
            clientSocket.send(sentence.encode())
            message = ""
            while message == "":
                response = clientSocket.recv(1024)
                decoded = response.decode()
                if str(decoded) != "":
                    message = str(decoded)
            results.configure(text=message)
            error.configure(text="")

        except:
            error.configure(text="Coordinates must be integers!", fg="red")
            return
        # send message to server to pin these coordinates

def unpin():
    if connection_status is False:
        error.configure(text="A connection must be established first!", fg="red")
    elif pin_x.get().strip() == "" or pin_y.get().strip() == "":
        error.configure(text="Please give coordinates of pin!", fg="red")
    else:
        values = [pin_x.get().strip(), pin_y.get().strip()]
        try:
            int_values = [int(x) for x in values]
            x = int_values[0]
            y = int_values[1]
            if x > board_width or y > board_height or x < 0 or y <0:
                error.configure(text="Pin coordinates are not on board!", fg="red")
                return
            sentence = "UNPIN " + str(x) + "," + str(y)
            clientSocket.send(sentence.encode())
            message = ""
            while message == "":
                response = clientSocket.recv(1024)
                decoded = response.decode()
                if str(decoded) != "":
                    message = str(decoded)
            results.configure(text=message)
            error.configure(text="")
        except:
            error.configure(text="Coordinates must be integers!", fg="red")
            return
        # send message to server to unpin these coordinates

def clear():
    if connection_status is False:
        error.configure(text="A connection must be established first!", fg="red")
    else:

        try:
            sentence = "CLEAR"
            clientSocket.send(sentence.encode())
            message = ""
            while message == "":
                response = clientSocket.recv(1024)
                decoded = response.decode()
                if str(decoded) != "":
                    message = str(decoded)
            results.configure(text=message)
            error.configure(text="")
        except:
            error.configure(text="Coordinates must be integers!", fg="red")
            return
        # send message to server to unpin these coordinates

# serverName = 'localhost'
# # Assign a port number
# serverPort = 6789

window = tkinter.Tk()

window.title("TCP Connection Menu")

connection_frame = tkinter.Frame(window).grid(row=2, rowspan=3)
post_frame = tkinter.Frame(window).grid(row=5, rowspan=6)
get_frame = tkinter.Frame(window).grid(row=12, rowspan=5)
pin_frame = tkinter.Frame(window).grid(row=18, rowspan=2)

# Connection frame widgets
status = tkinter.Label(window, text="Not connected!", fg='red')
status.grid(row=0, sticky="w")
tkinter.Label(window, text="Error:").grid(row=1, column=0, sticky="we")
error = tkinter.Label(window, text="")
error.grid(row=1, column=1, sticky="w", columnspan=3)

tkinter.Label(connection_frame, text = "Server IP:").grid(row = 2)
serverName = tkinter.Entry(connection_frame)
serverName.grid(row = 2, column = 1)

tkinter.Label(connection_frame, text = "Server Port:").grid(row = 3)
serverPort = tkinter.Entry(connection_frame)
serverPort.grid(row = 3, column = 1)

connect_btn = tkinter.Button(connection_frame, text = "Connect", command= connect).grid(row = 4, column = 0, sticky="we")
disconnect_btn = tkinter.Button(connection_frame, text = "Disconnect", command= disconnect).grid(row = 4, column = 1, sticky="we")

# Post frame widgets

board_w = tkinter.Label(post_frame, text="Board Width: ")
board_w.grid(row=5)
board_h = tkinter.Label(post_frame, text="Board Width: ")
board_h.grid(row=6)

tkinter.Label(post_frame, text="X Coor:").grid(row=7)
x_coor = tkinter.Entry(post_frame)
x_coor.grid(row = 7, column = 1)

tkinter.Label(post_frame, text="Y Coor:").grid(row = 7, column = 2)
y_coor = tkinter.Entry(post_frame)
y_coor.grid(row = 7, column = 3)

tkinter.Label(post_frame, text = "Width:").grid(row = 8)
note_width = tkinter.Entry(post_frame)
note_width.grid(row = 8, column = 1)

tkinter.Label(post_frame, text = "Height:").grid(row = 8, column = 2)
note_height = tkinter.Entry(post_frame)
note_height.grid(row = 8, column = 3)

tkinter.Label(post_frame, text = "Note/Message:").grid(row = 9)
note = tkinter.Entry(post_frame)
note.grid(row = 9, column=1, columnspan=3, sticky='we')

tkinter.Label(post_frame, text = "Colour:").grid(row = 10)
variable = tkinter.StringVar(post_frame)
variable.set(colors[0]) # default value

post_colors = tkinter.OptionMenu(post_frame, variable, *colors)
post_colors.grid(row = 10, column=1, sticky="we")

post_btn = tkinter.Button(post_frame, text = "POST", command=post).grid(row=10, column=2, columnspan=2, sticky="we")

# get frame widgets
tkinter.Label(get_frame, text = "").grid(row = 11)
v = tkinter.IntVar()
get_pins = tkinter.Radiobutton(get_frame, text="Pins", variable=v, value=1)
get_pins.grid(row = 12, sticky="we")
get_notes = tkinter.Radiobutton(get_frame, text="Notes", variable=v, value=2)
get_notes.grid(row = 12, column=1, sticky="we")

tkinter.Label(get_frame, text = "Contains:").grid(row = 13)
tkinter.Label(get_frame, text = "X coor:").grid(row = 14, column=0)
get_x = tkinter.Entry(get_frame)
get_x.grid(row = 14, column = 1)
tkinter.Label(get_frame, text = "Y coor:").grid(row = 14, column=2)
get_y = tkinter.Entry(get_frame)
get_y.grid(row = 14, column = 3)

tkinter.Label(get_frame, text = "Refers to:").grid(row = 15)
refersTo = tkinter.Entry(get_frame)
refersTo.grid(row = 15, column=1, columnspan=3, sticky='we')

tkinter.Label(get_frame, text = "Colour:").grid(row = 16)
variable2 = tkinter.StringVar(get_frame)
variable2.set(colors[0]) # default value

get_color = tkinter.OptionMenu(get_frame, variable2, *colors)
get_color.grid(row = 16, column=1, sticky="we")

get_btn = tkinter.Button(get_frame, text = "GET", command=get_results).grid(row=16, column=2, columnspan=2, sticky="we")

# get frame widgets
tkinter.Label(pin_frame, text = "").grid(row = 17)
tkinter.Label(pin_frame, text = "X coor:").grid(row = 18, column=0)
pin_x = tkinter.Entry(pin_frame)
pin_x.grid(row = 18, column = 1)
tkinter.Label(pin_frame, text = "Y coor:").grid(row = 18, column=2)
pin_y = tkinter.Entry(pin_frame)
pin_y.grid(row = 18, column = 3)

pin_btn = tkinter.Button(pin_frame, text = "PIN", command=pin).grid(row = 19, column = 0, sticky="we", columnspan=2)
unpin_btn = tkinter.Button(pin_frame, text = "UNPIN", command=unpin).grid(row = 19, column = 2, sticky="we", columnspan=2)

tkinter.Label(pin_frame, text = "").grid(row = 20)
clear_btn = tkinter.Button(pin_frame, text = "CLEAR", command=clear).grid(row = 21, column = 0, sticky="we", columnspan=2)

tkinter.Label(pin_frame, text = "").grid(row = 22)
tkinter.Label(pin_frame, text = "Results:").grid(row = 23, sticky="w")
results = tkinter.Label(pin_frame, text = "", wraplength=400)
results.grid(row = 24, sticky="w", columnspan=4, rowspan=4)

window.mainloop()


