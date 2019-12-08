import socket
import threading
import logging
import time
import random

SERVER_ADDRESS = ("127.0.0.1", 4261)


LIST_OF_MESSAGES = ["hey", "heloo", "wasap", "hi", "heyo"]


def main():
    s1 = socket.socket()
    s1.connect(SERVER_ADDRESS)
    print("conected")
    c = input()
    if c == "s":
        s1.send(("01000" + LIST_OF_MESSAGES[random.randint(0, 4)]).encode())
        print("sent")
    if c == "r":
        print("reciving")
        data = s1.recv(1024)
        print("got it")
        print(data.decode())
    input()
    s1.close()


if __name__ == '__main__':
    main()
