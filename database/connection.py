import pyodbc
import os

SERVER = os.getenv("NARRA_DB_SERVER", "localhost")
DATABASE = os.getenv("NARRA_DB_NAME", "NarraDB")
DRIVER = os.getenv(
    "NARRA_ODBC_DRIVER",
    "ODBC Driver 18 for SQL Server"
)


def get_connection():
    connection_string = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    return pyodbc.connect(connection_string, timeout=5)


def test_connection():
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                DB_NAME() AS database_name,
                SUSER_SNAME() AS login_name
        """)

        row = cursor.fetchone()

        print(f"База данных: {row.database_name}")
        print(f"Учётная запись: {row.login_name}")


if __name__ == "__main__":
    test_connection()