import html.parser
from typing import Optional

import staticpipes.utils
from staticpipes.check_base import BaseCheck
from staticpipes.check_report import CheckReport

FIND_LINKS_IN = {
    "a": {"attr": "href"},
    "img": {"attr": "src"},
    "link": {"attr": "href"},
    "script": {"attr": "src"},
}


class CheckInternalLinksHTMLParser(html.parser.HTMLParser):

    def __init__(self) -> None:
        super().__init__()
        self.links: list = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() in FIND_LINKS_IN:
            find_data = FIND_LINKS_IN[tag.lower()]
            attrs_dict = {
                k.lower(): v for k, v in attrs if k.lower() == find_data["attr"]
            }
            value = attrs_dict.get(find_data["attr"])
            if value:
                value = staticpipes.utils.get_link_internal(value)
                if value:
                    line, column = self.getpos()
                    self.links.append({"link": value, "line": line, "column": column})


def _get_dirs_files_to_check(source_dir: str, souce_filename: str, link: str) -> list:
    out = []
    if link.startswith("/"):
        # Absolute link

        # Do it once, assuming we are linking to a file
        out.append(staticpipes.utils.make_dir_and_filename_from_path(link[1:]))

        # Do it again, assuming we are linking to a directory
        # and we need to add "index.html" to the end
        out.append(
            staticpipes.utils.make_dir_and_filename_from_path(link[1:] + "/index.html")
        )
    else:
        # Relative link

        # Do it once, assuming we are linking to a file
        source_dir_bits = [i for i in source_dir.split("/") if i]
        link_bits = [i for i in link.split("/") if i]
        filename = link_bits.pop()

        while link_bits and link_bits[0] == "..":
            link_bits.pop(0)
            if len(source_dir_bits) > 0:
                source_dir_bits.pop()

        out.append(("/".join(source_dir_bits + link_bits), filename))

        # Do it again, assuming we are linking to a directory
        # and we need to add "index.html" to the end
        source_dir_bits = [i for i in source_dir.split("/") if i]
        link_bits = [i for i in link.split("/") if i]

        while link_bits[0] == "..":
            link_bits.pop(0)
            if len(source_dir_bits) > 0:
                source_dir_bits.pop()

        out.append(("/".join(source_dir_bits + link_bits), "index.html"))

    return out


class CheckInternalLinks(BaseCheck):

    def __init__(self, extensions: Optional[list] = None):
        self.extensions: list = extensions or ["html"]

    def check_build_file(self, dir: str, filename: str) -> list:
        # Check Extensions
        if self.extensions and not staticpipes.utils.does_filename_have_extension(
            filename, self.extensions
        ):
            return []

        # Go
        check_reports: list = []

        parser = CheckInternalLinksHTMLParser()
        parser.feed(self._build_directory.get_contents_as_str(dir, filename))

        for link in parser.links:
            dirs_files_to_check = _get_dirs_files_to_check(dir, filename, link["link"])
            if (
                len(
                    [
                        i
                        for i in dirs_files_to_check
                        if self._build_directory.has_file(i[0], i[1])
                    ]
                )
                == 0
            ):
                check_reports.append(
                    CheckReport(
                        dir=dir,
                        file=filename,
                        message="Can not find internal link: {}".format(link["link"]),
                        type="missing_link",
                        line=link["line"],
                        column=link["column"],
                        from_check=self,
                    )
                )
        return check_reports
