# MarkWiki
MarkWiki is a very simple single user wiki based on markdown. It is first and foremost a markdown renderer for a browser client but there's an opt-in feature to allow editing files in-browser as well. Though it isn't a complete system yet I hope to implement more small and simple features over time. 

## Features
- markdown rendering via [python-markdown](https://python-markdown.github.io/) with a few extensions
- automatic table-of-contents generation
- directory viewing and navigation (sitemap)
- support for relative links inside markdown and images
- make changes to files and save them back to disk. I highly recommend using version control to backup changes as the server doesn't handle backups yet. simply have a second git repo inside the `/text/` folder.

## Paths
- `/`: renders this readme
- `/text/<subpath>`: renders a markdown file if it can find one
- `/edit/<subpath>`: presents a textarea with the file content. POSTing to this path will write the changes to disk
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

(it's super trippy seeing the app inside itself)