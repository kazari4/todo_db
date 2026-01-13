import argparse
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("todo.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
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


def add_task(title: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO tasks (title, is_done, created_at)
        VALUES (?, 0, ?)
        """,
        (title, datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()
    conn.close()
    print(f"Added task: {title}")


def list_tasks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, title, is_done, created_at
        FROM tasks
        ORDER BY id
        """
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No tasks found.")
        return

    for task_id, title, is_done, created_at in rows:
        status = "x" if is_done else " "
        print(f"[{status}] {task_id}: {title} ({created_at})")


def mark_done(task_id: int):
    conn = get_connection()
    cur = conn.cursor()

    # 存在チェック
    cur.execute(
        """
        SELECT id FROM tasks WHERE id = ?
        """,
        (task_id,),
    )
    row = cur.fetchone()

    if row is None:
        print(f"Task with id {task_id} not found.")
        conn.close()
        return

    # 完了に更新
    cur.execute(
        """
        UPDATE tasks
        SET is_done = 1
        WHERE id = ?
        """,
        (task_id,),
    )
    conn.commit()
    conn.close()
    print(f"Marked task {task_id} as done.")


def parse_args():
    parser = argparse.ArgumentParser(description="ToDo application")

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", nargs="?", help="Task title")

    subparsers.add_parser("list", help="List all tasks")

    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument("id", type=int, help="Task ID")

    return parser.parse_args()


def main():
    init_db()
    args = parse_args()

    if args.command == "add":
        title = args.title
        if not title:
            title = input("Enter task: ").strip()
        if not title:
            print("Task title cannot be empty.")
            return
        add_task(title)

    elif args.command == "list":
        list_tasks()

    elif args.command == "done":
        mark_done(args.id)


if __name__ == "__main__":
    main()
