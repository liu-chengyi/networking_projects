import socket
import threading

def receive(client, nickname):
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "NICK":
                client.send(nickname.encode("ascii"))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write(client, nickname):
    while True:
        message = "{}: {}".format(nickname, input(""))
        client.send(message.encode("ascii"))

def main():
    nickname = input("Choose a nickname: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 55556))
    receive_thread = threading.Thread(target=receive, args=(client, nickname))
    receive_thread.start()
    write_thread = threading.Thread(target=write, args=(client, nickname))
    write_thread.start()


if __name__ == "__main__":
    main()