from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/select")
def new():
    return render_template('select2.html')

@app.route('/reselect', methods=['POST'])
def reselect():
    selected = int(request.form["level"])
    return render_template("reselect3.html", selected=selected)
    

@app.route('/confirm', methods=['POST'])
def confirm():
    selected = request.form.get("level")  # Captures the level selected
    challenged = request.form.get("challenge")  # Captures the challenge selected
    # Convert challenge values to a user-friendly format, if necessary
    challenge_text = {
        "timer": "Timer",
        "random_order": "Random Order",
        "none": "None"
    }.get(challenged, "None")  # Default to "None" if for some reason the challenge is not in the dictionary
    return render_template("confirm4.html", selected=selected, challenged=challenge_text)


if __name__ == "__main__":
    app.run(debug=True)
