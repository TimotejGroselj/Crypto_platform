import bcrypt as by
import pickle
from pathlib import Path

def id_to_hash(id:int):
    """
    vzame id userja (int) in vrne encrypted hash
    """
    with open(f"data.bin", "rb") as data:
            salt = pickle.load(data)
    id = str(id).encode('utf-8')
    return by.hashpw(id,salt).decode('utf-8')
