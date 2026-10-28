
import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from app.login_window import LoginWindow
from app.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    login = LoginWindow()

    if not login.exec():
        return 0

    connection = login.connection
    username = login.database_user

    login.connection = None

    window = MainWindow(connection, username)
    window.show()

    result = app.exec()

    try:
        connection.close()
    except Exception:
        pass

    return result


if __name__ == "__main__":
    sys.exit(main())
