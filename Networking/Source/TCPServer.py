### Simple Python script used to create a TCP Server and interact with TCP clients. (Use TCPClient.py to test)

### Low Level Networking Interface. Documentation : https://docs.python.org/3/library/socket.html
import socket

### IPv4 & IPv6 manipulation Library. Documentation : https://docs.python.org/3/library/ipaddress.html
import ipaddress

### System Specific parameters and functions. Documentation : https://docs.python.org/3/library/sys.html
import sys

### Miscellaneous operating system interfaces. Documentation : https://docs.python.org/3/library/os.html
import os

### Thread-based parallelism. Documentation : https://docs.python.org/3/library/threading.html 
import threading

### The IPv4 Address that the server will be bound to.
bind_ip = "0.0.0.0"

### The Port the server will be using.
bind_port = 0

### Defines the server socket.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

### The message which will be sent to clients when receving a packet. (Default = "Hello from server :)" ).
messagetosend = "Hello from server! :)"

### Variable used to determine if the server is currently listening to clients.
bListening = False

### Prints welcome message and starts the server configuration function.
def InitScript() :

	print("[*] Welcome TCP Server!")
	print("[*] Use this script to create a TCP Server and receive messages from clients. Type 'help' to list available commands")
	print("[*] Please configure your server first.")
	SetupConfiguration()

### This is the menu prompt. This function checks for a valid (recognized) command defined in the function.
def MenuPrompt():

	print("")
	cmd = input(">> ")

	if cmd == "help":
		PrintHelp()
	elif cmd == "setconfig":
		SetupConfiguration()
	elif cmd == "startlistening":
		StartListening()
	elif cmd == "setmessage":
		SetMessage()
	elif cmd == "exit":
	### Function used to close any python script. See sys documentation for more informations.
		sys.exit(1)
	elif cmd == "printinfo":
		PrintServerInfo()
	elif cmd == "clear":
		ClearScreen()
	### If the provided string is empty, go back to the menu.
	elif cmd == "":
		MenuPrompt()
	### If the provided string isn't recognized, print message and go back to the menu.
	else:
		print("")
		print(">> Unknown command. Type 'help' to list available commands.")
		MenuPrompt()

### Displays the 'help' panel.
def PrintHelp():

	### Print informations
	print("")
	print("[*] Available Commands :")
	print("")
	print("[*] help : Displays this screen")
	print("[*] setconfig : Setup server informations")
	print("[*] startlistening : Starts listening to clients")
	print("[*] printinfo : Display the current server informations")
	print("[*] setmessage : Set a message to send back to a client when the server receives a packet")
	print("[*] clear : Clears the screen (Windows, Darwin and Linux only)")
	print("[*] exit : Exits the script")

	### Go back to the menu.

	MenuPrompt()

### Function to input new server IPv4 and Port informations.
def SetupConfiguration():

	### Set references to global variables.

	global bind_ip
	global bind_port
	global server

	### Ask for IPv4 Input.

	print("")
	new_bind_ip = input(">> Please provide an IP address (Default = 172.0.0.1) : ")

	### If the provided string is empty, use defalut value.

	if new_bind_ip == "" :

		### Default Value.

		new_bind_ip = "127.0.0.1"

	### Elif provided string is an empty IPv4 (Invalid) :

	elif new_bind_ip == "0.0.0.0" :

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid IP address provided. Leaving...")
		print("[*] You can try to re-configure your server by typing 'setconfig'")
		MenuPrompt()
		return

	### Try to convert input string to IPv4.

	try:

		ipaddress.ip_address(new_bind_ip)
	
	### If the conversion fails :

	except Exception:
		
		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid IP address provided. Leaving...")
		print("[*] You can try to re-configure your server by typing 'setconfig'")
		MenuPrompt()
		return

	### Ask for Port input

	new_bind_port = input(">> Please provide a port (Default = 80) : ")

	### If the provided string is empty, use defalut value.

	if new_bind_port == "":

		new_bind_port = "80"

	### Try to convert input string to integer.
	
	try:

		int(new_bind_port)

	### If it fails :

	except ValueError:
		
		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid port provided. Leaving...")
		print("[*] You can try to re-configure your server by typing 'setconfig'")
		MenuPrompt()
		return

	### If the provided port is <= 0 (Invalid) :

	if int(new_bind_port) <= 0:
		
		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid port provided. Leaving...")
		print("[*] You can try to re-configure your server by typing 'setconfig'")
		MenuPrompt()
		return

	### If the provided port is above the max port value (Invalid) :

	elif int(new_bind_port) > 65535:

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid port provided. Leaving...")
		print("[*] You can try to re-configure your server by typing 'setconfig'")
		MenuPrompt()
		return

	### If the new IPv4 and Port are the same as the current ones :

	if bind_ip == new_bind_ip :

		if bind_port == int(new_bind_port) :

			### Print info message and go back to the menu.

			print("")
			print("[*] These values are already set, no need to update. Leaving...")
			MenuPrompt()
			return

	### Else, set these the new values.

	bind_ip = new_bind_ip
	bind_port = int(new_bind_port)	

	### Print confirmation message, applied infos and go back to the menu

	print("")
	print("[*] Server Configuration Updated!")
	PrintServerInfo()
	MenuPrompt()

