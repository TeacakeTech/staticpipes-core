from staticpipes.collection_base import BaseCollection, BaseCollectionItem


class DataTigCollection(BaseCollection):

    def __init__(self, config, datastore, type_id):
        self._config = config
        self._datastore = datastore
        self._type_id = type_id

    def get_items(self):
        for id in self._datastore.get_ids_in_type(self._type_id):
            yield DataTigCollectionItem(
                self._config,
                self._datastore,
                self._type_id,
                self._datastore.get_item(self._type_id, id),
            )


class DataTigCollectionItem(BaseCollectionItem):

    def __init__(self, config, datastore, type_id, item):
        self._config = config
        self._datastore = datastore
        self._type_id = type_id
        self._item = item

    def get_id(self) -> str:
        return self._item.get_id()

    def get_data(self) -> dict:
        out = {}
        for field_id in self._config.get_type(self._type_id).get_fields().keys():
            out[field_id] = self._item.get_field_value(field_id).get_api_value()
        return out
