import bcrypt
import pickle


def hash_value(value: int | str) -> str:
    """
    Hashes an integer or string value using bcrypt with a stored salt.
    Used to derive deterministic wallet IDs from user IDs.
    Returns the hashed string.
    """
    with open("data.bin", "rb") as f:
        salt = pickle.load(f)
    encoded = str(value).encode("utf-8")
    return bcrypt.hashpw(encoded, salt).decode("utf-8")
