from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def homepage():
    return """<h1> Welcome to the <b> Chimp Test </b> Game!</h1>
   <a href="/select">Start Game!</a>"""

@app.route("/select")
def new():
    return render_template('select2.html')

@app.route('/reselect', methods=['POST'])
def reselect():
    selected = int(request.form["level"])
    return render_template("reselect3.html", selected=selected)
    

@app.route('/confirm', methods=['POST'])
def confirm():
    selected = int(request.form["level"])
    challenged = int(request.form["challenge"])
    return render_template("confirm4.html", selected=selected, challenged=challenged)

if __name__ == "__main__":
    app.run(debug=True)
