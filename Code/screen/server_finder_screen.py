"""
The screen where you decide to which server to connect
"""
__author__ = "Alon Malka"

from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import ObjectProperty


class ServerFinderScreen(Screen):
    """
    The screen where you decide to which server to connect
    """
    error_label = ObjectProperty()
    
    def _choose_server(self, ip, port):
        app = App.get_running_app()
        try:
            port = int(port)
        except ValueError:
            self.error_label.text = "Port must be a number"
        except Exception as e:
            self.error_label.text = str(e)
        else:
            self.error_label.text = "OK"
            app.server_ip = ip
            app.server_port = port
            self.manager.transition.direction = "right"
            app.root.current = "login"
