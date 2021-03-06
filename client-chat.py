#!/usr/bin/env python3

"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import blowfish
import os
import random

sharedPrime = 167
sharedBase = 40
secret = random.randint(1000, 30000)
public_key = 0
cipher = 0
iv = b'\x84E\xd0\xd1Kv\x13b'
pub_key = (sharedBase**secret) % sharedPrime

def sendkey():
    global pub_key
    client_socket.send(bytes(str(pub_key), encoding="utf8"))
    print("Public key: ", pub_key)
    return

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            global cipher
            if cipher == 0:
                msg = client_socket.recv(BUFSIZ).decode("utf8")
                print(msg)
                if "exchangekeys" in msg:
                    print("Scret number: ", secret)
                    pub_key2 = ''.join(c for c in msg if c.isdigit())
                    print("Received Key: ", pub_key2)
                    shared_secret = (int(pub_key2)**secret) % sharedPrime
                    print("shared secret: ", shared_secret)
                    key = shared_secret.to_bytes(4, byteorder='big')
                    print(key)
                    cipher = blowfish.Cipher(key)
            else:
                msg = client_socket.recv(BUFSIZ)
                print("Mensagem encriptada: ", msg)
                msg = b"".join(cipher.decrypt_cfb(msg, iv))
                print("Mensagem desencriptada: ", msg)
                msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break

def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    if msg == "{quit}":
        client_socket.close()
        top.quit()
    msg = b"".join(cipher.encrypt_cfb(bytes(msg, encoding="utf8"), iv))
    print("Mensagem enviada: ", msg)
    my_msg.set("")  # Clears input field.
    client_socket.send(msg)

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

sendkey()

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.