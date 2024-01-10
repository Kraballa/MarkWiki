# MarkWiki
Basic wiki-like interface for a set of markdown files.

## Features
- file based routing. a markdown file under /tech/ai.md will be served at /tech/ai.html
- sitemap-like *ul* with all entries
- authentication system
- no editing, only viewing
- editing is done through ssh-ing into the raspi
- markdown rendering via [python-markdown](https://www.linode.com/docs/guides/how-to-use-python-markdown-to-convert-markdown-to-html/)


## Static Pages
Top level pages have to be static. They contain the following:
- "/": homepage
- "/sitemap": dynamic sitemap that links to all entries in a *ul* sort of style
- "/todo": more things to implement