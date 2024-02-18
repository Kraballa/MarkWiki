from flask import Flask, request, render_template, send_file, make_response, redirect
from markupsafe import Markup
from addnewline import NewLineExtension

import markdown
from markdown.extensions.toc import TocExtension
import os

app = Flask(__name__)

# !IMPORTANT! if you want to allow editing, set this to true
allow_editing = False
no_edit_text = "403 forbidden: editing has been disabled by the host. if this is an error, edit the configuration of the server"
not_found_text = "404 not found: the requested file has not been found"

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
    cont = buildSiteMap(subpath)
    return render_template("home.html", content=Markup(cont), path=request.path.replace("/sitemap", "| ", 1))

@app.get("/text/<path:subpath>")
def read(subpath):
    if not os.path.exists("." + request.path):
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

@app.get("/edit/<path:subpath>")
def edit(subpath):
    if not allow_editing:
        return make_response(no_edit_text, 403)

    path = "./text/" + subpath
    if(not os.path.exists(path)):
        return make_response(not_found_text, 404)
    with open(path, "r", encoding="utf-8") as input_file:
        text = input_file.read()
    return render_template("edit.html", content=text, path=sitemapToCurrentFolder(subpath), target=subpath)

@app.post("/edit/<path:subpath>")
def postEdit(subpath):
    if not allow_editing:
        return make_response(not_found_text, 404)
    
    print('submitted content to', subpath)
    path = './text/' + subpath

    if(not os.path.exists(path)):
        return make_response(not_found_text, 404)

    with open(path, "bw") as input_file:
        input_file.write(request.form['content'].encode())

    redir = request.path.replace("/edit", "/text", 1)
    return redirect(redir,code=301)

def parseMarkdown(filepath):
    md.reset()
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = md.convert(text)
    toc = md.toc
    # this is a bit jank but docs are lacking
    if(toc.startswith('<div class="toc">\n<ul></ul>\n</div>')):
        toc = ""
    return html, toc

def buildSiteMap(subpath):
    res = ['<h2>Sitemap</h2>','<ul>']

    dirs, files = getDirsAndFiles(subpath)    
    
    if(subpath != ""):
        res.append(buildParentLink(subpath))

    for dir in dirs:
        if dir.startswith('.'):
            continue
        path = "<li><b><a href='/sitemap"
        if(subpath != ""):
            path = path + "/"+subpath
        path = f"{path}/{dir}'>&#x1F4C1;{dir}</a></b></li>"
        res.append(path)

    for fle in files:
        path = "<li><a href='/text"
        if(subpath != ""):
            path = path + "/"+subpath
        path = f"{path}/{fle}'>&#x1F4C4;{fle}</a></li>"
        res.append(path)

    res.append('</ul>')
    return ' '.join(res)

# generate sorted lists of all directories and files on a path
def getDirsAndFiles(subpath):
    dirs = []
    files = []
    combined = "./text/" + subpath
    for entry in os.listdir(combined):
        path = combined + "/" + entry
        if(os.path.isdir(path)):
            dirs.append(entry)
        elif(os.path.isfile(path) and entry.endswith(".md")):
            files.append(entry)
    dirs.sort()
    files.sort()
    return dirs, files

def buildParentLink(subpath):
    parent = subpath.split("/")
    parent.pop()
    parent = "/".join(parent)
    if(parent != ""):
        parent = "/" + parent
    return f"<li><b><a href='/sitemap{parent}'>&#x1F4C1;..</a></b></li>"

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
