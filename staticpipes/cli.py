import argparse
import logging
import sys

from .worker import Worker


def cli(
    config,
    source_dir,
    build_directory,
    log_level=logging.INFO,
    secondary_source_directories: dict | None = None,
):
    # CLI options
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="subparser_name")

    build_parser = subparsers.add_parser("build", aliases=["b"])  # noqa
    build_parser.add_argument(
        "--check", action=argparse.BooleanOptionalAction, default=True
    )

    check_parser = subparsers.add_parser("check", aliases=["c"])  # noqa

    watch_parser = subparsers.add_parser("watch", aliases=["w"])  # noqa

    serve_parser = subparsers.add_parser("serve", aliases=["s"])  # noqa
    serve_parser.add_argument("-p", "--port", type=int)
    serve_parser.add_argument("-a", "--address")

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
    if args.subparser_name == "build" or args.subparser_name == "b":
        worker = Worker(
            config,
            source_dir,
            build_directory,
            secondary_source_directories=secondary_source_directories,
        )
        worker.build(run_checks=args.check, sys_exit_after_checks=True)

    elif args.subparser_name == "check" or args.subparser_name == "c":
        worker = Worker(
            config,
            source_dir,
            build_directory,
            secondary_source_directories=secondary_source_directories,
        )
        worker.check(sys_exit_after_checks=True)

    elif args.subparser_name == "watch" or args.subparser_name == "w":
        worker = Worker(
            config,
            source_dir,
            build_directory,
            secondary_source_directories=secondary_source_directories,
        )
        worker.watch()

    elif args.subparser_name == "serve" or args.subparser_name == "s":
        worker = Worker(
            config,
            source_dir,
            build_directory,
            secondary_source_directories=secondary_source_directories,
        )
        worker.serve(
            server_address=args.address or "localhost", server_port=args.port or 8000
        )
