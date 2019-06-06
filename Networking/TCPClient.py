### Simple Python script used to create a TCP Client and interact with TCP servers. (Use TCPServer.py to test)

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

### The IPv4 Address that the client will try to connect to.
targetIP = "0.0.0.0"

### The Port that the cient will be using.
targetPort = 0

### Defines the client socket.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

### The message which will be sent to server. (Default = "").
answer = ""

### Prints welcome message and launches the menu.
def initScript() :

	print("[*] Welcome TCP Client!")
	print("[*] Use this script to connect to and send a message to a TCP Server. Type 'help' to list available commands")
	menuPrompt()

### This is the menu prompt. This function checks for a valid (recognized) command defined in the function.
def menuPrompt():

	print("")
	cmd = input(">>> ")

	if cmd == "help":
		printHelp()
	elif cmd == "setupserver":
		promptServerInfo()
	elif cmd == "checkserver":
		checkServer(True, True)
	elif cmd == "sendmessage":
		sendMessage()
	elif cmd == "checkanswer":
		printAnswer()
	elif cmd == "exit":
	### Function used to close any python script. See sys documentation for more informations.
		sys.exit(1)
	elif cmd == "printinfo":
		printServerInfo()
	elif cmd == "clear":
		clearScreen()
	elif cmd == "":
	### If the provided string is empty, Draw an empty line and go back to the menu.
		print("")
		menuPrompt()
	else:
	### If the provided string isn't recognized, print message and go back to the menu.
		print("")
		print(">>> Unknown command. Type 'help' to list available commands.")
		menuPrompt()

### Displays the 'help' panel.
def printHelp():

	### Print informations
	print("")
	print("Available Commands :")
	print("")
	print("[*] help : Displays this screen")
	print("[*] setupserver : Setup server connection informations")
	print("[*] checkserver : Check connection's validity to the provided server")
	print("[*] printinfo : Display the current server informations")
	print("[*] sendmessage : Send a string message to the server")
	print("[*] checkanswer : Check for a potential server awnser")
	print("[*] clear : Clears the screen (Windows, Darwin and Linux only)")
	print("[*] exit : Exit the script")

	### Go back to the menu.

	menuPrompt()

### Function to input the target server's IPv4 and Port informations.
def promptServerInfo():

	### Set references to global variables.

	global targetIP
	global targetPort
	global server

	### Ask for IPv4 Input.

	print("")
	newTargetIP = input(">>> Please provide an IP address (Default = 172.0.0.1) : ")

	### If the provided string is empty, use defalut value.

	if newTargetIP == "" :

		### Default Value.

		newTargetIP = "127.0.0.1"

	### Elif provided string is an empty IPv4 (Invalid) :

	elif newTargetIP == "0.0.0.0" :

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid IP address provided. Leaving...")
		menuPrompt()
		return

	### Try to convert input string to IPv4.

	try:

		ipaddress.ip_address(newTargetIP)
	
	### If the conversion fails :

	except Exception:
		
		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid IP address provided. Leaving...")
		menuPrompt()
		return

	newTargetPort = input(">>> Please provide a port (Default = 80) : ")

	### If the provided string is empty, use defalut value.

	if newTargetPort == "":

		### Default Value.

		newTargetPort = "80"
	
	### Try to convert input string to integer.

	try:

		int(newTargetPort)

	### If the conversion fails :
	except ValueError:
		
		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid port provided. Leaving...")
		menuPrompt()
		return

	### If the provided port is <= 0 (Invalid) :

	if int(newTargetPort) <= 0:

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid port provided. Leaving...")
		menuPrompt()
		return

	### If the provided port is above the max port value (Invalid) :

	elif int(newTargetPort) > 65535:

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid port provided. Leaving...")
		menuPrompt()
		return
	
	### If the new IPv4 and Port are the same as the current ones :

	if targetIP == newTargetIP :

		if targetPort == int(newTargetPort) :

			### Print info message and go back to the menu.

			print("")
			print("[*] These values are already set, no need to update. Leaving...")
			menuPrompt()
			return

	### Else, set these the new values.

	targetIP = newTargetIP
	targetPort = int(newTargetPort)

	### Print confirmation message, applied infos and go back to the menu

	print("")
	print("[*] Server Information Updated!")
	printServerInfo()
	menuPrompt()

### Print the current server informations.
def printServerInfo():

	### Set global variables references.

	global targetIP
	global targetPort

	print("")
	print("[*] Current Configuration :")
	print("")
	if targetIP == "0.0.0.0":
		print("[*] Current Server IP Address : Not Set")
	else:
		print("[*] Current Server IP Address :", targetIP)
	if targetPort ==  0:
		print("[*] Current Server Port : Not Set")
	else:
		print("[*] Current Server Port :", targetPort)

	### Go back to the menu.

	menuPrompt()

### Attempt to connect to the server. 
### - bMenu (bool) defines if the script goes back to the menu if the execution succeeds. (Will always leave on connection fail)
### - bPrint (bool) defines if the success info should be printed or not.
def checkServer(bMenu, bPrint):

	### Set Global variable reference.

	global client
	
        ### Rebuild the client socket

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	#Try to connect the client to the server

	try:

		client.connect((targetIP, targetPort))

	### If it fails

	except Exception: 

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Unable to connect to server. Make sure that you server informations are valid and that your server is accessible.")
		menuPrompt()
		return

	if bPrint :

		print("[*] Connection to server successful!")

	if bMenu:

		menuPrompt()

### Send a message to the server.
def sendMessage():

	### Set global variable reference.

	global answer

	###Try to connect to the server.

	checkServer(False, False)

	### Ask for message input.

	print("")
	myString = input(">>> Input some string to send to the TCP server : ")

	### If the input string is empty :

	if len(myString) <= 0:

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : You provided an invalid message. Please input a valid message. Leaving...")
		menuPrompt()
		return

	### Try to send a message to the server.

	try:

		client.send(myString.encode())
	
	### If it fails :

	except Exception:

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Failed to send message. Leaving...")
		menuPrompt()
		return

	### Else print info message.

	print("")
	print("[*] Message successfully sent!")

	### Try to receive an answer from the server. 

	try :

		answer = client.recv(4096)
	
	### If it fails :

	except Exception :

		### Print info message and go bacck to the menu.

		print("")
		print("[*] No Immediate Answer detected.")
		menuPrompt()
		return
	
	### Else print info message.

	print("")
	print("[*] Received an answer! Type 'checkanswer' to read it")

	### Go back to the menu

	menuPrompt()

### Check for an answer and print it.
def printAnswer():

	### Set global variable reference.

	global answer

	### If answer is empty :

	if answer == "":

		### Print info message.

		print("")
		print("[*] Error : No recent message received.")

	else :

		### Try to print the message.

		try:

			print("")
			print("[*] Awnser Recently received! The server awnser is :", answer)
		
		### If it fails :

		except Exception :

			### Print Error message :

			print("")
			print("[*] Error : Message unreadable.")

	### Go back to the menu.

	menuPrompt()

### Function used to clear the console screen.
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

	### Reprint Welcome message.

	initScript()

### Starts the Script.
initScript()

	
