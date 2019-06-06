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
usingIP = "0.0.0.0"

### The Port the server will be using.
usingPort = 0

### Defines the server socket.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

### The message which will be sent to clients when receving a packet. (Default = "Hello from server :)" ).
messageToSend = "Hello from server! :)"

### Variable used to determine if the server is currently listening to clients.
bListening = False

### Prints welcome message and starts the server configuration function.
def initScript() :

	print("[*] Welcome TCP Server!")
	print("[*] Use this script to create a TCP Server and receive messages from clients. Type 'help' to list available commands")
	print("[*] Please configure your server first.")
	setupConfiguration()

### This is the menu prompt. This function checks for a valid (recognized) command defined in the function.
def menuPrompt():

	print("")
	cmd = input(">>> ")

	if cmd == "help":
		printHelp()
	elif cmd == "setconfig":
		setupConfiguration()
	elif cmd == "startlistening":
		startListening()
	elif cmd == "setmessage":
		setMessage()
	elif cmd == "exit":
	### Function used to close any python script. See sys documentation for more informations.
		sys.exit(1)
	elif cmd == "printinfo":
		printServerInfo()
	elif cmd == "clear":
		clearScreen()
	### If the provided string is empty, Draw an empty line and go back to the menu.
	elif cmd == "":
		menuPrompt()
	### If the provided string isn't recognized, print message and go back to the menu.
	else:
		print("")
		print(">>> Unknown command. Type 'help' to list available commands.")
		menuPrompt()

### Displays the 'help' panel.
def printHelp():

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

	menuPrompt()

### Function to input new server IPv4 and Port informations.
def setupConfiguration():

	### Set references to global variables.

	global usingIP
	global usingPort
	global server

	### Ask for IPv4 Input.

	print("")
	newIP = input(">>> Please provide an IP address (Default = 172.0.0.1) : ")

	### If the provided string is empty, use defalut value.

	if newIP == "" :

		### Default Value.

		newIP = "127.0.0.1"

	### Elif provided string is an empty IPv4 (Invalid) :

	elif newIP == "0.0.0.0" :

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid IP address provided. Leaving...")
		print("[*] You can try to re-configure your server by typing 'setconfig'")
		menuPrompt()
		return

	### Try to convert input string to IPv4.

	try:

		ipaddress.ip_address(newIP)
	
	### If the conversion fails :

	except Exception:
		
		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid IP address provided. Leaving...")
		print("[*] You can try to re-configure your server by typing 'setconfig'")
		menuPrompt()
		return

	### Ask for Port input

	newPort = input(">>> Please provide a port (Default = 80) : ")

	### If the provided string is empty, use defalut value.

	if newPort == "":

		newPort = "80"

	### Try to convert input string to integer.
	
	try:

		int(newPort)

	### If it fails :

	except ValueError:
		
		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid port provided. Leaving...")
		print("[*] You can try to re-configure your server by typing 'setconfig'")
		menuPrompt()
		return

	### If the provided port is <= 0 (Invalid) :

	if int(newPort) <= 0:
		
		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid port provided. Leaving...")
		print("[*] You can try to re-configure your server by typing 'setconfig'")
		menuPrompt()
		return

	### If the provided port is above the max port value (Invalid) :

	elif int(newPort) > 65535:

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid port provided. Leaving...")
		print("[*] You can try to re-configure your server by typing 'setconfig'")
		menuPrompt()
		return

	### If the new IPv4 and Port are the same as the current ones :

	if usingIP == newIP :

		if usingPort == int(newPort) :

			### Print info message and go back to the menu.

			print("")
			print("[*] These values are already set, no need to update. Leaving...")
			menuPrompt()
			return

	### Else, set these the new values.

	usingIP = newIP
	usingPort = int(newPort)	

	### Print confirmation message, applied infos and go back to the menu

	print("")
	print("[*] Server Configuration Updated!")
	printServerInfo()
	menuPrompt()

