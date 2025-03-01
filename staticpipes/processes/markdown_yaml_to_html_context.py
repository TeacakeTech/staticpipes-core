import yaml
from markdown_it import MarkdownIt

from staticpipes.pipes.process import BaseProcessor


class ProcessMarkdownYAMLToHTMLContext(BaseProcessor):

    def process_file(
        self, source_dir, source_filename, process_current_info, current_info
    ):

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
