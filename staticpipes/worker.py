import copy
import logging
import os

from .build_directory import BuildDirectory
from .current_info import CurrentInfo
from .exceptions import WatchFunctionalityNotImplementedException
from .source_directory import SourceDirectory

logger = logging.getLogger(__name__)


class Worker:

    def __init__(self, config, source_dir, build_directory):
        self.config = config
        self.source_directory = SourceDirectory(source_dir)
        self.build_directory = BuildDirectory(build_directory)
        self.current_info = None
        self._check_reports: list = []

        for pipeline in self.config.pipes:
            pipeline.config = self.config
            pipeline.source_directory = self.source_directory
            pipeline.build_directory = self.build_directory

        for check in self.config.checks:
            check.config = self.config
            check.build_directory = self.build_directory

    def build(self, run_checks=True):
        self.current_info = CurrentInfo(
            context=copy.copy(self.config.context), watch=False
        )
        self._build(run_checks=run_checks)

    def _build(self, run_checks=True):
        # Step 1: Prepare
        # start
        for pipeline in self.config.pipes:
            pipeline.start_prepare(self.current_info)
        # files
        rpsd = os.path.realpath(self.source_directory.dir)
        for root, dirs, files in os.walk(rpsd):
            if not self.build_directory.is_equal_to_source_dir(root):
                for file in files:
                    relative_dir = root[len(rpsd) + 1 :]
                    if not relative_dir:
                        relative_dir = "/"
                    self._prepare_file(relative_dir, file)
        # end
        for pipeline in self.config.pipes:
            pipeline.end_prepare(self.current_info)

        # Step 2: Build
        self.build_directory.prepare()
        # start
        for pipeline in self.config.pipes:
            pipeline.start_build(self.current_info)
        # files
        rpsd = os.path.realpath(self.source_directory.dir)
        for root, dirs, files in os.walk(rpsd):
            if not self.build_directory.is_equal_to_source_dir(root):
                for file in files:
                    relative_dir = root[len(rpsd) + 1 :]
                    if not relative_dir:
                        relative_dir = "/"
                    self._process_file(relative_dir, file)
        # end
        for pipeline in self.config.pipes:
            pipeline.end_build(self.current_info)
        self.build_directory.remove_all_files_we_did_not_write()

        # Step 3: check
        if run_checks:
            self._check()

    def _check(self):
        if not self.config.checks:
            logger.info("No checks defined")
            return

        self._check_reports: list = []
        # start
        for check in self.config.checks:
            for c_r in check.start_check():
                self._check_reports.append(c_r)
        # files
        rpbd = os.path.realpath(self.build_directory.dir)
        for root, dirs, files in os.walk(rpbd):
            for file in files:
                relative_dir = root[len(rpbd) + 1 :]
                if not relative_dir:
                    relative_dir = "/"
                for check in self.config.checks:
                    for c_r in check.check_file(relative_dir, file):
                        self._check_reports.append(c_r)
        # end
        for check in self.config.checks:
            for c_r in check.end_check():
                self._check_reports.append(c_r)

        # Log
        if len(self._check_reports) == 0:
            logger.info("Check Reports count: 0")
        else:
            logger.warn("Check Reports count: {}".format(len(self._check_reports)))
            for check_report in self._check_reports:
                report = (
                    "Report: \n"
                    + "  type      : {} from generator {}\n".format(
                        check_report.type, check_report.generator_class
                    )
                    + "  dir       : {}\n".format(check_report.dir)
                    + "  file      : {}\n".format(check_report.file)
                    + "  message   : {}\n".format(check_report.message)
                    + "  line, col : {}, {}".format(
                        check_report.line, check_report.column
                    )
                )
                logger.warn(report)

    def watch(self):
        # Only import this when watch function called,
        # so we can use build part without watch dependencies
        from .watcher import Watcher

        self.current_info = CurrentInfo(
            context=copy.copy(self.config.context), watch=True
        )
        # Build first - so we have complete site
        self._build()

        # Check
        if self.config.checks:
            logger.info(
                "Checks do not work in watch yet, so no future checks will be done"  # noqa
            )

        # start
        for pipeline in self.config.pipes:
            pipeline.start_watch(self.current_info)
        # Now watch
        watcher = Watcher(self)
        logger.info("Watching ...")
        watcher.watch()

    def serve(self, server_address: str, server_port: int):

        # Only import this when watch function called,
        # so we can use build part without watch dependencies
        import threading

        from .serve import server
        from .watcher import Watcher

        self.current_info = CurrentInfo(
            context=copy.copy(self.config.context), watch=True
        )
        # Build first - so we have complete site
        self._build()

        # Check
        if self.config.checks:
            logger.info(
                "Checks do not work in serve yet, so no future checks will be done"  # noqa
            )

        # Start HTTP server in background
        threading.Thread(
            target=server, args=(self.build_directory.dir, server_address, server_port)
        ).start()

        # start watching
        for pipeline in self.config.pipes:
            pipeline.start_watch(self.current_info)
        # Now watch
        watcher = Watcher(self)
        logger.info("Watching ...")
        watcher.watch()

    def _prepare_file(self, dir, filename):
        logger.info("Preparing {} {} ...".format(dir, filename))
        self.current_info.reset_for_new_file()
        for pipeline in self.config.pipes:
            pipeline.prepare_file(dir, filename, self.current_info)

    def _process_file(self, dir, filename):
        logger.info("Processing {} {} ...".format(dir, filename))
        self.current_info.reset_for_new_file()
        for pipeline in self.config.pipes:
            if self.current_info.current_file_excluded:
                pipeline.file_excluded_during_build(dir, filename, self.current_info)
            else:
                pipeline.build_file(dir, filename, self.current_info)

    def process_file_during_watch(self, dir, filename):
        # Check if we should process
        if self.build_directory.is_equal_to_source_dir(
            os.path.join(self.source_directory.dir, dir)
        ):
            return
        # Setup
        logger.info("Processing during watch {} {} ...".format(dir, filename))
        context_version: int = self.current_info.get_context_version()
        # Call each pipe for file
        self.current_info.reset_for_new_file()
        for pipeline in self.config.pipes:
            try:
                if self.current_info.current_file_excluded:
                    pipeline.file_changed_but_excluded_during_watch(
                        dir, filename, self.current_info
                    )
                else:
                    pipeline.file_changed_during_watch(dir, filename, self.current_info)
            except WatchFunctionalityNotImplementedException:
                logger.error(
                    (
                        "WATCH FEATURE NOT IMPLEMENTED IN PIPELINE {}, "
                        + "YOU MAY HAVE TO BUILD MANUALLY"
                    ).format(str(pipeline))
                )
        # If context changed, call each pipe for context
        if context_version != self.current_info.get_context_version():
            for pipeline in self.config.pipes:
                pipeline.context_changed_during_watch(
                    self.current_info,
                    context_version,
                    self.current_info.get_context_version(),
                )
