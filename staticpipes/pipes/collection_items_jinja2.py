import jinja2

from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class CollectionItemsJinja2(BasePipe):

    def __init__(
        self,
        type_id: str,
        jinja2_template,
        output_dir=None,
        output_filename_extension="html",
    ):
        self._type_id = type_id
        self._jinja2_template = jinja2_template
        self._output_dir = output_dir or type_id
        self._output_filename_extension = output_filename_extension
        self._jinja2_env = None  # type: ignore

    def _build(self, current_info: CurrentInfo):
        template = self._jinja2_env.get_template(self._jinja2_template)  # type: ignore
        collection = current_info.get_context("collection")[self._type_id]

        for item in collection.get_items():
            this_context = current_info.get_context().copy()
            this_context["item_id"] = item.get_id()
            this_context["item_data"] = item.get_data()
            contents = template.render(this_context)
            self.build_directory.write(
                self._output_dir,
                item.get_id() + "." + self._output_filename_extension,
                contents,
            )

    def start_build(self, current_info: CurrentInfo) -> None:
        self._jinja2_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.source_directory.dir),
            autoescape=jinja2.select_autoescape(),
        )  # type: ignore
        self._build(current_info)
