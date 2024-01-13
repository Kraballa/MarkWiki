from flask import Flask, request, render_template
from markupsafe import Markup
import markdown
import os

app = Flask(__name__)

md = markdown.Markdown(extensions=['toc'])

@app.get("/")
def index():
    text, toc = parseMarkdown("readme.md")
    return render_template("wiki.html", content=Markup(text), path=request.path,toc=Markup(toc))

@app.get("/sitemap")
def mainsitemap():
    return sitemap("")

@app.get("/sitemap/<path:subpath>")
def sitemap(subpath):
    cont = buildSiteMap(subpath)
    return render_template("wiki.html", content=Markup(cont), path=request.path)

@app.get("/text/<path:subpath>")
def read(subpath):
    filetext, toc = parseMarkdown("./text/" + subpath)
    return render_template("wiki.html", content=Markup(filetext), path=request.path, toc=Markup(toc))

def parseMarkdown(filepath):
    if not os.path.exists(filepath):
        return "<p>file not found</p>", ""
    if not filepath.endswith(".md"):
        return "<p>filetype not supported</p>", ""
    with open(filepath, "r") as input_file:
        text = input_file.read();
    html = md.convert(text)
    toc = md.toc
    # this is a bit jank but docs are lacking
    if(toc.startswith('<div class="toc">\n<ul></ul>\n</div>')):
        toc = ""
    return html, toc;

def buildSiteMap(subpath):
    res = ['<h2>Sitemap</h2>','<ul>']

    dirs = []
    files = []

    combined = "./text/" + subpath
    for entry in os.listdir(combined):
        path = combined + "/" + entry
        if(os.path.isdir(path)):
            dirs.append(entry)
        elif(os.path.isfile(path) and entry.endswith(".md")):
            files.append(entry)
    
    if(subpath != ""):
        parent = subpath.split("/")
        parent.pop()
        parent = "/".join(parent)
        if(parent != ""):
            parent = "/" + parent
        res.append(f"<li><a href='/sitemap{parent}'>..</a></li>")

    dirs.sort()
    files.sort()

    for dir in dirs:
        path = "<li><b><a href='/sitemap"
        if(subpath != ""):
            path = path + "/"+subpath
        path = f"{path}/{dir}'>{dir}</a></b></li>"
        res.append(path)
    for fle in files:
        path = "<li><i><a href='/text"
        if(subpath != ""):
            path = path + "/"+subpath
        path = f"{path}/{fle}'>{fle}</a></i></li>"
        res.append(path)

    res.append('</ul>')
    return ' '.join(res)