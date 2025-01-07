import logging

from src.core import AnimeAPI
from src.core.http import HTTPClient
from src.ui import CLI, ContentSelector, MpvPlayer, Prompt
from src.ui.commands import SearchCommand
from src.ui.preview import AnimePreviewGenerator
from src.utils import LoggerManager, check_dependencies

logger = logging.getLogger(__name__)


def main() -> None:
    """Main entry point of the application."""
    try:
        # Sets up logging
        logger_manager = LoggerManager()
        logger_manager.setup_logging()

        # Checks dependencies
        check_dependencies()

        # Initializes components
        http_client = HTTPClient()
        api_client = AnimeAPI(http_client)
        prompt = Prompt()
        preview_generator = AnimePreviewGenerator(http_client)
        selector = ContentSelector(prompt, preview_generator)
        player = MpvPlayer()
        
        # Runs CLI
        commands = {"search": SearchCommand(api_client, selector, player)}
        cli = CLI(commands)
        args = cli.parse_args()

        # Enables debug level
        if args.debug:
            logger_manager.enable_debug()

        cli.run(args)
    except KeyboardInterrupt:
        logger.info("Exit...")
    except Exception as error:
        logger.error(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
