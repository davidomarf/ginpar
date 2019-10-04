import os
import shutil
import config

def parse(path):
     return eval('f"""' + open(path).read() + '"""')

templates = {
    "header": parse("templates/header.html"),
    "bottom": parse("templates/bottom.html")
}

def build_sketch (sketch):
    content = eval('f"""' + open("./templates/sketch.html").read() + '"""')
    return content

def build_link(sketch):
    title = sketch.split("/")[-1].split(".")[0]
    return f'<a href="./{title}"">{title}</a><br/>\n'

def build_index(sketches):
    content = templates["header"]
    for s in sketches:
        content += build_link(s)
    return content + templates["bottom"]

## Remove existent /public folder and create an empty one
if os.path.exists("public"):
    shutil.rmtree('public')

os.mkdir('public')

## Copy static folder
shutil.copytree("static", "public/static")

## Create a sketches array
sketches_path = "./sketches"
sketches = []

for r, d, f in os.walk(sketches_path):
    for file in f:
        if ".js" in file:
            sketches.append(os.path.join(r, file))

## Create an index to contain all the sketches
index = open("public/index.html", "w")
index.write(build_index(sketches))
index.close()

for s in sketches:
    ## Ignore the path and extension of the sketch
    title = s.split("/")[-1].split(".")[0]

    ## Create a directory with the sketch title
    os.mkdir(f'public/{title}')

    ## Create index.html
    index_path = f'public/{title}/index.html'
    index = open(index_path, "w+")
    index.write(build_sketch(s))
    index.close()

    ## Create sketch.js
    sketch_path = f'public/{title}/sketch.js'
    sketch = open(sketch_path, "w+")

    ## Copy all the content from original sketches/{title}.js to sketch.js
    sf = open(s, 'r')
    for x in sf.readlines():
        sketch.write(x)
    sf.close()
    sketch.close()
    