import logging

from animeon.core import AnimeOnAPI, Extractor
from animeon.core.http import HTTPClient
from animeon.ui import CLI, ContentSelector, MpvPlayer, Prompt
from animeon.ui.commands import SearchCommand
from animeon.ui.preview import AnimePreviewGenerator
from animeon.utils import ConfigManager, LoggerManager, check_dependencies

logger = logging.getLogger(__name__)


def main() -> None:
    """Main entry point of the application."""
    # Sets up logging
    logger_manager = LoggerManager()
    logger_manager.setup_logging()

    try:
        # Checks dependencies
        check_dependencies()

        # Initializes components
        config = ConfigManager()
        http_client = HTTPClient()
        extractor = Extractor()
        api_client = AnimeOnAPI(
            http_client, extractor, timeout=config.get("api.timeout")
        )
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
        logger.info("Exiting...")


if __name__ == "__main__":
    main()
