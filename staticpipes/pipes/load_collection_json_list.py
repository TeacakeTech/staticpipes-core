import json

from staticpipes.collection import Collection, CollectionRecord
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class PipeLoadCollectionJSONList(BasePipe):

    def __init__(self, directory="", filename="data.json", collection_name="data"):
        self._directory = directory
        self._filename = filename
        self._collection_name = collection_name

    def start_prepare(self, current_info: CurrentInfo) -> None:
        """"""

        collection = Collection()

        with self.source_directory.get_contents_as_filepointer(
            self._directory, self._filename
        ) as fp:
            data = json.load(fp)
            idx = 0
            for raw_data in data:
                collection.add_record(CollectionRecord(id=str(idx), data=raw_data))
                idx += 1

        current_info.set_context(["collection", self._collection_name], collection)

    # TODO reload on watch
