from flask import Flask, render_template, request, jsonify
from scraper import scrape_url
from storage import init_db, get_all_emails

app = Flask(__name__)
init_db()

@app.route("/")
def index():
    emails = get_all_emails()
    return render_template("index.html", emails=emails)

@app.route("/scrape", methods=["POST"])
def scrape():
    url = request.json.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    emails = scrape_url(url)
    return jsonify({"emails": emails, "count": len(emails)})

@app.route("/emails")
def get_emails():
    emails = get_all_emails()
    result = [{"email": e[0], "source": e[1], "found_at": e[2]} for e in emails]
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)