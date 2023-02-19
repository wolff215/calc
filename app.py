from flask import Flask, render_template
from calc import check_activities, athlete_info

app = Flask(__name__)

@app.route('/')
def index():
    entries = check_activities()
    athlete = athlete_info()
    return render_template('index.html', entries=entries, athlete=athlete)

if __name__ == '__main__':
    app.run(debug=True)
