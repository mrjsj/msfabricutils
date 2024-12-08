from msfabricutils.common.quote_identifier import quote_identifier


def test_quote_character():
    assert quote_identifier("my_object") == '"my_object"'
    assert quote_identifier("my_object", "'") == "'my_object'"
    assert quote_identifier('"my_object"') == '"my_object"'
    assert quote_identifier("'''my_object'''", "'") == "'my_object'"
    assert quote_identifier("") == '""' 

