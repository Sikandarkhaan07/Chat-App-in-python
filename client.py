import threading
import socket

alias = input('Choose an alias >>>> ')
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',55555))

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == "alias?":
                client.send(alias.encode('ascii'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
        break


def client_send():
    while True:
        message = f'{alias}: {input("")}'.format(alias,input(''))
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

write_thread = threading.Thread(target=client_send)
write_thread.start()