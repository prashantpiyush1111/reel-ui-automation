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


def test_mock_mode_runs_four_comments_on_one_reel(capsys):
    run(config=BotConfig(), mock=True)
    output = capsys.readouterr().out
    assert "[OK] Reel 1, comment 1:" in output
    assert "[OK] Reel 1, comment 4:" in output
    assert "Automatic submit is local-only" in output


def test_mock_mode_groups_eight_comments_into_two_reels(capsys):
    comments = tuple(f"comment {index}" for index in range(1, 9))
    run(config=BotConfig(), comments=comments, mock=True)
    output = capsys.readouterr().out
    assert "[OK] Reel 1, comment 4:" in output
    assert "[OK] Reel 2, comment 1:" in output
    assert "[OK] Reel 2, comment 4:" in output


def test_live_mode_requires_comment():
    try:
        run(config=BotConfig(), live=True)
    except ValueError as exc:
        assert "requires at least one --comment" in str(exc)
    else:
        raise AssertionError("Live mode must require an explicit comment")
