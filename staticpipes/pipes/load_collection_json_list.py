import json

from staticpipes.collection import Collection, CollectionRecord
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class PipeLoadCollectionJSONList(BasePipe):
    """
    Creates a collection and loads data from a list
    in a single JSON file in the source directory.

    The index of position in the list (zero based) is
    used as the id of items in the collection.
    """

    def __init__(
        self,
        directory="",
        filename: str = "data.json",
        collection_name: str = "data",
    ):
        self._directory = directory
        self._filename = filename
        self._collection_name = collection_name

    def start_build(self, current_info: CurrentInfo) -> None:
        """"""

        collection = Collection()

        with self._source_directory.get_contents_as_filepointer(
            self._directory, self._filename
        ) as fp:
            data = json.load(fp)
            idx = 0
            for raw_data in data:
                collection.add_record(CollectionRecord(id=str(idx), data=raw_data))
                idx += 1

        current_info.set_context(["collection", self._collection_name], collection)

    # TODO reload on watch

    def get_description_for_logs(self) -> str:
        """"""
        return "Load Collection JSON List (Dir {}, Filename {}, Collection {})".format(
            self._directory, self._filename, self._collection_name
        )
