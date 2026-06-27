import os
from flask import Flask, render_template, request, jsonify
from scraper import scrape_url
from storage import init_db, get_all_results, delete_result

app = Flask(__name__)
init_db()

@app.route("/")
def index():
    results = get_all_results()
    return render_template("index.html", results=results)

@app.route("/scrape", methods=["POST"])
def scrape():
    url = request.json.get("url")
    depth = int(request.json.get("depth", 1))
    if not url:
        return jsonify({"error": "No URL"}), 400
    result = scrape_url(url, depth=depth)
    return jsonify(result)

@app.route("/results")
def get_results():
    return jsonify(get_all_results())

@app.route("/delete/<int:result_id>", methods=["DELETE"])
def delete(result_id):
    delete_result(result_id)
    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)