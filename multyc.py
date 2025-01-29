import socket
import threading
import sys

def receive_messages(client):
    while True:
        try:
            msg = client.recv(1024).decode()
            if not msg:
                break
            print(f"\n{msg}")
        except:
            print("\033[91mConnection lost.\033[0m")
            client.close()
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

username = input("\033[92mEnter your username: \033[0m")
client.send(username.encode())

thread = threading.Thread(target=receive_messages, args=(client,))
thread.start()

while True:
    try:
        msg = input("\033[95mYou: \033[0m")
        if msg.lower() == "exit":
            print("\033[91mDisconnected.\033[0m")
            client.close()
            sys.exit()
        client.send(msg.encode())
    except:
        break
