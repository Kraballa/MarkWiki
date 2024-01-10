# MarkWiki
Basic wiki-like interface for a set of markdown files.

## Features
I threw this together in 2 hours, not many features

- file based routing. a markdown file under text/tech/ai.md will be served at /tech/ai.html
- sitemap-like *ul* with all entries
- no editing, only viewing
- markdown rendering via [python-markdown](https://www.linode.com/docs/guides/how-to-use-python-markdown-to-convert-markdown-to-html/)

## Installation
1. install the latest python
2. install flask via `pip install -U flask`
3. run a developer server with `flask --app wikiserver run`

Simply place all markdown files and directories in `/text`.


## Static Pages
Top level pages have to be static. They contain the following:

- [/](/): this page
- [/sitemap](/sitemap): dynamic sitemap that links to all entries in a *ul* sort of style