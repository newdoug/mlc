#!/usr/bin/env python3
"""TODO"""

import argparse
import sys
from typing import List


def main(args: List[str]) -> int:
    """main returns exit code"""
    parser = argparse.ArgumentParser(
        description="TODO")
    parsed_args = parser.parse_args(args)
    # TODO

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
