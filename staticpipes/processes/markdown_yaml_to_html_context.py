import yaml
from markdown_it import MarkdownIt

from staticpipes.process_base import BaseProcessor


class ProcessMarkdownYAMLToHTMLContext(BaseProcessor):
    """
    Converts a Markdown file (with optional YAML) into HTML (and context variables).

    Optional YAML should be in a block at the top marked with "---".
    """

    def process_file(
        self, source_dir, source_filename, process_current_info, current_info
    ):
        """"""

        markdown = process_current_info.contents

        if markdown.startswith("---"):
            bits = markdown.split("---", 2)
            data = yaml.safe_load(bits[1])
            markdown = bits[2]
            for k, v in data.items():
                current_info.set_context(k, v)

        md = MarkdownIt("commonmark")
        html = md.render(markdown)
        process_current_info.contents = html
