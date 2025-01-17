import argparse
import logging
import os
import subprocess as sp
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--static', action='store_true', help='Will not fix errors, or format code')

arguments = parser.parse_args()
my_args = vars(arguments)

DIR_PATH = os.path.dirname(__file__)
FLAKE_CONFIG = os.path.join(DIR_PATH, '.flake8')
RUFF_CONFIG = os.path.join(DIR_PATH, 'ruff.toml')
logger = logging.getLogger(__name__)


def get_commands():
    black = ['black', '--skip-string-normalization', '-l', '120', '.']
    ruff = ['ruff', '--fix', '--config', RUFF_CONFIG, '.']
    flake8 = ['flake8', '--config', FLAKE_CONFIG, '.']

    if my_args.get('static'):
        ruff.remove('--fix')
        return ruff, flake8
    return black, ruff, flake8


def main():
    commands = get_commands()
    errors = []
    for command in commands:
        try:
            sp.check_call(command)
        except sp.CalledProcessError:
            errors.append(command[0])
    if errors:
        logger.error(f"Error raised from: {', '.join(errors)}")
        sys.exit(1)


if __name__ == '__main__':
    exit(main())
