import os


def rand_bytes(num_bytes: int) -> bytes:
    """Generate `num_bytes` random bytes"""
    return os.urandom(num_bytes)
