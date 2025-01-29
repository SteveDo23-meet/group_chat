import socket 

HEADER = 64
PORT = 5050 
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "disconnected ! "
SERVER = "10.0.0.10"
ADDR = (SERVER , PORT)

client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
client.connect(ADDR)

def send_messages():
    while True:
        msg = input("Enter message: ")
        if msg.lower() == "quit":
            send(DISCONNECT_MESSAGE)
            break
        send(msg)

    
def send(msg):
    message = msg.encode(FORMAT)
    msg_lenght=  len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b' ' * (HEADER - len(send_lenght))
    client.send(send_lenght)
    client.send(message)
    print (client.recv(2048).decode(FORMAT))
    
send_messages()
send("MISSION COMPLETED")
send (DISCONNECT_MESSAGE) 
client.close()
