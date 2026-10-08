from dataclasses import dataclass, field

from .detector import Match


@dataclass
class MockUI:
    """Deterministic local Reel-like UI used for offline workflow tests."""

    visible: bool = True
    comments_open: bool = False
    input_focused: bool = False
    typed_text: str = ""
    submitted_comments: list[str] = field(default_factory=list)
    reel_number: int = 1

    def locate(self, template_name: str) -> Match | None:
        if not self.visible:
            return None

        if template_name == "reel_marker.png":
            return Match(template_name, 100, 100, 80, 40, 0.99)

        if template_name == "comment_button.png":
            return Match(template_name, 900, 500, 40, 40, 0.98)

        if template_name == "comment_input.png" and self.comments_open:
            return Match(template_name, 700, 700, 300, 50, 0.97)

        if template_name == "close_comment.png" and self.comments_open:
            return Match(template_name, 1100, 100, 40, 40, 0.96)

        return None

    def click(self, match: Match) -> None:
        if match.name == "comment_button.png":
            self.comments_open = True
        elif match.name == "comment_input.png":
            self.input_focused = True
        elif match.name == "close_comment.png":
            self.comments_open = False
            self.input_focused = False

    def type_text(self, text: str) -> None:
        if not self.input_focused:
            raise RuntimeError("Mock input is not focused")
        self.typed_text += text

    def submit_comment(self) -> None:
        if not self.comments_open or not self.input_focused:
            raise RuntimeError("Mock comment input is not ready")
        if not self.typed_text:
            raise RuntimeError("Mock comment is empty")
        self.submitted_comments.append(self.typed_text)
        self.typed_text = ""
        self.input_focused = False

    def scroll(self) -> None:
        self.typed_text = ""
        self.comments_open = False
        self.input_focused = False
        self.reel_number += 1
