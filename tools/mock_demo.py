from src.mock_ui import MockUI


def main() -> None:
    ui = MockUI()

    print("Mock Reel UI demo")
    print("1. Detect reel:", ui.locate("reel_marker.png") is not None)

    button = ui.locate("comment_button.png")
    ui.click(button)
    print("2. Comments opened:", ui.comments_open)

    input_match = ui.locate("comment_input.png")
    ui.click(input_match)
    ui.type_text("Demo comment for local testing")
    print("3. Text prepared:", ui.typed_text)

    close_match = ui.locate("close_comment.png")
    ui.click(close_match)
    print("4. Comments closed:", not ui.comments_open)

    ui.scroll()
    print("5. Next reel simulated: ready")


if __name__ == "__main__":
    main()
