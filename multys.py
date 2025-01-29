import socket
import threading
from datetime import datetime

clients = {}

def private_message(msg, sender, recipient):
    for client, name in clients.items():
        if name == recipient:
            try:
                client.send(msg.encode())
            except:
                client.close()
                del clients[client]

def broadcast(msg, sender):
    for client, name in clients.items():
        if client != sender:
            try:
                client.send(msg.encode())
            except:
                client.close()
                del clients[client]

def handle_client(client, addr):
    client.send("Enter your username: ".encode())
    username = client.recv(1024).decode().strip()
    clients[client] = username
    print(f"\033[92m{username} ({addr}) joined the chat.\033[0m")
    broadcast(f"\033[96m{username} joined the chat!\033[0m", client)

    while True:
        try:
            msg = client.recv(1024).decode().strip()
            if not msg:
                break
            timestamp = datetime.now().strftime("%H:%M:%S")

            if msg.startswith("@"):  
                parts = msg.split(" ", 1)
                if len(parts) < 2:
                    client.send("\033[91mInvalid private message format.\033[0m".encode())
                    continue
                recipient_name = parts[0][1:]  
                private_msg = f"\033[93m(Private) [{timestamp}] {username}:\033[0m {parts[1]}"
                if recipient_name in clients.values():
                    private_message(private_msg, client, recipient_name)
                    client.send(private_msg.encode())  
                else:
                    client.send(f"\033[91mUser '{recipient_name}' not found.\033[0m".encode())
            else:  
                formatted_msg = f"\033[94m[{timestamp}] {username}:\033[0m {msg}"
                print(formatted_msg)
                broadcast(formatted_msg, client)
        except:
            break

    print(f"\033[91m{username} left the chat.\033[0m")
    broadcast(f"\033[91m{username} left the chat.\033[0m", client)
    del clients[client]
    client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 12345))
server.listen(10)

print("\033[93m Server is running...\033[0m")

while True:
    client, addr = server.accept()
    threading.Thread(target=handle_client, args=(client, addr)).start()
