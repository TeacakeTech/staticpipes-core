import jinja2

from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class DatatigItemsJinja2(BasePipe):

    def __init__(
        self,
        type_id: str,
        jinja2_template,
        output_dir=None,
        output_filename_extension="html",
    ):
        self.type_id = type_id
        self.jinja2_template = jinja2_template
        self.output_dir = output_dir or type_id
        self.output_filename_extension = output_filename_extension
        self.jinja2_env = None  # type: ignore

    def _build(self, current_info: CurrentInfo):
        template = self.jinja2_env.get_template(self.jinja2_template)  # type: ignore
        for id in current_info.context["datatig"]["datastore"].get_ids_in_type(
            self.type_id
        ):
            this_context = current_info.context.copy()
            this_context["item"] = current_info.context["datatig"][
                "datastore"
            ].get_item(self.type_id, id)
            contents = template.render(this_context)
            self.build_directory.write(
                self.output_dir, id + "." + self.output_filename_extension, contents
            )

    def start_build(self, current_info: CurrentInfo) -> None:
        self.jinja2_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.source_directory.dir),
            autoescape=jinja2.select_autoescape(),
        )  # type: ignore
        self._build(current_info)
