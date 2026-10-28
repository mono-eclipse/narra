import pyodbc
import os

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)


SERVER = os.getenv("NARRA_DB_SERVER", "localhost")
DATABASE = os.getenv("NARRA_DB_NAME", "NarraDB")
DRIVER = os.getenv(
    "NARRA_ODBC_DRIVER",
    "ODBC Driver 18 for SQL Server"
)


def odbc_value(value: str) -> str:
    """Безопасно оформляет значение для строки подключения ODBC."""
    return "{" + value.replace("}", "}}") + "}"


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Вход — Мои проекты")
        self.setFixedWidth(380)

        self.connection = None
        self.login_name = None
        self.database_user = None

        layout = QVBoxLayout(self)

        title = QLabel("Мои проекты")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold; padding: 8px;"
        )
        layout.addWidget(title)

        layout.addWidget(QLabel("Логин SQL Server"))

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Например, content_viewer")
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Пароль"))

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )
        self.password_input.returnPressed.connect(self.login)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(
                self,
                "Вход",
                "Введите логин и пароль.",
            )
            return

        connection_string = (
            f"DRIVER={{{DRIVER}}};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
            "Connection Timeout=5;"
            f"UID={odbc_value(username)};"
            f"PWD={odbc_value(password)};"
        )

        self.login_button.setEnabled(False)

        try:
            connection = pyodbc.connect(
                connection_string,
                timeout=5,
            )

            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    DB_NAME(),
                    SUSER_SNAME(),
                    USER_NAME(),
                    IS_MEMBER('db_datareader'),
                    IS_MEMBER('db_datawriter'),
                    IS_MEMBER('db_owner')
            """)

            row = cursor.fetchone()

            self.connection = connection
            self.login_name = row[1]
            self.database_user = row[2]

            QMessageBox.information(
                self,
                "Вход выполнен",
                f"База данных: {row[0]}\n"
                f"Вход SQL Server: {row[1]}\n"
                f"Пользователь базы: {row[2]}\n\n"
                f"Чтение (db_datareader): {row[3]}\n"
                f"Запись (db_datawriter): {row[4]}\n"
                f"Администратор (db_owner): {row[5]}",
            )

            self.password_input.clear()
            self.accept()

        except pyodbc.Error as error:
            print("\n=== ОШИБКА ПОДКЛЮЧЕНИЯ SQL SERVER ===")
            print(repr(error))
            print("====================================\n")

            QMessageBox.warning(
                self,
                "Ошибка входа",
                "Не удалось подключиться к SQL Server.\n\n"
                "Подробности смотри в консоли PyCharm.",
            )

        finally:
            self.login_button.setEnabled(True)

    def closeEvent(self, event):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

        event.accept()