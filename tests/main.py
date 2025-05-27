"""unittest main module"""

import sys
import unittest


def main() -> int:
    """unittest main runner"""
    # We're relying on auto-discovery. The `run.sh` script should be used to
    # ensure paths and organization is correct
    unittest.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())
