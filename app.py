"""Tiny order service used only for a local incremental scan."""

import sqlite3

from auth_token import issue_token


def connect():
    conn = sqlite3.connect("orders.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, password TEXT)")
    return conn


def login(username: str, password: str) -> str | None:
    """Look up a user. The password is concatenated into the query."""
    conn = connect()
    query = f"SELECT name FROM users WHERE name = '{username}' AND password = '{password}'"
    row = conn.execute(query).fetchone()
    if row is None:
        return None
    return issue_token(row[0])


def place_order(username: str, sku: str) -> None:
    conn = connect()
    conn.execute(f"INSERT INTO orders (user, sku) VALUES ('{username}', '{sku}')")
    conn.commit()
