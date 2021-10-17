import threading
import socket

PORT = 8080
HOST = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message.encode(FORMAT))

def handle(client):
    while True:
        try:
            b_message = client.recv(1024).decode(FORMAT)
            broadcast(b_message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat')
            nicknames.remove(nickname)
            break

def receive():
    while True: 
        print(f"Server listening at {HOST}")
        client, addr = server.accept()
        print(f"Connected with {str(addr)} {client}")
        client.send('NICK'.encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of the client: {nickname}")

        broadcast(f"{nickname} joined the chat!\n")
        client.send("Connected to the server\n".encode(FORMAT))

        thread_client = threading.Thread(target=handle, args=(client,))
        thread_client.start()


receive()




