import logging

from animeon.core import AnimeOnAPI, Extractor
from animeon.core.http import HTTPClient
from animeon.integrations.players import MpvPlayer
from animeon.integrations.prompters import FzfPrompter
from animeon.ui import CLI, ContentSelector
from animeon.ui.commands import SearchCommand
from animeon.utils import ConfigManager, LoggerManager, check_dependencies
from animeon.utils.preview import AnimePreviewGenerator, Formatter, ImageDownloader

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
        prompter = FzfPrompter()
        formatter = Formatter()
        image_downloader = ImageDownloader(http_client)
        preview_generator = AnimePreviewGenerator(formatter, image_downloader)
        selector = ContentSelector(prompter, preview_generator)
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
