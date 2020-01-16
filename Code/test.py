import socket
import threading
import logging
import time
import random

SERVER_ADDRESS = ("127.0.0.1", 4261)


LIST_OF_NAMES = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                 "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
                 "W", "X", "Y", "Z"]


def send_message(sock, msg):
    sock.sendall(str(len(msg)).encode() + b"-" + msg)


def receive_message(s):
    length = ""
    total_recv = 0
    message = ""
    data = s.recv(1).decode()
    while data != "-":
        length += data
        data = s.recv(1).decode()
    length = int(length)
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
    name = LIST_OF_NAMES[random.randint(1, len(LIST_OF_NAMES)-1)]
    send_message(s1, b"00" + name.encode())

    msg = receive_message(s1)
    print("Online dudes: " + msg)
    c = input("Enter command: ")
    while not c == "e":
        if c == "ul":
            send_message(s1, b"02")
            data = receive_message(s1)
            print("The user list: " + data)
        if c == "r":
            print("reciving")
            data = s1.recv(1024)
            print("got it")
            print(data.decode())
        c = input("Enter command: ")

    input()
    s1.close()


if __name__ == '__main__':
    main()
