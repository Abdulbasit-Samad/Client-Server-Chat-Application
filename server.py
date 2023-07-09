import tkinter as tk
import win32pipe
import win32file
import utilities
import socket
import threading
ip = ""
port = ""

def exit_chat():
       client.close()
       chat_window.destroy()
def receive_messages():
        
            # Receive message from client
            while True:
                client_msg = client.recv(1024).decode("utf-8")
            
                output_box.insert(tk.END, f"From Client : {client_msg}\n")

            #client_socket.close()

def send_messages():
            # Send message to client
            server_msg = input_box.get()
            client.send(server_msg.encode("utf-8"))
            input_box.delete(0, tk.END)

            #client_socket.close()
def get_input():
    global ip, port
    value1 = input_field1.get()
    value2 = input_field2.get()
    if utilities.validate_input(value1, value2):
        ip = value1
        port = value2
        win32pipe.ConnectNamedPipe(pipe, None)
        win32file.WriteFile(pipe, str(value1).encode())
        win32file.WriteFile(pipe, str(value2).encode())
        window.destroy()
    else:
        utilities.showerror('Error', 'Invalid IP Address or Port')


 
pipe_name = r'\\.\pipe\myfifo'
pipe = win32pipe.CreateNamedPipe(
           pipe_name,
           win32pipe.PIPE_ACCESS_DUPLEX,
           win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,
           1, 65536, 65536, 0, None        )

window = tk.Tk()
window.geometry("400x200")

window.title('Client Connectivity')


input_frame = tk.Frame(window)
input_frame.pack()


label1 = tk.Label(input_frame, text="Enter IP Address:")
label1.grid(row=0, column=0, padx=5, pady=5)
input_field1 = tk.Entry(input_frame)
input_field1.grid(row=0, column=1, padx=5, pady=5)


label2 = tk.Label(input_frame, text="Enter Port No:")
label2.grid(row=1, column=0, padx=5, pady=5)
input_field2 = tk.Entry(input_frame)
input_field2.grid(row=1, column=1, padx=5, pady=5)


button = tk.Button(window, text="Submit", command=get_input)
button.pack(pady=10)


window.mainloop()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, int(port)))
server.listen(5)

print("Waiting for connections...")

client, address = server.accept()

print(f"Connection established - {address[0]}:{address[1]}")
# Create chat window
chat_window = tk.Tk()
chat_window.title("Server Chat Box")

# Create input box
input_box = tk.Entry(chat_window)
input_box.pack()


# Create output box
output_box = tk.Text(chat_window, height=10, width=50)
output_box.pack()

# Create send button
send_button = tk.Button(chat_window, text="Send", command=send_messages, width=20)
send_button.pack()

exit_button = tk.Button(chat_window, text="Exit", command=exit_chat, width=20)
exit_button.pack()

# Start threads to receive and send messages
t1 = threading.Thread(target=receive_messages)
t2 = threading.Thread(target=send_messages)
t1.start()
t2.start()

# Run the chat window
chat_window.mainloop()





