import socket
import tkinter as tk
from tkinter import messagebox
import os
import pickle
import subprocess
import threading

# Connectivity setup initialization.
port = 8081
ip = '127.0.0.1'
s = socket.socket()

# Change frame on calling.
def raise_frame(frame):
    frame.tkraise()

# Connect to an open socket.
def connect(event, ip_entry, port_entry):
    global s, ip, port
    port = int(port_entry.get())
    ip = ip_entry.get()

    try:
        s.connect((ip, port))
        f2.tkraise()

        # Header and UI of the second frame.
        port_notify.config(text="Connected to " + ip + ":" + str(port))
        port_notify.config(width=500)

        # Receives the host name and whole shared directory in encoded form and then decode it.
        host = s.recv(1024)
        directory = s.recv(1024)

        try:
            directory = pickle.loads(directory)
            # Insert all the shared files in the listbox to show them.
            for item in directory[1]:
                text_list.insert(tk.END, item)

            # Create the header and UI for frame1 and frame2.
            hostname.config(text="Host: " + str(host))
            hostname.config(width=500)
            explore_from.config(text="Exploring files of " + str(host))
            explore_from.config(width=500)

        except EOFError:
            # Handle the EOFError here if needed
            pass

    except Exception as e:
        # If there is any error in the whole process return a message to the client and leave the socket from captured ip and port by calling disconnect.
        messagebox.showinfo("Status", "There is a network error. This can be because the network you want to join may not be open. Try another network")
        disconnect()


def disconnect():
    # Close the socket and return to the main frame.
    global s
    print("Disconnected")
    s.close()
    raise_frame(f1)  # Get back to the home page

# Create text box to insert the file you want to download.
def make_form():
    entries = {}
    ent = tk.Entry(f2)
    ent.insert(0, "0")
    ent.pack()
    ent.place(x=180, y=130)
    entries['handle'] = ent
    return entries

# Textbox to enter port.
def make_portbox():
    port_entry = tk.Entry(f1)
    port_entry.pack()
    port_entry.insert(0, port)
    port_entry.place(x=180, y=180)
    return port_entry

# Textbox to enter IP address.
def make_ipbox():
    ip_entry = tk.Entry(f1)
    ip_entry.pack()
    ip_entry.insert(0, ip)
    ip_entry.place(x=180, y=225)
    return ip_entry

# Function to create a hotspot.
def create_hotspot():
    ssid = "YourHotspotName"
    password = "YourPassword"

    # Stop existing services
    subprocess.call(['sudo', 'systemctl', 'stop', 'hostapd'])
    subprocess.call(['sudo', 'systemctl', 'stop', 'dnsmasq'])

    # Configure and start the hostapd service
    subprocess.call(['sudo', 'hostapd', '-B', '/etc/hostapd/hostapd.conf'])

    # Configure and start the dnsmasq service
    subprocess.call(['sudo', 'dnsmasq'])
# Function to connect to a Wi-Fi network.
def connect_wifi():
    pass

# Function to show available Wi-Fi networks.
def show_wifi():
    raise_frame(f4)
    print(wifi_list.get(tk.ACTIVE))
    del_wifi_list()
    all_wifi = subprocess.check_output(["nmcli", "-t", "-f", "SSID", "device", "wifi", "list"])

    all_wifi = all_wifi.decode("ascii")
    all_wifi = all_wifi.replace("\r", "")
    wifi_list_data = all_wifi.split("\n")
    wifi_list_data = wifi_list_data[4:]
    for item in wifi_list_data:
        act = item.split(":")
        if len(act) > 1:
            wifi_list.insert(tk.END, act[1])

def del_wifi_list():
    cs = wifi_list.size()
    if cs > 0:
        wifi_list.delete(0, tk.END)

# Function to download any file.
def download(entries):
    global s
    filename = entries['handle'].get()
    s = socket.socket()
    try:
        s.connect((ip, port))
        host = s.recv(1024)
        if filename != 'q':
            s.send(('www/' + filename).encode())
            data = s.recv(1024)
            print(data)
            if data == b'File Exists':
                data = s.recv(1024)
                filesize = int(data)
                f = open('downloaded/' + filename, 'wb')
                data = s.recv(1024)
                total_recv = len(data)
                f.write(data)
                print("Receiving data...")
                while total_recv < filesize:
                    data = s.recv(1024)
                    total_recv += len(data)
                    f.write(data)
                    print("Receiving...")
                messagebox.showinfo("Download", "Download successfully completed")
            else:
                messagebox.showinfo("Download", "File does not exist. Try another file.")
    except Exception as e:
        print("Some error occurred, please try again:", str(e))
    finally:
        s.close()


# Startfile("server.py")  # On starting a client GUI your server already starts

# Set up root geometry
root = tk.Tk()
root.geometry("500x500")
root.title("HubPort")

# Define frames
f1 = tk.Frame(root, bg="black", height="500", width="500")
f2 = tk.Frame(root, bg="black", height="500", width="500")
f3 = tk.Frame(root, bg="black", height="500", width="500")
f4 = tk.Frame(root, bg="black", height="500", width="500")

# Position frames
for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')

title = tk.Message(f1, text="WELCOME TO HUBPORT")
title.config(font=('times', 24, 'italic'), width=500, bg="black", fg="white")
port_entry = make_portbox()
ip_entry = make_ipbox()

# This is a button which is used to connect to the server taking the value of IP and port from the text box. It calls connect method with IP and port as argument.
port_button = tk.Button(f1, text="Connect", command=lambda: connect(event=None, ip_entry=ip_entry, port_entry=port_entry))
port_button.pack()
port_button.place(x=210, y=260)

title.pack()
title.place(x=40, y=10)

raise_frame(f1)

port_notify = tk.Message(f2)
port_notify.config(font=('times', 24, 'italic'), fg="white", bg="black")
port_notify.pack()

hostname = tk.Message(f2)
hostname.config(font=('times', 20, 'italic'), fg="white", bg="black")
hostname.pack()

disconnect_button = tk.Button(f2, text="Disconnect", command=disconnect)
disconnect_button.pack()
disconnect_button.place(x=210, y=220)

entries = make_form()
download_button = tk.Button(f2, text="Download", command=lambda: download(entries))
download_button.pack()
download_button.place(x=180, y=158)

explore_button = tk.Button(f2, text="Explore Files", command=lambda: raise_frame(f3))
explore_button.pack()
explore_button.place(x=210, y=325)

explore_from = tk.Message(f3)
explore_from.config(font=('times', 24, 'italic'), fg="white", bg="black")
explore_from.pack()

text_list = tk.Listbox(f3)
text_list.pack()
text_list.place(x=35, y=100)

text_show = tk.Message(f3)
text_show.config(font=('times', 13, 'italic'), fg="white", bg="black")
text_show.config(text="Documents")
text_show.config(width=500)
text_show.pack()
text_show.place(x=20, y=50)

create_button = tk.Button(f1, text="Create", command=create_hotspot)
create_button.pack()
create_button.place(x=180, y=360)

join_button = tk.Button(f1, text="Join", command=show_wifi)
join_button.pack()
join_button.place(x=240, y=360)

wifi_list = tk.Listbox(f4)
wifi_list.pack()
wifi_list.place(x=35, y=100)

refresh_button = tk.Button(f4, text="Refresh", command=show_wifi)
refresh_button.pack()
refresh_button.place(x=250, y=100)

connect_button = tk.Button(f4, text="Connect", command=connect_wifi)
connect_button.pack()
connect_button.place(x=250, y=150)

root.mainloop()
