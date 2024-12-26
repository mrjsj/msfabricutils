from typing import Any


def shorten_dict_values(obj: Any, max_length: int = 20) -> Any:
    """
    Recursively shorten string values in dictionaries and lists.
    Useful for printing out data structures in a readable format.

    Args:
        obj (Any): The data structure to shorten.
        max_length (int): The maximum length of string values to shorten.
    Returns:
        Any: A new data structure with string values shortened.
    """
    if isinstance(obj, dict):
        return {k: shorten_dict_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [shorten_dict_values(item) for item in obj]
    elif isinstance(obj, str):
        return obj[:max_length] + "... (truncated)" if len(obj) > max_length else obj
    else:
        return obj
