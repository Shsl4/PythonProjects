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
target_host = "0.0.0.0"

### The Port that the cient will be using.
target_port = 0

### Defines the client socket.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

### The message which will be sent to server. (Default = "").
answer = ""

### Prints welcome message and launches the menu.
def InitScript() :

	print("[*] Welcome TCP Client!")
	print("[*] Use this script to connect to and send a message to a TCP Server. Type 'help' to list available commands")
	MenuPrompt()

### This is the menu prompt. This function checks for a valid (recognized) command defined in the function.
def MenuPrompt():

	print("")
	cmd = input(">> ")

	if cmd == "help":
		PrintHelp()
	elif cmd == "setupserver":
		PromptServerInfo()
	elif cmd == "checkserver":
		CheckServer(True, True)
	elif cmd == "sendmessage":
		SendMessage()
	elif cmd == "checkanswer":
		PrintAnswer()
	elif cmd == "exit":
	### Function used to close any python script. See sys documentation for more informations.
		sys.exit(1)
	elif cmd == "printinfo":
		PrintServerInfo()
	elif cmd == "clear":
		ClearScreen()
	elif cmd == "":
	### If the provided string is empty, Draw an empty line and go back to the menu.
		print("")
		MenuPrompt()
	else:
	### If the provided string isn't recognized, print message and go back to the menu.
		print("")
		print(">> Unknown command. Type 'help' to list available commands.")
		MenuPrompt()

### Displays the 'help' panel.
def PrintHelp():

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

	MenuPrompt()

### Function to input the target server's IPv4 and Port informations.
def PromptServerInfo():

	### Set references to global variables.

	global target_host
	global target_port
	global server

	### Ask for IPv4 Input.

	print("")
	new_target_host = input(">> Please provide an IP address (Default = 172.0.0.1) : ")

	### If the provided string is empty, use defalut value.

	if new_target_host == "" :

		### Default Value.

		new_target_host = "127.0.0.1"

	### Elif provided string is an empty IPv4 (Invalid) :

	elif new_target_host == "0.0.0.0" :

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid IP address provided. Leaving...")
		MenuPrompt()
		return

	### Try to convert input string to IPv4.

	try:

		ipaddress.ip_address(new_target_host)
	
	### If the conversion fails :

	except Exception:
		
		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid IP address provided. Leaving...")
		MenuPrompt()
		return

	new_target_port = input(">> Please provide a port (Default = 80) : ")

	### If the provided string is empty, use defalut value.

	if new_target_port == "":

		### Default Value.

		new_target_port = "80"
	
	### Try to convert input string to integer.

	try:

		int(new_target_port)

	### If the conversion fails :
	except ValueError:
		
		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid port provided. Leaving...")
		MenuPrompt()
		return

	### If the provided port is <= 0 (Invalid) :

	if int(new_target_port) <= 0:

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid port provided. Leaving...")
		MenuPrompt()
		return

	### If the provided port is above the max port value (Invalid) :

	elif int(new_target_port) > 65535:

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Invalid port provided. Leaving...")
		MenuPrompt()
		return
	
	### If the new IPv4 and Port are the same as the current ones :

	if target_host == new_target_host :

		if target_port == int(new_target_port) :

			### Print info message and go back to the menu.

			print("")
			print("[*] These values are already set, no need to update. Leaving...")
			MenuPrompt()
			return

	### Else, set these the new values.

	target_host = new_target_host
	target_port = int(new_target_port)

	### Print confirmation message, applied infos and go back to the menu

	print("")
	print("[*] Server Information Updated!")
	PrintServerInfo()
	MenuPrompt()

### Print the current server informations.
def PrintServerInfo():

	### Set global variables references.

	global target_host
	global target_port

	print("")
	print("[*] Current Configuration :")
	print("")
	if target_host == "0.0.0.0":
		print("[*] Current Server IP Address : Not Set")
	else:
		print("[*] Current Server IP Address :", target_host)
	if target_port ==  0:
		print("[*] Current Server Port : Not Set")
	else:
		print("[*] Current Server Port :", target_port)

	### Go back to the menu.

	MenuPrompt()

### Attempt to connect to the server. 
### - bMenu (bool) defines if the script goes back to the menu if the execution succeeds. (Will always leave on connection fail)
### - bPrint (bool) defines if the success info should be printed or not.
def CheckServer(bMenu, bPrint):

	### Set Global variable reference.

	global client

	#Try to connect the client to the server

	try:

		client.connect((target_host, target_port))

	### If it fails

	except Exception: 

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Unable to connect to server. Make sure that you server informations are valid and that your server is accessible.")
		MenuPrompt()
		return

	if bPrint :

		print("[*] Connection to server successful!")

	if bMenu:

		MenuPrompt()

### Send a message to the server.
def SendMessage():

	### Set global variable reference.

	global answer

	###Try to connect to the server.

	CheckServer(False, False)

	### Ask for message input.

	print("")
	myString = input(">> Input some string to send to the TCP server : ")

	### If the input string is empty :

	if len(myString) <= 0:

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : You provided an invalid message. Please input a valid message. Leaving...")
		MenuPrompt()
		return

	### Try to send a message to the server.

	try:

		client.send(myString.encode())
	
	### If it fails :

	except Exception:

		### Print error message and go back to the menu.

		print("")
		print("[*] Error : Failed to send message. Leaving...")
		MenuPrompt()
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
		MenuPrompt()
		return
	
	### Else print info message.

	print("")
	print("[*] Received an answer! Type 'checkanswer' to read it")

	### Go back to the menu

	MenuPrompt()

### Check for an answer and print it.
def PrintAnswer():

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

	MenuPrompt()

### Function used to clear the console screen.
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

	### Reprint Welcome message.

	InitScript()

### Starts the Script.
InitScript()

	
