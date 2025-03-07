class BaseCollectionItem:

    def get_id(self):
        pass

    def get_data(self):
        pass


class BaseCollection:

    def add_item(self, item: BaseCollectionItem):
        pass

    def get_items(self):
        pass

    def get_item(self, id):
        pass
