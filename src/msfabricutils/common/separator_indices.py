def _separator_indices(string: str, separator: str) -> list[int]:
    """Find indices of a separator character in a string, ignoring separators inside quotes.

    Args:
        string (str): The input string to search through
        separator (str): The separator character to find

    Returns:
        A list of indices where the separator character appears outside of quotes

    Example:
        ```python
        separator_indices('a,b,"c,d",e', ',')
        [1, 8]
        ```
    """
    inside_double_quotes = False
    inside_single_quotes = False
    indices = []

    for idx, char in enumerate(string):
        if char == '"' and not inside_single_quotes:
            inside_double_quotes = not inside_double_quotes
        elif char == "'" and not inside_double_quotes:
            inside_single_quotes = not inside_single_quotes
        elif inside_double_quotes or inside_single_quotes:
            continue
        elif char == separator:
            indices.append(idx)

    return indices
