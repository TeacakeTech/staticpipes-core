from staticpipes.bundle_base import BaseBundle
from staticpipes.bundles.secondary_sources.python_docs import (
    DIRECTORY as BUNDLE_SECONDARY_SOURCE_PYTHON_DOCS_DIRECTORY,
)
from staticpipes.pipes.collection_records_process import PipeCollectionRecordsProcess
from staticpipes.pipes.copy_from_secondary_source import PipeCopyFromSecondarySource
from staticpipes.pipes.load_collection_python_docs import PipeLoadCollectionPythonDocs
from staticpipes.processes.jinja2_render_source_file import (
    ProcessJinja2RenderSourceFile,
)


class BundlePythonDocs(BaseBundle):
    """Parses some python classes in our environment and
    writes out reference pages for them."""

    def __init__(
        self,
        module_names: list[str],
        destination_dir: str = "reference",
        jinja2_environment=None,
    ):
        super().__init__()
        self._module_names = module_names
        self._pipes: list = [
            PipeCopyFromSecondarySource(
                secondary_source_name="bundle_python_docs",
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
                output_dir=destination_dir,
                context_key_record_data="python_document",
                processors=[
                    ProcessJinja2RenderSourceFile(
                        template="bundle_python_docs:reference.html",
                        jinja2_environment=jinja2_environment,
                    ),
                ],
            ),
        ]
        self._secondary_source_directory_paths: dict = {
            "bundle_python_docs": BUNDLE_SECONDARY_SOURCE_PYTHON_DOCS_DIRECTORY
        }

    def get_description_for_logs(self) -> str:
        """"""
        return "Python Docs (module names: {})".format(self._module_names)
