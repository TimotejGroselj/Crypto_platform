import random
import re
import sqlite3
import string

from crypto_utils import hash_value


class AuthManager:
    """Handles user registration, login validation, and password utilities."""

    def __init__(self):
        self.conn = sqlite3.connect("cryptodata.sqlite")
        self.cur = self.conn.cursor()

    def is_registered(self, email: str) -> bool:
        """Returns True if a user with the given email exists in the database."""
        return self.cur.execute(
            "SELECT username FROM users WHERE email = ?", (email,)
        ).fetchone() is not None

    def is_valid_email(self, email: str) -> bool:
        """Returns True if the email matches a basic valid format."""
        return bool(re.fullmatch(r".+@.+\..+", email))

    def validate_password(self, password: str) -> str | None:
        """
        Checks password strength (≥2 lowercase, ≥2 uppercase, ≥2 digits).
        Returns the name of the first failing requirement, or None if valid.
        """
        counts = {"lowercase": 0, "uppercase": 0, "digit": 0}
        for ch in password:
            if ch.islower():
                counts["lowercase"] += 1
            elif ch.isupper():
                counts["uppercase"] += 1
            elif ch.isdigit():
                counts["digit"] += 1
        for requirement, count in counts.items():
            if count < 2:
                return requirement
        return None

    def check_password(self, email: str, password: str) -> bool:
        """Returns True if the password matches the stored hash for the given email."""
        stored_hash = self.cur.execute(
            "SELECT password FROM users WHERE email = ?", (email,)
        ).fetchone()[0]
        return hash_value(password) == stored_hash

    def generate_password(self) -> str:
        """Generates a random password that satisfies the strength requirements."""
        password = ""
        while self.validate_password(password) is not None:
            password = "".join(
                random.choice(string.ascii_letters) + random.choice(string.digits)
                for _ in range(5)
            )
        return password

    def create_user(self, username: str, email: str, password: str) -> None:
        """Inserts a new user record with a hashed password."""
        with self.conn:
            self.cur.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, hash_value(password)),
            )

    def close(self) -> None:
        self.cur.close()
        self.conn.close()
