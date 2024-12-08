from msfabricutils.common.quote_identifier import quote_identifier


def build_merge_predicate(columns: list[str]) -> str:
    """
    Constructs a SQL merge predicate based on the provided column names.

    This function generates a string that represents the condition for merging
    records based on equality of the specified columns.

    Args:
        columns (list[str]): A list of column names to be used in the merge predicate.

    Returns:
        A SQL string representing the merge predicate.

    Example:
        ```python
        predicate = build_merge_predicate(['id', 'name'])
        print(predicate)
        \"\"\"
            (target."id" = source."id") AND (target."name" = source."name")
        \"\"\"
        ```
    """
    merge_predicate = [
        f"""
            (target.{quote_identifier(column)} = source.{quote_identifier(column)})
        """
        for column in columns
    ]
    return " AND ".join(merge_predicate)


def build_when_matched_update_predicate(columns: list[str]) -> str:
    """
    Constructs a SQL predicate for when matched update conditions.

    This function generates a string that represents the conditions for updating
    records when a match is found based on the specified columns.

    Args:
        columns (list[str]): A list of column names to be used in the update predicate.

    Returns:
        A SQL string representing the when matched update predicate.

    Example:
        ```python
        update_predicate = build_when_matched_update_predicate(['id', 'status'])
        print(update_predicate)
        \"\"\"
            (
                (target."id" != source."id")
                OR (target."id" IS NULL AND source."id" IS NOT NULL)
                OR (target."id" IS NOT NULL AND source."id" IS NULL)
            ) OR ...
        \"\"\"
        ```
    """
    when_matched_update_predicates = [
        f"""
            (
                (target.{quote_identifier(column)} != source.{quote_identifier(column)})
                OR (target.{quote_identifier(column)} IS NULL AND source.{quote_identifier(column)} IS NOT NULL)
                OR (target.{quote_identifier(column)} IS NOT NULL AND source.{quote_identifier(column)} IS NULL)
            )
        """
        for column in columns
    ]
    return " OR ".join(when_matched_update_predicates)


def build_when_matched_update_columns(columns: list[str]) -> dict[str, str]:
    """
    Constructs a mapping of columns to be updated when a match is found.

    This function generates a dictionary where the keys are the target column
    names and the values are the corresponding source column names.

    Args:
        columns (list[str]): A list of column names to be used in the update mapping.

    Returns:
        A dictionary mapping target columns to source columns.

    Example:
        ```python
        update_columns = build_when_matched_update_columns(['id', 'name'])
        print(update_columns)
        {
            'target."id"': 'source."id"',
            'target."name"': 'source."name"'
        }
        ```
    """
    return {
        f"target.{quote_identifier(column)}": f"source.{quote_identifier(column)}"
        for column in columns
    }
