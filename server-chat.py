#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import random
keys = []

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        #client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        key = client.recv(BUFSIZ).decode("utf8")
        global keys
        keys.append(key)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def distributekeys(clients):    
    i = 1
    for client in clients:
        aux = "exchangekeys" + keys[i]
        client.send(bytes(aux, encoding="utf8"))
        i -=1
    return

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = str(random.randint(1, 10000))
    #welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    #client.send(bytes(welcome, "utf8"))
    #msg = "%s has joined the chat!" % name
    #broadcast(bytes(msg, "utf8"))
    clients[client] = name
        
    if len(clients) == 2:
        distributekeys(clients)
    
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg)
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(msg)
        
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()