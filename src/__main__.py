import logging

from src.core import AnimeAPI
from src.core.http import HTTPClient
from src.ui import CLI, ContentSelector, MpvPlayer, Prompt
from src.ui.commands import SearchCommand
from src.ui.preview import AnimePreviewGenerator
from src.utils import check_dependencies, setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    """Main entry point of the application."""
    try:
        # TODO: Do something about logging
        check_dependencies()

        http_client = HTTPClient()
        api_client = AnimeAPI(http_client)
        prompt = Prompt()
        preview_generator = AnimePreviewGenerator(http_client)
        selector = ContentSelector(prompt, preview_generator)
        player = MpvPlayer()
        commands = {"search": SearchCommand(api_client, selector, player)}
        cli = CLI(commands)
        args = cli.parse_args()

        # Sets up logging if logview is enabled
        if args.logview:
            setup_logging()

        cli.run(args)
    except KeyboardInterrupt:
        logger.info("Exit...")
    except Exception as error:
        logger.error(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
