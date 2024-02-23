from flask import Flask, request, render_template, send_file, make_response, redirect
from markupsafe import Markup
from addnewline import NewLineExtension
from timeago import time_ago

import markdown
from markdown.extensions.toc import TocExtension
import os

app = Flask(__name__)

# !IMPORTANT! if you want to allow editing, set this to true
allow_editing = False
no_edit_text = "403 forbidden: editing has been disabled by the host. if this is an error, edit the configuration of the server"
not_found_text = "404 not found: the requested file has not been found"

new_file_template = """---
title:
tags:
---
"""

md = markdown.Markdown(extensions=[TocExtension(title="Table of Contents"), 'tables', 'fenced_code', 'meta', 'sane_lists', NewLineExtension()])

@app.get("/favicon.ico")
def favicon():
    return send_file("./static/favicon.ico")

@app.get("/")
def index():
    text, toc = parseMarkdown("readme.md")
    return render_template("home.html", content=Markup(text), toc=Markup(toc))

@app.get("/sitemap/")
@app.get("/sitemap/<path:subpath>/")
def sitemap(subpath=""):
    cont = buildSiteMap(subpath + ("/" if subpath != "" else ""))
    path = "| " + subpath 
    return render_template("home.html", content=cont, path=path)

@app.get("/text/<path:subpath>")
def read(subpath):
    if not os.path.exists("." + request.path):
        if subpath.endswith(".md"):
            return render_template("filecreate.html", path="/edit/" + subpath)
        else:
            return make_response(not_found_text + request.path, 404)

    if not subpath.endswith(".md"):
        return send_file("." + request.path)

    filetext, toc = parseMarkdown("." + request.path)
    return render_template("wiki.html", content=Markup(filetext), path=sitemapToCurrentFolder(subpath), toc=Markup(toc), raw=buildPathToRaw(subpath), edit=buildPathToEdit(subpath))

@app.get("/raw/<path:subpath>")
def readPlain(subpath):
    path = "./text/" + subpath
    if(not os.path.exists(path)):
        return make_response(no_edit_text, 403)
    
    with open(path, "r", encoding="utf-8") as input_file:
        text = input_file.read()
    response = make_response(text, 200)
    response.mimetype = "text/plain"
    return response

@app.get("/changes/")
def changes():
    cont = buildChangesView()
    return render_template("home.html", content=cont)

@app.get("/edit/<path:subpath>")
def edit(subpath):
    if not allow_editing and not app.debug:
        return make_response(no_edit_text, 403)

    path = "./text/" + subpath
    text = new_file_template
    if(os.path.exists(path)):
        with open(path, "r", encoding="utf-8") as input_file:
            text = input_file.read()
    return render_template("edit.html", content=text, path=sitemapToCurrentFolder(subpath), target=subpath)

@app.post("/edit/<path:subpath>")
def postEdit(subpath):
    if not allow_editing and not app.debug:
        return make_response(not_found_text, 404)
    
    path = './text/' + subpath
    # folders or file don't exist, make sure they do
    if(not os.path.exists(path)):
        _dir = "./text/" + os.path.dirname(subpath)
        _file = os.path.basename(subpath)
        print(f"dir: {_dir}, file: {_file}")
        os.makedirs(_dir, exist_ok=True)
        open(f"{_dir}/{_file}", "x").close()

    with open(path, "bw") as input_file:
        input_file.write(request.form['content'].encode())

    redir = "/text/" + subpath
    return redirect(redir,code=301)

def parseMarkdown(filepath):
    md.reset()
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = md.convert(text)
    toc = md.toc
    html = buildMetaView(md.Meta) + html
    return html, toc

def buildSiteMap(subpath):
    res = ['<h2>Sitemap</h2><ul>']

    dirs, files = getDirsAndFiles(subpath)    
    
    if(subpath != ""):
        res.append(buildParentLink(subpath))

    for _dir in dirs:
        res.append("<li><b><a href='/sitemap/")
        res.append(subpath)
        res.append(f"{_dir}'>&#x1F4C1;{_dir}</a></b></li>")

    for _file in files:
        res.append("<li><a href='/text/")
        res.append(subpath)
        res.append(f"{_file}'>&#x1F4C4;{_file}</a></li>")

    res.append('</ul>')
    return Markup(''.join(res))

def getDirsAndFiles(subpath):
    """
    generate sorted lists of all directories and files on a path
    """
    dirs = []
    files = []
    combined = "./text/" + subpath
    for entry in os.listdir(combined):
        path = combined + "/" + entry
        if os.path.isdir(path) and not entry.startswith("."):
            dirs.append(entry)
        elif(os.path.isfile(path) and entry.endswith(".md")):
            files.append(entry)
    dirs.sort()
    files.sort()
    return dirs, files

def buildParentLink(subpath):
    _dir = os.path.dirname(subpath + "../")
    return f"<li><b><a href='/sitemap/{_dir}'>&#x1F4C1;..</a></b></li>"

def buildPathToRaw(subpath):
    link = f"<a href='/raw/{subpath}'>Raw</a>"
    return Markup(link)

def buildPathToEdit(subpath):
    link = f"<a href='/edit/{subpath}'>Edit</a>"
    return Markup(link)

def sitemapToCurrentFolder(subpath):
    _dir = os.path.dirname(subpath)
    _file = os.path.basename(subpath)
    link = f"<a href='/sitemap/{_dir}/'>{_dir}</a>/{_file}"
    return Markup(link)

def getRecentFileChanges():
    """
    get a sorted list of the recent changes to files
    and how long ago the change was made
    """
    files = []
    mtime = []

    for root, _, contains in os.walk("text\\"):
        for item in contains:
            if not item.endswith(".md"):
                continue
            _file = str(os.path.join(root,item))
            files.append(_file.replace("\\", "/"))
            mtime.append(os.path.getmtime(_file))

    def sortf(idx):
        return -mtime[idx]
    
    def getEntry(idx):
        return (str(files[idx]), time_ago(mtime[idx]))

    indices = list(range(len(files)))
    indices.sort(key=sortf)
    indices = indices[0:10]
    return list(map(getEntry, indices))

def buildChangesView():
    data = getRecentFileChanges()
    res = ["<h3>Recent Modifications</h3>","<ul>"]
    for path, timeStr in data:
        res.append(f"<li><a href='/{path}'>{path}</a> - {timeStr}</li>")

    res.append("</ul>")
    return Markup(' '.join(res))

def buildMetaView(data: dict):
    tags = []
    # split and filter tags
    if('tags' in data):
        split = data['tags'][0].split(' ')
        for tag in filter(None, split):
            tags.append(tag)
    
    if(len(tags) == 0):
        return ""

    tagList = ["<ul class='tags'>"]
    for tag in tags:
        tagList.append(f"<li class='tag'>{tag}</li>")
    tagList.append("</ul>")
    return ' '.join(tagList)
