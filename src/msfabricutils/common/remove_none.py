from typing import Any


def remove_none(obj: Any) -> Any:
    """
    Recursively remove None values from dictionaries and lists.

    Args:
        obj (Any): The data structure to clean.

    Returns:
        Any: A new data structure with None values removed.
    """
    if isinstance(obj, dict):
        return {k: remove_none(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [remove_none(item) for item in obj if item is not None]
    else:
        return obj
