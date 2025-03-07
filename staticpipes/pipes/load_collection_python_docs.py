import inspect
import logging
import pkgutil
import pydoc

from staticpipes.collection import Collection, CollectionItem
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe

logger = logging.getLogger(__name__)


class PipeLoadCollectionPythonDocs(BasePipe):

    def __init__(
        self,
        pkgutil_walk_packages_args: list = [],
        module_names: list = [],
        collection_name: str = "python_docs",
    ):
        self._pkgutil_walk_packages_args = pkgutil_walk_packages_args
        self._module_names = module_names
        self._collection_name = collection_name

    def start_prepare(self, current_info: CurrentInfo) -> None:
        """"""
        # vars
        collection = Collection()
        # load
        for a1, a2 in self._pkgutil_walk_packages_args:
            for importer, modname, ispkg in pkgutil.walk_packages(a1, a2):
                collection.add_item(self._build_modname(modname, current_info))
        for modname in self._module_names:
            collection.add_item(self._build_modname(modname, current_info))
        # set context
        current_info.set_context(["collection", self._collection_name], collection)

    def _build_modname(self, modname, current_info: CurrentInfo):

        logger.debug("Building for " + modname)
        object, name = pydoc.resolve(modname)  # type: ignore

        data: dict = {"name": name, "classes": []}

        for k, v in inspect.getmembers(object):
            if inspect.isclass(v) and v.__module__ == modname:
                class_info = {
                    "class": v,
                    "name": v.__name__,
                    "functions": [],
                    "docstring": inspect.getdoc(v),
                    "comments": inspect.getcomments(v),
                }
                for class_k, class_v in inspect.getmembers(v):
                    if (
                        inspect.isfunction(class_v)
                        and not class_v.__name__.startswith("_")
                        and class_v.__module__ == modname
                    ):
                        class_info["functions"].append(  # type: ignore
                            {
                                "function": class_v,
                                "name": class_v.__name__,
                                "docstring": inspect.getdoc(class_v),
                                "comments": inspect.getcomments(class_v),
                            }
                        )
                data["classes"].append(class_info)

        return CollectionItem(id=name, data=data)
