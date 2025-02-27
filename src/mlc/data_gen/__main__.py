#!/usr/bin/env python3
"""Data (plaintext and ciphertext) generation script"""

import sys

from .main import main


sys.exit(main(sys.argv[1:]))
