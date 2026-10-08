from _bootstrap import REPO_ROOT

from src.template_validator import validate_templates
from src.templates import REQUIRED_TEMPLATES


def main() -> int:
    errors = validate_templates(REPO_ROOT / "templates", REQUIRED_TEMPLATES)

    if errors:
        print("Template validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Template validation passed.")
    print("Required UI templates are present and readable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
