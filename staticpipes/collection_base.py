import abc
import typing


class BaseCollectionRecord(abc.ABC):

    @abc.abstractmethod
    def get_id(self):
        pass

    @abc.abstractmethod
    def get_data(self):
        pass


class BaseCollection(abc.ABC):

    @abc.abstractmethod
    def add_record(self, record: BaseCollectionRecord) -> None:
        pass

    @abc.abstractmethod
    def get_records(self) -> list:
        pass

    @abc.abstractmethod
    def get_record(self, id) -> typing.Optional[BaseCollectionRecord]:
        pass
