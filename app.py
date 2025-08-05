from flask import Flask, render_template, request
import json

app = Flask(__name__)

def load_topics():
    with open("data/topics.json", "r") as f:
        return json.load(f)

@app.route("/")
def index():
    topics = load_topics()
    return render_template("index.html", topics=topics)

@app.route("/topic/<title>")
def topic(title):
    topics = load_topics()
    for t in topics:
        if t["title"].lower() == title.lower():
            return render_template("topic.html", topic=t)
    return "Topic not found", 404

@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    topics = load_topics()
    results = [t for t in topics if query in t["title"].lower()]
    return render_template("search.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)

import wikipedia

@app.route("/search")
def search():
    query = request.args.get("q", "")
    try:
        summary = wikipedia.summary(query, sentences=3)
        return render_template("search.html", results=[{"title": query.title(), "summary": summary}], query=query)
    except:
        return render_template("search.html", results=[], query=query)
