from src.main import build_parser, run
from src.config import BotConfig


def test_parser_defaults_to_safe_mode():
    args = build_parser().parse_args([])
    assert args.live is False
    assert args.mock is False
    assert args.once is False
    assert args.comment == []


def test_run_defaults_to_dry_run(capsys):
    run(config=BotConfig(), live=False)
    output = capsys.readouterr().out
    assert "Safe dry run complete." in output


def test_mock_mode_runs_full_safe_flow(capsys):
    run(config=BotConfig(), mock=True, comments=("Mock comment",))
    output = capsys.readouterr().out
    assert "[OK] reel detection" in output
    assert "[OK] prepare comment" in output
    assert "Mock comment" in output
    assert "no submit action exists" in output


def test_live_mode_requires_comment():
    try:
        run(config=BotConfig(), live=True)
    except ValueError as exc:
        assert "requires at least one --comment" in str(exc)
    else:
        raise AssertionError("Live mode must require an explicit comment")
