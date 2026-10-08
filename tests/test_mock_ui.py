from src.mock_ui import MockUI


def test_mock_ui_comment_flow():
    ui = MockUI()

    button = ui.locate("comment_button.png")
    assert button is not None

    ui.click(button)
    assert ui.comments_open

    input_match = ui.locate("comment_input.png")
    assert input_match is not None

    ui.click(input_match)
    ui.type_text("demo comment")

    assert ui.typed_text == "demo comment"

    close_match = ui.locate("close_comment.png")
    assert close_match is not None
    ui.click(close_match)

    assert not ui.comments_open
