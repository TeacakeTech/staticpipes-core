import inspect
import logging
import pkgutil
import pydoc

from staticpipes.collection import Collection, CollectionRecord
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe

logger = logging.getLogger(__name__)


class PipeLoadCollectionPythonDocs(BasePipe):

    def __init__(
        self,
        module_names: list = [],
        collection_name: str = "python_docs",
    ):
        self._module_names = module_names
        self._collection_name = collection_name

    def start_prepare(self, current_info: CurrentInfo) -> None:
        # vars
        collection = Collection()
        # load
        for modname in self._module_names:
            self._build_modname(modname, collection)
        # set context
        current_info.set_context(["collection", self._collection_name], collection)

    def _build_modname(self, modname, collection):

        # vars
        logger.debug("Building for " + modname)
        object, name = pydoc.resolve(modname)  # type: ignore

        data: dict = {"name": name, "classes": [], "modules": []}

        # other modules in a package
        if hasattr(object, "__path__"):
            for importer, modname, ispkg in pkgutil.iter_modules(object.__path__):
                data["modules"].append(  # type: ignore
                    {
                        "module_name": modname,
                        "full_name": name + "." + modname,
                        "is_package": ispkg,
                    }
                )

        # items in this module
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

        # Add to results
        collection.add_record(CollectionRecord(id=name, data=data))

        # Call for other modules we found
        for module in data["modules"]:
            if not collection.get_record(module["full_name"]):
                self._build_modname(module["full_name"], collection)
