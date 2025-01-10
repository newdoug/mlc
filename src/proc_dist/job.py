#!/usr/bin/env python3

import ctypes as ct
from enum import auto, IntEnum
from typing import List


# Some arbitrary upper limit to try to prevent weird errors
MAX_JOB_SIZE_BYTES: int = 0xFFFFFF
# Randomly generated via `os.urandom(4).hex()`
JOB_INFO_MAGIC: int = 0x76788DCD


class JobMessageType(IntEnum):
    """Job message types"""
    REQUEST = auto()
    RESPONSE = auto()
    # QUERY = auto()  # Maybe later...getting more complicated than I wanted


class JobInfoHeader(ct.LittleEndianStructure):
    """Job information"""
    _pack_ = 1
    _fields_ = [
        ("magic", ct.c_uint32),
        ("job_id", ct.c_uint32),
        ("message_type", ct.c_uint16),
        ("num_bytes", ct.c_uint32),
    ]


class Job:
    def __init__(self, job_id: int, function_id: int, func_args: List):
        self.job_id = job_id
        self.function_id = function_Id
        self.func_args = func_args

    def package_results(self, results) -> bytes:
        # TODO: serialize results??
        serialized_results = bytes(results)
        return bytes(JobInfoHeader(
            JOB_INFO_MAGIC,
            self.job_id,
            JobMessageType.RESPONSE.value,
            len(serialized_results))) + serialized_results

    def run(self) -> bytes:
        func = _get_func_from_id(function_id)
        results = func(*self.func_args)
        return self.package_results(results)

