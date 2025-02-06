import os
import time

import watchdog.events
from watchdog.observers import Observer


class Watcher(watchdog.events.FileSystemEventHandler):

    def __init__(self, worker):
        self.worker = worker
        self.ignore_extensions = [
            # Pycharm
            "~",
            # Vi:
            ".swp",
            ".swx",
        ]

    def on_created(self, event):
        self.on_modified(event)

    def on_deleted(self, event):
        pass
        # print("on_deleted " + str(event))
        # TODO

    def on_modified(self, event):
        for ext in self.ignore_extensions:
            if event.src_path.endswith(ext):
                return
        if isinstance(event, watchdog.events.DirModifiedEvent):
            return
        # print("on_modified " + str(event))

        rpsd = os.path.realpath(self.worker.source_directory.dir)

        relative_fn = event.src_path[len(rpsd) + 1 :]
        if "/" in relative_fn:
            bits = relative_fn.split("/")
            fn = bits.pop()
            self.worker.process_file_during_watch("/".join(bits), fn)
        else:
            self.worker.process_file_during_watch("", relative_fn)

    def on_moved(self, event):
        pass
        # print("on_moved " + str(event))
        # TODO

    def watch(self):
        observer = Observer()
        observer.schedule(self, self.worker.source_directory.dir, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
