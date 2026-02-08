import tkinter as tk
import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 12345  # Port to listen on (non-privileged ports are > 1023)
#lock = threading.Lock()

connection = False # this will be a conn object later

def insert_message(message):
    global msg_log
    msg_log.insert(tk.END, message + "\n")

def send_message():
    msg = entry_input.get()
    print(msg)
    if connection:
        connection.send(msg.encode())
    insert_message("You: " + msg)
    entry_input.delete(0,tk.END)

def receive_messages():
    global connection
    try:
        with connection:
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                rcv_msg = data.decode()
                print("received:", rcv_msg)
                insert_message("RCV: " + rcv_msg)
    except Exception:
        print("You were forcibly disconnected. Trying to connect again...")
        insert_message("You were forcibly disconnected. Trying to connect again...")
        connection.close()
        connection = False

def run_client():
    global connection
    print("Starting Client.")
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # TCP
        #with socket.socket() as s:
            #s.bind(('', PORT)) # blank string for host means any on local network
            try:
                s.connect((HOST, PORT))
            except Exception:
                print("Error in connecting. Retrying.")
                connection = False
            else:
                print("System: Connected")
                connection = s
                insert_message("You are connected!")
                receive_messages()
        

root = tk.Tk()
root.title("Message Exchange")
root.geometry("500x450")

# row 0
lbl = tk.Label(root, text="Messages")
lbl.grid()

# row 1

msg_log = tk.Text(root, wrap=tk.CHAR, width=50, height=20)
msg_log.grid(column=0,row=1,sticky=tk.E)

scrollbar = tk.Scrollbar(root)
scrollbar.grid(column=0, row=1, sticky=tk.NS+tk.E)

msg_log.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = msg_log.yview)

# row 2
entry_input = tk.Entry(root,width=50)
entry_input.grid(column=0, row=2)

btn_send = tk.Button(root, text="Send", command=send_message)
btn_send.grid(column=1, row=2)
server = threading.Thread(target=run_client)
server.start()
root.mainloop()
