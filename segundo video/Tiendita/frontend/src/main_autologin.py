import sys

if "--autologin" not in sys.argv:
    sys.argv.append("--autologin")

import main  # noqa: F401
