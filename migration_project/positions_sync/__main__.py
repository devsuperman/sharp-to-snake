"""``python -m positions_sync pings.csv`` -- real network client (given code)."""

import os
import sys

from course_support.urllib_client import UrllibClient
from positions_sync.cli import main

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:], os.environ, UrllibClient()))
