import html.parser
from typing import Optional

import staticpipes.utils
from staticpipes.check_base import BaseCheck
from staticpipes.check_report import CheckReport

DEFAULT_CHECK_HTML_TAG_SETTINGS = {"img": {"required_attributes": ["alt"]}}


class CheckHtmlTagsHTMLParser(html.parser.HTMLParser):

    def __init__(self, dir: str, filename: str, html_tag_settings, check: BaseCheck):
        super().__init__()
        self._html_tag_settings = html_tag_settings
        self._dir: str = dir
        self._filename: str = filename
        self.check_reports: list[CheckReport] = []
        self._check: BaseCheck = check

    def handle_starttag(self, tag, attrs):
        attrs_dict = {k: v for k, v in attrs}
        if tag.lower() in self._html_tag_settings:
            for attr in self._html_tag_settings[tag.lower()]["required_attributes"]:
                if attr not in attrs_dict or not attrs_dict[attr]:
                    line, column = self.getpos()
                    self.check_reports.append(
                        CheckReport(
                            dir=self._dir,
                            file=self._filename,
                            message="Tag {} is missing attribute {}".format(
                                tag.lower(), attr
                            ),
                            type="html_tag_missing_attribute",
                            line=line,
                            column=column,
                            from_check=self._check,
                        )
                    )


class CheckHtmlTags(BaseCheck):
    """Checks that HTML tags have certain attributes
    eg that all img tags have alt set."""

    def __init__(
        self,
        html_tag_settings: Optional[dict] = None,
        extensions: Optional[list] = None,
    ):
        self._html_tag_settings = html_tag_settings or DEFAULT_CHECK_HTML_TAG_SETTINGS
        self.extensions: list = extensions or ["html"]

    def check_build_file(self, dir: str, filename: str) -> list:
        # Check Extensions
        if self.extensions and not staticpipes.utils.does_filename_have_extension(
            filename, self.extensions
        ):
            return []

        # Go
        parser = CheckHtmlTagsHTMLParser(
            dir=dir,
            filename=filename,
            html_tag_settings=self._html_tag_settings,
            check=self,
        )
        parser.feed(self.build_directory.get_contents_as_str(dir, filename))
        return parser.check_reports
