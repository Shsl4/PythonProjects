import socket

targetIP = "127.0.0.1"
targetPort = 80

#Creating a socket object

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Send some data

client.sendto("AAABBBCCC".encode(), (targetIP, targetPort))

#Receive some data

data, addr = client.recvfrom(4096)

print(data)