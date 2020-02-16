import socket
import threading
import logging
import time
import random

SERVER_ADDRESS = ("127.0.0.1", 4261)

MESSAGE_LIST = []
INFORMATION = []

LIST_OF_NAMES = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                 "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
                 "W", "X", "Y", "Z"]


def send_message(sock, msg):
    sock.sendall(str(len(msg)).encode() + b"-" + msg)


def receive_message(sock):
    while True:
        length = ""
        total_got = 0
        msg = ""
        data = sock.recv(1).decode()
        while not data == "-":
            length += data
            data = sock.recv(1).decode()
        while total_got < int(length):
            data = sock.recv(1).decode()
            msg += data
            total_got += 1
        print(msg)


def check_for_updates():
    """
    Checks if there are any updates from the clients.
    :return: Nothing
    """
    while True:

        if len(MESSAGE_LIST) != 0:
            data = MESSAGE_LIST.pop()
            INFORMATION.append(data)


def print_information():
    while True:
        while len(INFORMATION) != 0:
            print(INFORMATION.pop())


def main():
    s1 = socket.socket()
    s1.connect(SERVER_ADDRESS)
    print("conected")

    name = LIST_OF_NAMES[random.randint(1, len(LIST_OF_NAMES)-1)]
    send_message(s1, b"00" + name.encode())
    listen_to_user_thread \
        = threading.Thread(target=receive_message, args=(s1,))
    listen_to_user_thread.start()
    """
    check_for_updates_thread \
        = threading.Thread(target=check_for_updates)
    check_for_updates_thread.start()
    print_information_thread \
        = threading.Thread(target=print_information)
    print_information_thread.start()
    """
    print("Your name is: "+ name)
    print("Enter command: ")
    c = input()
    while not c == "e":
        if c == "ul":
            send_message(s1, b"02")
            print("The user list: ")
        if c == "sm":
            name = input\
                ("Enter the name of the user you want to send a message to: ")
            text = input("Enter the message you want to send: ")
            message = (b"03" + name.encode() + b"#" + text.encode())
            send_message(s1, message)
        print("Enter command: ")
        c = input()


    input()
    s1.close()


if __name__ == '__main__':
    main()
