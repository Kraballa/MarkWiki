from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension

# The markdown extension does not allow lists following text without an extra newline.
# So all lists are prepended with an empty line as a bandaid fix.
class NewLiner(Preprocessor):
    def run(self, lines):
        new_lines = []
        for i, line in enumerate(lines):
            if len(line) > 0 and i > 0:
                if line.startswith(("*","1.","-")) and not lines[i-1].startswith(("*","1.","-")):
                    new_lines.append("")
            new_lines.append(line)
        return new_lines
    
class NewLineExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(NewLiner(md), "newliner", 10)
