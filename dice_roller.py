import random
import argparse


def roll_dice(dice_rolls: int, dice_size: int) -> int:
    """Roll dice_rolls number of dice with dice_size sides. Returns total sum."""
    dice_sum = 0
    for i in range(dice_rolls):
        roll = random.randint(1, dice_size)
        dice_sum += roll
        if roll == 1:
            print(f'You rolled a {roll}! Critical Fail')
        elif roll == dice_size:
            print(f'You rolled a {roll}! Critical Success!')
        else:
            print(f'You rolled a {roll}')
    print(f'You have rolled a total of {dice_sum}')
    return dice_sum


def parse_args():
    parser = argparse.ArgumentParser(
        description='Dice Roller - Roll any number of dice with any number of sides.'
    )
    parser.add_argument(
        '-n', '--num-dice',
        type=int,
        default=None,
        help='Number of dice to roll'
    )
    parser.add_argument(
        '-s', '--sides',
        type=int,
        default=None,
        help='Number of sides on each die'
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Use CLI args if provided, otherwise prompt interactively
    if args.num_dice is not None:
        dice_rolls = args.num_dice
    else:
        dice_rolls = int(input('How many dice would you like to roll? '))

    if args.sides is not None:
        dice_size = args.sides
    else:
        dice_size = int(input('How many sides are the dice? '))

    if dice_rolls <= 0:
        print('Error: Number of dice must be greater than 0.')
        return
    if dice_size <= 0:
        print('Error: Number of sides must be greater than 0.')
        return

    roll_dice(dice_rolls, dice_size)


if __name__ == "__main__":
    main()