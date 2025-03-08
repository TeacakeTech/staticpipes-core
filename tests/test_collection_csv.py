import os
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.pipes.collection_records_process
import staticpipes.pipes.load_collection_csv
import staticpipes.processes.jinja2
import staticpipes.watcher
import staticpipes.worker


def test_collection_csv():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[
            staticpipes.pipes.load_collection_csv.PipeLoadCollectionCSV(
                filename="data.csv"
            ),
            staticpipes.pipes.collection_records_process.PipeCollectionRecordsProcess(
                collection_name="data",
                processors=[
                    staticpipes.processes.jinja2.ProcessJinja2(
                        template="_templates/record.html"
                    )
                ],
            ),
        ],
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
    # test collection
    collection = worker.current_info.get_context()["collection"]["data"]
    assert len(collection.get_records()) == 2
    assert collection.get_records()[0].get_id() == "cat"
    assert collection.get_records()[0].get_data() == {
        "Description": "Floofy",
        "Title": "Cat",
    }
    assert collection.get_records()[1].get_id() == "dog"
    assert collection.get_records()[1].get_data() == {
        "Title": "Dog",
    }
    # test output
    with open(os.path.join(out_dir, "data", "cat.html")) as fp:
        contents = fp.read()
    contents = "".join([i.strip() for i in contents.split("\n")])
    assert (
        "<!doctype html><html><head><title>Cat</title></head><body>Floofy</body></html>"  # noqa
        == contents
    )