### Checks the Pv4 and Port informations and rebuild the server socket.
def CheckValidityAndRebuildSocket():

	### Set reference to global variables.

	global server
	global bind_ip
	global bind_port

	### Redefine the server socket.

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	### Check for the current IPv4's and Port's validity.

	if bind_ip == "0.0.0.0" or bind_port == 0:

		### If one of them is null, print error message and go back to the menu. 

		print("")
		print("[*] Error : Unable to server bind configuration. Please check your configuration. Leaving...")
		MenuPrompt()

	### Try to bind the server socket to the provided IPv4 and Port.

	try:

		server.bind((bind_ip, bind_port))

	### If it fails :

	except Exception:

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Unable to server bind configuration. Please check your configuration. Leaving...")
		MenuPrompt()
		return

### Function used to start listening to clients.
def StartListening(): 
	
	### Set global variable reference.

	global server

	### Try to rebuild the server socket

	CheckValidityAndRebuildSocket()

	### Aesthetics

	print("")

	### Try to start listening

	try :

		server.listen(5)
	
	### If it fails :

	except Exception :

		### Print error message and go back to the menu.

		print("[*] Error : Unable to listen using the desired IP and Port")
		MenuPrompt()
		return

	### Else print status message and listen.

	print("[*] This TCP Server will attempt to send '", messagetosend, "' back to a client when it receives a request")
	print("[*] Now Listening on %s through port %d" % (bind_ip, bind_port))
	print("[*] Send the code 'end' from a TCP client to end the listening.")
	bListening = True

	### While the server is listening.

	while bListening == True:

		### Try to accept clients.

		try :

			client, addr = server.accept()
		
		### If it fails :

		except Exception :

			### Do nothing.

			pass
		
		else:

			### Print the new connection message and start handling client.

			print("")
			print("[*] Accepted connection from %s : %d" % (addr[0], addr[1]))

			client_handler = threading.Thread(target=handle_client,args=(client,)) 
			client_handler.start()

### Function used to handle the client.
def handle_client(client_socket):
	
	### Set global variable reference.

	global messagetosend

	### When receiving a message, try to receive and decode it.

	try :

		request = client_socket.recv(4096).decode()


	### If client suddenly disconnects (Invalid Request) :
	except Exception :

		### Print status message.

		print("")
		print("[*] Remote host disconnected.")

	else :

		### Check if the received message is the shutdown code : 'end'

		if request == "end":

			### If so, print status messages and stop listening

			print("")
			print("[*] Shutdown message received. Leaving...")
			client_socket.send("SUCCESSFULLY TERMINATED.".encode())
			client_socket.close()
			StopListening()
			return

		### If the received message is empty :

		elif request == "":

			### Do nothing

			pass

		else:

			### Print the received message and send our message back (messagetosend)

			print("")
			print("[*] Received: %s" % request)
			client_socket.send(messagetosend.encode())
			client_socket.close()

### Function used to stop listening to clients.		
def StopListening(): 

	### Set global variable reference

	global bListening

	### Close the socket

	server.close()

	### Print status message and variable, then go back to the menu

	print("")
	print("[*] Closing connections...")
	bListening = False
	MenuPrompt()

### Function used to set the message that will be sent to a client when receving a packet.
def SetMessage():

	### Set global variable reference.

	global messagetosend

	### Print instruction message.

	print("")
	new_message = input("[*] Input a message to send back to a client when the receiving a packet : ")

	### If the provided message is empty :

	if new_message == "":

		### Print error messages and go back to the menu

		print("")
		print("[*] Error : Unable to send empty messages! Leaving...")
		MenuPrompt()
		return

	### Else try to set the new message as "messagetosend".

	try :

		messagetosend = new_message
	
	### If it fails :
	except Exception:

		### Print error and go back to the menu.

		print("[*] Unknown Error : Unable to set the new message. Leaving...")
		MenuPrompt()
		return

	### Print status message

	print("")
	print("[*] New message set!")
	MenuPrompt()
	
### Function used to clear the console screen
def ClearScreen():

	### Check the OS and use its cleaning command.

	### Windows

	if sys.platform == 'win32':
		os.system("cls")

	### Linux or macOS
	elif sys.platform == 'Linux' or sys.platform == 'darwin':
		os.system("clear")

	else:
		print("")
		print("[*] Error : Unknown Operating System, unable to clear.")
		return

	### Reprint welcome message.

	print("[*] Welcome TCP Server!")
	print("[*] Use this script to create a TCP Server. Type 'help' to list available commands")

	MenuPrompt()

### Print the current server informations
def PrintServerInfo():

	### Set global variables references.

	global bind_ip
	global bind_port
	global messagetosend

	print("")
	print("[*] Current Configuration :")
	print("")

	if bind_ip == "0.0.0.0":
		print("[*] Current Server IP Address : Not Set")
	else:
		print("[*] Current Server IP Address :", bind_ip)
	if bind_port ==  0:
		print("[*] Current Server Port : Not Set")
	else:
		print("[*] Current Server Port :", bind_port)

	print("[*] Current Message :", messagetosend)

	### Go back to the menu.

	MenuPrompt()

### Starts the Script.
InitScript()



