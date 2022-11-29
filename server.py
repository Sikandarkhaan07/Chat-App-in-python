from email import message
import threading
import socket
host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
aliases = []

def boardcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            boardcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            boardcast('{alias} has left the chat room!'.format(alias).encode('ascii'))
            aliases.remove(alias)
            break

def receive():
    while True:
        print('server is running and listening....')
        client,address = server.accept()
        print("Connected with {}".format(str(address)))

        client.send('alias?'.encode('ascii'))
        alias = client.recv(1024).decode('ascii')
        aliases.append(alias)
        clients.append(client)

        print("Nickname is {}".format(alias))
        boardcast("{} joined!".format(alias).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()
