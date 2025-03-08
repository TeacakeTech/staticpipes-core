import os
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.watcher
import staticpipes.worker
from staticpipes.pipes.load_collection_python_docs import PipeLoadCollectionPythonDocs


def test_collection_python_docs():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[
            PipeLoadCollectionPythonDocs(
                module_names=["staticpipes"],
            ),
        ],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "python_document_process",
        ),
        out_dir,
    )
    # run
    worker.build()
    # test staticpipes
    record = worker.current_info.get_context("collection")["python_docs"].get_record(
        "staticpipes"
    )
    assert record is not None
    assert [i for i in record.get_data()["modules"] if i["module_name"] == "pipes"]

    # test staticpipes.base_pipe
    record = worker.current_info.get_context("collection")["python_docs"].get_record(
        "staticpipes.pipe_base"
    )
    assert record is not None
    assert [i for i in record.get_data()["classes"] if i["name"] == "BasePipe"]
    assert not record.get_data()["modules"]

    # test staticpipes.pipes.python_document_process
    record = worker.current_info.get_context("collection")["python_docs"].get_record(
        "staticpipes.pipes.load_collection_python_docs"
    )
    assert record is not None
    assert [
        i
        for i in record.get_data()["classes"]
        if i["name"] == "PipeLoadCollectionPythonDocs"
    ]
    # only classes in this module should be included, so no imports
    # (We've tested BasePipe appears in it's proper place above)
    assert not [i for i in record.get_data()["classes"] if i["name"] == "BasePipe"]
