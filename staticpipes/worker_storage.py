import sqlite3
from contextlib import closing


class WorkerStorage:

    def __init__(self):
        self._connection = sqlite3.connect(":memory:")
        self._connection.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        with closing(self._connection.cursor()) as cur:
            cur.execute("""CREATE TABLE source_file (
                dir_name TEXT,
                file_name TEXT,
                excluded INT,
                PRIMARY KEY(dir_name, file_name)
                )""")

    def store_file_details(self, dir_name, file_name, excluded: bool) -> None:
        with closing(self._connection.cursor()) as cur:
            cur.execute(
                """INSERT OR REPLACE INTO source_file
                (dir_name, file_name, excluded)
                VALUES (?, ?, ?)""",
                [dir_name, file_name, 1 if excluded else 0],
            )
            self._connection.commit()

    def is_file_excluded(self, dir_name, file_name) -> bool:
        with closing(self._connection.cursor()) as cur:
            res = cur.execute(
                """SELECT excluded FROM source_file WHERE dir_name=? AND file_name=?""",
                [dir_name, file_name],
            ).fetchone()
            return (res["excluded"] > 0) if res else False
