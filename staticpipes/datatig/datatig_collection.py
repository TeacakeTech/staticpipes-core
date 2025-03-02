from staticpipes.collection_base import BaseCollection


class DataTigCollection(BaseCollection):

    def __init__(self, config, datastore, type_id):
        self._config = config
        self._datastore = datastore
        self._type_id = type_id

    def get_items(self):
        for id in self._datastore.get_ids_in_type(self._type_id):
            yield self._datastore.get_item(self._type_id, id)
