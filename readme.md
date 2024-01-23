# MarkWiki
Basic wiki-like interface for a set of markdown files. Create a folder called `text` inside this directory and paste all your markdown files. This file serves as a readme for GitHub as well as the homepage of the Wiki.

## Features
- automatically generated sitemap per directory with navigation options
- markdown rendering via [python-markdown](https://www.linode.com/docs/guides/how-to-use-python-markdown-to-convert-markdown-to-html/) with a few extensions
- no editing, just viewing
- relative in-markdown links work
- image support

## Paths
- `/`: renders this readme
- `/text/<subpath>`: renders a markdown file if it can find one
- `/sitemap`: links to all files and folders of the topmost folder aka. `/text`
- `/sitemap/<subpath>`: links to all files and folders in the subpath
- `/raw/<subpath>`: like `/text` but returns the raw file content

## Installation
1. install the latest python
2. install flask via `pip install flask`
3. install markdown via `pip install markdown`
4. run a developer server with `flask --app wikiserver run`

## Planned Features
- [x] automatic table of contents creation with a sidebar
- [ ] sidebar with newest and most recently changed files