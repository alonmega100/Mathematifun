import threading


class Room(object):
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
        with self._room_id_lock:
            return self._room_id

    def get_copy_of_users(self):
        with self._users_lock:
            return list(self._users.values())[:]

    def add_user(self, user):
        with self._users_lock:
            self._users[user.get_username()] = user
        user.set_room_id(self._room_id)

    def remove_user(self, username):
        with self._users_lock:
            self._users.pop(username)

    def print_users(self):
        print("printing the users")
        with self._users_lock:
            for user in self._users.keys():
                print(user)
