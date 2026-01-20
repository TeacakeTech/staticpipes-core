from staticpipes.pipe_bundle_base import BasePipeBundle
from staticpipes.pipes.collection_records_process import PipeCollectionRecordsProcess
from staticpipes.pipes.copy_from_secondary_source import PipeCopyFromSecondarySource
from staticpipes.pipes.load_collection_python_docs import PipeLoadCollectionPythonDocs
from staticpipes.processes.jinja2_render_source_file import (
    ProcessJinja2RenderSourceFile,
)


class BundlePythonDocs(BasePipeBundle):
    """ """

    def __init__(
        self, module_names: list = [], pass_number=1000, jinja2_environment=None
    ):
        super().__init__(pass_number)
        self._module_names = module_names
        self._pipes: list = [
            PipeCopyFromSecondarySource(
                secondary_source_name="python_docs",
                source_directory="/",
                source_filename="python_docs.css",
                destination_directory="css",
            ),
            PipeLoadCollectionPythonDocs(
                module_names=module_names,
                collection_name="python_docs",
            ),
            PipeCollectionRecordsProcess(
                collection_name="python_docs",
                output_dir="reference",
                context_key_record_data="python_document",
                processors=[
                    ProcessJinja2RenderSourceFile(
                        template="python_docs:reference.html",
                        jinja2_environment=jinja2_environment,
                    ),
                ],
            ),
        ]
