import csv

from staticpipes.collection_base import BaseCollection, BaseCollectionItem
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class LoadCollectionCSV(BasePipe):

    def __init__(self, directory="", filename="data.csv", collection_name="data"):
        self._directory = directory
        self._filename = filename
        self._collection_name = collection_name

    def start_prepare(self, current_info: CurrentInfo) -> None:

        items = []

        with self.source_directory.get_contents_as_filepointer(
            self._directory, self._filename
        ) as fp:
            csv_reader = csv.reader(
                fp,
            )
            header_row = next(csv_reader)
            for row in csv_reader:
                if row:
                    data = {header_row[i]: row[i] for i in range(1, len(row))}
                    items.append(BaseCollectionItem(id=row[0], data=data))

        current_info.set_context(
            ["collection", self._collection_name], BaseCollection(items=items)
        )

    # TODO reload on watch
