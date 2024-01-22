from flask import Flask, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def index(): 
    return render_template("scan_list.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
