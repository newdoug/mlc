"""Job classes, functions, and utilities"""

from dataclasses import dataclass
from socketserver import TCPServer, UDPServer


@dataclass
class SimpleJob:
    """Job with simple input and output. "Simple" as in "static", no complex
    state or connections required. More complex job management may be
    implemented and supported in the future.
    """

    name: str

    def run(self, settings: dict) -> dict:
        """Run the job"""
        if settings:
            raise NotImplementedError("No job implementation")
        return {}


class JobReceiver:
    def __init__(self, port: int, proto: str = "TCP"):
        self.port = port
        self.proto = proto.strip().upper()
        if self.proto == "TCP":
            self.server = TCPServer(port)
        elif self.proto == "UDP":
            self.server = UDPServer(port)
        else:
            raise ValueError(f"Invalid proto '{self.proto}'")

    def _recv(self):
        pass

    def receive_raw(self) -> bytes:
        pass

    def receive_settings(self) -> dict:
        """Receive message"""
