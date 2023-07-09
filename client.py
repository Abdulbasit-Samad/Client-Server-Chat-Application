import win32pipe
import win32file
import tkinter as tk
import utilities
import socket
import threading

def exit_chat():
       server.close()
       chat_window.destroy()

def receive_messages():
            # Receive message from server
            while True:
                server_msg = server.recv(1024).decode("utf-8")
                output_box.insert(tk.END, f"From Server : {server_msg}\n")
         
            #server_socket.close()

def send_messages():
            # Send message to server
            client_msg = input_box.get()
            server.send(client_msg.encode("utf-8"))
            #server_socket.close()


def get_input():
    value1 = input_field1.get()
    value2 = input_field2.get()
    if value1 == ip and value2 == port:
        window.destroy()
    else:
        utilities.showerror('Error', 'Invalid IP Address or Port')

# open the named pipe for reading
pipe_name = r'\\.\pipe\myfifo'
pipe = win32file.CreateFile(
    pipe_name,
    win32file.GENERIC_READ,
    0, None,
    win32file.OPEN_EXISTING,
    0, None
)

# read two values from the named pipe
ip = win32file.ReadFile(pipe, 65536)[1].decode()
port = win32file.ReadFile(pipe, 65536)[1].decode()

window = tk.Tk()
window.geometry("400x200")

window.title('Server Connectivity')


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
server.connect((ip, int(port)))

print("Connected to server")

# Create chat window
chat_window = tk.Tk()
chat_window.title("Client Chat Box")



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