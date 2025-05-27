#!/usr/bin/env python3
"""Generic actions management"""

import argparse
import sys
from typing import List


# TODO: jsonschema for action configs
ACTION_CONFIG_SCHEMA = "TODO"

ACTION_MANAGER_DESCRIPTION = f"""Action manager
Schema: {ACTION_CONFIG_SCHEMA}
"""


def _get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=ACTION_MANAGER_DESCRIPTION)
    parser.add_argument(
        "-r",
        "--run",
        help="Action config files (YAML) to run",
        metavar="CONFIG_FILE",
        nargs="+",
    )
    parser.add_argument(
        "-l",
        "--list",
        help="List available actions and information about each",
        action="store_true",
    )
    return parser


def main(args: List[str]) -> int:
    """Main returns exit code"""
    parser = _get_argparser()
    parsed_args = parser.parse_args(args)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
