"""
The room object
"""
import threading


class Room(object):
    """
    the rooms that the users study in. Contains a whiteboard.
    """
    _room_id = 0

    def __init__(self):
        Room._room_id += 1
        self._room_id = Room._room_id
        self._users = {}
        self.whiteboard = None
        self._room_id_lock = threading.Lock()
        self._users_lock = threading.Lock()

    @property
    def room_id(self):
        """
        returns the room id
        :return:
        """
        with self._room_id_lock:
            return self._room_id

    def set_room_id(self, room_id_):
        """
        Sets the room id
        :param room_id_:
        :return:
        """

        with self._room_id_lock:
            self._room_id = room_id_
            print("this is the room id, i just changed it", self._room_id)

    def get_copy_of_users(self):
        """
        Copies the users in the room to release the lock
        :return:
        """
        with self._users_lock:
            return list(self._users.values())[:]

    def add_user(self, user):
        """
        adds a user to the room
        :param user:
        :return:
        """
        with self._users_lock:
            self._users[user.get_username()] = user
        user.set_room_id(self._room_id)

    def remove_user(self, username):
        """
        removes a user from a room
        :param username:
        :return:
        """
        with self._users_lock:
            self._users.pop(username)

    def add_message(self, message):
        """
        adds a message to the room chat
        :param message:
        :return:
        """
        with self._users_lock:
            for user in self._users.values():
                user.send_message(f"07{message}".encode())

    def print_users(self):
        """
        prints the users that are in the room, mainly used for debugging
        :return:
        """
        print("printing the users")
        with self._users_lock:
            for user in self._users.keys():
                print(user)
