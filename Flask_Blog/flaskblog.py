from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    {
        "author": "Sridhar",
        "title": "Blog Post 1",
        "content": "Some random text for bp 1",
        "date_posted": "April 25, 2018"
    },
    {
        "author": "Sneha",
        "title": "Blog Post 2",
        "content": "Some random text for bp 2",
        "date_posted": "August 9, 2018"
    },
    {
        "author": "Lobo",
        "title": "Blog Post 3",
        "content": "Some random text for bp 3",
        "date_posted": "Dec 31, 2018"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title="About")

if __name__ == "__main__":
    app.run(debug=True)