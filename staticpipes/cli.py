import argparse
import logging
import sys

from .worker import Worker


def cli(config, source_dir, build_directory, log_level=logging.INFO):
    # CLI options
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="subparser_name")

    build_parser = subparsers.add_parser("build")  # noqa

    watch_parser = subparsers.add_parser("watch")  # noqa

    serve_parser = subparsers.add_parser("serve")  # noqa

    args = parser.parse_args()

    # Set up logging
    root_logger = logging.getLogger("staticpipes")
    root_logger.setLevel(log_level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(
        logging.Formatter("%(levelname)s - %(asctime)s - %(name)s - %(message)s")
    )
    root_logger.addHandler(handler)

    # Do work
    if args.subparser_name == "build":
        worker = Worker(config, source_dir, build_directory)
        worker.build()

    elif args.subparser_name == "watch":
        worker = Worker(config, source_dir, build_directory)
        worker.watch()

    elif args.subparser_name == "serve":
        worker = Worker(config, source_dir, build_directory)
        worker.serve()
