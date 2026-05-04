def get_int_input(prompt: str, max_value: float = float("inf")) -> int:
    """
    Prompts the user for an integer between 1 and max_value (inclusive).
    Re-prompts on invalid input, and returns max_value if the user chooses to leave.
    """
    while True:
        raw = input(prompt)
        if raw.isdecimal() and 0 < int(raw) <= max_value:
            return int(raw)
        while True:
            raw = input("Invalid input!\n1. Try again\n2. Leave\n")
            if raw.isdecimal() and int(raw) == 1:
                break
            elif raw.isdecimal() and int(raw) == 2:
                return max_value


def _is_non_negative_float(value: str) -> bool:
    """Returns True if value can be parsed as a non-negative float."""
    try:
        return float(value) >= 0
    except ValueError:
        return False


def get_float_input(prompt: str, max_value: float = float("inf")) -> float:
    """
    Prompts the user for a non-negative float.
    Re-prompts on invalid input, and returns 0.0 if the user chooses to leave.
    """
    while True:
        raw = input(prompt)
        if _is_non_negative_float(raw):
            value = float(raw)
            if value <= max_value:
                return value
        while True:
            raw = input("Invalid input!\n1. Try again\n2. Leave\n")
            if raw.isdecimal() and int(raw) == 1:
                break
            elif raw.isdecimal() and int(raw) == 2:
                return 0.0
