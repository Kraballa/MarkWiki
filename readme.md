# MarkWiki
Basic wiki-like interface for a set of markdown files. Drop all your markdown into `/text`. This file serves as a readme for GitHub as well as the homepage of the Wiki.

## Features
- automatically generated sitemap per directory with navigation options
- markdown rendering via [python-markdown](https://www.linode.com/docs/guides/how-to-use-python-markdown-to-convert-markdown-to-html/) with a few extensions
- no editing, just viewing
- relative in-markdown links work
- image support

## Installation
1. install the latest python
2. install flask via `pip install flask`
3. install markdown via `pip install markdown`
4. run a developer server with `flask --app wikiserver run`

## Planned Features
- [x] automatic table of contents creation with a sidebar
- [ ] sidebar with newest and most recently changed files