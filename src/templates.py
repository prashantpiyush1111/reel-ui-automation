from pathlib import Path


REQUIRED_TEMPLATES = (
    "reel_marker.png",
    "comment_button.png",
    "comment_input.png",
    "close_comment.png",
)


def validate_template_dir(directory: str | Path) -> list[str]:
    root = Path(directory)
    missing = [
        name for name in REQUIRED_TEMPLATES
        if not (root / name).is_file()
    ]
    return missing
