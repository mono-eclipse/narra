from database.connection import get_connection


def inspect_database():
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT TABLE_SCHEMA, TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)

        tables = cursor.fetchall()

        for schema, table in tables:
            print(f"\n{'=' * 50}")
            print(f"Таблица: {schema}.{table}")

            cursor.execute("""
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = ?
                  AND TABLE_NAME = ?
                ORDER BY ORDINAL_POSITION
            """, schema, table)

            for column in cursor.fetchall():
                print(
                    f"  {column.COLUMN_NAME}: "
                    f"{column.DATA_TYPE}, "
                    f"NULL={column.IS_NULLABLE}"
                )


if __name__ == "__main__":
    inspect_database()