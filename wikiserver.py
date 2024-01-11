from flask import Flask, request, render_template
import markdown
import os

app = Flask(__name__)

@app.get("/")
def index():
    readme_text = markdown.markdown(getFileContent("readme.md"))
    return render_template("wiki.html", content=readme_text, path=request.path)

@app.get("/sitemap")
def sitemap():
    cont = buildSiteMap()
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

def buildSiteMap():
    res = ['<h2>Sitemap</h2>','<ul>']

    for root, dirs, files in os.walk("text"):
        for file in files:
            path = root + "\\" +file
            path = path.replace("\\", "/")
            res.append(f"<li><a href='{path}'>{path.replace("text", "", 1)}</a></li>")
    res.append('</ul>')
    return ' '.join(res)