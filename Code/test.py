import socket
import threading
import logging
import time
import random

SERVER_ADDRESS = ("127.0.0.1", 4261)


LIST_OF_MESSAGES = ["hey", "heloo", "wasap", "hi", "heyo"]

import message


def send_message(s, msg):
    length = str(len(msg))
    length_length = len(length)
    total_sent = 0
    print(length_length)
    while total_sent < length_length:
        s.send(length[total_sent:total_sent + 1].encode())
        total_sent += 1
    s.send(b'-')
    total_sent = 0
    print(msg)
    while total_sent < int(length):
        s.send(msg[total_sent:total_sent + 1].encode())
        total_sent += 1
    s.send(b'-')
    s.send(msg.encode())


def receive_message(s):
    length = 0
    total_recv = 0
    message = ""
    data = s.recv(1).decode()
    while not data == "-":
        length += int(data)
        data = s.recv(1).decode()
    while total_recv < length:
        data = s.recv(1).decode()
        message += data
        total_recv += 1
    return message


def main():
    s1 = socket.socket()
    s1.connect(SERVER_ADDRESS)
    print("conected")
    time.sleep(1)

    name = "Alon"
    send_message(s1, name)

    msg = receive_message(s1)
    print(msg)

    c = input()
    while not c == "e":
        if c == "ul":
            s1.send(("02000" + LIST_OF_MESSAGES[random.randint(0, 4)]).encode())
            data = s1.recv(1024)
            print("got it")
            print(data.decode())
        if c == "r":
            print("reciving")
            data = s1.recv(1024)
            print("got it")
            print(data.decode())
        c = input()

    input()
    s1.close()


if __name__ == '__main__':
    main()
