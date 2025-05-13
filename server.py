import socket 
import threading 
import glob
import os
import shutil
from PIL import ImageGrab

HEADER= 64
PORT = 5050 
SERVER = socket.gethostbyname(socket.gethostname())
print (SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "disconnected ! "
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False
                break

            print(f"[{addr}] {msg}")

            #DIR
            if msg.upper().startswith("DIR"):
                try:
                    _, folder_path = msg.split(" ", 1)
                    folder_path = folder_path.strip()
                    files_list = glob.glob(folder_path + "\\*.*")
                    response = "\n".join(files_list) if files_list else "No files found."
                except Exception as e:
                    response = f"Error: {e}"
            else:
                response = "Msg received"
            #COPY
            if msg.upper().startswith("COPY"):
                try:
                    _, src, dst = msg.split(" ", 2)
                    src = src.strip()
                    dst = dst.strip()

                    shutil.copy(src, dst)
                    response = f"File copied from {src} to {dst} successfully."
                except Exception as e:
                    response = f"Error: {e}"

            else:
                response = "Msg received"

            #SCREENSHOT
            if msg.upper().startswith("SS"):
                try:
                    screenshot = ImageGrab.grab()
                    screenshot.save("screenshot.png")
                    screenshot.close()
                except Exception as e:
                    response = f"Error: {e}"
            else:
                response = "Msg received"
            
            #
            

    conn.close()

def start():
    server.listen()
    print (f"[LISTINING] Server is listening on {SERVER}")
    while True:
        conn , addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn , addr))
        thread.start()
        print (f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print ("[STARTING]")
start()