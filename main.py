import sys
import os

# Make sure project root is on sys.path when run as a bundled exe
if getattr(sys, "frozen", False):
    sys.path.insert(0, os.path.dirname(sys.executable))
else:
    sys.path.insert(0, os.path.dirname(__file__))

from db.database import initialize_db
from ui.app import App


def main():
    initialize_db()
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
