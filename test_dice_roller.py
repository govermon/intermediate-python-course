import pytest
from unittest.mock import patch
import io
import sys

from dice_roller import roll_dice, main, parse_args


# ── roll_dice() tests ──────────────────────────────────────────────────────────

def test_roll_dice_returns_integer():
    result = roll_dice(3, 6)
    assert isinstance(result, int)


def test_roll_dice_sum_within_range():
    """Total must be between num_dice * 1 and num_dice * dice_size."""
    num_dice, sides = 5, 10
    result = roll_dice(num_dice, sides)
    assert num_dice <= result <= num_dice * sides


def test_roll_dice_single_die():
    result = roll_dice(1, 6)
    assert 1 <= result <= 6


def test_roll_dice_d20():
    result = roll_dice(4, 20)
    assert 4 <= result <= 80


def test_roll_dice_critical_fail_message(capsys):
    """When a 1 is rolled, 'Critical Fail' should appear in output."""
    with patch('random.randint', return_value=1):
        roll_dice(1, 6)
    captured = capsys.readouterr()
    assert 'Critical Fail' in captured.out


def test_roll_dice_critical_success_message(capsys):
    """When max is rolled, 'Critical Success' should appear in output."""
    with patch('random.randint', return_value=6):
        roll_dice(1, 6)
    captured = capsys.readouterr()
    assert 'Critical Success' in captured.out


def test_roll_dice_normal_roll_message(capsys):
    """A mid-range roll should not show Critical Fail or Critical Success."""
    with patch('random.randint', return_value=3):
        roll_dice(1, 6)
    captured = capsys.readouterr()
    assert 'Critical Fail' not in captured.out
    assert 'Critical Success' not in captured.out
    assert 'You rolled a 3' in captured.out


def test_roll_dice_total_printed(capsys):
    with patch('random.randint', return_value=4):
        roll_dice(2, 6)
    captured = capsys.readouterr()
    assert 'You have rolled a total of 8' in captured.out


# ── parse_args() tests ─────────────────────────────────────────────────────────

def test_parse_args_defaults():
    with patch('sys.argv', ['dice_roller.py']):
        args = parse_args()
    assert args.num_dice is None
    assert args.sides is None


def test_parse_args_short_flags():
    with patch('sys.argv', ['dice_roller.py', '-n', '3', '-s', '6']):
        args = parse_args()
    assert args.num_dice == 3
    assert args.sides == 6


def test_parse_args_long_flags():
    with patch('sys.argv', ['dice_roller.py', '--num-dice', '5', '--sides', '20']):
        args = parse_args()
    assert args.num_dice == 5
    assert args.sides == 20


# ── main() integration tests ───────────────────────────────────────────────────

def test_main_with_cli_args(capsys):
    with patch('sys.argv', ['dice_roller.py', '-n', '2', '-s', '6']):
        main()
    captured = capsys.readouterr()
    assert 'You have rolled a total of' in captured.out


def test_main_invalid_dice_count(capsys):
    with patch('sys.argv', ['dice_roller.py', '-n', '0', '-s', '6']):
        main()
    captured = capsys.readouterr()
    assert 'Error' in captured.out


def test_main_invalid_sides(capsys):
    with patch('sys.argv', ['dice_roller.py', '-n', '2', '-s', '0']):
        main()
    captured = capsys.readouterr()
    assert 'Error' in captured.out


def test_main_interactive_mode(capsys):
    """Simulate interactive input when no CLI args provided."""
    with patch('sys.argv', ['dice_roller.py']), \
         patch('builtins.input', side_effect=['3', '6']):
        main()
    captured = capsys.readouterr()
    assert 'You have rolled a total of' in captured.out