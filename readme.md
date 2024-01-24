# MarkWiki
Basic wiki-like interface for a set of markdown files. Create a folder called `text` inside this directory and paste all your markdown files. This file serves as a readme for GitHub as well as the homepage of the Wiki.

## Features
- markdown rendering via [python-markdown](https://python-markdown.github.io/) with a few extensions
- automatic table-of-contents generation
- directory viewing and navigation (sitemap)
- support for relative links inside markdown and images

There is currently no support for in-browser editing.

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

## Demo
This is how the interface looks:

![img](static/demo.png)