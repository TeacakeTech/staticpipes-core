from staticpipes.collection_base import BaseCollection, BaseCollectionItem


class CollectionItem(BaseCollectionItem):

    def __init__(self, id=None, data=None):
        self._id = id
        self._data = data

    def get_id(self):
        return self._id

    def get_data(self):
        return self._data


class Collection(BaseCollection):

    def __init__(self):
        self._items = []

    def add_item(self, item: BaseCollectionItem):
        self._items.append(item)

    def get_items(self):
        return self._items

    def get_item(self, id):
        for item in self._items:
            if item.get_id() == id:
                return item
