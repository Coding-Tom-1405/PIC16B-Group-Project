from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template('homepage.html')

def write_to_csv(level, challenge):
    with open('/Users/gimdong-gyu/Desktop/newProject16B/game_setting.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([level, challenge])

@app.route("/select", methods=['GET', 'POST'])
def select():
    if request.method == 'POST':
        selected_level = request.form.get("level")
        selected_challenge = request.form.get("challenge")
        write_to_csv(selected_level, selected_challenge) 
        return redirect('http://localhost:8000')
    return render_template('select.html')


@app.route('/stats')
def stats():
    return render_template('stats.html') 



if __name__ == "__main__":
    app.run(debug=True)
