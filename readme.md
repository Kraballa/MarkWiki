# MarkWiki
Basic wiki-like interface for a set of markdown files. Drop all your markdown into `/text`.

## Features
- automatically generated sitemap per directory with navigation options
- markdown rendering via [python-markdown](https://www.linode.com/docs/guides/how-to-use-python-markdown-to-convert-markdown-to-html/)
- no editing, just viewing
- relative in-markdown links work
- does not support images or other flavours of markdown

## Installation
1. install the latest python
2. install flask via `pip install flask`
3. install markdown via `pip install markdown`
4. run a developer server with `flask --app wikiserver run`

## Planned Features
- automatic table of contents creation with a sidebar