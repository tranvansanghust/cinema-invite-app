def parse_string_to_array(string: str) -> []:
    """
    Parses a semicolon-separated string into an array
    """
    if not string:
        return []
    return string.split(";")