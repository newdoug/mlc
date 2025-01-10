#!/usr/bin/env python3
"""TODO"""

import argparse
import ctypes as ct
from enum import auto, IntEnum
import socket
import sys
from typing import List

from job import JobInfoHeader


def _read_all_from_client_chunks(connection) -> Iterable[bytes]:
    header = b""
    while len(header) != ct.sizeof(JobInfoHeader):
        header += connection.recv(ct.sizeof(JobInfoHeader) - len(header))

    if header.magic != JOB_INFO_MAGIC_NUM:
        raise ValueError(f"Got bad magic number in job info header "
                         f"'0x{hex(header.magic)}'")
    num_to_read = header.num_bytes
    if num_to_read > MAX_JOB_SIZE_BYTES:
        raise ValueError(f"Job on socket tried to read/send '{num_to_read}' "
                         f"bytes")

    while num_to_read > 0:
        data = connection.recv(num_to_read)
        if not data:
            break
        yield data
        num_to_read -= len(data)


def _read_all_from_client(connection) -> bytes:
    return b"".join(_read_all_from_client_chunks(connection))


def _run_server(port: int, host: str = "0.0.0.0"):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, port))
            sock.listen()
            conn, addr = sock.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)


def _client():
    # TODO: Unused, just keeping around for reference for when I need to use it

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"Hello, world")
        data = s.recv(1024)

    print(f"Received {data!r}")


def main(args: List[str]) -> int:
    """main returns exit code"""
    parser = argparse.ArgumentParser(
        description="Start some job worker(s)")
    parser.add_argument(
        "-p", "--tcp-ports",
        help="Port(s) for the worker to listen for jobs on",
        type=int,
        nargs="+")
    # parser.add_arguments(
    parsed_args = parser.parse_args(args)

    servers = []
    for port in parsed_args.ports:
        if port not in range(1, 0xFFFF + 1):
            print(f"Input port '{port}' must be in range [1, 65535]",
                  file=sys.stderr)
            return 1

    for port in parsed_args.ports:

    # TODO

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
