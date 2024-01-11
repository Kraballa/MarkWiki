from flask import Flask, request, render_template
import markdown
import os

app = Flask(__name__)

@app.get("/")
def index():
    readme_text = markdown.markdown(getFileContent("readme.md"))
    return render_template("wiki.html", content=readme_text, path=request.path)

@app.get("/sitemap")
def mainsitemap():
    return sitemap("")

@app.get("/sitemap/<path:subpath>")
def sitemap(subpath):
    cont = buildSiteMap(subpath)
    return render_template("wiki.html", content=cont, path=request.path)

@app.get("/text/<path:subpath>")
def read(subpath):
    readme_text = markdown.markdown(getFileContent("./text/" + subpath))
    return render_template("wiki.html", content=readme_text, path=request.path.replace("/text", "", 1))

def getFileContent(filepath):
    print(f"trying to open file {filepath}")
    if not os.path.exists(filepath):
        return "<p>file not found</p>"
    if not filepath.endswith(".md"):
        return "<p>filetype not supported</p>"
    with open(filepath, "r") as input_file:
        text = input_file.read();
    return text;

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