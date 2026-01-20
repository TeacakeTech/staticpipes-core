from staticpipes.pipe_bundle_base import BasePipeBundle
from staticpipes.pipes.collection_records_process import PipeCollectionRecordsProcess
from staticpipes.pipes.load_collection_python_docs import PipeLoadCollectionPythonDocs
from staticpipes.processes.jinja2 import ProcessJinja2


class PipeBundlePythonDocs(BasePipeBundle):
    """ """

    def __init__(
        self,
        module_names: list = [],
        pass_number=1000,
    ):
        super().__init__(pass_number)
        self._module_names = module_names
        self._pipes = [
            PipeLoadCollectionPythonDocs(
                module_names=module_names,
                collection_name="python_docs",
            ),
            PipeCollectionRecordsProcess(
                collection_name="python_docs",
                output_dir="reference",
                context_key_record_data="python_document",
                processors=[
                    ProcessJinja2(
                        template="_templates/reference.html",
                    ),
                ],
            ),
        ]
