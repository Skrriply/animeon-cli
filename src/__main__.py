import logging

from src.core import AnimeAPI
from src.ui import CLI, ContentSelector, MpvPlayer, Prompt
from src.ui.commands import SearchCommand
from src.utils import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    """Main entry point of the application."""
    try:
        api_client = AnimeAPI()
        prompt = Prompt()
        selector = ContentSelector(prompt)
        player = MpvPlayer()
        commands = {"search": SearchCommand(api_client, selector, player)}
        cli = CLI(commands)  # type: ignore
        args = cli.parse_args()

        # Sets up logging if logview is enabled
        if args.logview:
            setup_logging()

        cli.run(args)
    except KeyboardInterrupt:
        logger.info("Вихід...")
    except Exception as error:
        logger.error(f"Неочікувана помилка: {error}")


if __name__ == "__main__":
    main()
