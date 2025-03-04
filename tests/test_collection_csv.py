import os
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.pipes.load_collection_csv
import staticpipes.watcher
import staticpipes.worker


def test_collection_csv():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[staticpipes.pipes.load_collection_csv.LoadCollectionCSV()],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "fixtures", "collection_csv"
        ),
        out_dir,
    )
    # run
    worker.build()
    # test
    collection = worker.current_info.get_context()["collection"]["data"]
    assert len(collection.get_items()) == 2
    assert collection.get_items()[0].get_id() == "cat"
    assert collection.get_items()[0].get_data() == {
        "Description": "Floofy",
        "Title": "Cat",
    }
    assert collection.get_items()[1].get_id() == "dog"
    assert collection.get_items()[1].get_data() == {
        "Title": "Dog",
    }
