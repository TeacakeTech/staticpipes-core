import os.path
import tempfile

import datatig.repository_access
from datatig.models.siteconfig import SiteConfigModel
from datatig.readers.directory import process_type
from datatig.sqlite import DataStoreSQLite
from datatig.validate.jsonschema import JsonSchemaValidator

from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class LoadDatatig(BasePipe):

    def __init__(self):
        pass

    def start_prepare(self, current_info: CurrentInfo) -> None:

        # Repository Access
        repository_access = datatig.repository_access.RepositoryAccessLocalFiles(
            self.source_directory.dir
        )

        # Config
        config = SiteConfigModel(self.source_directory.dir)
        config.load_from_file(repository_access)

        # SQLite
        temp_dir = tempfile.mkdtemp()
        sqlite_filename = os.path.join(temp_dir, "datatig.sqlite")
        datastore = DataStoreSQLite(
            config, sqlite_filename, error_if_existing_database=True
        )

        # Load data
        for type in config.get_types().values():
            process_type(
                config,
                repository_access,
                type,
                lambda record: datastore.store(record),
                lambda error: datastore.store_error(error),
            )

        # Validate data
        validate_json_schema = JsonSchemaValidator(config, datastore)
        validate_json_schema.go()

        # Calendars
        datastore.process_calendars()

        # Into context
        current_info.set_context(
            "datatig",
            {
                "config": config,
                "datastore": datastore,
                "sqlite_filename": sqlite_filename,
            },
        )
