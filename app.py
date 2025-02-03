import json, datetime
from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form['search']
    
        with open("data.json") as f:
            posts = json.loads(f.read())

        posts = list(filter(lambda post: title.lower() in post['title'].lower(), posts))

        return render_template("index.html", posts=posts)

    return render_template("index.html")

@app.route("/posts")
def blogs():
    with open("data.json") as f:
        posts = json.loads(f.read())

    return render_template("posts.html", posts=posts)

@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    with open("data.json") as f:
        posts = json.loads(f.read())
    
    post = list(filter(lambda post: post['id'] == post_id, posts))[0]
    
    return render_template('detail.html', post=post)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        created_at = str(datetime.datetime.now().isoformat())

        with open("data.json") as f:
            posts = json.loads(f.read())

        posts.append({
            "id": len(posts) + 1,
            "title": title,
            "content": content,
            "created_at": created_at
        })

        with open("data.json", "w") as f:
            f.write(json.dumps(posts, indent=4))

        return render_template("add.html")

    return render_template("add.html")

@app.route("/delete/<int:post_id>")
def delete(post_id):
    with open("data.json") as f:
        posts = json.loads(f.read())

    posts = list(filter(lambda post: post['id'] != post_id, posts))

    with open("data.json", "w") as f:
        f.write(json.dumps(posts, indent=4))

    return redirect("/posts")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
