import typing

from staticpipes.collection_base import BaseCollection, BaseCollectionRecord


class CollectionRecord(BaseCollectionRecord):

    def __init__(self, id=None, data=None):
        self._id = id
        self._data = data

    def get_id(self):
        return self._id

    def get_data(self):
        return self._data


class Collection(BaseCollection):

    def __init__(self):
        self._records: list = []

    def add_record(self, record: BaseCollectionRecord) -> None:
        self._records.append(record)

    def get_records(self) -> list:
        return self._records

    def get_record(self, id) -> typing.Optional[BaseCollectionRecord]:
        for record in self._records:
            if record.get_id() == id:
                return record
        return None
