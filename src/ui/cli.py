import argparse
import logging
from typing import Mapping

from src import __version__
from src.ui.commands import BaseCommand

logger = logging.getLogger(__name__)


class CLI:
    """Command Line Interface for AnimeON."""

    def __init__(self, commands: Mapping[str, BaseCommand]) -> None:
        """
        Initializes CLI application.

        Args:
            commands: Dictionary of commands.
        """
        self.commands = commands
        self._parser = self._create_parser()

    @staticmethod
    def _create_parser() -> argparse.ArgumentParser:
        """Creates CLI argument parser."""
        logger.debug("Creating command line argument parser")

        parser = argparse.ArgumentParser(
            prog="animeon",
            description="CLI інструмент для пошуку та відтворення аніме",
            usage="%(prog)s [параметри] <query>",
            add_help=False,
        )
        parser._positionals.title = "Аргументи"
        parser._optionals.title = "Параметри"
        parser.add_argument("-h", "--help", action="help", help="Вивести довідку")
        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=f"%(prog)s {__version__}",
            help="Вивести версію застосунку",
        )
        parser.add_argument(
            "-d", "--debug", action="store_true", help="Увімкнути режим налагодження"
        )
        parser.add_argument("query", nargs="+", help="Пошуковий запит")

        return parser

    def parse_args(self) -> argparse.Namespace:
        """
        Parses CLI arguments.

        Returns:
            Parsed CLI arguments.
        """
        logger.debug("Parsing command line arguments")

        args = self._parser.parse_args()
        args.query = " ".join(args.query)  # Converts list of words to single string
        return args

    def run(self, args: argparse.Namespace) -> None:
        """
        Runs the CLI application.

        Args:
            args: Parsed CLI arguments.
        """
        search_command = self.commands.get("search")
        if search_command:
            search_command.execute(args.query)
