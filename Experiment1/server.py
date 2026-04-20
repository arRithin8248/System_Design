import socket

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(("localhost",5000))

server.listen(1)
print("Server Waiting for Client")

client_socket,addr=server.accept()

print("Connected with Client")

message=client_socket.recv(1024).decode()
print("Client Says",message)

client_socket.send("Hello from Server".encode())

client_socket.close()
server.close()