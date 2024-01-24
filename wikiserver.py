from flask import Flask, request, render_template, send_file, make_response
from markupsafe import Markup
from addnewline import NewLineExtension

import markdown
import os

app = Flask(__name__)

md = markdown.Markdown(extensions=['toc', 'tables', 'fenced_code', 'meta', 'sane_lists', NewLineExtension()])

@app.get("/")
def index():
    text, toc = parseMarkdown("readme.md")
    return render_template("wiki.html", content=Markup(text), path=request.path,toc=Markup(toc), raw="")

@app.get("/sitemap")
def mainsitemap():
    return sitemap("")

@app.get("/sitemap/<path:subpath>")
def sitemap(subpath):
    cont = buildSiteMap(subpath)
    return render_template("wiki.html", content=Markup(cont), path=request.path, raw="")

@app.get("/text/<path:subpath>")
def read(subpath):
    path = "./text/" + subpath

    if not os.path.exists(path):
        return make_response("", 404)

    if not subpath.endswith(".md"):
        return send_file(path)

    filetext, toc = parseMarkdown(path)
    return render_template("wiki.html", content=Markup(filetext), path=request.path, toc=Markup(toc), raw=buildPathToRaw(subpath))

@app.get("/raw/<path:subpath>")
def readPlain(subpath):
    path = "./text/" + subpath
    if(not os.path.exists(path)):
        return make_response("", 404)
    
    with open(path, "r", encoding="utf-8") as input_file:
        text = input_file.read()
    response = make_response(text, 200)
    response.mimetype = "text/plain"
    return response

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
    link = f"<a href='/raw/{subpath}'>Raw</a>\n|\n"
    return Markup(link)
