import threading
import socket

host = '127.0.0.1' # local host (otherwise should be ip address of the server)
port = 55556

# if there is a new client connect to us, put it in the clients list, and it should have its nickname
clients = []
nicknames = []

# broadcast function (send message to all clients currently connected)
def broadcast(message):
    for client in clients:
        client.send(message)

# handle the client connection
def handle(client):
    while True: 
        try:
            message = client.recv(1024)
            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(("{} left the chat".format(nickname)).encode('ascii'))
            nicknames.remove(nickname)
            break

# write a function that combines the functions above
def receive(server):
    while True:
        client, address = server.accept()
        print("Connected with {}".format(address))

        # ask the client for the nickname
        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

        print("Nickname of the client is {}".format(nickname))
        broadcast(("{} joined the chat!".format(nickname)).encode("ascii"))
        client.send("Connected to the server! ".encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def main():
    """Main entry point to start the server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen() # server start to listen to incoming connections

    print("Server is listening on {}:{}...".format(host, port))
    receive(server)

if __name__ == "__main__":
    main()