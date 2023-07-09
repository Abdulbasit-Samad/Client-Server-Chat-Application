import ipaddress
import tkinter as tk
from tkinter import messagebox
def showerror(title, msg):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, msg)
    root.destroy()
    root.mainloop()
# Create a Tkinter root window

def portno(port):
    check = True
    if int(port) <= 0 or int(port) > 65535:
        check = False
    return check
def validate_input(ip_address, port):
    try:
        ip_address_obj = ipaddress.ip_address(ip_address)
        return ip_address_obj.is_loopback and portno(port)
    except ValueError:
        return False