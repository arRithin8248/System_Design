import socket

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(("localhost",5000))

client.send("Hello Server".encode())

response=client.recv(1024).decode()


print("Server Says",response)

client.close()

