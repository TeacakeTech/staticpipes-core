import os
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.pipes.collection_records_process
import staticpipes.pipes.load_collection_json_list
import staticpipes.processes.jinja2
import staticpipes.watcher
import staticpipes.worker


def test_collection_json_list():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[
            staticpipes.pipes.load_collection_json_list.PipeLoadCollectionJSONList(),
        ],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "collection_json_list",
        ),
        out_dir,
    )
    # run
    worker.build()
    # test collection
    collection = worker.current_info.get_context()["collection"]["data"]
    assert len(collection.get_records()) == 2
    assert collection.get_records()[0].get_id() == "0"
    assert collection.get_records()[0].get_data() == {
        "Id": "cat",
        "Description": "Floofy",
        "Title": "Cat",
    }
    assert collection.get_records()[1].get_id() == "1"
    assert collection.get_records()[1].get_data() == {
        "Id": "dog",
        "Title": "Dog",
    }
