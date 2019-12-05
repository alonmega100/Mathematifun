import socket
import threading
import logging
import time
import random

SERVER_ADDRESS = ("127.0.0.1", 4261)


LIST_OF_MESSAGES = ["hey", "heloo", "wasap", "hi", "heyo"]


def main():
    i = input()
    if i == "1":
        s1 = socket.socket()
        s1.connect(SERVER_ADDRESS)
        print("conected")
        print("reciving")
        data = s1.recv(1024)
        print("got it")
        print(data.decode())
        input()
        s1.close()
    if i == "2":
        s1 = socket.socket()
        s1.connect(SERVER_ADDRESS)
        print("conected")
        s1.send(b"01001Hey")
        print("sent")
        s1.close()


if __name__ == '__main__':
    main()
