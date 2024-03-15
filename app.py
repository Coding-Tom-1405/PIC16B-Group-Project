from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template('homepage.html')


@app.route("/select", methods=['GET', 'POST'])
def select():
    if request.method == 'POST':
        selected_level = request.form.get("level")
        selected_challenge = request.form.get("challenge")
        return "Game started with Level: {} and Challenge: {}".format(selected_level, selected_challenge)
    return render_template('select.html')


# @app.route("/play")
# def play():
#     # Render a template for the web game
#     return render_template("play.html")

@app.route('/stats')
def stats():
    return render_template('stats.html') 



if __name__ == "__main__":
    app.run(debug=True)
