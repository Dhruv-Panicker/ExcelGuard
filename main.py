from flask import Flask, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)
@app.route("/login")
def login():
  return render_template("login.html")
@app.route("/scan_list")
def scan_list(): 
  return render_template("scan_list.html")
@app.route("/scanning")
def scanning():
  return render_template("scanning.html")
@app.route("/scan_results")
def scan_results():
  return render_template("scan_results.html")
@app.route("/view_scan")
def view_scan():
  return render_template("view_scan.html")
@app.route("/settings")
def settings():
  return render_template("settings.html")
@app.route("/logout")
def logout():
  return render_template("logout.html")

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)
