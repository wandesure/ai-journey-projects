"""
SQLite database backend for user authentication.
Persists user credentials so password changes survive app restarts.
"""

import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).parent / "users.db"


def get_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database schema."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def db_exists():
    """Check if database file exists and has users."""
    if not DB_PATH.exists():
        return False
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


def seed_from_secrets(secrets_credentials):
    """
    Seed database from Streamlit secrets on first run.
    Only runs if database is empty.
    """
    if db_exists():
        return

    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    usernames = secrets_credentials.get("usernames", {})
    for username, data in usernames.items():
        cursor.execute(
            "INSERT OR REPLACE INTO users (username, email, name, password) VALUES (?, ?, ?, ?)",
            (username, data["email"], data["name"], data["password"])
        )

    conn.commit()
    conn.close()


def get_all_users():
    """
    Get all users in format compatible with streamlit-authenticator.
    Returns dict: {"usernames": {username: {email, name, password}, ...}}
    """
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, email, name, password FROM users")
    rows = cursor.fetchall()
    conn.close()

    usernames = {}
    for row in rows:
        usernames[row["username"]] = {
            "email": row["email"],
            "name": row["name"],
            "password": row["password"]
        }

    return {"usernames": usernames}


def update_password(username, hashed_password):
    """Update a user's password hash."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        (hashed_password, username)
    )
    conn.commit()
    conn.close()


def get_user(username):
    """Get a single user by username."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, email, name, password FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "username": row["username"],
            "email": row["email"],
            "name": row["name"],
            "password": row["password"]
        }
    return None


def add_user(username, email, name, hashed_password):
    """Add a new user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, name, password) VALUES (?, ?, ?, ?)",
        (username, email, name, hashed_password)
    )
    conn.commit()
    conn.close()