### Checks the Pv4 and Port informations and rebuild the server socket.
def checkValidityAndRebuildSocket():

	### Set reference to global variables.

	global server
	global usingIP
	global usingPort

	### Redefine the server socket.

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	### Check for the current IPv4's and Port's validity.

	if usingIP == "0.0.0.0" or usingPort == 0:

		### If one of them is null, print error message and go back to the menu. 

		print("")
		print("[*] Error : Unable to server bind configuration. Please check your configuration. Leaving...")
		menuPrompt()

	### Try to bind the server socket to the provided IPv4 and Port.

	try:

		server.bind((usingIP, usingPort))

	### If it fails :

	except Exception:

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Unable to server bind configuration. Please check your configuration. Leaving...")
		menuPrompt()
		return

### Function used to start listening to clients.
def startListening(): 
	
	### Set global variable reference.

	global server

	### Try to rebuild the server socket

	checkValidityAndRebuildSocket()

	### Aesthetics

	print("")

	### Try to start listening

	try :

		server.listen(5)
	
	### If it fails :

	except Exception :

		### Print error message and go back to the menu.

		print("[*] Error : Unable to listen using the desired IP and Port")
		menuPrompt()
		return

	### Else print status message and listen.

	print("[*] This TCP Server will attempt to send '", messageToSend, "' back to a client when it receives a request")
	print("[*] Now Listening on %s through port %d" % (usingIP, usingPort))
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

			client_handler = threading.Thread(target=handleClient,args=(client,)) 
			client_handler.start()

### Function used to handle the client.
def handleClient(clientSocket):
	
	### Set global variable reference.

	global messageToSend

	### When receiving a message, try to receive and decode it.

	try :

		request = clientSocket.recv(4096).decode()


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
			clientSocket.send("SUCCESSFULLY TERMINATED.".encode())
			clientSocket.close()
			stopListening()
			return

		### If the received message is empty :

		elif request == "":

			### Do nothing

			pass

		else:

			### Print the received message and send our message back (messagetosend)

			print("")
			print("[*] Received: %s" % request)
			clientSocket.send(messageToSend.encode())
			clientSocket.close()

### Function used to stop listening to clients.		
def stopListening(): 

	### Set global variable reference

	global bListening

	### Close the socket

	server.close()

	### Print status message and variable, then go back to the menu

	print("")
	print("[*] Closing connections...")
	bListening = False
	menuPrompt()

### Function used to set the message that will be sent to a client when receving a packet.
def setMessage():

	### Set global variable reference.

	global messageToSend

	### Print instruction message.

	print("")
	newMessage = input("[*] Input a message to send back to a client when the receiving a packet : ")

	### If the provided message is empty :

	if newMessage == "":

		### Print error messages and go back to the menu

		print("")
		print("[*] Error : Unable to send empty messages! Leaving...")
		menuPrompt()
		return

	### Else try to set the new message as "messagetosend".

	try :

		messageToSend = newMessage
	
	### If it fails :
	except Exception:

		### Print error and go back to the menu.

		print("[*] Unknown Error : Unable to set the new message. Leaving...")
		menuPrompt()
		return

	### Print status message

	print("")
	print("[*] New message set!")
	menuPrompt()
	
### Function used to clear the console screen
def clearScreen():

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

	menuPrompt()

### Print the current server informations
def printServerInfo():

	### Set global variables references.

	global usingIP
	global usingPort
	global messageToSend

	print("")
	print("[*] Current Configuration :")
	print("")

	if usingIP == "0.0.0.0":
		print("[*] Current Server IP Address : Not Set")
	else:
		print("[*] Current Server IP Address :", usingIP)
	if usingPort ==  0:
		print("[*] Current Server Port : Not Set")
	else:
		print("[*] Current Server Port :", usingPort)

	print("[*] Current Message :", messageToSend)

	### Go back to the menu.

	menuPrompt()

### Starts the Script.
initScript()



