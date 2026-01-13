import sqlite3
from pathlib import Path

DB_PATH = Path("todo.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            is_done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


def main():
    init_db()
    print("Database initialized successfully.")


if __name__ == "__main__":
    main()
