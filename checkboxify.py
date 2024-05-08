from markdown import Markdown
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension

# preprocessor extensions shouldn't actually be used like this
# instead some sort of inline processor would have been the correct choice
# but this way is simpler
class Checkboxifier(Preprocessor):
    def run(self, lines):
        new_lines = []
        for line in lines:
            if line.startswith("- [ ]"):
                new_lines.append(f"<input type='checkbox'/> {line[6:]}<br>")
            elif line.startswith("- [x]"):
                new_lines.append(f"<input type='checkbox' checked/> <span class='dim'>{line[6:]}</span><br>")
            elif line.startswith("- [/]"):
                new_lines.append(f"<input type='checkbox' class='semi'/> {line[6:]}<br>")
            else:
                new_lines.append(line)
        return new_lines

class CheckboxifyExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(Checkboxifier(md), "checkboxify", 12)