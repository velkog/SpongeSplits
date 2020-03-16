from asyncore import dispatcher
from socket import AF_INET, SOCK_STREAM

PORT = 16834  # TODO: move this into a config file


class LiveSplitSignal(dispatcher):
    def __init__(self):
        dispatcher.__init__(self)
        self.create_socket(AF_INET, SOCK_STREAM)
        self.connect(("localhost", PORT))

    def start(self):
        self.send(b"starttimer\r\n")

    def start_or_split(self):
        self.send(b"startorsplit\r\n")

    def split(self):
        self.send(b"split\r\n")
