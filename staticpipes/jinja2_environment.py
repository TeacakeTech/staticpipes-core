from typing import Optional

import jinja2

from staticpipes.source_directory import SourceDirectory


class Jinja2Environment:

    def __init__(self, autoescape: bool = True, filters: dict | None = None):
        self._jinja2_environment: Optional[jinja2.Environment] = None
        self._autoescape = autoescape
        self._filters = filters or {}

    def get(
        self, source_directory: SourceDirectory, secondary_source_directories: dict
    ) -> jinja2.Environment:
        if not self._jinja2_environment:
            loaders: list = [jinja2.FileSystemLoader(source_directory.dir)]
            if secondary_source_directories:
                loaders.append(
                    jinja2.PrefixLoader(
                        {
                            k: jinja2.FileSystemLoader(ssd.dir)
                            for k, ssd in secondary_source_directories.items()
                        },
                        delimiter=":",
                    )
                )
            self._jinja2_environment = jinja2.Environment(
                loader=jinja2.ChoiceLoader(loaders),
                autoescape=self._autoescape,
            )
            for k, v in self._filters.items():
                self._jinja2_environment.filters[k] = v

        return self._jinja2_environment
