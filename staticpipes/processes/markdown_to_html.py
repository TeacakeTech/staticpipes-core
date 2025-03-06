from markdown_it import MarkdownIt

from staticpipes.process_base import BaseProcessor


class ProcessMarkdownToHTML(BaseProcessor):

    def process_file(
        self, source_dir, source_filename, process_current_info, current_info
    ):

        md = MarkdownIt("commonmark")
        html = md.render(process_current_info.contents)
        process_current_info.contents = html
