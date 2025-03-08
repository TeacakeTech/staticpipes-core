import csv

from staticpipes.collection import Collection, CollectionRecord
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class PipeLoadCollectionCSV(BasePipe):

    def __init__(self, directory=None, filename=None, collection_name="data"):
        self._directory = directory
        self._filename = filename
        self._collection_name = collection_name

    def start_prepare(self, current_info: CurrentInfo) -> None:
        collection = Collection()

        with self.source_directory.get_contents_as_filepointer(
            self._directory or "", self._filename
        ) as fp:
            self._load(fp, collection)

        current_info.set_context(["collection", self._collection_name], collection)

    def _load(self, fp, collection):
        csv_reader = csv.reader(
            fp,
        )
        header_row = next(csv_reader)
        for row in csv_reader:
            if row:
                data = {header_row[i]: row[i] for i in range(1, len(row))}
                collection.add_record(CollectionRecord(id=row[0], data=data))

    # TODO reload on watch
