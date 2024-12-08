import re

from msfabricutils.etl.helpers.merge_helpers import (
    build_merge_predicate,
    build_when_matched_update_columns,
    build_when_matched_update_predicate,
)


def test_build_merge_predicate():
    columns = ["column1", "column2"]
    expected_output = """
        (target."column1" = source."column1") 
        AND 
        (target."column2" = source."column2")
    """

    actual_output = build_merge_predicate(columns)
    assert re.sub(r"\s+", " ", actual_output.strip()) == re.sub(
        r"\s+", " ", expected_output.strip()
    )


def test_build_when_matched_update_predicate():
    column_names = ["column1", "column2", "column3"]
    expected_output = """
        (
            (target."column1" != source."column1")
            OR (target."column1" IS NULL AND source."column1" IS NOT NULL)
            OR (target."column1" IS NOT NULL AND source."column1" IS NULL)
        )
         OR 
        (
            (target."column2" != source."column2")
            OR (target."column2" IS NULL AND source."column2" IS NOT NULL)
            OR (target."column2" IS NOT NULL AND source."column2" IS NULL)
        )
         OR 
        (
            (target."column3" != source."column3")
            OR (target."column3" IS NULL AND source."column3" IS NOT NULL)
            OR (target."column3" IS NOT NULL AND source."column3" IS NULL)
        )
    """

    actual_output = build_when_matched_update_predicate(column_names)
    assert re.sub(r"\s+", " ", actual_output.strip()) == re.sub(
        r"\s+", " ", expected_output.strip()
    )


def test_build_when_matched_update_columns():
    column_names = ["column1", "column2", "column3"]
    expected_output = {
        'target."column1"': 'source."column1"',
        'target."column2"': 'source."column2"',
        'target."column3"': 'source."column3"',
    }

    actual_output = build_when_matched_update_columns(column_names)
    assert actual_output == expected_output
