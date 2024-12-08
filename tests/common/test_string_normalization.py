from msfabricutils.common.string_normalization import character_translation, to_snake_case
from msfabricutils.etl import get_default_config


def test_to_snake_case():
    assert to_snake_case("CustomerID") == "customer_id"
    assert to_snake_case("IDNumber") == "id_number"
    assert to_snake_case("DebtorIDNumber") == "debtor_id_number"
    assert to_snake_case("HTMLLink") == "html_link"
    assert to_snake_case("ThisIsATest") == "this_is_a_test"
    assert to_snake_case("__DebtorID") == "__debtor_id"
    assert to_snake_case("This-Is-A-Test") == "this_is_a_test"
    assert to_snake_case("I'm a teapot") == "i'm_a_teapot"
    assert to_snake_case("__batch_id") == "__batch_id"
    assert to_snake_case("__created_at") == "__created_at"
    assert to_snake_case("__modified_at") == "__modified_at"
    assert to_snake_case("__valid_from") == "__valid_from"
    assert to_snake_case("__valid_to") == "__valid_to"
    assert (
        to_snake_case("this-contains_ ALLKinds OfWord_Boundaries")
        == "this_contains_all_kinds_of_word_boundaries"
    )


def test_special_character_translation():
    assert character_translation("Profit&Loss", {"&": "_and_"}) == "Profit_and_Loss"
    assert character_translation("Profit/Loss", {"/": "_or_"}) == "Profit_or_Loss"
    assert character_translation("Profit*Loss", {"*": "_times_"}) == "Profit_times_Loss"
    assert character_translation("Profit\\Loss", {"\\": "_or_"}) == "Profit_or_Loss"
    assert character_translation("Profit(Loss", {"(": "_"}) == "Profit_Loss"
    assert character_translation("Profit)Loss", {")": "_"}) == "Profit_Loss"


def test_default_normalization_strategy():
    config = get_default_config()

    def combined_normalization(text: str) -> str:
        translated = character_translation(text, config.character_translation_map)
        return to_snake_case(translated)

    assert combined_normalization("Profit&Loss") == "profit_and_loss"
    assert combined_normalization("Profit/Loss") == "profit_or_loss"
    assert combined_normalization("Profit*Loss") == "profit_times_loss"
    assert combined_normalization("Profit\\Loss") == "profit_or_loss"
    assert combined_normalization("Profit(Loss") == "profit_loss"
    assert combined_normalization("Profit)Loss") == "profit_loss"
    assert (
        combined_normalization("Growth% &   Loss + EBIDTA")
        == "growth_percent_and_loss_plus_ebidta"
    )
