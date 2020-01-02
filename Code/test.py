import socket
import threading
import logging
import time
import random

SERVER_ADDRESS = ("127.0.0.1", 4261)


LIST_OF_MESSAGES = ["hey", "heloo", "wasap", "hi", "heyo"]


def send_message(s, msg):
    length = str(len(msg))
    length_length = str(len(length))

    total_sent = 0
    while total_sent < int(length_length):
        s.send(length[total_sent:total_sent + 1].encode())
        total_sent += 1
    s.send(b'-')
    total_sent = 0
    while total_sent < int(length):
        s.send(msg[total_sent:total_sent + 1].encode())
        total_sent += 1


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
    send_message(s1, "00" + name)

    msg = receive_message(s1)
    print("Online dudes: " + msg)

    c = input()
    while not c == "e":
        if c == "ul":
            send_message(s1, "02")
            data = receive_message(s1)
            print("got it")
            print("the data i got: " + data)
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
