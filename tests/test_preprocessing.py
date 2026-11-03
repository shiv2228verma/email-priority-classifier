from preprocessing import clean_text, combine_email_text

def test_clean_text_normalizes_case_and_whitespace():
    assert clean_text("  HELLO\n   World  ") == "hello world"

def test_clean_text_handles_missing_values():
    assert clean_text(None) == ""
    assert clean_text(float("nan")) == ""

def test_combine_email_text_handles_empty_subject():
    assert combine_email_text("", "Please review this") == "please review this"
