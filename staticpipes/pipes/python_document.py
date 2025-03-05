import inspect
import pkgutil

import jinja2

from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class PipePythonDocument(BasePipe):

    def __init__(
        self,
        packages: list,
        jinja2_template,
        output_dir=None,
        output_filename_extension="html",
    ):
        self._packages = packages
        self._output_dir = output_dir
        self._output_filename_extension = output_filename_extension
        self._jinja2_env = None  # type: ignore
        self._jinja2_template = jinja2_template
        self._jinja2_env = None  # type: ignore
        self._modules_found_names = []

    def start_build(self, current_info: CurrentInfo) -> None:
        self._jinja2_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.source_directory.dir),
            autoescape=jinja2.select_autoescape(),
        )  # type: ignore

        for pkg in self._packages:
            self._inspect_package(pkg, current_info)

    def _inspect_package(self, package, current_info: CurrentInfo):

        for k, v in inspect.getmembers(package):
            if inspect.ismodule(v):
                self._inspect_module(v, current_info)

    def _inspect_module(self, module, current_info: CurrentInfo):
        self._modules_found_names.append(module.__name__)

        # print(module.__name__)

        template = self._jinja2_env.get_template(self._jinja2_template)  # type: ignore

        this_context = current_info.get_context().copy()
        this_context["module_name"] = module.__name__
        this_context["modules"] = []
        this_context["classes"] = []

        for k, v in inspect.getmembers(module):
            if inspect.ismodule(v) and [
                i for i in self._packages if v.__name__.startswith(i.__name__)
            ]:
                this_context["modules"].append({"module": v})
                if v.__name__ not in self._modules_found_names:
                    self._inspect_module(v, current_info)
            if inspect.isclass(v):
                class_info = {"class": v, "name": v.__name__, "functions": []}
                for class_k, class_v in inspect.getmembers(v):
                    if inspect.isfunction(class_v) and not class_v.__name__.startswith(
                        "_"
                    ):
                        class_info["functions"].append(
                            {"function": class_v, "name": class_v.__name__}
                        )
                this_context["classes"].append(class_info)

        contents = template.render(this_context)
        self.build_directory.write(
            self._output_dir,
            module.__name__ + "." + self._output_filename_extension,
            contents,
        )
