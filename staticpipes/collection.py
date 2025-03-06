from staticpipes.collection_base import BaseCollection, BaseCollectionItem


class Collection(BaseCollection):

    def __init__(self, items=[]):
        self._items = items

    def get_items(self):
        return self._items


class CollectionItem(BaseCollectionItem):

    def __init__(self, id=None, data=None):
        self._id = id
        self._data = data

    def get_id(self):
        return self._id

    def get_data(self):
        return self._data
