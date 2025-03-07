import json

from staticpipes.collection import Collection, CollectionItem
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class PipeLoadCollectionJSONList(BasePipe):

    def __init__(self, directory="", filename="data.json", collection_name="data"):
        self._directory = directory
        self._filename = filename
        self._collection_name = collection_name

    def start_prepare(self, current_info: CurrentInfo) -> None:
        """"""

        items = []

        with self.source_directory.get_contents_as_filepointer(
            self._directory, self._filename
        ) as fp:
            data = json.load(fp)
            idx = 0
            for raw_data in data:
                items.append(CollectionItem(id=str(idx), data=raw_data))
                idx += 1

        current_info.set_context(
            ["collection", self._collection_name], Collection(items=items)
        )

    # TODO reload on watch
