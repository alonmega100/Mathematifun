class User:
    number_id = 0

    def __init__(self, username, password):
        self.username = username
        self.user_id = User.number_id
        User.number_id += 1
        self.password = password
        self.message_list = []
        self.action_list = []

    def __str__(self):
        return f"{self.username} {self.user_id} {self.password}"

    def add_message(self, text, destination):
        self.message_list.insert("Text:" + str(text) + "Destination:" +
                                 str(destination))
